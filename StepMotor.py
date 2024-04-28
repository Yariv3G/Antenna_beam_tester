import serial
# import STEP_MOTOR_PORT, STEP_MOTOR_BAUD_RATE
import time
from typing import Optional

class StepMotor:
    def __init__(self,STEP_MOTOR_PORT,STEP_MOTOR_BAUD_RATE):
        self.ser = serial.Serial(STEP_MOTOR_PORT, STEP_MOTOR_BAUD_RATE, timeout=1)
        self.ser.flushInput()

    def write_serial_cmd(self,command):
        self.set_echo(True)
        self.ser.write(command.encode())
        time.sleep(0.1)
        ans = self.ser.readlines()
        return ans

    def flush_serial_buffer(self,echo:Optional[bool]=None):
        self.ser.reset_input_buffer()
        if echo is not None:
            return self.ser.readlines()

    def turn_left(self, steps,echo:Optional[bool]=None):
        ans = self.write_serial_cmd(command= f"l{steps}\n")
        return ans


    def turn_right(self, steps,echo:Optional[bool]=None):
        ans = self.write_serial_cmd(command=f"r{steps}\n")
        return ans

    def apply_power(self, echo:Optional[bool]=None):
            ans = self.write_serial_cmd(command=f"p1\n")
            return ans

    def release_power(self):
            ans = self.write_serial_cmd(command=f"p0\n")
            return ans

    def set_step_delay(self, delay_ms):
        ans = self.write_serial_cmd(command=f"d{delay_ms}\n")
        return ans

    def set_echo(self, echo_on:bool):
        if echo_on == True :
            self.ser.write(b"e1\n")
            status='echo on'
        else:
            self.ser.write(b"e0\n")
            status = 'echo off'
        return self.ser.readlines(),status

    def get_firmware_version(self):

        self.ser.write(b"v\n")
        return self.ser.readline().decode().strip()

    def display_help(self):

        self.ser.write(b"h\n")
        time.sleep(5)
        return self.ser.readlines()

if __name__ == "__main__":
    STEP_MOTOR_PORT = 'com10'
    STEP_MOTOR_BAUD_RATE = 9600
    m = StepMotor(STEP_MOTOR_PORT, STEP_MOTOR_BAUD_RATE)
    ans = m.set_step_delay(100)
    print(ans)
    tic = time.time()
    ans = m.turn_left(1)
    print('time passed' ,time.time()-tic)
    print(ans)
    tic = time.time()
    ans = m.turn_left(180)
    print(ans,'took ',time.time()-tic, 's')
    # # time.sleep(5)
    # help_info = m.display_help()
    # help_info = [line_bytes.decode().strip() for line_bytes in help_info]
    #
    # for line in help_info:
    #     print(line)
    # print(m.display_help())
    # m.flush_serial_buffer()


    #
    # print(m.set_step_delay(100))
    # print(m.turn_right(180))


