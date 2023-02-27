pygame.mixer.init(44100, -16, 2, 1024)

with open('packages/config.py', encoding='utf-8') as f:
    exec(f.read())

with open('packages/languages.py', encoding='utf-8') as f:
    language_dict = eval(f.read())

current_playlist = []
current_play_media = []
current_queue_list = []


class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.minsize(*screen_size)
        self.title('Ideal Player')
        self.geometry('800x400+350+300')
        if background_image:
            self.bg_image = ImageTk.PhotoImage(
                Image.open(background_image).resize(screen_size,
                                                    Image.Resampling.LANCZOS))
            self.bg_label = ttk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0)

        self.is_playing = False
        self.is_pause = False
        self.waiting = False
        self.current_playing_object = None
        self.current_playing_filename = ''
        self.current_playing_ind = None
        self.language_dict = language_dict[language]
        self.choose_file_button = ttk.Button(
            self,
            text=self.language_dict['Choose file to play'],
            command=self.choose_file_button_func)
        self.choose_file_button.place(x=50, y=50)

        self.add_to_queue_button = ttk.Button(
            self,
            text=self.language_dict['Add to queue'],
            command=self.multiple_choose_files)
        self.add_to_queue_button.place(x=200, y=50)

        self.current_playing_label = ttk.Label(
            self, text=self.language_dict['Current playing: '], wraplength=600)
        self.current_playing_label.place(x=50, y=340)

        self.pause_button = ttk.Button(self,
                                       text=self.language_dict['Pause'],
                                       command=self.pause_playing)
        self.pause_button.place(x=200, y=100)

        self.stop_button = ttk.Button(self,
                                      text=self.language_dict['Stop'],
                                      command=self.stop_playing)
        self.stop_button.place(x=50, y=100)

        self.previous_button = ttk.Button(self,
                                          text=self.language_dict['Previous'],
                                          command=self.play_previous)
        self.next_button = ttk.Button(self,
                                      text=self.language_dict['Next'],
                                      command=self.play_next)
        self.random_playing_button = ttk.Button(
            self,
            text=self.language_dict['Random playing'],
            command=self.random_playing)
        self.previous_button.place(x=50, y=150)
        self.next_button.place(x=200, y=150)
        self.random_playing_button.place(x=50, y=200)

        self.multiple_choose_files_button = ttk.Button(
            self,
            text=self.language_dict['Clear queue'],
            command=self.clear_queue)
        self.multiple_choose_files_button.place(x=200, y=200)

        self.playing_mode_button = ttk.Button(
            self,
            text=self.language_dict['Play mode'][0],
            command=self.change_playing_mode)
        self.playing_mode_button.place(x=50, y=300)
        self.change_language_button = ttk.Button(
            self,
            text=self.language_dict['Choose language'],
            command=self.change_language)
        self.change_language_button.place(x=50, y=250)
        self.playing_mode = 0

        self.bind(
            '<Button-3>', lambda e: self.player_queue.selection_clear(0, END)
            or self.focus_set())

        self.bind('<w>', lambda e: self.play_previous())
        self.bind('<s>', lambda e: self.play_next())
        self.bind('<z>', lambda e: self.random_playing())
        self.bind('<a>', lambda e: self.move_volume_bar_set_value(-5))
        self.bind('<d>', lambda e: self.move_volume_bar_set_value(5))
        self.bind('<space>', lambda e: self.pause_playing())
        self.bind('<e>', lambda e: self.stop_playing())
        self.bind('<x>', lambda e: self.choose_file_button_func())
        self.bind('<c>', lambda e: self.multiple_choose_files())
        self.bind('<r>', lambda e: self.clear_queue())
        self.bind('<v>', lambda e: self.change_playing_mode())
        self.bind('<q>', lambda e: self.destroy())

        self.slider = StringVar()
        self.volume_interval = [0, 100]
        self.volume_length = self.volume_interval[0] - self.volume_interval[1]
        self.current_volume_percentage = 100
        self.slider.set(
            f'{self.language_dict["Volume"]}: {self.current_volume_percentage}%'
        )
        self.slider_label = ttk.Label(self, textvariable=self.slider)
        self.slider_label.place(x=400, y=280)
        self.set_move_volume_bar = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            length=200,
            value=self.current_volume_percentage,
            command=lambda e: self.change_move_volume_bar(e))
        self.set_move_volume_bar.place(x=500, y=280)

        self.display_player_queue()

        self.check_is_playing()

    def change_language(self):
        menubar = Menu(self, tearoff=False)
        for each in language_dict:
            menubar.add_command(
                label=each,
                command=lambda each=each: self.change_language_func(each))
        menubar.tk_popup(x=self.winfo_pointerx(), y=self.winfo_pointery())

    def change_language_func(self, language):
        self.language_dict = language_dict[language]
        self.choose_file_button.configure(
            text=self.language_dict['Choose file to play'])
        self.add_to_queue_button.configure(
            text=self.language_dict['Add to queue'])
        self.current_playing_label.configure(
            text=
            f'{self.language_dict["Current playing: "]} {self.current_playing_filename}'
        )
        self.pause_button.configure(text=self.language_dict['Pause'])
        self.stop_button.configure(text=self.language_dict['Stop'])
        self.previous_button.configure(text=self.language_dict['Previous'])
        self.next_button.configure(text=self.language_dict['Next'])
        self.random_playing_button.configure(
            text=self.language_dict['Random playing'])
        self.multiple_choose_files_button.configure(
            text=self.language_dict['Clear queue'])
        self.playing_mode_button.configure(
            text=self.language_dict['Play mode'][self.playing_mode])
        self.change_language_button.configure(
            text=self.language_dict['Choose language'])
        self.slider.set(
            f'{self.language_dict["Volume"]}: {self.current_volume_percentage}%'
        )

    def check_is_playing(self):
        if self.is_playing:
            if not pygame.mixer.get_busy():
                if self.playing_mode == 0:
                    self.play_next()
                elif self.playing_mode == 1:
                    self.current_playing_object.play()
                elif self.playing_mode == 2:
                    self.random_playing()
                self.after(2000, self.check_is_playing)
                return
        self.after(100, self.check_is_playing)

    def show(self, text=''):
        self.current_playing_label.configure(text=text)

    def choose_file_button_func(self):
        play_filename = filedialog.askopenfilename(
            title="Choose file you want to play",
            filetypes=(("all files", "*"), ))
        if play_filename:
            self.play_music(play_filename)

    def play_music(self, play_filename):
        if play_filename in current_playlist:
            self.show(
                f'{self.language_dict["Current playing: "]} {play_filename}')
            ind = current_queue_list.index(play_filename)
            self.current_playing_ind = ind
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(ind)
            if play_filename in current_playlist:
                current_playing = current_play_media[current_playlist.index(
                    play_filename)]
                current_playing.set_volume(self.current_volume_percentage /
                                           100)
            else:
                self.append_new_music(play_filename)
                return
            if self.is_playing:
                self.is_playing = False
                self.waiting = True
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
            if file_type.lower() in supported_audio_file_formats:
                self.show(
                    f'{self.language_dict["Current playing: "]} {play_filename}'
                )
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
                    self.is_playing = False
                    self.waiting = True
                    self.current_playing_object.fadeout(500)
                    self.after(600,
                               lambda: self.append_new_music(play_filename))
                else:
                    self.append_new_music(play_filename)
                    self.is_playing = True

    def play_current_music(self, current_playing):
        pygame.mixer.fadeout(200)
        current_playing.play()
        self.is_playing = True
        self.waiting = False

    def append_new_music(self, play_filename, mode=0):
        if mode == 0:
            current_playlist.append(play_filename)
            current_playing = pygame.mixer.Sound(play_filename)
            current_playing.set_volume(self.current_volume_percentage / 100)
            current_play_media.append(current_playing)
            self.current_playing_object = current_playing
            self.current_playing_filename = play_filename
            pygame.mixer.fadeout(200)
            current_playing.play()
            self.is_playing = True
            self.waiting = False
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
        self.player_queue.config(activestyle='none')
        self.player_queue_bar_v.configure(command=self.player_queue.yview)
        self.player_queue_bar_h.configure(command=self.player_queue.xview)
        self.player_queue.place(x=370, y=50, width=400, height=200)
        self.player_queue.bind('<Double-1>', self.choose_queue)
        self.player_queue.bind('<Button-3>', self.delete_queue)

    def add_to_queue(self, mode=0, play_filename=None):
        if mode == 0:
            play_filename = filedialog.askopenfilename(
                title="Choose the files you want to add to queue",
                filetypes=(("all files", "*"), ))
        if play_filename:
            if play_filename not in current_playlist and play_filename not in current_queue_list:
                file_type = os.path.splitext(play_filename)[1][1:]
                if file_type.lower() in supported_audio_file_formats:
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
            self.pause_button.configure(text=self.language_dict['Repause'])
            self.is_pause = True

    def unpause_playing(self):
        if self.is_pause:
            pygame.mixer.unpause()
            self.pause_button.configure(text=self.language_dict['Pause'])
            self.is_pause = False

    def stop_playing(self):
        if self.is_playing:
            pygame.mixer.stop()
            self.is_playing = False
            self.stop_button.configure(text=self.language_dict['Play'])
        else:
            if self.current_playing_object:
                pygame.mixer.fadeout(200)
                self.current_playing_object.play()
                self.stop_button.configure(text=self.language_dict['Stop'])
                self.is_playing = True

    def play_next(self):
        if self.waiting:
            return
        if current_queue_list:
            if not self.current_playing_filename or (
                    self.current_playing_filename not in current_queue_list):
                current_ind = self.current_playing_ind - 1 if self.current_playing_ind is not None else -1
            else:
                current_ind = current_queue_list.index(
                    self.current_playing_filename)
            if current_ind >= len(current_queue_list) - 1:
                current_ind = -1
            next_filename = current_queue_list[current_ind + 1]
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(current_ind + 1)
            self.focus_set()
            self.play_music(next_filename)

    def play_previous(self):
        if self.waiting:
            return
        if current_queue_list:
            if not self.current_playing_filename or (
                    self.current_playing_filename not in current_queue_list):
                current_ind = self.current_playing_ind if self.current_playing_ind is not None else 0
            else:
                current_ind = current_queue_list.index(
                    self.current_playing_filename)
            if current_ind <= 0:
                current_ind = len(current_queue_list)
            next_filename = current_queue_list[current_ind - 1]
            self.player_queue.selection_clear(0, END)
            self.player_queue.selection_set(current_ind - 1)
            self.play_music(next_filename)

    def multiple_choose_files(self):
        play_filenames = filedialog.askopenfilenames(
            title="Choose the files you want to play",
            filetypes=(("all files", "*"), ))
        if play_filenames:
            play_filename = play_filenames[0]
            for each in play_filenames:
                self.add_to_queue(mode=1, play_filename=each)

    def random_playing(self):
        if self.waiting:
            return
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

    def change_playing_mode(self):
        if self.playing_mode == 0:
            self.playing_mode = 1
        elif self.playing_mode == 1:
            self.playing_mode = 2
        elif self.playing_mode == 2:
            self.playing_mode = 3
        elif self.playing_mode == 3:
            self.playing_mode = 0
        self.playing_mode_button.configure(
            text=self.language_dict['Play mode'][self.playing_mode])

    def change_move_volume_bar(self, e):
        self.current_volume_percentage = round(float(e) * 2) / 2
        self.slider.set(
            f'{self.language_dict["Volume"]}: {self.current_volume_percentage}%'
        )
        if self.current_playing_object:
            self.current_playing_object.set_volume(
                self.current_volume_percentage / 100)

    def move_volume_bar_set_value(self, change):
        if self.current_volume_percentage + change > 100:
            self.current_volume_percentage = 100
        elif self.current_volume_percentage + change < 0:
            self.current_volume_percentage = 0
        else:
            self.current_volume_percentage += change
        self.slider.set(
            f'{self.language_dict["Volume"]}: {self.current_volume_percentage}%'
        )
        self.set_move_volume_bar.set(self.current_volume_percentage)
        if self.current_playing_object:
            self.current_playing_object.set_volume(
                self.current_volume_percentage / 100)


root = Root()
root.focus_force()
root.mainloop()
