import pygame
import os
import time
import sys
import pyglet
import keyboard
import tkinter
from tkinter import filedialog
import pygame.midi
from pyglet.window import mouse
from tkinter import Tk
from threading import Thread

#abs_path = os.path.dirname(sys.executable)
abs_path = os.path.dirname(__file__)
os.chdir(abs_path)

with open('packages/Ideal Player.py', encoding='utf-8-sig') as f:
    exec(f.read())
