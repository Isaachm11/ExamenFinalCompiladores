#!/usr/bin/env python
# coding: utf-8

# ## Reading the actions csv

# In[15]:


import csv


# In[16]:


actions = []
with open("action1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        actions.append(row)


# In[17]:


symbols = actions.pop(0)
print(symbols)
print(actions)


# ## Reading the input

# In[18]:


f = open("entrada1.txt", "r")
input_string = f.readline()
f.close()
print(input_string)


# In[48]:


map_symbols_actions = {}
for i in range(len(actions)):
    for j in range(len(symbols)):
#         print(i, j)
#         print(actions[i][j])
        map_symbols_actions[i+1, symbols[j]] = actions[i][j]
        print(map_symbols_actions)
        print('\n')


# Nota: Ya tengo el mapa de estado y símbolo. Es decir, si estoy en el estado **1** y me llega un **+** me voy a **s3**. Se manda llamar de la siguiente forma:

# In[50]:


print(map_symbols_actions[1, '+'])


# ## Leyendo las producciones

# In[72]:


productions = {}
with open('producciones1.txt', 'r') as file:
    lines = file.readlines()

    for i in range(len(lines)):
        splited_line = lines[i].split()
        production = splited_line[2].split(',')
        productions[i+1, splited_line[0]] = production[0]
print(productions)


# In[ ]:
