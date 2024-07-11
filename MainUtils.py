#!/usr/bin/python3
"""Handles and cleans out dictionary"""
import shlex

def convert_dict(line):
    attr_dict = {}
    #remove trailing comma from every 2nd element - John,
    for i in range(1, len(line),2):
        if i != (len(line) - 1):
            line[i] = line[i][:-1] 
    #remove last element from every even element - {first_name:        
    for i in range(0, len(line), 2):
        line[i] = line[i][:-1]
        
    # Check if every 2nd element(rep. value of a dict, is a string representing a integer 
    for i in range(1, len(line), 2):
        if line[i].isdigit():
            line[i] = int(line[i])
         # Check if the element is a string representing a float
        elif line[i].replace('.', '', 1).isdigit(): 
            line[i] = float(line[i])
    
    for i in range(0, len(line), 2):
        attr_dict[line[i]] = line[i+1]
    
 
    return attr_dict


if __name__ == '__main__':
    string = ['first_name:', 'John,', 'age:', '89']
    result_dict = convert_dict(string)
    print(result_dict)