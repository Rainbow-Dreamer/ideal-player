import traceback
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter.scrolledtext import ScrolledText
import PIL.Image, PIL.ImageTk
from tkinter import filedialog
import os, sys
import re
from yapf.yapflib.yapf_api import FormatCode
import pygame

#abs_path = os.path.dirname(sys.executable)
abs_path = os.path.dirname(__file__)
os.chdir(abs_path)

with open('packages/Ideal Player.py', encoding='utf-8-sig') as f:
    exec(f.read())
