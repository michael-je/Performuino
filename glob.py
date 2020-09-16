terminate_flag = False

# all inbound messages are appended to this list
# ("where I come from", (what, I, say))
#   ('twitch', ("msg", "sender_username"))
#   ('arduino')
#   ('osc',[filter1, filter2, .., "msg"])
inbound_messages = []

twitch_commands = []    # outbound messages to twitch   ("command", "msg")
arduino_commands = []   # outbound messages to arduino  ("command")
osc_commands = []       # outbound messages to osc      ("route1 route2 route3...", "command")
obs_commands = []       # outbound messages to obs

opList = {}             # used to identify current chat memebers, currently not being used

# progress flags are used to mark when an event happens, limiting or making available certain actions
progress_flags = {
    "start_available": False,
    "beep_available": False,
    "bloop_available": False,
    "dink_available": False,
    "thing_available": False,
    "light_available": False,
    "color_available": False,
    "kick_available": False,
    "hats_available": False,
    "faster_available": False,
    "slower_available": False,
    "stop_available": False
}