import glob
import re

commands = (
    "(q)uit",
    "(c)ommands",
    "chat()",
    "osc()",
    "obs()"
)


def main():
    print('User interface online. Enter "c" too see commands.')
    while not glob.terminate_flag:
        # try:
        raw_input = input()
        if raw_input.lower() == "q":
            glob.terminate_flag = True
            print("Terminating program.")

        elif raw_input.lower() == "c":
            print("commands: ", ", ".join(commands))

        elif raw_input[:4].lower() == "chat":
            msg = re.search(r"\(.*\)", raw_input).group()[1:-1]
            glob.twitch_commands.append(("chat", msg))
            print("Sending message to twitch chat.")

        elif raw_input[:3].lower() == "osc":
            # todo resolve how to send raw messages, instead of string objects incased in ""
            msg = re.search(r"\(.*\)", raw_input).group()[1:-1]
            glob.osc_commands.append(("/command", msg))
            print("Sending message to OSC client.")

        elif raw_input[:3].lower() == "obs":
            msg = re.search(r"\(.*\)", raw_input).group()[1:-1]
            glob.obs_commands.append(msg)
            print("Sending message to OBS.")

        else:
            print("Invalid command.")

        # maybe implement this later
        # elif raw_input[:3] == "ban":
        #     user = re.search(r"\(\w+\)", raw_input).group()[1:-1]
        #     print(1)
        #     glob.twitch_commands.append(("ban", user))
        #
        # elif raw_input[:7] == "timeout":
        #     user = re.search(r"\(\w+\)", raw_input).group()[1:-1]
        #     print(3)
        #     glob.twitch_commands.append(("timeout", user))
        # todo test and find possible exception cases
        # except: