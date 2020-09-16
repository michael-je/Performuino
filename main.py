# The central handler of the script. It launches the threads which communicate with the various externals.
# These threads append their inputs to the glob.inbound_messages list, then this script processes them
# and sends out appropriate commands to the threads via their dedicated lists in glob
# todo create the polling mechanism for twitch chat
# todo it might be possible to just keep the processing functions in the interface scripts themselves, that would be some good optimisation

import arduino_interface
import twitch_bot
import osc_interface
import obs_interface
import ui
import glob
import cfg

import threading
from time import sleep


def main():
    print('\n -- Program launching. Enter "q" to terminate -- \n')
    # launches all interfaces in as threads
    if cfg.launch_twitch_bot:
        twitch_bot_thread = threading.Thread(target=twitch_bot.main)
        twitch_bot_thread.start()
    if cfg.launch_arduino_interface:
        arduino_interface_thread = threading.Thread(target=arduino_interface.main)
        arduino_interface_thread.start()
    if cfg.launch_osc_interface:
        osc_server_thread = threading.Thread(target=osc_interface.main)
        osc_server_thread.start()
    if cfg.launch_obs_interface:
        obs_interface_thread = threading.Thread(target=obs_interface.main)
        obs_interface_thread.start()
    ui_thread = threading.Thread(target=ui.main)
    ui_thread.start()

    while not glob.terminate_flag:
        if glob.inbound_messages:
            new_messages = glob.inbound_messages[:]
            glob.inbound_messages.clear()
            for message in new_messages:
                if message[0] == 'arduino':
                    process_arduino_message(message[1])
                elif message[0] == 'twitch':
                    process_twitch_message(message[1])
                elif message[0] == 'osc':
                    process_osc_message(message[1])

        sleep(cfg.threads_delay)

    print("Main script terminated.")


# noinspection PyRedundantParentheses
def process_arduino_message(message):
    # todo add in processing for arduino messages
    pass


def process_twitch_message(message):
    # this is temporary
    # direct commands from twitch chat to arduino
    # finds the correct command corresponding to a given keyword and sends it to arduino_interface
    if message == "start" and glob.progress_flags["start_available"]:
        glob.progress_flags["start_available"] = False
        glob.osc_commands.append(("start", "start"))
        print("start received")

    elif message == "beep" and glob.progress_flags["beep_available"]:
        glob.osc_commands.append(("beep", "beep"))

    elif message == "bloop" and glob.progress_flags["bloop_available"]:
        glob.osc_commands.append(("bloop", "bloop"))

    elif message == "dink" and glob.progress_flags["dink_available"]:
        glob.osc_commands.append(("dink", "dink"))

    elif message == "thing" and glob.progress_flags["thing_available"]:
        glob.osc_commands.append(("thing", "thing"))

    elif message == "light" and glob.progress_flags["light_available"]:
        glob.osc_commands.append(("light", "light"))

    elif message == "color" and glob.progress_flags["color_available"]:
        glob.osc_commands.append(("color", "color"))

    elif message == "kicks" and glob.progress_flags["kick_available"]:
        glob.osc_commands.append(("kicks", "kicks"))

    elif message == "hats" and glob.progress_flags["hats_available"]:
        glob.osc_commands.append(("hats", "hats"))

    elif message == "faster" and glob.progress_flags["faster_available"]:
        glob.osc_commands.append(("faster", "faster"))

    elif message == "slower" and glob.progress_flags["slower_available"]:
        glob.osc_commands.append(("slower", "slower"))

    elif message == "stop" and glob.progress_flags["stop_available"]:
        glob.osc_commands.append(("stop", "stop"))



def process_osc_message(message):
    # this is just an example
    if message[0] == 'LED':
        glob.arduino_commands.append(cfg.arduino_commands['led'])

    elif message[0] == 'lowCap':
        glob.arduino_commands.append(cfg.arduino_commands['lowCap'])

    elif message[0] == 'dac_value':
        glob.arduino_commands.append(cfg.arduino_commands['dac_value'])
        glob.arduino_commands.append((str(message[1])))
        glob.arduino_commands.append('!')

    elif message[0] == 'lowCap_pwm':
        glob.arduino_commands.append(cfg.arduino_commands['lowCap_pwm'])
        glob.arduino_commands.append((str(message[1])))
        glob.arduino_commands.append('!')

    elif message[0] == 'noise1':
        glob.arduino_commands.append(cfg.arduino_commands['noise1'])

    elif message[0] == 'noise2':
        glob.arduino_commands.append(cfg.arduino_commands['noise2'])

    elif message[0] == 'solenoid_on':
        glob.arduino_commands.append(cfg.arduino_commands['solenoid_on'])

    elif message[0] == 'solenoid_off':
        glob.arduino_commands.append(cfg.arduino_commands['solenoid_off'])

    elif message[0] == 'projector':
        glob.arduino_commands.append(cfg.arduino_commands['projector'])
        glob.arduino_commands.append(str(message[1]))

    elif message[0] in ["eyes_on", "eyes_off", "mouth_on", "mouth_off", "lamp_on", "lamp_off", "bloop_on", "bloop_off"]:
        glob.arduino_commands.append(cfg.arduino_commands[message[0]])

    elif message[0] == "voice":
        glob.obs_commands.append(("display_subtitle", int(message[1])))

    elif message[0] == "motor_pwm":
        glob.arduino_commands.append(cfg.arduino_commands["motor_pwm"])
        glob.arduino_commands.append((str(message[1])))
        glob.arduino_commands.append("!")

    elif message[0] == "commands_on":
        glob.obs_commands.append(("commands_on", ""))

    elif message[0] == "commands_reset":
        glob.obs_commands.append(("commands_reset", ""))

    elif message[0] == "commands_next":
        glob.obs_commands.append(("commands_next", ""))

    elif message[0] == "reset_flags":
        glob.progress_flags["start_available"] = False
        glob.progress_flags["beep_available"] = False
        glob.progress_flags["bloop_available"] = False
        glob.progress_flags["dink_available"] = False
        glob.progress_flags["thing_available"] = False
        # add in more flags later if needed

    elif message[0] == "flag":
        glob.progress_flags[message[1]] = bool(int(message[2]))
        print(f"flag set to {bool(int(message[2]))}")

    elif message[0] == "commands_soft_reset":
        glob.obs_commands.append(("commands_soft_reset", ""))

    elif message[0] == "projector_off":
        glob.arduino_commands.append(cfg.arduino_commands["projector_off"])




if __name__ == "__main__":
    main()
