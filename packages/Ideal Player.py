class Button:
    def __init__(self,
                 img,
                 x,
                 y,
                 command=None,
                 click='left',
                 button_resize_num=3):
        self.img = pyglet.resource.image(img)
        self.img.width /= button_resize_num
        self.img.height /= button_resize_num
        self.x = x
        self.y = y
        self.button = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        self.command = command
        if click == 'left':
            self.click = mouse.LEFT
        elif click == 'right':
            self.click = mouse.RIGHT
        elif click == 'middle':
            self.click = mouse.MIDDLE
        else:
            self.click = mouse.LEFT
        self.bindings = {}

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self):
        range_x, range_y = self.get_range()
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]

    def draw(self):
        self.button.draw()

    def check(self, button):
        if self.command:
            if self.inside() and button == self.click:
                self.command()
        if self.bindings:
            for each in self.bindings:
                if self.inside() and button == each:
                    self.bindings[each]()

    def bind(self, click, command):
        if click == 'left':
            click = mouse.LEFT
        elif click == 'right':
            click = mouse.RIGHT
        elif click == 'middle':
            click = mouse.MIDDLE
        else:
            click = mouse.LEFT
        self.bindings[click] = command


def choose_file_button_func():
    global last_place
    global play_filename
    global is_playing
    play_filename = filedialog.askopenfilename(initialdir=last_place,
                                               title="选择你想播放的文件",
                                               filetype=(("all files",
                                                          "*.*"), ))
    if play_filename:
        memory = play_filename[:play_filename.rindex('/') + 1]
        with open('browse memory.txt', 'w', encoding='utf-8-sig') as f:
            f.write(memory)
        last_place = memory
        play_music()


def play_music():
    global is_playing
    global current_playing_object
    if play_filename in current_playlist:
        ind = current_playlist.index(play_filename)
        if current_playing_object:
            current_playing_object.pause()
        current_playing = pyglet.media.load(play_filename,
                                            streaming=False).play()
        current_play_media[ind] = current_playing
        current_playing_object = current_playing
        current_playing_label.text = f'当前正在播放: {play_filename}'
    else:
        file_type = os.path.splitext(play_filename)[1][1:]
        if file_type in supported_audio_file_formats:
            current_playing = pyglet.media.load(play_filename,
                                                streaming=False).play()
            current_playlist.append(play_filename)
            current_play_media.append(current_playing)
            if current_playing_object:
                current_playing_object.pause()
            current_playing_object = current_playing
            current_playing_label.text = f'当前正在播放: {play_filename}'
    is_playing = True


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
root = Tk()
root.withdraw()

play_filename = None
is_playing = False
current_playing_object = None
#player = pyglet.media.Player()
current_playlist = []
current_play_media = []
display_player_queue_open = False
try:
    with open('browse memory.txt', encoding='utf-8-sig') as f:
        last_place = f.read()
except:
    last_place = "./"

mouse_pos = 0, 0
screen_width, screen_height = screen_size
pressed = keyboard.is_pressed
pygame.mixer.init(frequency, size, channel, buffer)
pyglet.resource.path = [abs_path]
for each in ['background_image']:
    each_value = eval(each)
    each_path = os.path.dirname(each_value)
    if each_path:
        if each_path == 'resources':
            exec(f"{each} = '{each_value}'")
        else:
            pyglet.resource.path.append(each_path.replace('/', '\\'))
            exec(f"{each} = '{os.path.basename(each_value)}'")
pyglet.resource.reindex()
if icon_name:
    icon = pyglet.resource.image(icon_name)
background = pyglet.resource.image(background_image)
if not background_size:
    ratio_background = screen_width / background.width
    background.width = screen_width
    background.height *= ratio_background
else:
    background.width, background.height = background_size

batch = pyglet.graphics.Batch()
pyglet.options['search_local_libs'] = True
window = pyglet.window.Window(*screen_size, caption='Ideal Player')
window.set_location(200, 150)
if icon_name:
    window.set_icon(icon)
choose_file_button = Button(choose_file_image,
                            *button_places[0],
                            choose_file_button_func,
                            button_resize_num=2)
open_player_queue_buttoon = Button(open_player_queue_image,
                                   *button_places[1],
                                   display_player_queue,
                                   button_resize_num=2)

current_playing_label = pyglet.text.Label('当前正在播放: ',
                                          font_name=fonts,
                                          font_size=fonts_size,
                                          bold=bold,
                                          x=label1_place[0],
                                          y=label1_place[1],
                                          color=message_color,
                                          anchor_x=label_anchor_x,
                                          anchor_y=label_anchor_y,
                                          multiline=True,
                                          width=1100)


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos = x, y


@window.event
def on_mouse_press(x, y, button, modifiers):
    choose_file_button.check(button)
    open_player_queue_buttoon.check(button)


@window.event
def on_draw():
    window.clear()
    background.blit(backgrond_place_x, backgrond_place_y)
    choose_file_button.draw()
    open_player_queue_buttoon.draw()
    current_playing_label.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / fps)

pyglet.app.run()
