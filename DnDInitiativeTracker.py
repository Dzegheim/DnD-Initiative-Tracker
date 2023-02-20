import random
import sys
import os
import pandas as pd
import readline

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()

def InitSort(Data):
    Data = Data.sort_values(by=['Init', 'Mod'], ascending = [False, False], ignore_index = True)
    return Data

def AddToInit(Data):
    Name = input('Name: ')
    Init = input('Init (leave blank to generate from Mod): ')
    Mod = input('Mod: ')
    Init = (random.randint(1,20)+int(Mod)) if (Init == '') else int(Init)
    HP = input('HP: ')
    Conditions = input('Conditions: ')
    print('Do you want to add the following entity to the initiative list? [yN]\n\tName: ', Name, '\n\tInit: ', Init, '\n\tMod: ', Mod, '\n\tHP: ', HP, '\n\tConditions: ', Conditions, sep='')
    YN = input()
    if YN.lower() in ('yes', 'true', 't', 'y', '1'):
        Data = Data.append({'Turn': ' ', 'Name': Name, 'Init': Init, 'Mod': Mod, 'HP': HP, 'Conditions': Conditions}, ignore_index=True)
        return InitSort(Data)
    else:
        return Data

def EditInit(Data, CurrTurn):
    CurrPlayer = Data['Name'][CurrTurn]
    inp = input('Change initiative of which ID: ')
    if inp.isnumeric():
        ID = int(inp)
        if ID < len(Data['Name']):
            name =  Data['Name'][ID]
            print('You selected ', name, ', what do you want to change their Initiative to?', sep='')
            inp2 = input('New Initiative: ')
            if inp2.isnumeric():
                Data['Init'][ID] = int(inp2)
                Data = InitSort(Data)
                CurrTurn = Data['Name'].loc[lambda x: x==name].index.tolist()[0]
                print(Data)
    return Data, CurrTurn

def ApplyDamage(Data):
    inp = input('Who do you wish to apply damage to? (Insert ID from the tracker list, invalid choice will result in return to action selection) ')
    if inp.isnumeric():
        ID = int(inp)
        if ID < len(Data['Name']):
            print('You selected ', Data['Name'][ID], ', if you chose the wrong character apply 0 damage.', sep='')
            DMG = int(input('How much damage to apply? (Negative values will result in healing) '))
            Data['HP'][ID] = int(Data['HP'][ID]) - DMG
    return Data

def ApplyCondition(Data):
    inp = input('Who do you wish to apply a condition to? (Insert ID from the tracker list, invalid choice will result in return to action selection) ')
    if inp.isnumeric():
        ID = int()
        if ID < len(Data['Name']):
            print('You selected ', Data['Name'][ID], ', if you chose the wrong character apply no condition.', sep='')
            Data['Conditions'][ID] = rlinput('Alter the Conditions to: ', prefill = Data['Conditions'][ID])
    return Data

def NextTurn(Data, CurrTurn):
    for ind in Data.index:
        Data['Turn'][ind] = ' '
    CurrTurn = CurrTurn+1 if CurrTurn+1 < len(Data['Name']) else 0
    Data['Turn'][CurrTurn] = '==>'
    return Data, CurrTurn

def SetTurn(Data, CurrTurn):
    inp = input('Insert new turn ID ')
    if inp.isnumeric():
        NewTurn = int(inp)
        if NewTurn < len(Data['Turn']):
            for ind in Data.index:
                Data['Turn'][ind] = ' '
            Data['Turn'][NewTurn] = '==>'
            CurrTurn = NewTurn
        else:
            input('Invalid selection, please retry. Hit any key to proceed. ')
    else:
        input('Type an Integer. Hit any key to proceed. ')
    return Data, CurrTurn

def RemoveFromInit(Data, CurrTurn):
    inp = input('Who do you wish to remove? (Insert ID from the tracker list, invalid choice will result in return to action selection) ')
    if inp.isnumeric():
        ID = int()
        if ID < len(Data['Name']):
            print('You selected ', Data['Name'][ID], ', do you really wish to remove them? [yN]', sep='', end=' ')
            YN = input()
            if YN.lower() in ('yes', 'true', 't', 'y', '1'):
                Data = Data.drop(ID)
                Data = Data.reset_index(drop=True)
                if ID < CurrTurn:
                    CurrTurn = CurrTurn-1
                elif ID == CurrTurn:
                    if CurrTurn < len(Data['Turn'])-1:
                        Data['Turn'][ID] = '==>'
                    else:
                        CurrTurn = 0
                        Data['Turn'][0] = '==>'
    return Data, CurrTurn

def SaveToFile(Data):
    Outname = input('File name to save? (Will be saved in current path, and WILL overwrite already existing files) ')
    if Outname is None or Outname == '':
        Outname = 'Initiatives.csv'
    Data.drop('Turn', axis= 'columns').to_csv(Outname, header=True, index=False)
    input('Operation completed. Hit any key to proceed. ')

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        Data = pd.DataFrame(columns=['Turn', 'Name', 'Init', 'Mod', 'HP', 'Conditions'])
        Data = AddToInit(Data)
        print(Data)
        CurrTurn = 0
        Data['Turn'][0] = '==>'
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            Data = pd.read_csv(sys.argv[1], sep=',', dtype=str)
            for ind in Data.index:
                Data.at[ind,'Mod'] = int(Data.at[ind,'Mod'])
                Data.at[ind,'HP'] = int(Data.at[ind,'HP'])
                if (str(Data.at[ind,'Init']) == 'nan'): #I can't be arsed figuring out what a NaN is in non-numpy python right now.
                    Data.at[ind,'Init'] = (random.randint(1,20)+int(Data.loc[ind,'Mod']))
                Data.at[ind,'Init'] = int(Data.at[ind,'Init'])
            #Replace negative values with 1
            Data = Data.assign(Turn = [' ']*len(Data['Name']))
            Data = Data.reindex(columns = ['Turn', 'Name', 'Init', 'Mod', 'HP', 'Conditions'])
            #Sort the results and set initial turn
            Data = InitSort(Data)
            CurrTurn = 0
            Data['Turn'][0] = '==>'
        else:
            print('Check input filename.')
    while True:
        #Clear window
        os.system('cls' if os.name=='nt' else 'clear')
        #Print initiatives
        print(Data)
        #Ask for actions
        Instruction = input ('\nAvailable actions:\n\t[aA] Add - Add someone to the list;\n\t[rR] Remove - remove someone from the list;\n\t[eE] Edit - Change someones initiative value;\n\t[dD] Damage - Apply damage to someone;\n\t[cC] Condition - Apply a condition to someone;\n\t[nN] Next - Go to next turn;\n\t[tT] Turn - Set a specific turn;\n\t[sS] Save - Save an initiative file;\n\t[qQ] Quit - Exit from the tracker.\nChoose an action ')
        if Instruction.lower() in ('a', 'd', 'c', 'e', 'n', 'q', 'r', 's', 't'):
            #Add to initiative
            if Instruction.lower() == 'a':
                Data = AddToInit(Data)
            #Remove from list
            elif Instruction.lower() == 'r':
                Data, CurrTurn = RemoveFromInit(Data, CurrTurn)
            #Edit Initiative from list
            elif Instruction.lower() == 'e':
                Data, CurrTurn = EditInit(Data, CurrTurn)
            #Apply damage
            elif Instruction.lower() == 'd':
                Data = ApplyDamage(Data)
            #Apply Condition
            elif Instruction.lower() == 'c':
                Data = ApplyCondition(Data)
            #Next turn
            elif Instruction.lower() == 'n':
                Data, CurrTurn = NextTurn(Data, CurrTurn)
            #Set a specific turn
            elif Instruction.lower() == 't':
                Data, CurrTurn = SetTurn(Data, CurrTurn)
            #Save a file
            elif Instruction.lower() == 's':
                SaveToFile(Data)
            #Quit
            elif Instruction.lower() == 'q':
                YN = input('Are you sure you want to quit? [yN] ')
                if YN.lower() in ('yes', 'true', 't', 'y', '1'):
                    break
                else:
                    continue
        else:
            input('Invalid selection, retry. Hit any key to proceed. ')
            continue
