import random
import sys
import os
import pandas as pd
import numpy as np

def InitSort(Data):
    return Data.sort_values(["Init", "DEX"], ascending = [False, False], ignore_index = True)

def AddToInit(Data):
    Name = input("Name: ")
    Init = input("Init: ")
    Init = (random.randint(1,20)+int(Init)) if (Init.startswith("+") or Init.startswith("-")) else int(Init)
    DEX = input("DEX: ")
    HP = input("HP: ")
    print("Do you want to add the following entity to the initiative list? [yN]\n\tName: ", Name, "\n\tInit: ", Init, "\n\tDEX: ", DEX, "\n\tHP: ", HP, sep="")
    YN = input()
    if YN.lower() in ("yes", "true", "t", "y", "1"):
        Data = Data.append({"Turn": " ", "Name": Name, "Init": Init, "DEX": DEX, "HP": HP}, ignore_index=True)
        return InitSort(Data)
    else:
        return Data

def ApplyDamage(Data):
    ID = int(input("Who do you wish to apply damage to? (Insert ID from the tracker list, invalid choice will result in return to action selection) "))
    if ID < len(Data["Name"]):
        print("You selected ", Data["Name"][ID], ", if you chose the wrong character apply 0 damage.", sep="")
        DMG = int(input("How much damage to apply? (Negative values will result in healing) "))
        Data["HP"][ID] -= DMG
    return Data

def NextTurn(Data, CurrTurn):
    Data["Turn"][CurrTurn] = " "
    CurrTurn = CurrTurn+1 if CurrTurn+1 < len(Data["Name"]) else 0
    Data["Turn"][CurrTurn] = "==>"
    return Data, CurrTurn

def SetTurn(Data, CurrTurn):
    NewTurn = int(input("Insert new turn ID "))
    if NewTurn < len(Data["Turn"]):
        Data["Turn"][CurrTurn] = " "
        Data["Turn"][NewTurn] = "==>"
        CurrTurn = NewTurn
    else:
        input("Invalid selection, please retry. Hit any key to proceed. ")
    return Data, CurrTurn

def RemoveFromInit(Data, CurrTurn):
    ID = int(input("Who do you wish to remove? (Insert ID from the tracker list, invalid choice will result in return to action selection) "))
    if ID < len(Data["Name"]):
        print("You selected ", Data["Name"][ID], ", do you really wish to remove them? [yN]", sep="", end=" ")
        YN = input()
        if YN.lower() in ("yes", "true", "t", "y", "1"):
            Data = Data.drop(ID)
            Data = Data.reset_index(drop=True)
            if ID < CurrTurn:
                CurrTurn = CurrTurn-1
            elif ID == CurrTurn:
                if CurrTurn < len(Data["Turn"])-1:
                    Data["Turn"][ID] = "==>"
                else:
                    CurrTurn = 0
                    Data["Turn"][0] = "==>"
    return Data, CurrTurn

def SaveToFile(Data):
    Outname = input("File name to save? (Will be saved in current path, and WILL overwrite already existing files) ")
    if Outname is None or Outname == "":
        Outname = "Initiatives.txt"
    with open("./"+Outname, 'w') as F:
        Output = Data.drop("Turn", 1).to_string(header=True, index=False)
        F.write(Output)
        F.write("\n")
        F.close()
    input("Operation completed. Hit any key to proceed. ")

print("Welcome to the initiative tracker.")
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        Data = pd.read_csv(sys.argv[1], sep="\s+|\t", engine = "python", dtype={"Init" : "str"})
        #Check if initiative values start with "+" or "-". If they do roll a die, if they don't keep the value.
        InitArr = np.zeros(len(Data["Init"]), dtype=int)
        for I, Init in enumerate(Data["Init"]):
            InitArr[I] = (random.randint(1,20)+int(Init)) if (Init.startswith("+") or Init.startswith("-")) else int(Init)
        #Replace negative values with 1
        for I, Init in enumerate(InitArr):
            if Init <= 0:
                InitArr[I] = 1
        Data["Init"] = InitArr
        Data = Data.assign(Turn = [" "]*len(Data["Name"]))
        Data = Data.reindex(columns = ["Turn", "Name", "Init", "DEX", "HP"])
        #Sort the results and set initial turn
        Data = InitSort(Data)
        CurrTurn = 0
        Data["Turn"][0] = "==>"
    while True:
        #Clear window
        os.system('cls' if os.name=='nt' else 'clear')
        #Print initiatives
        print(Data)
        #Ask for actions
        Instruction = input ("\nAvailable actions:\n\t[aA] Add - Add someone to the list;\n\t[dD] Damage - Apply damage to someone;\n\t[nN] Next - Go to next turn;\n\t[qQ] Quit - Exit from the tracker;\n\t[rR] Remove - remove someone from the list;\n\t[sS] Save - Save an initiative file;\n\t[tT] Turn - Set a specific turn.\nChoose an action ")
        if Instruction.lower() in ("a", "d", "n", "q", "r", "s", "t"):
            #Add to initiative
            if Instruction.lower() == "a":
                Data = AddToInit(Data)
            #Apply damage
            if Instruction.lower() == "d":
                Data = ApplyDamage(Data)
            #Next turn
            if Instruction.lower() == "n":
                Data, CurrTurn = NextTurn(Data, CurrTurn)
            #Quit
            if Instruction.lower() == "q":
                YN = input("Are you sure you want to quit? [yN] ")
                if YN.lower() in ("yes", "true", "t", "y", "1"):
                    break
                else:
                    continue
            #Remove from list
            if Instruction.lower() == "r":
                Data, CurrTurn = RemoveFromInit(Data, CurrTurn)
            #Save a file
            if Instruction.lower() == "s":
                SaveToFile(Data)
            #Set a specific turn
            if Instruction.lower() == "t":
                Data, CurrTurn = SetTurn(Data, CurrTurn)
        else:
            input("Invalid selection, retry. Hit any key to proceed. ")
            continue
else:
    print("No file provided.")
