#! /usr/bin/env python3

import cmd, sys
import glob
import configparser

class ConfigShell(cmd.Cmd):
    intro = 'Welcome to the Config generator. Type ? or help tp list all commands.\n'
    prompt = '(cgen)'
    file = None
    
    def do_list_configs(self, arg):
        'List existing configs'
        for config in glob.glob("./*.conf"):
            print(str(config))
    
    def do_show_config(self, arg):
        'Shows the content of a config'
        with open(arg, 'r') as config:
            print(config.read())
        
    def do_new_config(self, arg):
        'Generate a new config file. Types enables: MySQL'
        configlist = ['mysql']
        arg = arg.lower()
        if arg != "" and arg not in configlist:
            print("Not a valid config purpose")
            arg = ""
        while arg == "":
            arg = input('Enter the purpose of the config: ').lower()
            if arg in configlist: #valid entry
                break
            else:
                arg = ""
                print('Not a valid config purpose!')
        
        config = configparser.ConfigParser()
        
        if arg == "mysql":
            # Generate MySQL config.
            hostname = input('Hostname: ')
            database = input('Database: ')
            username = input('Username: ')
            password = input('Password: ')
            config['MySQL'] = {'host': hostname, 'database': database, 'user': username, 'password': password}
            with open('mysql.conf', 'w') as configfile:
                config.write(configfile)
            print('Configuration generation successful!')
        
    def do_exit(self, arg):
        'Exit the shell'
        print('Bye')
        return True
    
if __name__ == '__main__':
    ConfigShell().cmdloop()
