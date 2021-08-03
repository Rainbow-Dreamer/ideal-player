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

with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())

current_playlist = []
current_play_media = []


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(800, 400)
        self.title('Ideal Player')
        self.geometry('800x400+350+300')

        self.is_playing = False
        self.current_playing_object = None
        try:
            with open('browse memory.txt', encoding='utf-8-sig') as f:
                self.last_place = f.read()
        except:
            self.last_place = "./"
        self.choose_file_button = ttk.Button(
            self, text='选择文件播放', command=self.choose_file_button_func)
        self.choose_file_button.place(x=50, y=100)

        self.add_to_queue_button = ttk.Button(self,
                                              text='加入队列',
                                              command=self.add_to_queue)
        self.add_to_queue_button.place(x=200, y=100)

        self.current_playing_label = ttk.Label(self,
                                               text='当前正在播放: ',
                                               wraplength=600)
        self.current_playing_label.place(x=50, y=300)

        self.display_player_queue()

    def show(self, text=''):
        self.current_playing_label.configure(text=text)

    def choose_file_button_func(self):
        play_filename = filedialog.askopenfilename(initialdir=self.last_place,
                                                   title="选择你想播放的文件",
                                                   filetype=(("all files",
                                                              "*.*"), ))
        if play_filename:
            memory = play_filename[:play_filename.rindex('/') + 1]
            if self.last_place != memory:
                with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
                    f.write(memory)
                self.last_place = memory
            self.play_music(play_filename)
            self.is_playing = True

    def play_music(self, play_filename):
        if play_filename in current_playlist:
            self.show(f'当前正在播放: {play_filename}')
            ind = current_playlist.index(play_filename)
            current_playing = current_play_media[ind]
            if self.is_playing:
                self.current_playing_object.fadeout(500)
                self.after(600, current_playing.play)
            else:
                current_playing.play()
            self.current_playing_object = current_playing
            self.is_playing = True
        else:
            file_type = os.path.splitext(play_filename)[1][1:]
            if file_type in supported_audio_file_formats:
                self.show(f'当前正在播放: {play_filename}')
                self.player_queue.insert(END, os.path.basename(play_filename))
                if self.is_playing:
                    self.current_playing_object.fadeout(500)
                    self.after(600,
                               lambda: self.append_new_music(play_filename))
                else:
                    self.append_new_music(play_filename)
                self.is_playing = True

    def append_new_music(self, play_filename, mode=0):
        current_playing = pygame.mixer.Sound(play_filename)
        current_playlist.append(play_filename)

        current_play_media.append(current_playing)

        if mode == 0:
            self.current_playing_object = current_playing
            current_playing.play()

    def display_player_queue(self):
        self.player_queue_bar_v = Scrollbar(self, orient='vertical')
        self.player_queue_bar_h = Scrollbar(self, orient='horizontal')
        self.player_queue_bar_v.place(x=775, y=150, height=200, anchor=CENTER)
        self.player_queue_bar_h.place(x=470, y=250, width=300)
        self.player_queue = Listbox(self,
                                    yscrollcommand=self.player_queue_bar_v.set,
                                    xscrollcommand=self.player_queue_bar_h.set)
        self.player_queue_bar_v.configure(command=self.player_queue.yview)
        self.player_queue_bar_h.configure(command=self.player_queue.xview)
        self.player_queue.place(x=470, y=50, width=300, height=200)

    def add_to_queue(self):
        play_filename = filedialog.askopenfilename(initialdir=self.last_place,
                                                   title="选择你想想要加入队列的文件",
                                                   filetype=(("all files",
                                                              "*.*"), ))
        if play_filename:
            memory = play_filename[:play_filename.rindex('/') + 1]
            if self.last_place != memory:
                with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
                    f.write(memory)
                self.last_place = memory

            if play_filename not in current_playlist:
                file_type = os.path.splitext(play_filename)[1][1:]
                if file_type in supported_audio_file_formats:
                    self.player_queue.insert(END,
                                             os.path.basename(play_filename))
                    self.append_new_music(play_filename, mode=1)


root = Root()
root.focus_force()
root.mainloop()
