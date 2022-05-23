# -*- coding: utf-8 -*-
"""Bitgo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sFU3UpbJHScZBwhIdEaR5Kd9RzK6D3uQ
"""

from collections import deque

def bfs(vertices, edges):
  
        visited = {k:False for k in vertices}
  
        queue = deque()
        for v in vertices:
            if(dir_count[v] == 0):
                queue.append(v)
                visited[v] = True
  
        while queue:
  
            s = queue.pop()
  
            for i in edges[s]:
                dir_count[i]-=1
                if visited[i] == False and dir_count[i]:
                    total_count[i]+=total_count[s]+1
                    queue.append(i)
                    visited[i] = True

import requests
from tqdm import tqdm

URL = "https://blockstream.info/api/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732/txids"

r = requests.get(url = URL)

dict = {}
vertices = set(r.json())
edges = {k:[] for k in vertices}
dir_count = {}

for txid in tqdm(vertices):
    URL = "https://blockstream.info/api/tx/"+txid
    r1 = requests.get(url = URL)
    if "vin" in r1.json():
        vin = r1.json()["vin"]
        parents = []
        count = 0
        for txn in vin:
            parentid = txn["txid"]
            if(parentid in vertices):
                edges[parentid].append(txid)
                count+=1
        dir_count[txid] = count

print(dir_count)

total_count = {k:0 for k in vertices}
bfs(vertices,edges)

from queue import PriorityQueue

print (total_count)
q = PriorityQueue()
n = 0
for v in total_count:
    if n == 10:
        q.get()
        n-=1
    q.put((total_count[v],v))
    n+=1

for i in range(10):
    print(q.get())