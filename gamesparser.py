
import re
import array
import numpy as np 
file = open("./data/Games/Abhijeet_Gupta.pgn")
lines = file.readlines()
file.close()
key = []
key2 =[]
for line in lines:
    #print("->" +str(line))
    if line.startswith('[') and line.rstrip('\n').endswith(']'):
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.replace(' "',';"')
        arr = line.split(';')
        exist =","
        if(arr[0] not in key):
            key.append(line = arr[0].rstrip('\r\n'))   
        if (exist in arr[1]):
            print("multiple " + arr[0]+ " -> "+ arr[1])
            if((arr[0]+"*") not in key2):
                key2.append(arr[0]+"*") 
        else:
            print("non "+ arr[0]+ " -> "+ arr[1]+ "")
            
           
               
       #print(line)
        print("-----------------")
    else:
        print("")
   
print(key)
print(key2)