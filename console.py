import cmd
import shlex
import re
import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)


from models import storage
from models.base_model import BaseModel
from models.user import User
from models.tweet import Tweet
from MainUtils import convert_dict
from demo import dict_for_create

class HBNBCommand(cmd.Cmd):
    prompt = '(TweetBox)'
    __classes = {       
        "User",        
        "Tweet"
    }
    
    def precmd(self, line):
        pattern = r"(\w+)\.(\w+)\(\)"
        match = re.match(pattern, line)
        if match:
            class_name = match.group(1)
            method_name = match.group(2)
            line = method_name + ' ' + class_name
            return line
        
        pattern = r"(\w+)\.(\w+)\((\".*?\"|'.*?')\)"           
        match = re.match(pattern, line)
        if match:
                class_name = match.group(1)
                method_name = match.group(2)
                inst_id = match.group(3)[1:-1] # without quotes
                line = method_name + ' ' + class_name + ' ' + inst_id
                return line 
                    
        pattern = r'(\w+)\.(\w+)\((\".*?\"|\'.*?\'),\s*(\".*?\"|\'.*?\'|\w+),\s*(\".*?\"|\'.*?\'|\d+)\)'
        match = re.match(pattern, line)
        if match:
            class_name = match.group(1)
            method_name = match.group(2)
            inst_id = match.group(3)  #[1:-1] # without quotes
            attr_name = match.group(4) #[1:-1]
            attr_value = match.group(5)  #.strip('\'"') update has handled quotes already
            line = method_name + ' ' + class_name + ' ' + inst_id + ' ' + attr_name + ' ' + attr_value
            return line
        
        pattern = r'(\w+)\.(\w+)\((\".*?\"|\'.*?\'),\s*{(.*?)}\)'
        match = re.match(pattern, line)
        if match:
            class_name, method_name, inst_id, attr_dict = match.groups()            
            attr_dict_str = str(attr_dict)
            line = method_name + ' ' + class_name + ' ' + inst_id + ' ' + attr_dict_str
            print(attr_dict_str)
            print(line)
            return line
     
        else:
            return line
        
        
    def do_create(self, line):
        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        else:
            cls = globals()[args[0]]
            obj = cls()
            new_dict = {}
            for arg in args[1:]:
                if "=" in arg:
                    key, value = arg.split('=', 1)
                    value = value.strip('"')
                    value = value.replace('_', ' ')
                    sign = '-'
                    if value.isdigit():
                        value = int(value)
                    elif value[0] == sign:
                        value1 = value[1:]
                        #handles negative float
                        if (value1.replace('.', '', 1).isdigit()):                            
                            value = float(value)
                    #handles positive float        
                    elif (value.replace('.', '', 1).isdigit()):
                        value = float(value)
                    new_dict[key] = value
            for key, value in new_dict.items():
                setattr(obj, key, value)
                
            obj.save()
            storage.save()
        print(obj.id)
            
    def do_update(self, line):
        args = shlex.split(line)
        print(len(args))
        if not args:
            print("** class name missing **")
            return
        if args:
            if len(args) > 4:
                class_name = args[0]
                id = args[1]
                attr_dict_str = args[2:]
                # print("attr_dict - {}".format(attr_dict_str))
                attr_dict = convert_dict(attr_dict_str)
                if class_name not in HBNBCommand.__classes:                
                    print("** class doesn't exist **")
                    return
                keycheck = "{}.{}".format(class_name, id)
                objects = storage.all()
                if keycheck not in objects.keys():
                    print("** no instance found **")
                    return
                else:
                    obj = objects[keycheck]
                    
                    # try:
                    #     attr_dict = ast.literal_eval(attr_dict)
                    # except (SyntaxError, ValueError):
                    #     print("** invalid dictionary format **")
                    #     return
                    
                    for key, value in attr_dict.items():
                        # try:
                        #     if value.isdigit():
                        #         value = int(value)
                        #     else:
                        #         value = float(value)
                        # except ValueError:
                        #     pass
                        setattr(obj, key, value)
                        obj.save()
                        storage.save()
  
            if len(args) == 4:
                class_name, id, attr_key, attr_value = args[:4]
                attr_value.strip('\'"')
                try:
                    if attr_value.isdigit():
                        attr_value = int(attr_value)
                    else:
                        attr_value = float(attr_value)
                except ValueError:
                    pass
                
                keycheck = "{}.{}".format(class_name, id)
                objects = storage.all()
                if keycheck not in objects.keys():
                    print("** no instance found **")
                    return
                else:
                    obj = objects[keycheck]
                    setattr(obj, attr_key, attr_value)
                    storage.save()
                
            if len(args) == 1:
                if args[0] not in HBNBCommand.__classes:                
                    print("** class doesn't exist **")
                    return
                else:
                    print("** instance id missing **")
                    return
            if len(args) == 2:
                class_name, id = args
                keycheck = "{}.{}".format(class_name, id)
                objects = storage.all()
                if keycheck not in objects.keys():
                    print("** no instance found **")
                    return
                else:
                    print("** attribute name missing **")
                    return
            if len(args) == 3:
                print(" ** value missing ** ")
                return
                
       
            
    def do_show(self, line):
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args:
            if len(args) == 2:
                class_name, class_id = args
                keycheck = "{}.{}".format(class_name, class_id)
                objects = storage.all()
                if keycheck not in objects.keys():
                    print("** no instance found **")
                    return  
                else:
                    print(objects[keycheck])
            else:
                if args[0] not in HBNBCommand.__classes:                
                    print("** class doesn't exist **")
                    return
                else:
                    print("** instance id missing **")
                    return
                
    def do_all(self, line):
        print("I wan print ooo")
        args = shlex.split(line)
        objects = storage.all()
        if not args:
            for obj in objects.values():
                print(obj)
                print("------------------------")
        else:
            class_name = args[0]
            if class_name in HBNBCommand.__classes:
                class_objects = storage.all(class_name)
                for obj in class_objects.values():
                    print(obj)
                    print("------------------------")
            else:
                print("** class doesn't exist **")
        
        
        
            
    def do_count(self, line):
        objects = storage.all()
        args = line.split()
        if not args:
            dict_length = len(objects)
            print(dict_length)
        else:
            class_name = args[0]
            if class_name in HBNBCommand.__classes:
                count = 0
                for key, obj in objects.items():
                    dot_index = key.find('.')
                    key_class_name = key[:dot_index]
                    if key_class_name == class_name:
                        count += 1
                print(count)
                return
            else:
                print("** class doesn't exist **")
                return
                
                    
  
    
                
    def do_destroy(self, line):
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args:
            if len(args) == 2:
                class_name, class_id = args
                keycheck = "{}.{}".format(class_name, class_id)
                objects = storage.all()
                if keycheck not in objects.keys():
                    print("** no instance found **")
                    return  
                else:
                    storage.delete(objects[keycheck])                  
                    storage.save()
            else:
                if args[0] not in HBNBCommand.__classes:                
                    print("** class doesn't exist **")
                    return
                else:
                    print("** instance id missing **")
                    return
                
    
        
        
    
      
    def emptyline(self):
        """an empty line + ENTER shouldn’t execute anything"""
        pass
    
    def do_quit(self, line):
        """This exits the program"""
        return True
    
    def do_EOF(self, line):
        """This handles EOF and Ctrl + D signals"""
        print() #to exit cleanly
        return True
    
    
    
if __name__ == '__main__':
    HBNBCommand().cmdloop()

