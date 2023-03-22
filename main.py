#!/usr/bin/env python
# coding: utf-8

# In[174]:


from pymongo import MongoClient
import sys
sys.setrecursionlimit(20000)
import json
from random import choice
import uuid
from PIL import Image
import numpy as np
from IPython.display import  display, clear_output
from time import sleep, time

START = 3
FINISH = 4
WHITE = 0
GREEN = 1
CIMA ='U'
BAIXO = 'D'
ESQUERDA = 'L'
DIREITA = 'R'  


class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://root:root@localhost:27017/')
        self.db = self.client['figma']
        self.collection = self.db.items
    def find_one(self, iteration):
        data =  self.client.db.collection.find_one({'_id': iteration})
        if data:
            return data.get('data')
        return None

    def create(self, matrix, iteration):
        data = {
            "_id": iteration,
            "data": matrix
        }
        return self.client.db.collection.insert_one(data).inserted_id

def total_adjacent_green(i, j, old_matrix):
    rows = len(old_matrix)
    columns = len(old_matrix[0])
    total_green = 0
    if i-1 >= 0 and j-1 >=0:
        total_green += 1 if old_matrix[i-1][j-1] == GREEN else 0
    if i-1 >=0: 
        total_green += 1 if old_matrix[i-1][j] == GREEN else 0
    if j-1 >=0:
        total_green += 1 if old_matrix[i][j-1] == GREEN else 0
    if i+1 < rows and j+1 < columns:
        total_green += 1 if old_matrix[i+1][j+1] == GREEN else 0
    if i+1 < rows:
        total_green += 1 if old_matrix[i+1][j] == GREEN else 0
    if j+1 < columns:
        total_green += 1 if old_matrix[i][j+1] == GREEN else 0
    if i+1 < rows and j-1 >=0:
        total_green += 1 if old_matrix[i+1][j-1] == GREEN else 0
    if i-1 >= 0 and j+1 < columns:
        total_green += 1 if old_matrix[i-1][j+1] == GREEN else 0
    return total_green
    
def next_white(total_green):
    if total_green > 1 and total_green < 5:
        return GREEN
    return WHITE

def next_green(total_green):
    if total_green > 3 and total_green < 6:
        return GREEN
    return WHITE

def next_matrix(old_matrix, iteration):
    global database
    new_matrix = database.find_one(iteration+1)
    if new_matrix:
        return new_matrix
    rows = len(old_matrix)
    columns = len(old_matrix[0])
    i, j = 0,0
    new_matrix = [[None for y in list(range(columns))] for x in range(rows)]
    while i < rows:
        j=0
        while j < columns:
            if old_matrix[i][j] == WHITE:
                new_matrix[i][j] = next_white(total_adjacent_green(i, j, old_matrix))
            elif old_matrix[i][j] == GREEN:
                new_matrix[i][j] = next_green(total_adjacent_green(i, j, old_matrix))
            elif old_matrix[i][j] == START or old_matrix[i][j] == FINISH:
                new_matrix[i][j] = old_matrix[i][j]
            j+=1
        i+=1
    database.create(new_matrix, iteration+1)
    return new_matrix

def write_image(matrix,  i, j, iteration):
    
    print(i, j, iteration, matrix[i][j])

    rows = len(matrix)
    columns = len(matrix[0])
    m = list(range(rows))
    colors = {
        START: (255 , 255,0),
        FINISH: (0,   0,   0),
        GREEN: (2, 175,   85),
        WHITE: (255, 255, 255),
        'blue': (0,   0,   255),
        'red': (255,   0,   0),
        'brown': (121,  85,   72),

    }
    cont_i = 0
    cont_j = 0
    sleep_time = 0.15
    while cont_i < rows:
        cont_j=0
        m[cont_i] = list(range(columns))
        while cont_j < columns:
            if cont_i != i or cont_j != j:
                m[cont_i][cont_j] = colors[matrix[cont_i][cont_j]]
            cont_j+=1
        cont_i+=1
    m[i][j] = colors['blue']
    if matrix[i][j] == GREEN:
        sleep_time = 3
        m[i][j] = colors['red']
    if matrix[i][j] == FINISH:
        m[i][j] = colors['brown']
    array = np.array(m, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array).resize(size=(550, 450))

    display(new_image,)
    sleep(sleep_time)
    clear_output(wait=True)
    
       
def move(i, j, tree, matrix, iteration):
    global is_finish
    if tree.get('dead'):
        return tree.copy()
    rows = len(matrix)
    columns = len(matrix[0])
    
    new_matrix = next_matrix(matrix, iteration)
    if matrix[i][j] == FINISH:
        is_finish =True
        return {"finish": (i,j, iteration)}
    if matrix[i][j] == GREEN:
        return {"dead": (i,j, iteration)}
    directions = [DIREITA]*35+ [BAIXO]*25+ [ESQUERDA]*4+ [CIMA]*4
    # descomentar a linha caso queira ver o resultado visual
    #     write_image(matrix, i, j, iteration)
    while len(directions) and not is_finish:
        direction = choice(directions)
        directions=list(filter((direction).__ne__, directions))
        if direction == DIREITA and j+1  < columns and not tree.get(DIREITA,{}).get('dead'):
            tree[DIREITA] = move(i, j+1, tree.get(DIREITA,{}), new_matrix, iteration+1)
            if tree[DIREITA].get('dead'):
                continue
        elif direction == BAIXO and i+1 < rows and not tree.get(BAIXO,{}).get('dead'):
            tree[BAIXO] = move(i+1, j, tree.get(BAIXO,{}), new_matrix, iteration+1)
            if tree[BAIXO].get('dead'):
                continue
        elif direction == ESQUERDA and j-1 >= 0 and not tree.get(ESQUERDA,{}).get('dead'):
            tree[ESQUERDA] = move(i, j-1, tree.get(ESQUERDA,{}),new_matrix, iteration+1)
            if tree[ESQUERDA].get('dead'):
                continue
        elif direction == CIMA and i-1 >= 0 and not tree.get(CIMA,{}).get('dead'):
            tree[CIMA]= move(i-1, j, tree.get(CIMA,{}), new_matrix, iteration+1)
            if tree[CIMA].get('dead'):
                continue
    if not is_finish:
        tree['dead'] = (i,j, iteration)
    return tree.copy()

file = open('input.txt')
matrix = [[int(v) for v in x.replace('\n','').split(' ')] for x in file.readlines()]
file.close()
i = 0
root = {}
global is_finish
global database

database = Database()

is_finish = False
unique_id = uuid.uuid4()
start = time()
print('Start:', start)
while not is_finish:
    i+=1
    sleep(2)
    root = move(0,0, root, matrix, 0)
print('Finish:', time()-start)
json_object = json.dumps(root, indent=1)
with open(f"root/root_{unique_id}_{i}_final.json", "w") as outfile:
    outfile.write(json_object)
final_root_file = f"root/root_{unique_id}_{i}_final.json"
print('File: ', final_root_file)


# In[175]:


# busca o caminho final
def print_finished(data,iteration,  as_array=True):
    iteration+=1
    if isinstance(data, dict):
        if data.get('finish'):
            if as_array:
                return [True]
            return ' '
        if data.get('dead'):
            return ''
    if not isinstance(data, dict) and data.get('dead'):
        return ''
    for direction in data:
        result = print_finished(data[direction], iteration, as_array)
        if result:
            if as_array:
                return [direction]+ result
            return f'{direction} {result}'
f = open(final_root_file)
root = json.load(f)
f.close()
directions = print_finished(root, 0)
print(directions)
print(len(directions))


# In[176]:


## checa o caminho encontrado

file = open('input.txt')
matrix = [[int(v) for v in x.replace('\n','').split(' ')] for x in file.readlines()]
file.close()
iteration = 0
i, j = 0,0
for direction in directions:
    matrix = next_matrix(matrix, iteration)
    if direction == DIREITA:
        j+=1
    if direction == ESQUERDA:
        j-=1
    if direction == CIMA:
        i-=1
    if direction == BAIXO:
        i+=1
    # write_image(matrix, i, j, iteration)
    iteration+=1


# In[180]:


solution_file = open('solution', 'w')
for d in directions[:-1]:
    solution_file.write(f'{d} ')
solution_file.close()


# In[ ]:




