# Import libraries
import time
import os
import vlc
from threading import Thread

# Declare global variables (to be used in other functions)
score_final = 0
archive_list = []
name = None


# Sound
sound_door_locked = vlc.MediaPlayer("sound_effects/sound_door_locked.mp3")
sound_door_creak = vlc.MediaPlayer("sound_effects/sound_door_creak.mp3")
sound_door_open_close = vlc.MediaPlayer("sound_effects/sound_door_open_close.mp3")
sound_door_knock = vlc.MediaPlayer("")
sound_door_pound = vlc.MediaPlayer("")
sound_phone_ring = vlc.MediaPlayer("")
sound_phone_call = vlc.MediaPlayer("")
sound_radio_buzz = vlc.MediaPlayer("")
sound_radio_warning = vlc.MediaPlayer("")


# Function for setup
def setup():
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


def new_game():
    os.system('clear')
    global name
    print("\t\t\t\t" + '\033[1m' + "NEW GAME" + '\033[0m', end='\n')
    name = input("Enter player name: ")
    print(f"\nWelcome {name}!")
    input("\n\t\t\t\tPress Enter to start. ")
    prologue_1()


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


def load_game_print():
    with open("database.txt", "r") as file:
        i = 0
        for line in file.readlines():
            i += 1
            name_update, event_update, archive_update = line.split(', ')
            print(f"{i}.{name_update}, {event_update}")
        save_slot = input("Enter save slot number: ")
        if save_slot.isnumeric():
            if int(save_slot) > i or int(save_slot) <= 0:
                os.system('clear')
                print(f"'{save_slot}' not recognized.")
                load_game()
            else:
                load_game_load(save_slot)
        else:
            os.system('clear')
            print(f"'{save_slot}' not recognized.")
            load_game()


def load_game_load(save_slot):
    os.system('clear')
    global name
    with open("database.txt", "r") as file:
        name, event, archive_update = file.readlines()[int(save_slot) - 1].split(', ')
    print(f"Welcome back {name}!")
    time.sleep(2)
    archive_list_update(archive_update)
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
            event()
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


def save_game(event):
    os.system('clear')
    with open("database.txt", "a") as file:
        file.write(f"\n{name}, {event.__name__}, {len(archive_list)}")
    print(f"Saving game", end='')
    for i in range(3):
        time.sleep(1)
        print(".", end='')
    time.sleep(1.5)


def archive():
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "ARCHIVE" + '\033[0m', end='\n')
    global archive_list
    archive_list_length = len(archive_list)
    for i in range(archive_list_length):
        print(f"{i + 1}.{archive_list[i]}")
    print(f"{archive_list_length + 1}.Quit to menu")
    archive_choice = input(f"Select option 1 to {archive_list_length + 1}: ")
    if archive_choice.isnumeric():
        os.system('clear')
        archive_choice = int(archive_choice)
        if archive_choice == archive_list_length + 1:
            pass
        else:
            eval(archive_list[archive_choice - 1])(2)
    else:
        archive()


def archive_list_update(archive_update):
    global archive_list
    archive_list = []
    with open("archive_list_completed.txt", "r") as file:
        line = file.readline().split(', ')
        for i in range(int(archive_update)):
            archive_list.append(line[i])


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


# Function for countdown clock
def time_record():
    t = 1
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(f"\r{timer}", end='')
        time.sleep(1)
        t += 1


def clock(clock_version):
    if clock_version == 1:
        print('\033[3m' + "\n23:59" + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to leave. ")
        pass


# Function 'memo1'
def memo1(access_point):
    os.system('clear')
    with open("memo1.txt", "r") as memo1_reader:
        print(memo1_reader.read())
    global archive_list
    if access_point == 1:
        archive_list.append(memo1)
        time.sleep(10)
        memo1_choice1()
        pass
    elif access_point == 2:
        time.sleep(5)
        memo1_choice2()


def memo1_choice1():
    memo1_choice = input("\n\t\t\t\tPress Enter to leave.")
    if memo1_choice == "":
        pass
    elif memo1_choice == "menu":
        menu(memo1_choice1)
    else:
        os.system('clear')
        print(f"'{memo1_choice}' not recognized.")
        memo1_choice1()


def memo1_choice2():
    memo1_choice = input("\n\t\t\t\tPress Enter to leave.")
    if memo1_choice == "":
        archive()
    elif memo1_choice == "menu":
        menu(memo1_choice2)
    else:
        os.system('clear')
        print(f"'{memo1_choice}' not recognized.")
        memo1_choice2()


# Function 'newspaper1'
def newspaper1(access_point):
    os.system('clear')
    print("\t\t\t" + '\033[1m' + "Family brutally murdered by the father" + '\033[0m', end='\n')
    with open("newspaper1.txt", "r") as file:
        print(file.read())
    global archive_list
    if access_point == 1:
        archive_list.append(newspaper1)
        time.sleep(10)
        newspaper1_choice1()
        pass
    elif access_point == 2:
        time.sleep(5)
        newspaper1_choice2()


def newspaper1_choice1():
    newspaper1_choice = input("\n\t\t\t\tPress Enter to leave.")
    if newspaper1_choice == "":
        pass
    elif newspaper1_choice == "menu":
        menu(newspaper1_choice1)
    else:
        os.system('clear')
        print(f"'{newspaper1_choice}' not recognized.")
        newspaper1_choice1()


def newspaper1_choice2():
    newspaper1_choice = input("\n\t\t\t\tPress Enter to leave.")
    if newspaper1_choice == "":
        archive()
    elif newspaper1_choice == "menu":
        menu(newspaper1_choice2)
    else:
        os.system('clear')
        print(f"'{newspaper1_choice}' not recognized.")
        newspaper1_choice2()


def door_entrance(access_point):
    if access_point == 1:
        print('\033[3m' + "\nlocked." + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass


def phone():
    number = input("\n\t\tDial number or press Enter to go back. ")
    if number == "":
        pass
    else:
        os.system('clear')
        print("...")
        time.sleep(1.5)
        print("Doesn't seem like it's working")
        time.sleep(1)
        phone()


def radio(access_point):
    if access_point == 1:
        print("\n...")
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass


def bathroom(access_point):
    if access_point == 1:
        print('\033[3m' + "\nlocked." + '\033[0m')
        time.sleep(1)
        input("\n\t\t\t\tPress Enter to go back. ")
        pass


# Function to calculate score
def score_add(score):
    global score_final
    score_final += score
    return score_final


# Function 'prologue_1'
def prologue_1():
    os.system('clear')
    print("Where am I?")
    time.sleep(3)
    print("This is not my bed...", end=' ')
    time.sleep(2)
    print("nor it is my room?")
    time.sleep(3)
    print("Ugh!", end='')
    for i in range(3):
        time.sleep(0.5)
        print(".", end='')
    time.sleep(2)
    print(" My head hurts.")
    time.sleep(4)
    print("There's a memo over here.")
    time.sleep(2)
    prologue1_memo()

    # prologue1_memo

    os.system('clear')
    sound_door_creak.play()
    time.sleep(5)
    print("WHO'S THERE!?")
    time.sleep(1)
    for i in range(3):
        time.sleep(1.2)
        print(".", end='')
    time.sleep(2)
    print("\nThe door is unlocked?")
    time.sleep(1)
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
    time.sleep(3)
    print("\nNote: Readings such as memos can be accessed via 'archive' in the menu.")
    time.sleep(3)
    chap1_note()

    # chap1_note


def chap1_1():
    os.system('clear')
    time.sleep(1.5)
    print("It looked like a normal hallway.")
    time.sleep(2)
    print("Wooden floor, ", end='')
    time.sleep(1.2)
    print("white walls, ", end='')
    time.sleep(1.5)
    print("and ", end='')
    time.sleep(2)
    print("normal...")
    time.sleep(4)
    os.system('clear')
    time.sleep(2)
    print('\033[3m' + "clack." + '\033[0m')
    time.sleep(0.8)
    print("...")
    time.sleep(1.5)
    print("The door behind me closed...")
    time.sleep(2.5)
    chap1_hallway_door()

    # chap1_hallway_door


def chap1_2():
    os.system('clear')
    sound_door_locked.play()
    time.sleep(2.5)
    print("It's locked")
    time.sleep(2)
    print("Looks like there's no turning back.")
    time.sleep(2)
    os.system('clear')
    time.sleep(1)
    print("Hmm... ", end='')
    time.sleep(1.5)
    print("This clock seems out of place?")
    time.sleep(2)
    chap1_clock()

    # chap1_clock()


def chap1_3():
    os.system('clear')
    time.sleep(2)
    print("There are beer bottles all over the floor.")
    time.sleep(2)
    print("Someone must have been drinking.")
    time.sleep(3)
    print("\nIt's quite dirty but,", end=' ')
    time.sleep(1.5)
    print("this newspaper might give me some hint.")
    time.sleep(2)
    chap1_newspaper()

    # chap1_newspaper


def chap1_4():
    os.system('clear')
    time.sleep(2)
    print("...")
    time.sleep(2)
    print("This is kinda scary.")
    time.sleep(2)
    print("I need to find a way out of here.")
    time.sleep(2)
    print("I have a very bad feeling about this place")
    time.sleep(3)
    print("\nThis door,", end=' ')
    time.sleep(1.5)
    print("there's a coat rack beside it.")
    time.sleep(2)
    print("That must mean", end=' ')
    time.sleep(1)
    print("it leads to the outside?")
    time.sleep(2)
    chap1_entrance_door()

    # chap1_entrance_door()


def chap1_5():
    os.system('clear')
    time.sleep(2)
    print("Hmm,", end=' ')
    time.sleep(1.5)
    print("doesn't seem like I'll make it out anytime soon.", end=' ')
    time.sleep(1.5)
    print("Wonderful.")
    time.sleep(1.5)
    print("I mean,", end=' ')
    time.sleep(1.5)
    print("all the windows burglar-proofed, caged.")
    time.sleep(3)
    print("\nLet me guess,", end=' ')
    time.sleep(1.5)
    print("this landline doesn't work too.")
    time.sleep(2)
    phone()

    # phone


def chap1_6():
    os.system('clear')
    time.sleep(2)
    print("Right,", end=' ')
    time.sleep(1.5)
    print("not much to see here.")
    time.sleep(3)
    print("This must be the bathroom.")
    time.sleep(2)
    chap1_bathroom()

    # chap1_bathroom()


def chap1_7():
    os.system('clear')
    time.sleep(2)
    print("I can't go in there.")
    time.sleep(3)
    print("\nUgh,")
    time.sleep(2)
    print("Why is it cold all of a sudden?")
    time.sleep(2.5)
    print("All the windows are closed,", end=' ')
    time.sleep(2)
    print("how?")
    time.sleep(3)
    print("\nNo matter how long I think about it,", end=' ')
    time.sleep(2)
    print("something about this place is")
    time.sleep(1.5)
    print('\033[1m' + "unsettling" + '\033[0m')
    time.sleep(3)
    print("\nThis is,", end=' ')
    time.sleep(1.5)
    print("a wedding photo.")
    time.sleep(2)
    print("Joey x Nora")
    time.sleep(2)
    print("It looked like it was taken in the 70s.")
    time.sleep(3)
    print("\nThere's a radio, but it doesn't seem to be working.")
    time.sleep(2)
    chap1_radio()

    # chap1_radio()


def chap1_8():
    os.system('clear')
    time.sleep(2)
    print("Looks like I went through everything already.")
    time.sleep(2)
    print("There's just one last thing,", end=' ')
    time.sleep(1.5)
    print("the basement.")
    time.sleep(2)
    print("I noticed the door was open since earlier, but it was pitch black beyond that.")
    time.sleep(3)
    print("I have to go down there, don't I?")
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
    choice = input("\n\t\t\t\tPress Enter. ")
    if choice == "":
        chapter_transition("Chapter 1", "\tChapter 2", "LOOP")
        chap2_1()
    elif choice == "menu":
        menu(chap1_8)
    else:
        os.system('clear')
        print(f"'{choice}' not recognized.")
        chap1_radio()


def chap2_1():
    os.system('clear')
    time.sleep(1.5)
    print("Huh?")
    time.sleep(1.5)
    print("Wait,", end=' ')
    time.sleep(1.5)
    print("oh no...")
    time.sleep(2)
    print("Didn't I just go through here?")
    time.sleep(2)
    print("...")
    time.sleep(2)
    print("\nThis couldn't be real right?")
    time.sleep(2)
    print("But it's definitely the same hallway.")
    time.sleep(2.5)
    print("I don't know what's going on but, ")


# Function 'game over'
def game_over():
    print(score_add(0))


# if __name__ == '__main__':
    a = Thread(target=time_record)
    b = Thread(target=setup)
    a.start()
    b.start()


# setup()
chap2_1()
