#!/usr/bin/python3

import shlex

def dict_for_create(line):
    line = str(line)
    args = shlex.split(line)
    args_list = args[1:]
    for i in range(len(args_list)):
        args_list[i] = args_list[i][:-1]
    # print(args_list)
    attr_dict = {}
    
    for i in range(1, len(args_list), 2):
        if args_list[i].isdigit():
            args_list[i] = int(args_list[i])
        # Check if the element is a string representing a float
        elif args_list[i].replace('.', '', 1).isdigit():
            args_list[i] = float(args_list[i])
        else:
            args_list[i].strip() 
    
    for i in range(0, len(args_list), 1):
        args_list[i].strip()
        key, separator, value = args_list[i].partition('=')
        key.strip('\"')
        value.strip('\"')
        # print("{} - {}".format(key, value))
    
        
        if value.isdigit():
            value = int(value)
        # Check if the value starts with a plus or minus sign followed by a digit    
        elif len(value) > 1 and (value[0] == '+' or value[0] == '-') and value[1].isdigit():
            sign = -1 if value[0] == '-' else 1
            remaining_part = value[1:]
            # Check if the remaining part contains a decimal point
            if '.' in remaining_part:
                sign * float(value)
            else:
                sign * int(remaining_part)
            
            try:
                value = float(value)
            except ValueError:
                pass
          
        attr_dict[key] = value
        
    return (attr_dict)
        
if __name__ == '__main__':
    string = ['city_id="0001"', 'user_id="0001"', 'name="My_little_house"', 'number_rooms=4', 'number_bathrooms=2', 'max_guest=10', 'price_by_night=300', 'latitude=37.773972', 'longitude=-122.431297']
    result_dict = dict_for_create(string)
    print(result_dict)