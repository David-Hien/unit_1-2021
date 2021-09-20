# Import libraries
import time
import os
from threading import Thread

# Declare global variables (to be used in other functions)
score_final = 0
saves_list = []
names_list = []
archive_list = []


# Function for setup
def setup():
    os.system('clear')
    print("\t\t\t\t" + '\033[1m' + "NIGHTMARE" + '\033[0m', end='\n')
    print("1.New game")
    print("2.Load game")
    print("3.Leaderboard")
    print("4.Credits")
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
    print("\t\t\t\t" + '\033[1m' + "NEW GAME" + '\033[0m', end='\n')
    name = input("Enter player name: ")
    print(f"\nWelcome {name}!")
    global saves_list
    global names_list
    saves_list.append(prologue_1)
    names_list.append(name)
    new_game_choice1()


def new_game_choice1():
    start = input("\n\t\t\t\tPress Enter to start. ")
    if start == "":
        prologue_1()
    elif start == "menu":
        menu(new_game_choice1)
    else:
        os.system('clear')
        print(f"'{start}' not recognized.")
        new_game_choice1()


def load_game():
    os.system('clear')
    global saves_list
    global names_list
    print("\t\t\t\t" + '\033[1m' + "LOAD GAME" + '\033[0m', end='\n')
    save_slot = int(input("Enter save slot number: "))
    print(f"\nWelcome back {names_list[save_slot]}!")
    saves_list[save_slot]()


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
    global saves_list
    global names_list
    saves_list.append(event)
    names_list.append(names_list[-1])
    print(f"Saving game to slot {len(saves_list) - 1}", end='')
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
        print(f"{i + 1}.{archive_list[i].__name__}")
    print(f"{archive_list_length + 1}.Quit to menu")
    archive_choice = input(f"Select option 1 to {archive_list_length + 1}: ")
    if archive_choice.isnumeric():
        os.system('clear')
        archive_choice = int(archive_choice)
        if archive_choice == archive_list_length + 1:
            pass
        else:
            archive_list[archive_choice - 1](2)
    else:
        archive()


# Function for the transition between chapters
def chapter_transition(chap_name1, chap_name2, chap_name3):
    os.system('clear')
    time.sleep(2)
    print(f"\n\t\t\t\t{chap_name1} end")
    time.sleep(4)
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
    clock_inspect = input("\n\t\t\t\tPress E to inspect. ")
    if clock_inspect == "e":
        if clock_version == 1:
            print('\033[3m' + "\n23:59" + '\033[0m')
            time.sleep(1)
            clock_exit = input("\n\t\t\t\tPress Enter to leave. ")
            if clock_exit:
                pass
    else:
        os.system('clear')
        print(f"'{clock_inspect}' not recognized.")
        clock(clock_version)


# Function 'memo1'
def memo1(access_point):
    os.system('clear')
    print("Date: __/__/__")
    print("\n\tI woke up in this dark room with seemingly no windows and one locked door.")
    print("I tried breaking the door but it won't budge. I don't know how long it has been,")
    print("it's always dark. Ever since I got here, I've this strange feeling that whatever")
    print("is behind that door, is far worse than in here.")
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
    print("\n\t...the murder of the wife and her two children by their husband and")
    print("father. This brutal killing took place while the family was gathered at home")
    print("on a Saturday evening. The father shot his wife as she was cleaning up the")
    print("kitchen after dinner. When his twelve-year-old daughter came to investigate")
    print("the commotion, the father shot her, too. His six-year-old son had the good")
    print("sense to hide in the bathroom, but reports suggest he lured him out by telling")
    print("him it was just a game. The boy was found shot once in the head from point-blank")
    print("range. The mother, who he shot in the stomach, was pregnant at the time. Police")
    print("arriving on-scene after neighbors called 911...")
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
    door_open = input("\n\t\t\t\tPress E to open. ")
    if door_open == "e":
        if access_point == 1:
            print('\033[3m' + "\nlocked." + '\033[0m')
            time.sleep(1)
            door_exit = input("\n\t\t\t\tPress Enter to go back. ")
            if door_exit:
                pass
    else:
        os.system('clear')
        print(f"'{door_open}' not recognized.")
        door_entrance(access_point)


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
    prologue_1_choice1()

    # prologue_1_choice1

    os.system('clear')
    time.sleep(2)
    print('\033[3m' + "clack." + '\033[0m')
    time.sleep(0.8)
    print("WHO'S THERE!?")
    time.sleep(1)
    for i in range(3):
        time.sleep(1.2)
        print(".", end='')
    time.sleep(2)
    print("\nThe door is opened?")
    time.sleep(1)
    prologue_2_choice1()


def prologue_1_choice1():
    prologue_1_choice = input("\n\t\t\t\tPress E to read. ")
    if prologue_1_choice == "e":
        memo1(1)
    elif prologue_1_choice == "menu":
        menu(prologue_1_choice1)
    else:
        os.system('clear')
        print(f"'{prologue_1_choice}' not recognized.")
        prologue_1_choice1()


def prologue_2_choice1():
    prologue_2_choice = input("\n\t\t\t\tPress E to open. ")
    if prologue_2_choice == "e":
        chap1_1()
    elif prologue_2_choice == "menu":
        menu(prologue_2_choice1)
    else:
        os.system('clear')
        print(f"'{prologue_2_choice}' not recognized.")
        prologue_2_choice1()


# Function 'chap1_1'
def chap1_1():
    chapter_transition("Prologue", "Chapter 1", "THE BEGINNING")
    time.sleep(3)
    print("Note: You can access the menu at any point by typing 'menu' into the console.")
    time.sleep(3)
    print("\nNote: Readings such as memos can be accessed via 'archive' in the menu.")
    time.sleep(3)
    chap1_1_choice1()

    # chap1_1_choice1

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
    chap1_2_choice1()

    # chap1_2_choice1

    os.system('clear')
    time.sleep(1)
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
    clock(1)

    # clock(1)

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
    chap1_3_choice1()

    # chap1_3_choice1

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
    door_entrance(1)

    # door_entrance(1)


def chap_test():
    os.system('clear')
    time.sleep(2)
    print("Yes of course,", end=' ')
    time.sleep(1.5)
    print("another locked door.", end=' ')
    time.sleep(1.5)
    print("Wonderful.")
    time.sleep(1.5)
    print("Just like every 'cliché' horror game ever created")


def chap1_1_choice1():
    chap1_1_choice = input("\n\t\t\t\tPress Enter to continue. ")
    if chap1_1_choice == "":
        pass
    elif chap1_1_choice == "menu":
        menu(chap1_1_choice1)
    else:
        os.system('clear')
        print(f"'{chap1_1_choice}' not recognized.")
        chap1_1_choice1()


def chap1_2_choice1():
    chap1_2_choice = input("\n\t\t\t\tPress E to open. ")
    if chap1_2_choice == "e":
        pass
    elif chap1_2_choice == "menu":
        menu(chap1_2_choice1)
    else:
        os.system('clear')
        print(f"'{chap1_2_choice}' not recognized.")
        chap1_2_choice1()


def chap1_3_choice1():
    chap1_3_choice = input("\n\t\t\t\tPress E to inspect. ")
    if chap1_3_choice == "e":
        newspaper1(1)
        pass
    elif chap1_3_choice == "menu":
        menu(chap1_3_choice1)
    else:
        os.system('clear')
        print(f"'{chap1_3_choice}' not recognized.")
        chap1_3_choice1()


# Function 'game over'
def game_over():
    print(score_add(0))


# if __name__ == '__main__':
    a = Thread(target=time_record)
    b = Thread(target=setup)
    a.start()
    b.start()


# chap1_1()
# memo1(1)
# chap_test()
setup()
