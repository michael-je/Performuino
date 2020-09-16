# arduino_interface sends the commands directly to arduino after ecnoding them
# so send the exact commands the arduino code uses into glob.arduino_commands

import cfg
import glob

import serial
import subprocess
from time import sleep


def main():
    # tries to establish a valid connection with the Arduino, prints an error if unsuccessful
    if not cfg.COM_PORT:
        COM_PORT = get_arduino_port()
    if COM_PORT is None:
        print('No COM Port found for Arduino. Terminating arduino_interface.')
        # glob.terminate_flag = True
        return  # add a way for it to communicate with main script about no connection?
    ser = serial.Serial(COM_PORT, cfg.BAUD)
    print("Arduino interface connected.")

    while not glob.terminate_flag:
        if glob.arduino_commands:
            new_commands = glob.arduino_commands[:]
            glob.arduino_commands.clear()

            for command in new_commands:
                try:
                    ser.write(command.encode())
                except serial.serialutil.SerialException:
                    print('Arduino connection lost. Terminating.')
                    return
                except AttributeError:
                    print('Arduino interface received an incorrect command.')

        # figure out how to receive messages from Arduino, add it here.

        sleep(cfg.threads_delay)

    ser.close()
    print("Arduino Interace terminated.")


def get_arduino_port():
    # finds the arduino COM port using the os
    ports = subprocess.check_output(["ls /dev/*"], shell=True)
    ports = ports.decode('utf-8')
    ports_list = ports.split('\n')
    for port in ports_list:
        if port.find("usbmodem") != -1:
            return port
    return None


def test(ser):
    while True:
        val = input("Enter 1 or 0 to control Arduino LED. Type end to end and close the port")
        if val == 'end':
            ser.close()
            break
        else:
            ser.write(val.encode())


if __name__ == "__main__":
    main()
