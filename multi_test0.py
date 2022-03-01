# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:36:16 2021

@author: JAE
"""

from multiprocessing import Process
import multiprocessing

def f(name):
    print('hello', name)

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    
    