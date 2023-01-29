import logging
import socket
import sys
import threading
import time
import contextlib


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 20


class DroneManager(object):
    speed = 20

    def __init__(self, host_ip='192.168.10.2', host_port=8889, drone_ip='192.168.10.1', drone_port=8889):

        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))

        self.response = None
        self.stop_event = threading.Event()
        self._response_thread = threading.Thread(
            target=self.receive_response, args=(self.stop_event,))  # we need to set a comma to make tuple
        self._response_thread.start()

        self.patrol_event = None
        self.is_patrol = False
        # to allow just one patrol thread
        self._patrol_semaphore = threading.Semaphore(1)
        self._patrol_thread = None

        self.__command_semaphore = threading.Semaphore(1)
        self._command_thread = None

        self._send_command('command')
        self._send_command('streamon')

    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                logger.info({'action': 'receive_response',
                            'response': self.response})
            except socket.error as ex:
                logger.error({'action': 'receive_response', 'ex': ex})
                break

    def __del__(self):
        self.stop()

    def stop(self):
        self.stop_event.set()
        retry = 0
        while self._response_thread.isAlive():
            time.sleep(0.3)
            # to catch the error when i close socket
            if retry > 30:
                break
            retry += 1
        self.socket.close()

    def send_command(self, command, blocking=True):
        self._command_thread = threading.Thread(
            target=self._send_command,
            args=(command, blocking,)
        )
        self._command_thread.start()

    def _send_command(self, command, blocking=True):
        is_acquire = self.__command_semaphore.acquire(blocking=blocking)
        if is_acquire:
            with contextlib.ExitStack() as stack:
                stack.callback(self.__command_semaphore.release)
                logger.info({'action': 'send_command', 'command': command})
                self.socket.sendto(command.encode('utf-8'), self.drone_address)

                retry = 0
                while self.response is None:
                    time.sleep(0.3)
                    if retry > 3:
                        break
                    retry += 1
                if self.response == None:
                    response = None
                else:
                    response = self.response.decode('utf-8')
                self.response = None
                return response
        else :
            logger.warning({'action': 'send_command', 'command': command , 'status' : 'not_acquire'})

    def takeoff(self):
        return self._send_command('takeoff')

    def land(self):
        return self._send_command('land')

    def move(self, diraction, distance):
        return self._send_command(f'{diraction}{distance}')

    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)

    def dwon(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)

    def patrol(self):
        if not self.is_patrol:
            self.patrol_event = threading.Event()
            self._patrol_thread = threading.Thread(
                target=self._patrol, args=(self._patrol_semaphore, self.patrol_event,))
            self._patrol_thread.start()
            self.is_patrol = True

    def _patrol(self, semaphore, stop_event):
        is_acquire = semaphore.acquire(blocking=False)
        if is_acquire:
            logger.info({'action': '_patrol', 'status': 'acquire'})
            with contextlib.ExitStack() as stack:
                stack.callback(semaphore.release)
                status = 0
                while not stop_event:
                    status += 1
                    if status == 1:
                        self.up()
                    if status == 2:
                        self.down()
                    if status == 3:
                        status = 0
                    time.sleep(0.5)
        else:
            logger.warning({'action': 'patrol', 'status': 'not_acquire'})

    def stop_patrol(self):
        if self.is_patrol:
            self.patrol_event.set()
            retry = 0
            while self._patrol_thread.isAlive():
                time.sleep(0.3)
                if retry > 300:
                    break
                retry += 1
                self.is_patrol = False


if __name__ == '__main__':
    drone_manager = DroneManager()
    drone_manager.takeoff()
    time.sleep(10)
    drone_manager.land()
    drone_manager.stop()
