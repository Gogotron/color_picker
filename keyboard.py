from time import sleep
from time import time
KEYBOARD_BRIGHTNESS_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_brightness"
KEYBOARD_COLOR_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_color"
KEYBOARD_STATE_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_state"


def get_state():
    with open(KEYBOARD_STATE_FILE,'r') as f:
        state = int(f.read())
    return state


def set_state(state):
    with open(KEYBOARD_STATE_FILE,'w') as f:
        f.write(str(state))


def get_color():
    with open(KEYBOARD_COLOR_FILE,'r') as f:
        color = f.read().split(" ")[0]
    return color


def set_color(color):
    with open(KEYBOARD_COLOR_FILE,'w') as f:
        f.write(" ".join((color,)*3))


def get_brightness():
    with open(KEYBOARD_BRIGHTNESS_FILE,'r') as f:
        n = int(f.read())
    return n


def set_brightness(n):
    with open(KEYBOARD_BRIGHTNESS_FILE,'w') as f:
        f.write(str(n))


def toggle():
    state = get_state()
    set_state((state+1)%2)


def int_to_hex(n):
    return "%02X" % n


def col_to_rgb(col):
    if isinstance(col, str):
        rgb = map(lambda x: int(x, 16), map(''.join, zip(*[iter(col)]*2)))
    else:
        rgb = map(round, col)
    return tuple(rgb)


class Keyboard:
    def __init__(self):
        self.set_color((0,0,0))
        set_brightness(9)

    def fade_to(self, col, dur=2, steps=10):
        r_, g_, b_ = col_to_rgb(col)
        r, g, b = self.rgb
        start = time()
        for i in range(steps):
            t = (i+1)/steps
            self.set_color((
                (1-t)*r + t*r_,
                (1-t)*g + t*g_,
                (1-t)*b + t*b_,
            ))
            sleep(max(t*dur-(time()-start),0))

    def set_color(self, col):
        self.set_color_int(col_to_rgb(col))

    def set_color_int(self, rgb):
        set_color("".join(map(int_to_hex, rgb)))
        self.rgb = rgb



if __name__ == "__main__":
    k = Keyboard()
    while True:
        k.fade_to("D70270", 10, 100)
        sleep(60*3)
        k.fade_to("7835B6", 20, 100)
        sleep(60*3)
        k.fade_to("0038A4", 20, 100)
        sleep(60*3)
        k.fade_to("000000", 10, 100)
        sleep(5)
