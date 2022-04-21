from stat import S_ISDIR
import os

def RecursiveFileSearch(strTop):
    print(f'dir > {strTop}')
    for strNext in os.listdir(strTop):
        strNextSearchIn = f'{strTop}{os.sep}{strNext}'
        if S_ISDIR(os.stat(strNextSearchIn, follow_symlinks = True).st_mode): # is a directory
            RecursiveFileSearch(strNextSearchIn)
        else: # is a file
            print(f'file > {strNextSearchIn}')
    pass

RecursiveFileSearch(os.getcwd())




