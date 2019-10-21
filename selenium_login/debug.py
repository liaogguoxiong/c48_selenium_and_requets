#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-20 12:05
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : debug.py
# @Des:

with open("11","r",encoding="utf-8") as f:
    name=f.readlines()

name3=[]
for n in name:
    n=n.strip()
    name3.append(n)
print(name3)
with open("111","r",encoding="utf-8") as f:
    name1=f.readlines()

name2=[]
for i in name1:
    i=i.strip()
    # print(i[:-19])
    # print(i[-18:])
    name2.append(i)

print(name2)

for j in name2:
    for k in name3:
        if j[-18:] in k:
            k=k+"-"+j[:-19]
            print(k)
            with open("input_file","a",encoding="utf-8") as f:
                f.write(k)
                f.write("\n")


