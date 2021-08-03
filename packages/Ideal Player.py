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
pygame.mixer.init(44100, -16, 1, 1024)







def display_player_queue():
    global display_player_queue_open
    global player_queue_window
    if not display_player_queue_open:
        display_player_queue_open = True
        current_location = window.get_location()
        player_queue_window = tkinter.Toplevel()
        player_queue_window.title('当前播放队列')
        #player_queue_window.minsize(700, 200)
        player_queue_window.geometry(
            '%dx%d+%d+%d' %
            (700, 300, current_location[0] + 50, current_location[1] + 350))
        player_queue_window.player_queue_bar = tkinter.Scrollbar(
            player_queue_window)
        player_queue_window.player_queue_bar.place(x=607,
                                                   y=100,
                                                   height=170,
                                                   anchor=tkinter.CENTER)
        player_queue_window.player_queue = tkinter.Listbox(
            player_queue_window,
            yscrollcommand=player_queue_window.player_queue_bar.set)
        player_queue_window.player_queue.place(x=0, y=0, width=600)
        for each in current_playlist:
            player_queue_window.player_queue.insert(tkinter.END, each)
        player_queue_window.protocol("WM_DELETE_WINDOW",
                                     close_player_queue_window)
        player_queue_window.mainloop()
    else:
        player_queue_window.lift()


def close_player_queue_window():
    global display_player_queue_open
    global player_queue_window
    player_queue_window.destroy()
    display_player_queue_open = False


with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())

play_filename = None
is_playing = False
current_playing_object = None
current_playlist = []
current_play_media = []
display_player_queue_open = False
try:
    with open('browse memory.txt', encoding='utf-8-sig') as f:
        last_place = f.read()
except:
    last_place = "./"

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(800, 400)
        self.title('Ideal Player')
        self.geometry('800x400+350+300')
        
        self.choose_file_button = ttk.Button(self, text='选择文件', command=self.choose_file_button_func)
        self.choose_file_button.place(x=200, y=100)
        
        self.current_playing_label = ttk.Label(self, text='当前正在播放: ', wraplength=600)
        self.current_playing_label.place(x=50, y=200)
    
    def show(self, text=''):
        self.current_playing_label.configure(text=text)
    
    def choose_file_button_func(self):
        global last_place
        global is_playing
        play_filename = filedialog.askopenfilename(initialdir=last_place,
                                                   title="选择你想播放的文件",
                                                   filetype=(("all files",
                                                              "*.*"), ))
        if play_filename:
            memory = play_filename[:play_filename.rindex('/') + 1]
            if last_place != memory:
                with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
                    f.write(memory)
                last_place = memory
            self.play_music(play_filename)
            is_playing = True
    
    def play_music(self, play_filename):
        global is_playing
        global current_playing_object
        if play_filename in current_playlist:
            self.show(f'当前正在播放: {play_filename}')
            ind = current_playlist.index(play_filename)
            current_playing = current_play_media[ind]
            if is_playing:
                current_playing_object.fadeout(500)
                self.after(600, current_playing.play)
            else:
                current_playing.play()
            current_playing_object = current_playing
            is_playing = True
        else:
            file_type = os.path.splitext(play_filename)[1][1:]
            if file_type in supported_audio_file_formats:
                self.show(f'当前正在播放: {play_filename}')
                if is_playing:
                    current_playing_object.fadeout(500)
                    self.after(600, lambda: self.append_new_music(play_filename))
                else:
                    self.append_new_music(play_filename)                             
                is_playing = True
        
    
    def append_new_music(self, play_filename, mode=0):
        global current_playing_object
        current_playing = pygame.mixer.Sound(play_filename)
        current_playlist.append(play_filename)
        current_play_media.append(current_playing)
        current_playing_object = current_playing        
        if mode == 0:
            current_playing.play()
            




root = Root()
root.focus_force()
root.mainloop()
