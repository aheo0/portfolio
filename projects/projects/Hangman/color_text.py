from __future__ import print_function

class Colors:
    '''Colors for printing in the terminal'''
    
    default = '\033[0m'
    Runderline = '\033[24m'
    
    dim = '\033[3m'
    underline = '\033[4m'
    
    black = '\033[30m'
    white = '\033[37m'
    
    def __init__(self, dim):
        self.theme = dim
        
        if dim:
            #;1m for bright colors is not supported by cloud9 terminal
            self.red = '\033[31m'
            self.green = '\033[32m'
            self.yellow = '\033[33m'
            self.blue = '\033[34m'
            self.purple = '\033[35m'
            self.cyan = '\033[36m'
        else:
            self.red = '\033[31m'
            self.green = '\033[32m'
            self.yellow = '\033[33m'
            self.blue = '\033[34m'
            self.purple = '\033[35m'
            self.cyan = '\033[36m'
    
    def reformat(self):
        '''shortcut to resetting the terminal
        no inputs -> None'''
        import sys
        print(self.default, end='')