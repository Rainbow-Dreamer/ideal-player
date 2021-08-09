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

pygame.mixer.init(44100, -16, 1, 1024)

with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())

current_playlist = []
current_play_media = []
current_queue_list = []


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(800, 400)
        self.title('Ideal Player')
        self.geometry('800x400+350+300')

        self.is_playing = False
        self.is_pause = False
        self.current_playing_object = None
        self.current_playing_filename = None
        self.current_playing_ind = None
        try:
            with open('browse memory.txt', encoding='utf-8-sig') as f:
                self.last_place = f.read()
        except:
            self.last_place = "./"
        self.choose_file_button = ttk.Button(
            self, text='选择文件播放', command=self.choose_file_button_func)
        self.choose_file_button.place(x=50, y=100)

        self.add_to_queue_button = ttk.Button(
            self, text='加入队列', command=self.multiple_choose_files)
        self.add_to_queue_button.place(x=200, y=100)

        self.current_playing_label = ttk.Label(self,
                                               text='当前正在播放: ',
                                               wraplength=600)
        self.current_playing_label.place(x=50, y=300)

        self.pause_button = ttk.Button(self,
                                       text='暂停',
                                       command=self.pause_playing)
        self.pause_button.place(x=200, y=150)

        self.stop_button = ttk.Button(self,
                                      text='停止',
                                      command=self.stop_playing)
        self.stop_button.place(x=50, y=150)

        self.previous_button = ttk.Button(self,
                                          text='上一首',
                                          command=self.play_previous)
        self.next_button = ttk.Button(self, text='下一首', command=self.play_next)
        self.random_playing_button = ttk.Button(self,
                                                text='随机播放',
                                                command=self.random_playing)
        self.previous_button.place(x=50, y=200)
        self.next_button.place(x=200, y=200)
        self.random_playing_button.place(x=50, y=250)

        self.multiple_choose_files_button = ttk.Button(
            self, text='清空队列', command=self.clear_queue)
        self.multiple_choose_files_button.place(x=200, y=250)

        self.bind(
            '<Button-3>', lambda e: self.player_queue.selection_clear(0, END)
            or self.focus_set())

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

    def play_music(self, play_filename):
        if play_filename in current_playlist:
            self.show(f'当前正在播放: {play_filename}')
            ind = current_queue_list.index(play_filename)
            self.current_playing_ind = ind
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(ind)
            if play_filename in current_playlist:
                current_playing = current_play_media[current_playlist.index(
                    play_filename)]
            else:
                self.append_new_music(play_filename)
                return
            if self.is_playing:
                self.current_playing_object.fadeout(500)
                self.after(600,
                           lambda: self.play_current_music(current_playing))
            else:
                pygame.mixer.fadeout(200)
                current_playing.play()
                self.is_playing = True
            self.current_playing_object = current_playing
            self.current_playing_filename = play_filename

        else:
            file_type = os.path.splitext(play_filename)[1][1:]
            if file_type in supported_audio_file_formats:
                self.show(f'当前正在播放: {play_filename}')
                if play_filename not in current_queue_list:
                    self.player_queue.insert(END,
                                             os.path.basename(play_filename))
                    self.player_queue.selection_clear(0, END)
                    self.player_queue.selection_set(END)
                    current_queue_list.append(play_filename)
                else:
                    current_ind = current_queue_list.index(play_filename)
                    self.player_queue.selection_clear(0, END)
                    self.player_queue.selection_set(current_ind)
                self.current_playing_ind = current_queue_list.index(
                    play_filename)
                if self.is_playing:
                    self.current_playing_object.fadeout(500)
                    self.after(600,
                               lambda: self.append_new_music(play_filename))
                else:
                    self.append_new_music(play_filename)
                    self.is_playing = True

    def play_current_music(self, current_playing):
        pygame.mixer.fadeout(200)
        current_playing.play()

    def append_new_music(self, play_filename, mode=0):
        if mode == 0:
            current_playlist.append(play_filename)
            current_playing = pygame.mixer.Sound(play_filename)
            current_play_media.append(current_playing)
            self.current_playing_object = current_playing
            self.current_playing_filename = play_filename
            pygame.mixer.fadeout(200)
            current_playing.play()
            self.is_playing = True
        elif mode == 1:
            current_queue_list.append(play_filename)

    def display_player_queue(self):
        self.player_queue_bar_v = Scrollbar(self, orient='vertical')
        self.player_queue_bar_h = Scrollbar(self, orient='horizontal')
        self.player_queue_bar_v.place(x=775, y=150, height=200, anchor=CENTER)
        self.player_queue_bar_h.place(x=370, y=250, width=400)
        self.player_queue = Listbox(self,
                                    yscrollcommand=self.player_queue_bar_v.set,
                                    xscrollcommand=self.player_queue_bar_h.set)
        self.player_queue_bar_v.configure(command=self.player_queue.yview)
        self.player_queue_bar_h.configure(command=self.player_queue.xview)
        self.player_queue.place(x=370, y=50, width=400, height=200)
        self.player_queue.bind('<Double-1>', self.choose_queue)
        self.player_queue.bind('<Button-3>', self.delete_queue)

    def add_to_queue(self, mode=0, play_filename=None):
        if mode == 0:
            play_filename = filedialog.askopenfilename(
                initialdir=self.last_place,
                title="选择你想想要加入队列的文件",
                filetype=(("all files", "*.*"), ))
        if play_filename:
            memory = play_filename[:play_filename.rindex('/') + 1]
            if self.last_place != memory:
                with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
                    f.write(memory)
                self.last_place = memory

            if play_filename not in current_playlist and play_filename not in current_queue_list:
                file_type = os.path.splitext(play_filename)[1][1:]
                if file_type in supported_audio_file_formats:
                    self.player_queue.insert(END,
                                             os.path.basename(play_filename))
                    self.append_new_music(play_filename, mode=1)

    def choose_queue(self, e):
        current = self.player_queue.curselection()
        if current and current_queue_list:
            current_filename = current_queue_list[current[0]]
            self.play_music(current_filename)

    def delete_queue(self, e):
        current = self.player_queue.curselection()
        if current and current_queue_list:
            current = current[0]
            current_filename = current_queue_list[current]
            del current_queue_list[current]
            if current_filename in current_playlist:
                playlist_ind = current_playlist.index(current_filename)
                del current_playlist[playlist_ind]
                del current_play_media[playlist_ind]
            self.player_queue.delete(current)
            self.player_queue.selection_clear(0, END)
            self.focus_set()

    def pause_playing(self):
        if self.is_pause:
            self.unpause_playing()
        elif self.is_playing:
            pygame.mixer.pause()
            self.pause_button.configure(text='继续播放')
            self.is_pause = True

    def unpause_playing(self):
        if self.is_pause:
            pygame.mixer.unpause()
            self.pause_button.configure(text='暂停')
            self.is_pause = False

    def stop_playing(self):
        if self.is_playing:
            pygame.mixer.stop()
            self.is_playing = False
            self.stop_button.configure(text='播放')
        else:
            if self.current_playing_object:
                pygame.mixer.fadeout(200)
                self.current_playing_object.play()
                self.stop_button.configure(text='停止')
                self.is_playing = True

    def play_next(self):
        if current_queue_list:
            if not self.current_playing_filename or (
                    self.current_playing_filename not in current_queue_list):
                current_ind = self.current_playing_ind - 1 if self.current_playing_ind is not None else -1
            else:
                current_ind = current_queue_list.index(
                    self.current_playing_filename)
            if current_ind == len(current_queue_list) - 1:
                current_ind = -1
            next_filename = current_queue_list[current_ind + 1]
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(current_ind + 1)
            self.play_music(next_filename)

    def play_previous(self):
        if current_queue_list:
            if not self.current_playing_filename or (
                    self.current_playing_filename not in current_queue_list):
                current_ind = self.current_playing_ind if self.current_playing_ind is not None else 0
            else:
                current_ind = current_queue_list.index(
                    self.current_playing_filename)
            if current_ind == 0:
                current_ind = len(current_queue_list)
            next_filename = current_queue_list[current_ind - 1]
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(current_ind - 1)
            self.play_music(next_filename)

    def multiple_choose_files(self):
        play_filenames = filedialog.askopenfilenames(
            initialdir=self.last_place,
            title="选择你想播放的文件",
            filetype=(("all files", "*.*"), ))
        if play_filenames:
            play_filename = play_filenames[0]
            memory = play_filename[:play_filename.rindex('/') + 1]
            if self.last_place != memory:
                with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
                    f.write(memory)
                self.last_place = memory
            for each in play_filenames:
                self.add_to_queue(mode=1, play_filename=each)

    def random_playing(self):
        if current_queue_list:
            self.play_music(random.choice(current_queue_list))

    def clear_queue(self):
        current_queue_list.clear()
        current_playlist.clear()
        current_play_media.clear()
        self.player_queue.selection_clear(0, END)
        self.player_queue.delete(0, END)
        self.focus_set()
        self.current_playing_ind = None


root = Root()
root.focus_force()
root.mainloop()
