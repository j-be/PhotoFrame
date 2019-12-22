import sys
import os
import signal
from random import shuffle

if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk


PHOTO_DIR = os.path.join(os.getenv('HOME'), 'Pictures')
DELAY = 5000


class Photos(object):
    photos = []
    i = -1

    def reload(self, _=None, __=None):
        print("Reloading photos")
        self.i = -1
        self.photos = []
        for (dirpath, dirnames, filenames) in os.walk(PHOTO_DIR):
            for f in filenames:
                if f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.png') or f.endswith('.PNG'):
                    self.photos += [os.path.join(PHOTO_DIR, f)]
            break
        shuffle(self.photos)

    def next_photo(self):
        self.i = (self.i + 1) % len(self.photos)
        return self.photos[self.i]


class TkState(object):
    canvas = None
    current_photo = None
    w = 0
    h = 0

    def get_ratio(self, img_width, img_height):
        return min(float(self.w) / img_width, float(self.h) / img_height)

    def new_canvas(self, root):
        self.canvas = tkinter.Canvas(root, width=tk_state.w, height=tk_state.h)
        self.canvas.pack()
        self.canvas.configure(background='black', highlightbackground='black')


tk_state = TkState()
photos = Photos()
photos.reload()


def tick():
    # Open image and read geometry
    im = Image.open(photos.next_photo())
    img_width, img_height = im.size

    # Scale down if needed
    if img_width > tk_state.w or img_height > tk_state.h:
        ratio = tk_state.get_ratio(img_width, img_height)
        img_width = int(img_width * ratio)
        img_height = int(img_height * ratio)
        im = im.resize((img_width, img_height), Image.ANTIALIAS)

    # Display the image
    tk_state.current_photo = ImageTk.PhotoImage(im)
    tk_state.canvas.create_image(tk_state.w / 2, tk_state.h / 2, image=tk_state.current_photo)

    tk_state.canvas.after(DELAY, tick)


def setup_tk():
    root = tkinter.Tk()
    tk_state.w, tk_state.h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (tk_state.w, tk_state.h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

    tk_state.new_canvas(root)
    tk_state.canvas.after(1, tick)

    root.mainloop()


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, photos.reload)
    setup_tk()
