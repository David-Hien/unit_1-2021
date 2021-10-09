# Import libraries
import time
import os
import vlc
from threading import Thread
from threading import Timer


# Sound effects
sound_door_locked = vlc.MediaPlayer("sound_effects/sound_door_locked.mp3")
sound_door_creak = vlc.MediaPlayer("sound_effects/sound_door_creak.mp3")
sound_door_creak_open = vlc.MediaPlayer("sound_effects/sound_door_creak_open.mp3")
sound_door_open_close = vlc.MediaPlayer("sound_effects/sound_door_open_close.mp3")
sound_door_knock = vlc.MediaPlayer("sound_effects/sound_door_knock.mp3")
sound_door_slam = vlc.MediaPlayer("sound_effects/sound_door_slam.mp3")
sound_phone_ring = vlc.MediaPlayer("")
sound_phone_call = vlc.MediaPlayer("")
sound_radio_buzz = vlc.MediaPlayer("")
sound_radio_warning = vlc.MediaPlayer("")
sound_baby_cry = vlc.MediaPlayer("sound_effects/sound_baby_cry.mp3")


# These functions store values independently
# Records name
def name_record(string):
    name_record.name = string


# Modify the archive list
def archive_modifier(list_value):
    if list_value == "reset":
        archive_modifier.archive_list = []
    else:
        archive_modifier.archive_list.append(list_value)


# Acts as a trigger once certain conditions are met
def basement_unlock(status):
    basement_unlock.is_unlock = status


def bathroom_unlock(status):
    bathroom_unlock.is_unlock = status


# Function for setup, start of game
def setup():
    basement_unlock(False)
    bathroom_unlock(False)
    archive_modifier("reset")
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "NIGHTMARE" + '\033[0m', end='\n')
    print("1.New game")
    print("2.Load game")
    print("3.Leaderboard")
    print("4.Credits")
    print("5.Quit")
    game_choice = input("Select option 1 to 4: ")
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
    name_record(name)
    print(f"\nWelcome {name}!")
    input("\n\t\t\t\tPress Enter to start. ")
    prologue_1()


# Load an existing game from the database
# Check for saves
def load_game():
    os.system('clear')
    with open("database.txt", "r") as file:
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
    with open("database.txt", "r") as file:
        i = 0
        for line in file.readlines():
            i += 1
            name_update, event_update, archive_update = line.split(', ')
            if event_update.count("Chapter"):
                chapter = event_update
            elif event_update.count("chap1"):
                chapter = "Chapter 1"
            elif event_update.count("prologue"):
                chapter = "Prologue"
            else:
                chapter = event_update
            print(f"{i}.{name_update}, {chapter}")
        print(f"{i + 1}.Quit to menu")
        save_slot = input("Enter save slot number: ")
        if save_slot.isnumeric():
            if int(save_slot) > i + 1 or int(save_slot) <= 0:
                os.system('clear')
                print(f"'{save_slot}' not recognized.")
                load_game()
            elif int(save_slot) == i + 1:
                setup()
            else:
                load_game_load(save_slot)
        else:
            os.system('clear')
            print(f"'{save_slot}' not recognized.")
            load_game()


# Load the selected save
def load_game_load(save_slot):
    os.system('clear')
    with open("database.txt", "r") as file:
        name, event, archive_update = file.readlines()[int(save_slot) - 1].split(', ')
    print(f"Welcome back {name}!")
    name_record(name)
    time.sleep(2)
    archive_list_update(archive_update)
    if event.count("Chapter"):
        eval(f"chap{event.split(' ')[-1]}")()
    else:
        eval(event)()


def leaderboard():
    pass


def credit():
    pass


def quit_game():
    pass


# Function menu
def menu(event):
    os.system('clear')
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
            pass
        elif menu_choice == 2:
            save_game(event)
            setup()
        elif menu_choice == 3:
            archive()
            menu(event)
        elif menu_choice == 4:
            game_over()
        else:
            os.system('clear')
            print(f"'{menu_choice}' not recognized.")
            menu(event)
    else:
        os.system('clear')
        print(f"'{menu_choice}' not recognized.")
        menu(event)


# Append the 'event' into the database to be used for load_game
def save_game(event):
    os.system('clear')
    try:
        checkpoint = event.__name__
    except AttributeError:
        checkpoint = event
    with open("database.txt", "a") as file:
        file.write(f"\n{name_record.name}, {checkpoint}, {len(archive_modifier.archive_list)}")
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
def archive_list_update(archive_update):
    archive_modifier("reset")
    with open("archive_list_completed.txt", "r") as file:
        line = file.readline().split(', ')
        for i in range(int(archive_update)):
            archive_modifier(line[i])


# Prints out the narration from narration.txt
def narrate(start, end):
    with open("narration.txt", "r") as file:
        t = file.readlines()
        lines = int(start) - 1
        while lines < int(end):
            for letters in t[lines]:
                print(letters, end='')
                time.sleep(0.04)
            time.sleep(1)
            lines += 1


# Use from chapter 2 onwards, executes player's input
def input_recognize(chapter_num):
    print("\nNote: Type 'help' into the console to see command list.")
    choice = input("\n>")
    if choice == "menu":
        menu(f"Chapter {chapter_num}")
        input_recognize(chapter_num)
    elif choice == "help":
        with open("command_list.txt", "r") as file:
            print(file.read())
        input_recognize(chapter_num)
    elif choice == "clear console":
        os.system('clear')
        input_recognize(chapter_num)
    else:
        try:
            eval(choice)(int(chapter_num))
        except NameError:
            print(f"'{choice}' not recognized.")
        except SyntaxError:
            print(f"'{choice}' not recognized.")
        input_recognize(chapter_num)


# Function for the transition between chapters
def chapter_transition(chap_name1, chap_name2, chap_name3):
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
    os.system('clear')


# Function for time recording
def time_record():
    t = 1
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(f"\r{timer}", end='')
        time.sleep(1)
        t += 1


# Function 'memo1'
def memo1(access_point):
    os.system('clear')
    with open("memo1.txt", "r") as memo1_reader:
        print(memo1_reader.read())
    if access_point == 1:
        archive_modifier(memo1)
    time.sleep(5)
    input("\n\t\t\t\tPress Enter to leave.")
    pass


# Function 'newspaper1'
def newspaper1(access_point):
    os.system('clear')
    print("\t\t\t" + '\033[1m' + "Family brutally murdered by the father" + '\033[0m', end='\n')
    with open("newspaper1.txt", "r") as file:
        print(file.read())
    if access_point == 1:
        archive_modifier(newspaper1)
    time.sleep(5)
    input("\n\t\t\t\tPress Enter to leave.")
    pass


# Function 'clock'
def clock(clock_version):
    if clock_version == 1 or clock_version == 3:
        print('\033[3m' + "\n23:59" + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to leave. ")
        pass
    elif clock_version == 2:
        print('\033[3m' + "\n23:58" + '\033[0m')
        time.sleep(1)

        def wait():
            os.system('clear')
            print('\033[3m' + "\n23:59" + '\033[0m')
            basement_unlock(True)
            input("\n\t\t\t\tPress Enter to leave. ")
            sound_door_creak.play()
            time.sleep(5)
            pass

        t = Timer(9, wait)
        t.start()
        choice = input("\n\t\t\t\tPress Enter to leave. ")
        if choice is not None:
            t.cancel()
            pass


def door_entrance(access_point):
    if access_point:
        sound_door_locked.play()
        time.sleep(2.5)
        print('\033[3m' + "\nlocked." + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass


def phone(access_point):
    if access_point:
        number = input("\n\t\tDial number or press Enter to go back. ")
        if number.isnumeric():
            if number == "":
                pass
            else:
                os.system('clear')
                time.sleep(1.5)
                narrate(77, 78)
                time.sleep(1)
                phone(access_point)
        else:
            os.system('clear')
            print(f"'{number}' has to be integers.")
            phone(access_point)


def radio(access_point):
    if access_point == 1 or access_point == 2 or access_point == 3:
        time.sleep(1.5)
        narrate(82, 82)
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass


def bathroom(access_point):
    if access_point == 1:
        sound_door_locked.play()
        time.sleep(2.5)
        print('\033[3m' + "\nlocked." + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass
    if access_point == 2:
        sound_door_locked.play()
        time.sleep(2.5)
        print('\033[3m' + "\nlocked." + '\033[0m')
        time.sleep(2)
        input("\n\t\t\t\tPress Enter to go back. ")
        time.sleep(0.5)
        print("\n>", end='')
        time.sleep(3)
        sound_door_knock.play()
        time.sleep(2)
        pass
    if access_point == 3:
        if bathroom_unlock.is_unlock:
            time.sleep(1.5)
            narrate(95, 96)
            sound_baby_cry.play()
            narrate(97, 98)
            time.sleep(1.5)
            sound_baby_cry.stop()
            sound_door_slam.play()
            time.sleep(0.5)
            narrate(99, 102)
            time.sleep(2)
            input("\n\t\t\t\tPress Enter to go back. ")
            pass
        else:
            sound_door_locked.play()
            time.sleep(2.5)
            print('\033[3m' + "\nlocked." + '\033[0m')
            time.sleep(2)
            input("\n\t\t\t\tPress Enter to go back. ")
            pass


def basement(access_point):
    if access_point == 2:
        if basement_unlock.is_unlock:
            time.sleep(1.5)
            narrate(86, 86)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to countinue. ")
            basement_unlock(False)
            chapter_transition("Chapter 2", "\tChapter 3", "DUSK")
            chap3()
        else:
            sound_door_locked.play()
            time.sleep(2.5)
            print('\033[3m' + "\nlocked." + '\033[0m')
            time.sleep(1.5)
            narrate(88, 89)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to go back. ")
            pass
    if access_point == 3:
        if basement_unlock.is_unlock:
            time.sleep(1.5)
            narrate(106, 106)
            time.sleep(1)
            input("\n\t\t\t\tPress Enter to countinue. ")
            basement_unlock(False)
            chapter_transition("Chapter 3", "\tChapter 4", "THE CRY")
            chap3()
        else:
            sound_door_locked.play()
            time.sleep(2.5)
            print('\033[3m' + "\nlocked." + '\033[0m')
            time.sleep(2)
            input("\n\t\t\t\tPress Enter to go back. ")
            print("\n>", end='')
            time.sleep(3)
            sound_door_creak_open.play()
            time.sleep(5)
            bathroom_unlock(True)
            pass


# Function 'prologue_1'
def prologue_1():
    os.system('clear')
    time.sleep(1.5)
    narrate(2, 5)
    time.sleep(2)
    prologue1_memo()

    # prologue1_memo

    os.system('clear')
    sound_door_creak.play()
    time.sleep(5)
    narrate(7, 8)
    time.sleep(2)
    prologue2_exit()

    # prologue2_exit


def prologue1_memo():
    choice = input("\n\t\t\t\tPress E to read. ")
    if choice == "e":
        memo1(1)
    elif choice == "menu":
        menu(prologue1_memo)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        prologue1_memo()


def prologue2_exit():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice == "e":
        chap1_0()
    elif choice == "menu":
        menu(prologue2_exit)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        prologue2_exit()


# Function 'chap1'
def chap1_0():
    chapter_transition("Prologue", "Chapter 1", "THE BEGINNING")
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
    narrate(12, 14)
    time.sleep(2)
    sound_door_slam.play()
    time.sleep(0.8)
    narrate(16, 17)
    time.sleep(2)
    chap1_hallway_door()

    # chap1_hallway_door


def chap1_2():
    os.system('clear')
    sound_door_locked.play()
    time.sleep(2.5)
    narrate(19, 23)
    time.sleep(2)
    chap1_clock()

    # chap1_clock()


def chap1_3():
    os.system('clear')
    time.sleep(1.5)
    narrate(25, 28)
    time.sleep(2)
    chap1_newspaper()

    # chap1_newspaper


def chap1_4():
    os.system('clear')
    time.sleep(1.5)
    narrate(30, 36)
    time.sleep(2)
    chap1_entrance_door()

    # chap1_entrance_door()


def chap1_5():
    os.system('clear')
    time.sleep(1.5)
    narrate(38, 41)
    time.sleep(2)
    chap1_phone()

    # chap1_phone


def chap1_6():
    os.system('clear')
    time.sleep(1.5)
    narrate(43, 45)
    time.sleep(2)
    chap1_bathroom()

    # chap1_bathroom()


def chap1_7():
    os.system('clear')
    time.sleep(1.5)
    narrate(47, 49)
    time.sleep(2)
    chap1_radio()

    # chap1_radio()


def chap1_8():
    os.system('clear')
    time.sleep(1.5)
    narrate(51, 52)
    time.sleep(1)
    narrate(53, 56)
    time.sleep(2)
    chap1_end()


def chap1_note():
    choice = input("\n\t\t\t\tPress Enter to continue. ")
    if choice == "":
        chap1_1()
    elif choice == "menu":
        menu(chap1_0)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_note()


def chap1_hallway_door():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice == "e":
        chap1_2()
    elif choice == "menu":
        menu(chap1_1)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_hallway_door()


def chap1_clock():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice == "e":
        clock(1)
        chap1_3()
    elif choice == "menu":
        menu(chap1_2)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_clock()


def chap1_newspaper():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice == "e":
        newspaper1(1)
        chap1_4()
    elif choice == "menu":
        menu(chap1_3)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_newspaper()


def chap1_entrance_door():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice == "e":
        door_entrance(1)
        chap1_5()
    elif choice == "menu":
        menu(chap1_4)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_entrance_door()


def chap1_phone():
    phone(1)
    chap1_6()


def chap1_bathroom():
    choice = input("\n\t\t\t\tPress E to open. ")
    if choice == "e":
        bathroom(1)
        chap1_7()
    elif choice == "menu":
        menu(chap1_6)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_bathroom()


def chap1_radio():
    choice = input("\n\t\t\t\tPress E to inspect. ")
    if choice == "e":
        radio(1)
        chap1_8()
    elif choice == "menu":
        menu(chap1_7)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_radio()


def chap1_end():
    choice = input("\n\t\t\t\tPress Enter to continue. ")
    if choice == "":
        chapter_transition("Chapter 1", "\tChapter 2", "LOOP")
        chap2()
    elif choice == "menu":
        menu(chap1_8)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_radio()


def chap2():
    os.system('clear')
    time.sleep(1.5)
    narrate(60, 71)
    time.sleep(2)
    input("\n\t\t\t\tPress Enter. ")
    os.system('clear')
    input_recognize(2)


def chap3():
    os.system('clear')
    time.sleep(1.5)
    narrate(91, 91)
    time.sleep(2)
    input("\n\t\t\t\tPress Enter. ")
    input_recognize(3)


# Function 'game over'
def game_over():
    pass

    # if __name__ == '__main__':
    a = Thread(target=time_record)
    b = Thread(target=setup)
    a.start()
    b.start()


setup()
