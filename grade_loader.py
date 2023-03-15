import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

def fish_grade_load():
    f2 = open(BASE_DIR+"\\fish_list.txt",'r',encoding="utf-8")

    fish_list = {}
    i = 0
    while 1:
        temp=f2.readline().strip()
        
        if temp == '-':
            i += 1
            continue
        
        if temp == '':
            break
        
        fish_list[temp] = i
    return fish_list