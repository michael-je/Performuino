# twitch bot can only receive commands as tuples.

import cfg
import glob

import socket
import re
from time import sleep
from datetime import datetime

chatter_times = {}


def main():
    # connect to the twitch API and give credentials provided in cfg
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    # regular expression comilpiles for parsing the raw messages later
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    CHAT_MSG_SENDER = re.compile(r"^:\w+")

    connected_flag = False
    while not glob.terminate_flag:
        # block that handles incoming messages from twitch chat
        try:
            response_buffer = s.recv(1024).decode("utf-8")
            seperated_responses = response_buffer.split('\r\n')

            for raw_response in seperated_responses:
                # When the server sends over a ping we must reply with pong, else we get disconnected
                if raw_response == "PING :tmi.twitch.tv":
                    s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    print("PONG sent.")

                # this block runs while the bot is establishing a connection
                elif not connected_flag:
                    if __name__ == "__main__":  # debugging
                        print(raw_response)
                    if raw_response == f':{cfg.NICK}.tmi.twitch.tv 366 {cfg.NICK} #{cfg.CHAN} :End of /NAMES list':
                        connected_flag = True
                        # setblocking(0) along with the try/except block seems to fix the socket blocking problem
                        s.setblocking(False)
                        print("Twitch bot connected.")

                # runs once the bot is connected
                # parses the raw messages for the message content and sender username
                elif raw_response:  # because sometimes we receive empty messages
                    message = CHAT_MSG.sub("", raw_response)
                    sender_username = CHAT_MSG_SENDER.search(raw_response).group()[1:]

                    if __name__ == "__main__" and message:  # debugging
                        print("raw_response:", raw_response)
                        print("message:", message)
                        print("message_sender:", sender_username)
                    elif message.find('tmi.twitch.tv') == -1 and message:
                        # print(f'new message received: {message}')
                        if cfg.twitch_chat_spam_filter_seconds:
                            if not filter_message(sender_username):
                                command = process_message(message)
                                print(f"message received = {message}, command {command}")
                                print(f"twitch bot: command = {command}")
                                if command is not None:
                                    glob.inbound_messages.append(('twitch', command))
                                    print(command)
                            else:
                                print("Message blocked.")

        # this exception is raised if there is no data in the recv buffer, we want to ignore it and keep running
        except BlockingIOError:
            pass

        # block that handles outgoung messages to twitch chat
        if glob.twitch_commands:
            new_commands = glob.twitch_commands[:]
            glob.twitch_commands.clear()

            for command in new_commands:
                if command[0] == 'chat':
                    send_chat_msg(s, command[1])

                # todo maybe implement this later
                # elif command[0] == 'ban':
                #     ban_user(s, command[1])
                # elif command[0] == 'timout':
                #     timout_user(s, command[1])

        sleep(cfg.threads_delay)
        
    s.close()
    print("Twitch bot terminated.")


def send_chat_msg(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))


def filter_message(chatter):
    # returns True if message should be ignored, false otherwise
    # also manages data in the global chatter_times dictionary
    output = False

    global chatter_times
    now = datetime.now()
    chatter_last_message_time = chatter_times.get(chatter)

    if chatter_last_message_time is not None:       # check whether the chatter already has a recorded time in the dict
        delta_datetime = now - chatter_last_message_time
        time_delta = delta_datetime.total_seconds()
        if time_delta < cfg.twitch_chat_spam_filter_seconds:    # if length between messages is less than set output to True, to block the message
            output = True
        else:
            chatter_times[chatter] = now    # otherwise leave output alone and just update their last message time
    else:
        chatter_times[chatter] = now
    return output


def process_message(message):
    # parse incoming messages and check if they fit to a command word
    # only checks if the first word of the message matches
    # if the first "word" is longer than 100 characters, the message is ignored
    words = message.split()
    if isinstance(words, list):
        first_word = words[0]
    else:
        first_word = words

    if len(first_word) > 100:
        return None
    else:
        parsed_word = "".join(c.lower() for c in first_word if c.isalpha())

    if parsed_word in cfg.twitch_accepted_messages:
        return parsed_word
    else:
        return None


# maybe implement this later
# def ban_user(sock, user):
#     send_chat_msg(sock, ".ban {}".format(user))
#     print("banning user: {}".format(user))
#
#
# def timout_user(sock, user, seconds=600):
#     # todo verify whether this works or not
#     send_chat_msg(sock, ".timout {} {}".format(user, seconds))
#     print("timing out user: {}, for {} seconds.".format(user, seconds))


if __name__ == "__main__":
    main()

