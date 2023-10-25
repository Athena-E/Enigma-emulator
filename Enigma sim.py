import pygame as pg
import math
import sys
import myEnigma as eni
import time


pg.init()

white = (255, 255, 255)
gray = (100, 100, 100)
d_gray = (50, 50, 50)
red = (200, 0, 0)
black = (0, 0, 0)
yellow = (245, 183, 49)



def pointInCircle(mouse_x, mouse_y, circle_x, circle_y, radius):
    if math.sqrt((circle_x - mouse_x)**2 + (circle_y - mouse_y)**2) <= radius:
        return True
    return False

def pointInSquare(mouse_x, mouse_y, square_x, square_y, length_x, length_y):
    if mouse_x > square_x and mouse_x < square_x + length_x:
        if mouse_y > square_y and mouse_y < square_y + length_y:
            return True
    return False


class letter_key:

    def __init__(self, text, position, radius):
        self.position = position
        self.radius = radius

        letter_font = pg.font.SysFont("Corbel", int(radius * 1.5))
        self.text = letter_font.render(f"{text}", True, white)
        self.letter = text

    def clicked(self, events):
        mousePos = pg.mouse.get_pos()
        if pointInCircle(mousePos[0], mousePos[1], self.position[0], self.position[1], self.radius):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False

    def render(self, display, fill_color, outline_color):
        text_coords = self.text.get_rect()
        text_coords.center = self.position

        pg.draw.circle(display, outline_color, self.position, self.radius+2)
        pg.draw.circle(display, fill_color, self.position, self.radius)
        display.blit(self.text, (text_coords))

    def hover(self, display):
        mousePos = pg.mouse.get_pos()
        if pointInCircle(mousePos[0], mousePos[1], self.position[0], self.position[1], self.radius):
            self.render(display, black, white)
            #pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            self.render(display, black, gray)
            #pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


class rotor_window:

    def __init__(self, position, length):
        self.length = length
        self.position = position
        self.start_letter = "A"
        letter_font = pg.font.SysFont("Corbel", int(self.length))
        self.text = letter_font.render(f"{self.start_letter}", True, black)
        
        self.ring_setting = "A"

    def render(self, display):
        rect = pg.Rect(0, 0, self.length, self.length)
        rect.center = self.position
        text_coords = self.text.get_rect()
        text_coords.center = rect.center
        pg.draw.rect(display, white, rect)
        display.blit(self.text, (text_coords))

    def clicked(self, events):
        mousePos = pg.mouse.get_pos()
        left_x = self.position[0]-self.length/2
        top_y = self.position[1]-self.length/2
        if pointInSquare(mousePos[0], mousePos[1], left_x, top_y, self.length, self.length):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False


class rotor_slot:

    def __init__(self, position, length):
        self.current_rotor = 1
        self.length = length
        self.position = position
        letter_font = pg.font.SysFont("Corbel", int(self.length/6))
        self.text = letter_font.render(f"{self.current_rotor}", True, white)

    def render(self, display):
        rect = pg.Rect(0, 0, self.length/6, self.length)
        rect.center = self.position
        text_coords = self.text.get_rect()
        text_coords.center = rect.center
        pg.draw.rect(display, gray, rect)
        display.blit(self.text, (text_coords))


    def clicked(self, events):
        mousePos = pg.mouse.get_pos()
        left_x = self.position[0]-self.length/12
        top_y = self.position[1]-self.length/2
        if pointInSquare(mousePos[0], mousePos[1], left_x, top_y, self.length/6, self.length):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False


class ring_setting_window:

    def __init__(self, position, length):
        self.length = length
        self.position = position
        self.current_setting = "A"
        letter_font = pg.font.SysFont("Corbel", int(self.length/6))
        self.text = letter_font.render(f"{self.current_setting}", True, black)

    def render(self, display):
        rect = pg.Rect(0, 0, self.length/6, self.length/6)
        rect.center = self.position
        text_coords = self.text.get_rect()
        text_coords.center = rect.center
        pg.draw.rect(display, white, rect)
        display.blit(self.text, (text_coords))

    def clicked(self, events):
        mousePos = pg.mouse.get_pos()
        left_x = self.position[0]-self.length/2
        top_y = self.position[1]-self.length/2
        if pointInSquare(mousePos[0], mousePos[1], left_x, top_y, self.length, self.length):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False


class plugboard_button_class:

    def __init__(self, position, length):
        self.position = position
        self.length_x = length
        self.length_y = height/12
        self.show = False

    def render(self, display):
        rect = pg.Rect(self.position[0]-self.length_x/2, self.position[1], self.length_x, self.length_y)
        pg.draw.rect(display, gray, rect)

    def clicked(self, events):
        mousePos = pg.mouse.get_pos()
        if pointInSquare(mousePos[0], mousePos[1], self.position[0]-self.length_x/2, self.position[1], self.length_x, self.length_y):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False



def shift_letter(letter):
    asc_pos = ord(letter) + 1
    if asc_pos > 90:
        diff = asc_pos - 90
        asc_pos = 64+diff

    return chr(asc_pos)


def update_all_windows():
    r1_window.start_letter = eni.r1.offset
    letter_font = pg.font.SysFont("Corbel", int(r1_window.length))
    r1_window.text = letter_font.render(f"{r1_window.start_letter}", True, black)
    r1_window.render(screen)

    r2_window.start_letter = eni.r2.offset
    letter_font = pg.font.SysFont("Corbel", int(r2_window.length))
    r2_window.text = letter_font.render(f"{r2_window.start_letter}", True, black)
    r2_window.render(screen)

    r3_window.start_letter = eni.r3.offset
    letter_font = pg.font.SysFont("Corbel", int(r3_window.length))
    r3_window.text = letter_font.render(f"{r3_window.start_letter}", True, black)
    r3_window.render(screen)    

def check_line(letter_string, output_letter):
    flag = False
    if output_letter in letter_string:
        flag = True
    return flag

def light_up(output_letter):
    on_top = check_line(top_line, output_letter)
    on_mid = check_line(mid_line, output_letter)
    if on_top == True:
        letter_pos = top_line.find(output_letter)
        light = top_lights[letter_pos]
    elif on_mid == True:
        letter_pos = mid_line.find(output_letter)
        light = mid_lights[letter_pos]
    else:
        letter_pos = bottom_line.find(output_letter)
        light = bottom_lights[letter_pos]
    
    light.render(screen, yellow, black)


screen = pg.display.set_mode((1000, 600), pg.RESIZABLE)
pg.display.set_caption("Engima")


width = screen.get_width()
height = screen.get_height()
radius = int(width/50)
length = width/25



top_line = "QWERTZUIO"
mid_line = "ASDFGHJK"
bottom_line = "PYXCVBNML"



top_lights = [letter_key(top_line[4-(i//3)], ((width/2 - radius*i), (height/3)), radius)
for i in range(12, -15, -3)]

mid_lights = [letter_key(mid_line[3-(i//3)], ((width/2 - radius*1.5)-radius*i, (height/3)+radius*2.5), radius)
for i in range(9, -15, -3)]

bottom_lights = [letter_key(bottom_line[4-(i//3)], ((width/2 - radius*i), (height/3)+radius*5), radius)
for i in range(12, -15, -3)]


top_keys = [letter_key(top_line[4-(i//3)], ((width/2 - radius*i), (height*2/3)), radius)
for i in range(12, -15, -3)]

mid_keys = [letter_key(mid_line[3-(i//3)], ((width/2 - radius*1.5)-radius*i, (height*2/3)+radius*2.5), radius)
for i in range(9, -15, -3)]

bottom_keys = [letter_key(bottom_line[4-(i//3)], ((width/2 - radius*i), (height*2/3)+radius*5), radius)
for i in range(12, -15, -3)]


r1_window = rotor_window((width/2-length*2, height*(1/3)-length*2.5), length)
r2_window = rotor_window((width/2, height*(1/3)-length*2.5), length)
r3_window = rotor_window((width/2+length*2, height*(1/3)-length*2.5), length)


r1_slot = rotor_slot((width/2 - length*2.9, height*(1/3)-length*2.5), length*2)
r2_slot = rotor_slot((width/2 - 0.9*length, height*(1/3)-length*2.5), length*2)
r3_slot = rotor_slot((width/2+length*1.1, height*(1/3)-length*2.5), length*2)


r1_setting_window = ring_setting_window((width/2 - length*2.9, height*(1/3)-length*4), length*2)
r2_setting_window = ring_setting_window((width/2 - 0.9*length, height*(1/3)-length*4), length*2)
r3_setting_window = ring_setting_window((width/2+length*1.1, height*(1/3)-length*4), length*2)

plugboard_button = plugboard_button_class((width/2, height-height/12), width/6)


# assume ringstellung is "A"
eni.r1 = eni.Rotor(r1_window.start_letter, r1_window.ring_setting, eni.rotor_wirings[r1_slot.current_rotor])
eni.r2 = eni.Rotor(r2_window.start_letter, r2_window.ring_setting, eni.rotor_wirings[r2_slot.current_rotor])
eni.r3 = eni.Rotor(r3_window.start_letter, r3_window.ring_setting, eni.rotor_wirings[r3_slot.current_rotor])


eni.rotor_order = [r1_slot.current_rotor, r2_slot.current_rotor, r3_slot.current_rotor]


output_letter = False


while True:

    events = pg.event.get()
    for event in events:

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            pass

        if event.type == pg.VIDEORESIZE:
            screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            
            # width = screen.get_width()
            # height = screen.get_height()
            # radius = width/50
            # length = width/25

            # top_lights = [letter_key(top_line[4-(i//3)], ((width/2 - radius*i), (height*1/3)), radius)
            # for i in range(12, -15, -3)]
            # mid_lights = [letter_key(mid_line[3-(i//3)], ((width/2 - radius*1.5)-radius*i, (height/3)+radius*2.5), radius)
            # for i in range(9, -15, -3)]
            # bottom_lights = [letter_key(bottom_line[4-(i//3)], ((width/2 - radius*i), (height/3)+radius*5), radius)
            # for i in range(12, -15, -3)]

            # top_keys = [letter_key(top_line[4-(i//3)], ((width/2 - radius*i), (height*2/3)), radius)
            # for i in range(12, -15, -3)]
            # mid_keys = [letter_key(mid_line[3-(i//3)], ((width/2 - radius*1.5)-radius*i, (height*2/3)+radius*2.5), radius)
            # for i in range(9, -15, -3)]
            # bottom_keys = [letter_key(bottom_line[4-(i//3)], ((width/2 - radius*i), (height*2/3)+radius*5), radius)
            # for i in range(12, -15, -3)]

            # r1_window = rotor_window((width/2-length*2, height*(1/3)-length*2.5), length)
            # r2_window = rotor_window((width/2, height*(1/3)-length*2.5), length)
            # r3_window = rotor_window((width/2+length*2, height*(1/3)-length*2.5), length)

            # r1_slot = rotor_slot((width/2 - length*2.9, height*(1/3)-length*2.5), length*2)
            # r2_slot = rotor_slot((width/2 - 0.9*length, height*(1/3)-length*2.5), length*2)
            # r3_slot = rotor_slot((width/2+length*1.1, height*(1/3)-length*2.5), length*2)

            # r1_setting_window = ring_setting_window((width/2 - length*2.9, height*(1/3)-length*4), length*2)
            # r2_setting_window = ring_setting_window((width/2 - 0.9*length, height*(1/3)-length*4), length*2)
            # r3_setting_window = ring_setting_window((width/2+length*1.1, height*(1/3)-length*4), length*2)

            # plugboard_button = plugboard_button_class((width/2, height-height/12), width/6)


    screen.fill(black)
    

    r1_window.render(screen)
    r2_window.render(screen)
    r3_window.render(screen)

    r1_slot.render(screen)
    r2_slot.render(screen)
    r3_slot.render(screen)

    r1_setting_window.render(screen)
    r2_setting_window.render(screen)
    r3_setting_window.render(screen)


    plugboard_button.render(screen)


    for light in top_lights:
        light.render(screen, d_gray, black)
    for light in mid_lights:
        light.render(screen, d_gray, black)
    for light in bottom_lights:
        light.render(screen, d_gray, black)

    for key in top_keys:
        key.hover(screen)
        if key.clicked(events):
            eni.turn_rotors(eni.rotor_order, eni.rotor_notches, eni.r3, eni.r2, eni.r1)
            eni.r3.update()
            update_all_windows()
            input_letter = key.letter
            output_letter = eni.rotor_encrypt(eni.r1, eni.r2, eni.r3, eni.reflector, input_letter, eni.plugboard_dict)
            print(output_letter)
            light_up(output_letter)

    for key in mid_keys:
        key.hover(screen)
        if key.clicked(events):
            eni.turn_rotors(eni.rotor_order, eni.rotor_notches, eni.r3, eni.r2, eni.r1)
            eni.r3.update()
            update_all_windows()
            input_letter = key.letter
            output_letter = eni.rotor_encrypt(eni.r1, eni.r2, eni.r3, eni.reflector, input_letter, eni.plugboard_dict)
            print(output_letter)
            light_up(output_letter)

    for key in bottom_keys:
        key.hover(screen)
        if key.clicked(events):
            eni.turn_rotors(eni.rotor_order, eni.rotor_notches, eni.r3, eni.r2, eni.r1)
            eni.r3.update()
            update_all_windows()
            input_letter = key.letter
            output_letter = eni.rotor_encrypt(eni.r1, eni.r2, eni.r3, eni.reflector, input_letter, eni.plugboard_dict)
            print(output_letter)
            light_up(output_letter)

    if output_letter != False:
        light_up(output_letter)

    if r1_window.clicked(events):
        eni.r1.update()
        next_letter = eni.r1.offset
        r1_window.start_letter = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r1_window.length))
        r1_window.text = letter_font.render(f"{r1_window.start_letter}", True, black)
        r1_window.render(screen)

    if r2_window.clicked(events):
        eni.r2.update()
        next_letter = eni.r2.offset
        r2_window.start_letter = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r2_window.length))
        r2_window.text = letter_font.render(f"{r2_window.start_letter}", True, black)
        r2_window.render(screen)

    if r3_window.clicked(events):
        eni.r3.update()
        next_letter = eni.r3.offset
        r3_window.start_letter = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r3_window.length))
        r3_window.text = letter_font.render(f"{r3_window.start_letter}", True, black)
        r3_window.render(screen)


    if r1_slot.clicked(events):
        if r1_slot.current_rotor == 5:
            r1_slot.current_rotor = 1
        else:
            r1_slot.current_rotor += 1
        letter_font = pg.font.SysFont("Corbel", int(r1_slot.length/5))
        r1_slot.text = letter_font.render(f"{r1_slot.current_rotor}", True, white)
        r1_slot.render(screen)

        eni.r1.wiring = eni.rotor_wirings[r1_slot.current_rotor]
        eni.r1.new_wiring = eni.r1.get_new_wiring()
        eni.rotor_order[0] = r1_slot.current_rotor

    if r2_slot.clicked(events):
        if r2_slot.current_rotor == 5:
            r2_slot.current_rotor = 1
        else:
            r2_slot.current_rotor += 1
        letter_font = pg.font.SysFont("Corbel", int(r2_slot.length/5))
        r2_slot.text = letter_font.render(f"{r2_slot.current_rotor}", True, white)

        eni.r2.wiring = eni.rotor_wirings[r2_slot.current_rotor]
        eni.r2.new_wiring = eni.r2.get_new_wiring()
        eni.rotor_order[1] = r2_slot.current_rotor

    if r3_slot.clicked(events):
        if r3_slot.current_rotor == 5:
            r3_slot.current_rotor = 1
        else:
            r3_slot.current_rotor += 1
        letter_font = pg.font.SysFont("Corbel", int(r3_slot.length/5))
        r3_slot.text = letter_font.render(f"{r3_slot.current_rotor}", True, white)
        r3_slot.render(screen)

        eni.r3.wiring = eni.rotor_wirings[r3_slot.current_rotor]
        eni.r3.new_wiring = eni.r3.get_new_wiring()
        eni.rotor_order[2] = r3_slot.current_rotor

    
    if r1_setting_window.clicked(events):
        next_letter = shift_letter(r1_setting_window.current_setting)
        r1_setting_window.current_setting = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r1_setting_window.length/6))
        r1_setting_window.text = letter_font.render(f"{r1_setting_window.current_setting}", True, black)
        r1_setting_window.render(screen)

        eni.r1.ring_setting = next_letter
        eni.r1.new_wiring = eni.r1.get_new_wiring()

    if r2_setting_window.clicked(events):
        next_letter = shift_letter(r2_setting_window.current_setting)
        r2_setting_window.current_setting = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r2_setting_window.length/6))
        r2_setting_window.text = letter_font.render(f"{r2_setting_window.current_setting}", True, black)
        r2_setting_window.render(screen)

        eni.r2.ring_setting = next_letter
        eni.r2.new_wiring = eni.r2.get_new_wiring

    if r3_setting_window.clicked(events):
        next_letter = shift_letter(r3_setting_window.current_setting)
        r3_setting_window.current_setting = next_letter
        letter_font = pg.font.SysFont("Corbel", int(r3_setting_window.length/6))
        r3_setting_window.text = letter_font.render(f"{r3_setting_window.current_setting}", True, black)
        r3_setting_window.render(screen)

        eni.r3.ring_setting = next_letter
        eni.r3.new_wiring = eni.r3.get_new_wiring()


    if plugboard_button.clicked(events):
        screen.fill(black)
        pg.display.update()
        print(plugboard_button.show)
        if plugboard_button.show == False:
            screen.fill(black)
            pg.display.flip()
        else:
            print("hello")
        plugboard_button.show = not plugboard_button.show




    pg.display.flip()
