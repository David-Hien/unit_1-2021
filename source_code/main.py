# Import libraries
import time
import os
import vlc
import sys
import select
from threading import Thread

# Sound effects
sound_door_locked = vlc.MediaPlayer("sound_effects/sound_door_locked.mp3")
sound_door_creak = vlc.MediaPlayer("sound_effects/sound_door_creak.mp3")
sound_door_creak_open = vlc.MediaPlayer("sound_effects/sound_door_creak_open.mp3")
sound_door_open_close = vlc.MediaPlayer("sound_effects/sound_door_open_close.mp3")
sound_door_knock = vlc.MediaPlayer("sound_effects/sound_door_knock.mp3")
sound_door_slam = vlc.MediaPlayer("sound_effects/sound_door_slam.mp3")
sound_radio_buzz = vlc.MediaPlayer("sound_effects/sound_radio_buzz.mp3")
sound_radio_music1 = vlc.MediaPlayer("sound_effects/sound_radio_music1.mp3")
sound_radio_40128 = vlc.MediaPlayer("sound_effects/sound_radio_40128.mp3")
sound_baby_cry = vlc.MediaPlayer("sound_effects/sound_baby_cry.mp3")
sound_error = vlc.MediaPlayer("sound_effects/sound_error.mp3")
sound_gunshot = vlc.MediaPlayer("sound_effects/sound_gunshot.mp3")
sound_footsteps_closer = vlc.MediaPlayer("sound_effects/sound_footsteps_closer.mp3")
sound_footsteps_away = vlc.MediaPlayer("sound_effects/sound_footsteps_away.mp3")


# These functions store values independently
# Records name
def name_record(string: str):
    name_record.name = string


# Modify the archive list
def archive_modifier(list_value: str):
    if list_value == "reset":
        archive_modifier.archive_list = []
    else:
        archive_modifier.archive_list.append(list_value)


# Acts as a trigger once certain conditions are met
def basement_unlock(status: bool):
    basement_unlock.is_unlock = status


def bathroom_unlock(status: bool):
    bathroom_unlock.is_unlock = status


def entrance_unlock(status: bool):
    entrance_unlock.is_unlock = status


def taken_cover(status: bool):
    taken_cover.is_safe = status


# Function for time recording
def time_record(t: int):
    # Checks if status True then stops
    while not time_record_pause.status:
        time.sleep(1)
        t += 1

    mins, secs = divmod(t, 60)
    time_record.t = t
    time_record.timer = "{:02d}:{:02d}".format(mins, secs)


# Let time_record function know when to stop
def time_record_pause(status: bool):
    time_record_pause.status = status


# Caesar cypher encryptor used to encode that database
def message_encoder(key: int, message: str):
    secret_message = ""
    for letter in message:
        code = ord(letter) + key
        while code > 122:
            code -= 57

        encoded_letter = chr(code)
        secret_message += encoded_letter

    return secret_message


# Decodes the Caesar cypher
def message_decoder(key: int, message: str):
    decoded_message = ""
    for letter in message:
        code = ord(letter) - key
        while code < 65:
            code += 57

        decoded_letter = chr(code)
        decoded_message += decoded_letter

    return decoded_message


# Function for setup, start of game
def setup():
    # Reset everything
    basement_unlock(False)
    bathroom_unlock(False)
    entrance_unlock(False)
    time_record_pause(False)
    taken_cover(False)
    archive_modifier("reset")
    # CLear terminal
    os.system('clear')
    # Print main screen
    print("\t\t\t\t" + '\033[1m' + "NIGHTMARE" + '\033[0m', end='\n')
    print("1.New game")
    print("2.Load game")
    print("3.Leaderboard")
    print("4.Credits")
    print("5.Quit")
    # User input
    game_choice = input("Select option 1 to 5: ")
    if game_choice.isnumeric():
        game_choice = int(game_choice)
        if game_choice == 1:
            new_game()
        elif game_choice == 2:
            load_game()
        elif game_choice == 3:
            leaderboard()
        elif game_choice == 4:
            credit()
        elif game_choice == 5:
            quit_game()
        else:
            os.system('clear')
            print(f"'{game_choice}' not recognized.")
            setup()
    else:
        os.system('clear')
        print(f"'{game_choice}' not recognized.")
        setup()


# Creates new game and record player name
def new_game():
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "NEW GAME" + '\033[0m', end='\n')
    name = input("Enter player name: ")
    # Record player name
    name_record(string=name)
    print(f"\nWelcome {name}!")
    input("\n\t\t\t\tPress Enter to start. ")
    # Start timer as a Thread
    time_record_thread = Thread(target=time_record, args=(1,))
    time_record_thread.start()
    prologue_1()


# Load an existing game from the database
# Check for saves
def load_game():
    os.system('clear')
    with open("database.txt", "r") as file:
        # Check for saves
        if file.read() == "":
            print("No saves yet.")
            time.sleep(2)
            input("\n\t\t\tPress Enter to go back to start page. ")
            setup()
        else:
            print("\t\t\t\t" + '\033[1m' + "LOAD GAME" + '\033[0m', end='\n')
            load_game_print()


# Print options
def load_game_print():
    # Print load options
    with open("database.txt", "r") as file:
        i = 0
        for line in file.readlines():
            i += 1
            name_update, event_update, archive_update, time_update = line.split(', ')
            mins, secs = divmod(int(time_update), 60)
            time_formated = "{:02d}:{:02d}".format(mins, secs)
            print(f"{i}.{message_decoder(int(time_update), name_update)}, {event_update}, {time_formated}")

        print(f"{i + 1}.Quit to menu")
        save_slot = input("Enter save slot number: ")
        if save_slot.isnumeric():
            save_slot = int(save_slot)
            if save_slot > i + 1 or save_slot <= 0:
                os.system('clear')
                print(f"'{save_slot}' not recognized.")
                load_game()
            elif save_slot == i + 1:
                setup()
            else:
                load_game_load(save_slot=save_slot)
        else:
            os.system('clear')
            print(f"'{save_slot}' not recognized.")
            load_game()


# Load the selected save
def load_game_load(save_slot: int):
    os.system('clear')
    with open("database.txt", "r") as file:
        name, event, archive_update, time_update = file.readlines()[int(save_slot) - 1].split(', ')

    name = message_decoder(int(time_update), name)
    print(f"Welcome back {name}!")
    # Update all variables
    name_record(string=name)
    archive_list_update(archive_update=archive_update)
    time.sleep(2)
    # Start time_record
    time_record_pause(False)
    time_record_thread = Thread(target=time_record, args=(int(time_update),))
    time_record_thread.start()
    # Run the function equilavent to the loaded save
    if event.count("Chapter"):
        eval(f"chap{event.split(' ')[-1]}")()
    else:
        prologue_1()


# Shows the list of names + time/score in order
def leaderboard():
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "LEADERBOARD" + '\033[0m', end='\n')
    with open("leaderboard.txt", "r") as file:
        i = 0
        for lines in file.readlines():
            i += 1
            player, score = lines.split(", ")
            mins, secs = divmod(int(score), 60)
            score = "{:02d}:{:02d}".format(mins, secs)
            print(f"{i}.{player}, {score}")

    input("\n\t\t\t\tPress Enter to go back. ")
    setup()


def leaderboard_update():
    time_record_pause(status=True)
    time.sleep(1)
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name_record.name}, {time_record.t}\n")

    with open("leaderboard.txt", "r") as file:
        tup = []
        # Put the player names with their corresponding time into tuples
        # and sort them from smallest to largest based on time
        for lines in file.readlines():
            tup.append(tuple((lines.split(", ")[0], lines.split(", ")[1])))

        tup.sort(key=lambda x: x[1])

    with open("leaderboard.txt", "w") as file:
        for lines in tup:
            file.write(f"{lines[0]}, {lines[1]}")


def credit():
    os.system('clear')
    with open("credit.txt", "r") as file:
        lines = file.readlines()
        skip_line = "\n"
        for i in range(1, 25):
            os.system('clear')
            print(skip_line * (24 - i))
            for j in range(i):
                print(lines[j], end='')

            time.sleep(0.8)

        time.sleep(5)

    sound_radio_music1.stop()
    setup()


def quit_game():
    pass


# Function menu
def menu(event: str):
    # Pause time_record
    time_record_pause(True)
    sound_radio_music1.pause()
    os.system('clear')
    time.sleep(1)
    print(time_record.timer)
    print("\t\t\t\t" + '\033[1m' + "MENU" + '\033[0m', end='\n')
    print("1.Resume")
    print("2.Save game")
    print("3.Archive")
    print("4.Quit")
    menu_choice = input("Select option 1 to 4: ")
    if menu_choice.isnumeric():
        menu_choice = int(menu_choice)
        if menu_choice == 1:
            os.system('clear')
            sound_radio_music1.play()
            # Resumes time_record
            time_record_pause(status=False)
            time_record_thread = Thread(target=time_record, args=(time_record.t,))
            time_record_thread.start()
            pass
        elif menu_choice == 2:
            save_game(event=event)
            setup()
        elif menu_choice == 3:
            archive()
            menu(event=event)
        elif menu_choice == 4:
            setup()
        else:
            os.system('clear')
            print(f"'{menu_choice}' not recognized.")
            menu(event=event)
    else:
        os.system('clear')
        print(f"'{menu_choice}' not recognized.")
        menu(event=event)


# Append the 'event' into the database to be used for load_game
def save_game(event: str):
    os.system('clear')
    with open("database.txt", "a") as file:
        file.write(f"\n{message_encoder(time_record.t, name_record.name)}, {event}, "
                   f"{len(archive_modifier.archive_list)}, {time_record.t}")

    print(f"Saving game", end='')
    for i in range(3):
        time.sleep(1)
        print(".", end='')

    time.sleep(1.5)


# User can access documents opened
def archive():
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "ARCHIVE" + '\033[0m', end='\n')
    archive_list_length = len(archive_modifier.archive_list)
    for i in range(archive_list_length):
        print(f"{i + 1}.{archive_modifier.archive_list[i]}")

    print(f"{archive_list_length + 1}.Quit to menu")
    archive_choice = input(f"Select option 1 to {archive_list_length + 1}: ")
    if archive_choice.isnumeric():
        os.system('clear')
        archive_choice = int(archive_choice)
        if archive_choice == archive_list_length + 1:
            pass
        else:
            eval(archive_modifier.archive_list[archive_choice - 1])(2)
            archive()
    else:
        archive()


# Modify the archive based on the saved data from the database
def archive_list_update(archive_update: str):
    archive_modifier("reset")
    with open("archive_list_completed.txt", "r") as file:
        line = file.readline().split(', ')
        for i in range(int(archive_update)):
            archive_modifier(list_value=line[i])


# Prints out the narration from narration.txt
def narrate(start: int, end: int):
    with open("narration.txt", "r") as file:
        t = file.readlines()
        lines = start - 1
        while lines < end:
            for letters in t[lines]:
                print(letters, end='')
                time.sleep(0.03)
            time.sleep(0.8)
            lines += 1


# Use from chapter 2 onwards, executes player's input
def input_recognize(chapter_num: int):
    print("\nNote: Type 'help' into the console to see command list.")
    choice = input("\n>")
    if choice == "menu":
        menu(f"Chapter {chapter_num}")
        input_recognize(chapter_num=chapter_num)
    elif choice == "help":
        with open("command_list.txt", "r") as file:
            print(file.read())
        input_recognize(chapter_num=chapter_num)
    elif choice == "clear console":
        os.system('clear')
        input_recognize(chapter_num=chapter_num)
    else:
        try:
            eval(choice)(int(chapter_num))
        except NameError:
            print(f"'{choice}' not recognized.")
        except SyntaxError:
            print(f"'{choice}' not recognized.")
        except TypeError:
            print(f"'{choice}' not recognized.")
        input_recognize(chapter_num=chapter_num)


def input_recognize_alter(access_point: int, wait: int):
    start = time.time()
    print("\nNote: Type 'help' into the console to see command list.")
    print("\n>", end='')
    # Create a temporal input that allows the user to input within a certain amount of time
    i, o, e = select.select([sys.stdin], [], [], float(wait))
    if i:
        def delay_fix(wait_new: int):
            end = time.time()
            wait_new -= end - start
            try:
                input_recognize_alter(access_point=access_point, wait=wait_new)
            except ValueError:
                game_over(1)

        choice = sys.stdin.readline().strip()
        if choice == "menu":
            print("Can't access menu due to active quest.")
            delay_fix(wait_new=wait)
        elif choice == "help":
            with open("command_list.txt", "r") as file:
                print(file.read())
            delay_fix(wait_new=wait)
        elif choice == "clear console":
            os.system('clear')
            delay_fix(wait_new=wait)
        else:
            try:
                eval(choice)(access_point)
            except NameError:
                print(f"'{choice}' not recognized.")
            except SyntaxError:
                print(f"'{choice}' not recognized.")
            except TypeError:
                print(f"'{choice}' not recognized.")
            delay_fix(wait_new=wait)
    else:
        if access_point == 4:
            if taken_cover.is_safe:
                time.sleep(4)
                sound_footsteps_away.play()
                time.sleep(25)
                sound_footsteps_away.stop()
                sound_door_open_close.audio_set_volume(40)
                sound_door_open_close.play()
                time.sleep(6)
                sound_door_open_close.stop()
                basement_unlock(status=True)
                input("\n\t\t\t\tPress Enter to leave. ")
                entrance_unlock(status=True)
                sound_radio_music1.audio_set_volume(100)
            else:
                game_over(1)


# Function for the transition between chapters
def chapter_transition(chap_name1: str, chap_name2: str, chap_name3: str):
    os.system('clear')
    time.sleep(2)
    print(f"\n\t\t\t\t{chap_name1} end")
    time.sleep(2)
    sound_door_open_close.play()
    time.sleep(2)
    os.system('clear')
    print(f"\n\t\t\t{chap_name2}", end=" ")
    time.sleep(2)
    print('\033[1m' + chap_name3 + '\033[0m')
    time.sleep(4)
    sound_door_open_close.stop()
    os.system('clear')


def door_locked():
    sound_door_locked.play()
    time.sleep(2.5)
    print('\033[3m' + "\nlocked." + '\033[0m')
    time.sleep(1)
    sound_door_locked.stop()
    input("\n\t\t\t\tPress Enter to go back. ")


# Function 'game over'
def game_over(access_point):
    if access_point == 1:
        sound_gunshot.play()
        time.sleep(1.92)
        sound_gunshot.stop()
        sound_radio_music1.stop()
        os.system('clear')
        with open("game_over_screen1.txt", "r") as file:
            print(file.read())

    sound_radio_buzz.play()
    time.sleep(3.5)
    sound_radio_buzz.stop()
    os.system('clear')
    time.sleep(1)
    input("\n\t\t\t\tPress Enter to continue.")
    save_game(event="Chapter 4")


# Function 'memo1'
def memo1(access_point: int):
    os.system('clear')
    with open("memo1.txt", "r") as memo1_reader:
        print(memo1_reader.read())

    if access_point == 1:
        archive_modifier(list_value="memo1")

    time.sleep(3)
    input("\n\t\t\t\tPress Enter to leave.")
    pass


# Function 'newspaper1'
def newspaper1(access_point: int):
    os.system('clear')
    print("\t\t\t" + '\033[1m' + "Family brutally murdered by the father" + '\033[0m', end='\n')
    with open("newspaper1.txt", "r") as file:
        print(file.read())

    if access_point == 1:
        archive_modifier(list_value="newspaper1")

    time.sleep(3)
    input("\n\t\t\t\tPress Enter to leave.")
    pass


# Function 'clock'
def clock(clock_version: int):
    if clock_version == 1 or clock_version == 3 or clock_version == 4:
        print('\033[3m' + "\n23:59" + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to leave. ")
        pass
    elif clock_version == 2:
        print('\033[3m' + "\n23:58" + '\033[0m')
        time.sleep(1)
        print("\n\t\t\t\tPress Enter to leave. ", end='')
        i, o, e = select.select([sys.stdin], [], [], 9)
        if i:
            input()
            pass
        else:
            os.system('clear')
            print('\033[3m' + "\n23:59" + '\033[0m')
            basement_unlock(status=True)
            input("\n\t\t\t\tPress Enter to leave. ")
            sound_door_creak.play()
            time.sleep(5)
            pass


def door_entrance(access_point: int):
    if access_point:
        if entrance_unlock.is_unlock:
            time.sleep(1)
            narrate(start=115, end=115)
            input("\n\t\t\t\tPress Enter to countinue. ")
            chapter_transition(chap_name1="Chapter 4", chap_name2="\tThe end.", chap_name3="")
            leaderboard_update()
            credit()
        else:
            door_locked()
            pass


def phone(access_point: int):
    if access_point:
        number = input("\n\t\tDial number or press Enter to go back. ")
        if number == "":
            pass
        elif number.isnumeric():
            if number == "40128" and access_point == 4:
                bathroom_unlock(status=True)
                time.sleep(0.5)
                sound_door_creak_open.play()
                time.sleep(5)
                sound_door_creak_open.stop()

                def footsteps_closer():
                    sound_footsteps_closer.play()
                    time.sleep(30)
                    sound_footsteps_closer.stop()

                footsteps_closer_thread = Thread(target=footsteps_closer)
                footsteps_closer_thread.start()
                input_recognize_alter(access_point=4, wait=30)
                pass
            else:
                os.system('clear')
                time.sleep(1.5)
                narrate(75, 76)
                time.sleep(1)
                phone(access_point=access_point)
        else:
            os.system('clear')
            print(f"'{number}' has to be integers.")
            phone(access_point=access_point)


def radio(access_point: any):
    if access_point == 1 or access_point == 2 or access_point == 3:
        time.sleep(1.5)
        narrate(start=80, end=80)
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass
    elif access_point == 4:
        time.sleep(1.5)
        print('\033[3m' + "\nNow playing: Camille Saint-Saëns by Danse Macabre" + '\033[0m')
        time.sleep(1.5)
        sound_radio_music1.audio_set_volume(60)
        time.sleep(0.5)
        sound_radio_40128.play()
        time.sleep(5)
        sound_radio_40128.stop()
        sound_radio_music1.audio_set_volume(100)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass
    elif access_point == "radio_music1":
        sound_radio_music1.play()


def bathroom(access_point: int):
    if access_point == 1:
        door_locked()
        pass
    elif access_point == 2:
        door_locked()
        time.sleep(0.5)
        print("\n>", end='')
        time.sleep(3)
        sound_door_knock.play()
        time.sleep(2)
        sound_door_knock.stop()
        pass
    elif access_point == 3:
        if bathroom_unlock.is_unlock:
            time.sleep(1.5)
            narrate(start=95, end=96)
            sound_baby_cry.play()
            time.sleep(1)
            narrate(start=97, end=98)
            time.sleep(1.5)
            sound_baby_cry.stop()
            sound_door_slam.play()
            time.sleep(0.5)
            sound_door_slam.stop()
            narrate(start=99, end=102)
            time.sleep(2)
            basement_unlock(status=True)
            input("\n\t\t\t\tPress Enter to go back. ")
            sound_door_creak.play()
            time.sleep(5)
            sound_door_creak.stop()
            pass
        else:
            door_locked()
            pass
    elif access_point == 4:
        if bathroom_unlock.is_unlock:
            time.sleep(1)
            sound_door_slam.audio_set_volume(70)
            sound_door_slam.play()
            time.sleep(0.8)
            sound_door_slam.stop()
            sound_radio_music1.audio_set_volume(60)
            taken_cover(status=True)
        else:
            door_locked()
            pass


def basement(access_point: int):
    if access_point == 2:
        if basement_unlock.is_unlock:
            time.sleep(1.5)
            narrate(start=84, end=84)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to countinue. ")
            basement_unlock(status=False)
            chapter_transition(chap_name1="Chapter 2", chap_name2="\tChapter 3", chap_name3="DUSK")
            chap3()
        else:
            sound_door_locked.play()
            time.sleep(2.5)
            print('\033[3m' + "\nlocked." + '\033[0m')
            time.sleep(1)
            sound_door_locked.stop()
            narrate(start=86, end=87)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to go back. ")
            pass
    if access_point == 3:
        if basement_unlock.is_unlock:
            time.sleep(1.5)
            narrate(start=106, end=106)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to countinue. ")
            bathroom_unlock(status=False)
            basement_unlock(status=False)
            chapter_transition(chap_name1="Chapter 3", chap_name2="Chapter 4", chap_name3="THE MAN WITH THE GUN")
            chap4()
        else:
            door_locked()
            print("\n>", end='')
            time.sleep(3)
            sound_door_creak_open.play()
            time.sleep(5)
            sound_door_creak_open.stop()
            bathroom_unlock(status=True)
            pass
    if access_point == 4:
        door_locked()
        pass


# Function 'prologue_1'
def prologue_1():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=2, end=5)
    time.sleep(2)
    prologue1_memo()

    # prologue1_memo

    os.system('clear')
    sound_door_creak.play()
    time.sleep(5)
    sound_door_creak.stop()
    narrate(start=7, end=8)
    time.sleep(2)
    prologue2_exit()

    # prologue2_exit


def prologue1_memo():
    choice = input("\n\t\t\t\tPress E to read. ")
    if choice.lower() == "e":
        memo1(access_point=1)
    elif choice == "menu":
        menu(event="Prologue")
        prologue1_memo()
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        prologue1_memo()


def prologue2_exit():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice.lower() == "e":
        chap1_0()
    elif choice == "menu":
        menu(event="Prologue")
        prologue2_exit()
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        prologue2_exit()


# Function 'chap1'
def chap1_0():
    chapter_transition(chap_name1="Prologue", chap_name2="Chapter 1", chap_name3="THE BEGINNING")
    time.sleep(3)
    print("Note: You can access the menu at any point by typing 'menu' into the console.")
    time.sleep(2)
    print("\nNote: Readings such as memos can be accessed via 'archive' in the menu.")
    time.sleep(2)
    chap1_note()

    # chap1_note


def chap1_1():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=12, end=14)
    time.sleep(2)
    sound_door_slam.play()
    time.sleep(0.8)
    sound_door_slam.stop()
    narrate(start=16, end=17)
    time.sleep(2)
    chap1_hallway_door()

    # chap1_hallway_door


def chap1_2():
    os.system('clear')
    sound_door_locked.play()
    time.sleep(2.5)
    sound_door_locked.stop()
    narrate(start=19, end=23)
    time.sleep(2)
    chap1_clock()

    # chap1_clock()


def chap1_3():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=25, end=28)
    time.sleep(2)
    chap1_newspaper()

    # chap1_newspaper


def chap1_4():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=30, end=36)
    time.sleep(2)
    chap1_entrance_door()

    # chap1_entrance_door()


def chap1_5():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=38, end=41)
    time.sleep(2)
    chap1_phone()

    # chap1_phone


def chap1_6():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=43, end=45)
    time.sleep(2)
    chap1_bathroom()

    # chap1_bathroom()


def chap1_7():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=47, end=49)
    time.sleep(2)
    chap1_radio()

    # chap1_radio()


def chap1_8():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=51, end=52)
    time.sleep(1)
    narrate(start=53, end=56)
    time.sleep(2)
    chap1_end()


def chap1_note():
    choice = input("\n\t\t\t\tPress Enter to continue. ")
    if choice == "":
        chap1_1()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_note()


def chap1_hallway_door():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice.lower() == "e":
        chap1_2()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_hallway_door()


def chap1_clock():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice.lower() == "e":
        clock(clock_version=1)
        chap1_3()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_clock()


def chap1_newspaper():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice.lower() == "e":
        newspaper1(access_point=1)
        chap1_4()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_newspaper()


def chap1_entrance_door():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice.lower() == "e":
        door_entrance(access_point=1)
        chap1_5()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_entrance_door()


def chap1_phone():
    phone(access_point=1)
    chap1_6()


def chap1_bathroom():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice.lower() == "e":
        bathroom(access_point=1)
        chap1_7()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_bathroom()


def chap1_radio():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice.lower() == "e":
        radio(access_point=1)
        chap1_8()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_radio()


def chap1_end():
    choice = input("\n\t\t\t\tPress Enter to continue. ")
    if choice == "":
        chapter_transition(chap_name1="Chapter 1", chap_name2="\tChapter 2", chap_name3="LOOP")
        chap2()
    elif choice == "menu":
        menu(event="Chapter 1")
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_radio()


def chap2():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=60, end=71)
    time.sleep(2)
    input("\n\t\t\t\tPress Enter. ")
    os.system('clear')
    input_recognize(chapter_num=2)


def chap3():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=91, end=91)
    time.sleep(2)
    input("\n\t\t\t\tPress Enter. ")
    input_recognize(chapter_num=3)


def chap4():
    os.system('clear')
    time.sleep(1.5)
    narrate(start=110, end=111)
    time.sleep(2)
    input("\n\t\t\t\tPress Enter. ")
    radio(access_point="radio_music1")
    input_recognize(chapter_num=4)


setup()
