### English version
### Scroll down for Italian version

# D&D Initiative Tracker
A short python script for console, used to help manage and track initiative and combat in Dungeons&Dragons, Pathfinder and other similar systems.

# Usage
This is a console script created with the intent to be used by terminal. The first and only command line argument required is a path to a specifically formatted text document. The document must be formatted in _**FOUR**_ columns (in any order and separated by any combination of tabs and spaces) that _**CAN**_ be called:
+ **Name** - Names of the entities to be tracked, all in a single word. Examples: *Hero*, *Goblin1*, *Ancient_Red_Dragon*, *LairEffects*.
+ **Init** - Initiative of the entities. [This is optional, d20 will be rolled with the Mod if left blank, even if blank in csv file]
+ **Mod** - Ability modifier affecting the initiative roll, that will be used to break initiative ties. Should there be a tie of both modifier and intiaitve, no further decision is made by the program.
+ **HP** - Hitpoints of the characters. Useful to track combat.
+ **Conditions** - List of conditions of initiative member. Useful to track combat.

An example of a valid document can be found in the repository under the name `InitExample.txt`. To start the script simply pass the full path of the file as the first argument, one such example may be `python /path/to/script/DnDInitiativeTracker.py path/to/file/InitExample.txt`.
After reading the initiatives and rolling the necessary ones, the list will be sorted and the program will print it with an arrow showing the current turn, and prompt the user to choose actions to perform. These available actions are:
+ **Add** - Add another entity to the list. The program will prompt to insert a name, an initiative score or modifier, a dexterity score and an HP score. Before adding the entity, the program will prompt for confirmation.
+ **Damage** - Apply damage to someone. The program will prompt to select an entity via their turn order ID (note that it counts from 0), and then insert an amount of damage. If the user wishes to heal the entity instead, they can insert a negative score. Example: after selecting ID 8, the user types 6, dealing 6 damage to the entity with ID 8. If the user instead types -6, the entity will be healed by 6 HP.
+ **Conditon** - Edit the text string for the condtions imposed on initiatie member.
+ **Next** - Go to next turn. This will make the arrow indicating the turn advance by one.
+ **Quit** - Exit from the tracker. If the user confirms, the program quits. **No data is saved.**
+ **Remove** - Remove someone from the list. The program prompts to select the ID of an entity, and then ask for confirmation. If the user confirms, the entity is removed from the turn order.
+ **Save** - Save an initiative file. The program will save a file with the given name in the current directory with the current turn order. The file is formatted such that it can be loaded from the program. If no name is provided, the default name is `Initiatives.txt`.
+ **Turn** - Set a specific turn. The Program will prompt to insert the ID of an entity, and the turn tracker will jump to that entity.

# License
This code is lincensed under the MIT License.

### Versione italiana

# Gestione dell'Iniziativa per D&D
Un breve script python utilizzato per aiutare a gestire initiativa e turni di combattimento in Dungeons&Dragons.

# Uso
Questo script è stato pensato per essere utilizzato da console/terminale. Il primo e unico parametro da linea di comando è il path a un file formattato in maniera specifica come spiegato di seguito. Il documento deve essere diviso in **QUATTRO** colonne (l'ordine è irrilevante e possono essere separate da una qualsiasi combinazione di tabulazioni e spazi) i cui nomi **DEVONO** essere:
+ **Name** - Nomi delle entità di cui tenere traccia, in un'unica parola. Esempi: *Eroe*, *Goblin1*, *DragoRossoAntico*, *EffettiDiTana*.
+ **Init** - Iniziativa delle entità. Se è un numero (senza segni di punteggiatura) sarà trattata come numero, se è un modificatore (come per esempio *+4* o *-3*) il codice lancerà un d20 e applicherà il modificatore, ottenendo un punteggio di iniziativa valido.
+ **DEX** - **Punteggio** (non modificatore) di Destrezza, utilizzato in caso di pareggio di iniziativa. In caso di pareggio sia di iniziativa che di destrezza, il programma non prenderà ulteriori decisioni.
+ **HP** - Punti ferita del personaggio. Utile per tenere traccia del combattimento.

Un esempio di documento valido può essere trovato nella repository, con nome `InitExample.txt`. Per lanciare lo script passare il path del file come primo argomento, per esempio `python /path/per/lo/script/DnDInitiativeTracker.py /path/per/il/file/InitExample.txt`.
Dopo aver letto le iniziative e lanciato i dadi necessari, la lista viene riordinata e il programma la stampa, indicando il primo turno con una freccia e chiedendo all'utente di scegliere azioni da eseguire. Le azioni possibili sono:
+ **Add** - Aggiunge un altra entità alla lista. Il programma chiederà un nome, un'iniziativa o modificatore, un punteggio di destrezza e i punti ferita. Prima di aggiungere l'entità, il programma chiederà conferma.
+ **Damage** - Applica del danno a qualcuno. Il programma chiederà di scegliere un'entità tramite l'ID del turno (si noti che conta da 0), e poi chiederà di inserire un ammontare di danno. Per curare qualcuno basterà inserire un valore negativo. Esempio: dopo aver selezionato 8 come ID, se l'utente scrive 6 l'entità riceverà 6 danni, mentre se scrive -6 l'entità verrà curata di 6 punti ferita.
+ **Next** - Procede al prossimo turno. La freccia che indica il turno avanzerà alla prossima entità.
+ **Quit** - Esce dal programma. Se l'utente conferma, il programma di chiude. **Nessun progresso viene salvato.**
+ **Remove** - Rimuove qualcuno dalla lista. Il programma chiede di selezionare l'ID di un'entità e poi chiede conferma, se l'utente conferma l'entità viene rimossa dall'ordine dei turni.
+ **Save** - Salva un file di iniziativa. Il programma salva il file con il nome fornito nella cartella corrente, indicando l'ordine di turno attuale. Il file è formattato in modo da essere leggibile dal programma. Se non viene fornito un nome, quello di default è `Initiatives.txt`.
+ **Turn** - Setta un turno specifico. Il programma chiede l'ID di un'entità, e l'indicatore di turno salterà a quel valore.

# Licenza
Questo codice è rilasciato con la MIT License.
