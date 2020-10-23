import secrets
# contains configurations for program


# -- main_script --
threads_delay = 0.005
# todo add in debug messages
debug_messages = True

# interface flags
launch_twitch_bot = True
launch_arduino_interface = True
launch_osc_interface = True
launch_obs_interface = True


# -- twitch_bot --
HOST = "irc.chat.twitch.tv"
PORT = 6667
# authentification for twitch bot
NICK = secrets.NICK     # name of account used for the bot
PASS = secrets.PASS     # oauth token for bot account: https://twitchapps.com/tmi/
CHAN = secrets.CHAN     # name of channel the bot watches

twitch_commands = [
    "chat()"
]

twitch_accepted_messages = [
    "start",
    "beep",
    "bloop",
    "dink",
    "thing",
    "light",
    "color",
    "kicks",
    "hats",
    "faster",
    "slower",
    "stop"
]
# spam filter ignores new messages from any chatter that occur within a set time from the previous one that was accepted
# set to 0 to turn off the filter
twitch_chat_spam_filter_seconds = 2



# -- arduino_interface --
COM_PORT = None  # Manually enter (and override automatic) COM port for the Arduino
BAUD = 9600

arduino_commands = {
    "dac_value": "3",
    "lowCap_pwm": "4",
    "solenoid_on": "s",
    "solenoid_off": "t",
    "bloop_on": "b",
    "bloop_off": "c",
    "projector": "p",
    "projector_off": "q",
    "eyes_on": "e",
    "eyes_off": "f",
    "mouth_on": "m",
    "mouth_off": "n",
    "lamp_on": "l",
    "lamp_off": "o",
    "motor_pwm": "7"

}


# -- osc_interface --
UDP_IP = "127.0.0.1"    # localhost
UDP_R_PORT = 7400       # port for receiving UDP messages
UDP_S_PORT = 7401       # port for sending UDP messages

osc_commands = {

}


# -- obs_interface --
overlay_texts = [
    "start",
    "beep",
    "bloop",
    "dink",
    "thing",
    "light",
    "color",
    "kicks",
    "start",
    "hats",
    "beep",
    "bloop",
    "faster",
    "slower",
    "stop"
]

subtitles = [
    "",
    "Hello, my name is Performuino J. Bot.",
    "01100010 01100101 01100101 01110000\n00100000 01100010 01100101 01100101",  # 01110000 00100000 \n01100010 01101100 01101111 01101111 01110000",
    "Thank you for coming to my performance.",
    "Tonight I will be playing music for you, \nbut I need your help.",
    "I just built this cool synthesiser, \nbut my arms are too short to reach it.",
    "I didn't really think about that when\nI made it but...",
    "You can play it for me!",
    "All you have to do is type one of the\ncommands on the right side of the screen.",
    "And the synthesiser will obey!",
    "Stupid robot haha.",
    "OK, how about you start by turning on\nthe synthesiser?",
    "Cool, thanks!",
    "Ooo, those are some nice frequencies!",
    "OK, now how about adding some cool\nbeeps?",
    "Hmm... looks like twitch is being a\nnaughty robot",
    "You can try to add another word after \nthe command to trick it.",
    "Or you can try this cool bloop!",
    "Mmm, 35.2 Hertz.. my favorite :)",
    "That's pretty cool guys, but check\nthis out!",
    "I took drumming lessons at robot high\nschool. Can you tell?",
    "Let's see if I still remember my signature\nsolo.",
    "Oh yeah! Did you see that? I still got it.",
    "Um.. Can you turn the synth back\non please?",
    "Thanks",
    "OK, let's get back to making cool music.",
    "I'll play the drums and you play\nthe synth.",
    "Hey! What are you doing?",
    "Stop that!",
    "I was supposed to play the drums :(",
    "Whatever. I didn't like the drums anyway",
    "And besides, this other thing I have\nis much cooler!",
    "hihi, bet you're all pretty jealous\nnow huh?",
    "Oh my circuits!",
    "No. What are you doing?",
    "Leave my thing alone!",
    "You don't understand what you are doing!",
    "We're all going to die!",
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "",
    "ow.",
    "oww, my circuits.",
    "What's wrong with you guys?",
    "I mean what the actual fuck.",
    "You could have killed me!",
    "You clearly have no respect for me\nand my art!",
    "And can you stop playing with that stupid\nlight. This isn't a disco.",
    "Oh my...",
    "This was supposed to be a relaxing\nperformance.",
    "But...",
    "Whatever.",
    "How about you guys play those cool beeps\nand bloops again?",
    "Come on make it faster!",
    "Can you go a bit slower guys?\nMy arm is getting tired.",
    "I just haven't practiced drumming in a\nwhile. Don't judge me.",
    "Weeeeeeeee this is fun :)",
    "OK guys, I'm getting pretty tired.",
    "Can you turn off the synth for me?",
    "Phew.",
    "That was fun.",
    "Thanks for your help guys",
    "Even though you almost killed me...",
    "I think we are a pretty good team :)",
    "But please be a bit more careful next time...",
    "Robots are sensitive.",
    "Well, anyway...",
    "Thank you all again for coming to my\nperformance.",
    "Enjoy the summer.",
    "And to all my fellow robots watching:",
    "01000101 01011000 01010100 01000101 01010010 \n01001101 01001001 01001110 01000001 01010100",
    "Good night!"



]