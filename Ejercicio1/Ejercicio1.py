#!/usr/bin/env python
# coding: utf-8

# ## Reading the actions csv

# In[1]:


import csv
import collections


# In[2]:


actions = []
with open("action1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        actions.append(row)


# In[3]:


symbols = actions.pop(0)
print(symbols)
print(actions)


# ## Reading the goto csv

# In[4]:


gotos = collections.defaultdict(list)
goto_symbols = []
with open("goto1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    goto_symbols = next(reader)
    print(goto_symbols)
    for row in reader:
        print(row)
#       If list is empty add an empty goto
        if not row:
            for goto_symbol in goto_symbols:
                gotos[goto_symbol].append('')
                
#       If it is not empty add each goto to each symbol
        else:
            for i in range(len(row)):
                gotos[goto_symbols[i]].append(int(row[i]))
print(gotos['S'])


# In[5]:


map_symbols_actions = {}
for i in range(len(actions)):
    for j in range(len(symbols)):
#         print(i, j)
#         print(actions[i][j])
        map_symbols_actions[i+1, symbols[j]] = actions[i][j]
        print(map_symbols_actions)
        print('\n')


# Nota: Ya tengo el mapa de estado y símbolo. Es decir, si estoy en el estado **1** y me llega un **+** me voy a **s3**. Se manda llamar de la siguiente forma:

# In[6]:


map_symbols_actions[1, '+']


# ## Leyendo las producciones

# In[7]:


productions = []
productions.append(tuple())
with open('producciones1.txt', 'r') as file:
    lines = file.readlines()

    for i in range(len(lines)):
        splited_line = lines[i].split()
        print(splited_line[2].split(','))
        production = splited_line[2].split(',')[0]
        number_of_pops = splited_line[2].split(',')[1]
        productions.append((splited_line[0], production, int(number_of_pops)))
productions


# ## Important elements to consider when iterating through the input

# ## Reading the input

# In[8]:


def read_input():
    f = open("entrada1.txt", "r")
    input_string = f.readline()
    f.close()
    input_string = input_string.replace(' ','')[:-1]
    return input_string


# Symbols: 
# - ['+', '*', 'a', '$'] 
# 
# Actions:
# 0. ['s3', 's4', 's2', '']
# 1. ['', '', '', 'accept']
# 2. ['r3', 'r3', 'r3', 'r3']
# 3. ['s3', 's4', 's2', '']
# 4. ['s3', 's4', 's2', '']
# 5. ['s3', 's4', 's2', '']
# 6. ['s3', 's4', 's2', '']
# 7. ['r1', 'r1', 'r1', 'r1']
# 8. ['r2', 'r2', 'r2', 'r2']
# 
# Productions:
# 0. ()
# 1. ('S', '+SS')
# 2. ('S', '*SS')
# 3. ('S', 'a')
# 
# Gotos:
# - {'S': [1, '', '', 5, 6, 7, 8]}

# In[9]:


input_string = read_input()

states_stack = []
states_stack.append(0)

# for i in range(len(input_string)):
i = 0
max_i = len(input_string) - 1

while True:
    symbol = input_string[i]
    actual_state = states_stack[len(states_stack)-1]
    index_of_symbol = symbols.index(symbol)
    next_state = actions[actual_state][index_of_symbol]
    
    if next_state == 'accept':
        print("Éxito")
        break
        
    elif next_state == '':
        print("Error")
        break

    elif next_state[0]=='s':
        print(states_stack, next_state)
        states_stack.append(int(next_state[1:]))
        
        i += 1
        
#     It is an 'r', meaning a reduction
    else:
        new = productions[int(next_state[1:])][0]
        old = productions[int(next_state[1:])][1]
        pop_amount = productions[int(next_state[1:])][2]
        reduction = new + '->' + old
        input_string = input_string.replace(old, new, 1)
        
        if pop_amount>1:
            i = i - pop_amount + 1
            
        for _ in range(pop_amount):
            states_stack.pop()
            
#         Agarra el último de la lista
        reduction_state = states_stack[-1]
        goto = gotos[new][reduction_state]
        
        states_stack.append(goto)
        actual_state = states_stack[-1]
        
        next_state = actions[actual_state][index_of_symbol]
        print(states_stack, reduction)
        


# In[ ]:




