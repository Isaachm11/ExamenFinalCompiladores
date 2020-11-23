# Command to run the program
# python Ejercicio4.py action1.csv goto1.csv producciones1.txt entrada1.txt
#!/usr/bin/env python
# coding: utf-8


import csv
import collections
import sys

actions_file_name = sys.argv[1]
goto_file_name = sys.argv[2]
productions_file_name = sys.argv[3]
input_file_name = sys.argv[4]

# ## Reading the actions csv
actions = []
with open(actions_file_name, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        actions.append(row)

symbols = actions.pop(0)

# ## Reading the goto csv
gotos = collections.defaultdict(list)
goto_symbols = []
with open(goto_file_name, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    goto_symbols = next(reader)
    for row in reader:
#       If list is empty add an empty goto
        if not row:
            for goto_symbol in goto_symbols:
                gotos[goto_symbol].append('')
                
#       If it is not empty add each goto to each symbol
        else:
            for i in range(len(row)):
                gotos[goto_symbols[i]].append(int(row[i]))

map_symbols_actions = {}
for i in range(len(actions)):
    for j in range(len(symbols)):
        map_symbols_actions[i+1, symbols[j]] = actions[i][j]



# ## Leyendo las producciones
productions = []
productions.append(tuple())
with open(productions_file_name, 'r') as file:
    lines = file.readlines()

    for i in range(len(lines)):
        splited_line = lines[i].split()
        production = splited_line[2].split(',')[0]
        number_of_pops = splited_line[2].split(',')[1]
        productions.append((splited_line[0], production, int(number_of_pops)))


# ## Reading the input
def read_input():
    f = open(input_file_name, "r")
    input_string = f.readline()
    f.close()
    input_string = input_string.replace(' ','')[:-1]
    return input_string

input_string = read_input()
input_list = list(input_string)

states_stack = []
states_stack.append(0)

i = 0
number_of_pops_input_list = 0

while True:
    symbol = input_string[i]
    actual_state = states_stack[len(states_stack)-1]
    index_of_symbol = symbols.index(symbol)
    next_state = actions[actual_state][index_of_symbol]
    
    if next_state == 'accept':
        print(input_list, states_stack, next_state)
        break
        
    elif next_state == '':
        print("Error")
        break

    elif next_state[0]=='s':
        print(input_list, states_stack, next_state)
        states_stack.append(int(next_state[1:]))
        
        i += 1
        
#     It is an 'r', meaning a reduction
    else:
        new = productions[int(next_state[1:])][0]
        old = productions[int(next_state[1:])][1]
        pop_amount = productions[int(next_state[1:])][2]
        reduction = new + '->' + old
        input_string = input_string.replace(old, new, 1)
        
        print(input_list, states_stack, reduction)
        
        if pop_amount>1:
            move_i_places = pop_amount-1
            i = i - move_i_places
            for _ in range(move_i_places):
                input_list.pop(i-1)
            
        for _ in range(pop_amount):
            states_stack.pop()
        
        input_list[i-1] = new 

        reduction_state = states_stack[-1]
        goto = gotos[new][reduction_state]
        
        states_stack.append(goto)
        actual_state = states_stack[-1]
        
        next_state = actions[actual_state][index_of_symbol]


# In[ ]:




