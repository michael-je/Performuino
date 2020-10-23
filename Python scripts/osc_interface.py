# commands sent to the OSC_interface should be tuples, so that the data can be routed client-side
# tuples should contain 2 elements (route, msg). Both should be strings.

import glob
import cfg

from pythonosc import udp_client, osc_server, dispatcher
from time import sleep
import threading


def receive_server(s):
    # simple function that the server_thread should target
    s.serve_forever()


def example_handler(*args):
    # handles messages passed by the dispatcher
    filter_arg, *msg_args = args
    msg_args = tuple(msg_args)
    glob.inbound_messages.append(('osc', msg_args))


# filters messages received by the server and passes them to the handler
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/command", example_handler)
# todo add filters for dispatcher


def main():
    # intialise the client and server_thread
    client = udp_client.SimpleUDPClient(cfg.UDP_IP, cfg.UDP_S_PORT)

    server = osc_server.ThreadingOSCUDPServer((cfg.UDP_IP, cfg.UDP_R_PORT), dispatcher)
    server_thread = threading.Thread(target=receive_server, args=[server], daemon=True)
    server_thread.start()

    print("OSC server online.")
    while not glob.terminate_flag:
        if glob.osc_commands:
            new_commands = glob.osc_commands[:]
            glob.osc_commands.clear()

            for command in new_commands:
                route, msg = command
                client.send_message(route, msg)
                print(f"sent {route} {msg} to osc")

        sleep(cfg.threads_delay)

    print("OSC server terminated.")


if __name__ == "__main__":
    main()