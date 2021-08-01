class Button:
    def __init__(self, img, x, y):
        self.img = pyglet.resource.image(img)
        self.img.width /= button_resize_num
        self.img.height /= button_resize_num
        self.x = x
        self.y = y

    def MakeButton(self):
        return pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self):
        range_x, range_y = self.get_range()
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]


def choose_file_func():
    root = Tk()
    root.withdraw()
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
        file_type = os.path.splitext(play_filename)[1][1:]
        if file_type in ['mp3', 'ogg', 'wav']:
            current_playing = pyglet.media.load(play_filename, streaming=False)
            player.queue(current_playing)
            if current_playlist:
                player.next_source()
            player.play()
            current_playlist.append(current_playing)
            is_playing = True
    root.destroy()


with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())
play_filename = None
is_playing = False
player = pyglet.media.Player()
current_playlist = []
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
choose_file = Button(choose_file_image, *button_places[0])
choose_file_button = choose_file.MakeButton()


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos = x, y


@window.event
def on_mouse_press(x, y, button, modifiers):
    global is_playing
    if choose_file.inside() & button & mouse.LEFT:
        if is_playing:
            player.pause()
            is_playing = False
        player_thread = Thread(target=choose_file_func)
        player_thread.setDaemon(True)
        player_thread.start()


@window.event
def on_draw():
    window.clear()
    background.blit(backgrond_place_x, backgrond_place_y)
    choose_file_button.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / fps)
pyglet.app.run()
