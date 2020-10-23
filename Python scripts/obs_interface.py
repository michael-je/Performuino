import glob
import cfg

from time import sleep

overlay_counter = 0
max_overlay_counter = len(cfg.overlay_texts) - 1


def process_command(command):
    global overlay_counter
    if not isinstance(command, tuple):
        command = (command, "")

    if command[0] == "commands_next":
        if overlay_counter <= max_overlay_counter:
            overlay_file = open("text_overlay_commands.txt", "a")
            overlay_file.write(cfg.overlay_texts[overlay_counter])
            overlay_file.write("\n")
            overlay_file.close()
            overlay_counter += 1
        else:
            print("No more messages in cfg.overlay_texts.")

    elif command[0] == "display_subtitle":
        subtitle_file = open("text_overlay_subtitles.txt", "w")
        try:
            subtitle_file.write(cfg.subtitles[command[1]])
        except IndexError:
            print("Invalid subtitle index.")
        subtitle_file.close()

    elif command[0] == "commands_on":
        overlay_file = open("text_overlay_commands.txt", "a")
        overlay_file.write("COMMANDS:\n\n")
        overlay_file.close()

    elif command[0] == "commands_reset":
        overlay_file = open("text_overlay_commands.txt", "w")
        overlay_file.close()
        overlay_counter = 0

    elif command[0] == "commands_soft_reset":
        overlay_file = open("text_overlay_commands.txt", "w")
        overlay_file.close()

    else:
        print("Invalid command for OBS.")


def main():
    overlay_file = open("text_overlay_commands.txt", "w")  # first truncate any existing data in text_overlay_1
    overlay_file.close()
    subtitle_file = open("text_overlay_subtitles.txt", "w")
    subtitle_file.close()

    print("OBS interface online.")
    while not glob.terminate_flag:
        if glob.obs_commands:
            new_commands = glob.obs_commands[:]
            glob.obs_commands.clear()
            for command in new_commands:
                process_command(command)

        sleep(cfg.threads_delay)

    # truncate all the data from text_overlay_1 before closing
    overlay_file = open("text_overlay_commands.txt", "w")
    overlay_file.close()
    print("OBS interface terminated.")


if __name__ == "__main__":
    main()
