# Command to run the program
# python Ejercicio1.py action1.csv goto1.csv producciones1.txt entrada1.txt
#!/usr/bin/env python
# coding: utf-8

import csv
import collections
import sys

# Get the files names
actions_file_name = sys.argv[1]
goto_file_name = sys.argv[2]
productions_file_name = sys.argv[3]
input_file_name = sys.argv[4]

# ## Reading the actions csv
actions = []
with open(actions_file_name, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Append each row in the csv to the actions list
    for row in reader:
        actions.append(row)

# Pop the first list of the matrix as they are the terminate symbols
symbols = actions.pop(0)

# ## Reading the goto csv
# This is a default dict: Each key will automaticaly have a list as a value
gotos = collections.defaultdict(list)
goto_symbols = []
with open(goto_file_name, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Get the list of symbols with the first row 
    goto_symbols = next(reader)

    # For the rest of the rows...
    for row in reader:
        # If list is empty add an empty to each goto symbol
        if not row:
            for goto_symbol in goto_symbols:
                gotos[goto_symbol].append('')
                
        # If it is not empty add each goto to each symbol
        else:
            for i in range(len(row)):
                # If the got is empty add empty string
                if row[i] == '':
                    gotos[goto_symbols[i]].append('')
                # If is not empty add the int of the goto
                else:
                    gotos[goto_symbols[i]].append(int(row[i]))

# ## Reading the productions txt
productions = []
productions.append(tuple())
with open(productions_file_name, 'r') as file:
    lines = file.readlines()

    # For each line in the file
    for i in range(len(lines)):
        # Split a string into a list where each word is a list item, and the separator is a space (' ')
        splited_line = lines[i].split()

        # Split the thrid element (which is the production) with a comma so we have the production
        production = splited_line[2].split(',')[0]
        # Split the thrid element (which is the production) with a comma so we have the number of pops
        number_of_pops = splited_line[2].split(',')[1]

        # Add to the productions list the tuple(non-terminal symbol, the production, number of pops)
        productions.append((splited_line[0], production, int(number_of_pops)))


# ## Reading the input
def read_input():
    f = open(input_file_name, "r")
    input_string = f.readline()
    f.close()
    # Remove empty spaces and new line in input string
    input_string = input_string.replace(' ','')
    input_string = input_string.replace('\n','')
    return input_string

input_string = read_input()
# Variable which save the states we have in the stack
states_stack = []
# Add state 0 as first default
states_stack.append(0)
# Variable that will help iterate through input string
i = 0

while True:
    # Get the character in the i index
    symbol = input_string[i]
    # Get the last state in the stack
    actual_state = states_stack[-1]
    # Get the index of the actual character so we find the next action in the mapping of actions
    index_of_symbol = symbols.index(symbol)
    # Get the next action to do
    next_state = actions[actual_state][index_of_symbol]
    
    # If accep is the next action print the stack and 'accept'. Finish the program
    if next_state == 'accept':
        print(states_stack, next_state)
        break

    # If the next action is empty string exit the program and the input is not accepted
    elif next_state == '':
        print("Error")
        break

    # If the next state is a transition, 
    elif next_state[0]=='s':
        # Print the stack with next state
        print(states_stack, next_state)
        # Add to the states stack the next state int (meaning whitout the 's')
        states_stack.append(int(next_state[1:]))
        
        # Increase 1 to i to move to the next character in input string
        i += 1
        
    # If it is a reduction
    else:
        # Get the non-terminal symbol
        new = productions[int(next_state[1:])][0]
        # Get the production that will be replaces by the non-terminal symbol
        old = productions[int(next_state[1:])][1]
        # Get the amount of pops that will be done in the reduction
        pop_amount = productions[int(next_state[1:])][2]

        # Create a string that will be printed
        reduction = new + '->' + old
        # Replace the the production for its non-terminal symbol just the first time the production is found (left most in input string)
        input_string = input_string.replace(old, new, 1)
        
        # Print the states stack with the genetared string of reduction
        print(states_stack, reduction)
        
        # If pop amount > 1 we have to substract pop_amount - 1 so we go back in the input string to grab the correct character
        if pop_amount>1:
            move_i_places = pop_amount-1
            i = i - move_i_places
            
        # Delete number of pop_amount states from states_stack 
        for _ in range(pop_amount):
            states_stack.pop()
            
        # Grab the last state
        reduction_state = states_stack[-1]
        # Get the goto
        goto = gotos[new][reduction_state]
        
        # Add the goto to the states stack as it will be the next state
        states_stack.append(goto)

