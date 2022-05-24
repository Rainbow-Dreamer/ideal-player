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
import random
from PIL import Image, ImageTk

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
sys.path.append('packages')

with open('packages/Ideal Player.py', encoding='utf-8') as f:
    exec(f.read())
