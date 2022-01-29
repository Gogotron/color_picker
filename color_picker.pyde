from keyboard import Keyboard
k = Keyboard()

mode = 0
third = 0
show_third = False


def setup():
    size(256*2,256*2);
    loadPixels()
    update()


def draw():
    if mouseX!=pmouseX or mouseY!=pmouseY:
        update_keyboard()
    if show_third:
        textAlign(CENTER)
        text(third,width/2,height/2)


def order_from_mode(a, b, c):
    if mode == 0:
        return a, b, c
    if mode == 1:
        return a, c, b
    if mode == 2:
        return c, a, b
    if mode == 3:
        return b, a, c
    if mode == 4:
        return b, c, a
    if mode == 5:
        return c, b, a
    raise Exception


def keyReleased():
    changes = {
        "i":50, "u":-50,
        "k":10, "j":-10,
        "m": 1, "n":-1
    }
    if key == " ":
        global mode
        mode = (mode+1) % 6
        update()
    elif key in changes:
        global third
        change = changes[key]
        if change>0 and third!=255 or change<0 and third!=0:
            third += change
            third = max(0,min(third,255))
            update()
    elif key == TAB:
        global show_third
        show_third = not show_third
        update_background()


def update_background():
    for i in range(256*2):
        for j in range(256*2):
            pixels[i+j*256*2] = color(*order_from_mode(i/2, j/2, third))
    updatePixels()


def update_keyboard():
    k.set_color(order_from_mode(mouseX/2, mouseY/2, third))
 

def update():
    update_background()
    update_keyboard()
