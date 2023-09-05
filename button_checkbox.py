import pygame
from pygame import Rect
from button import KeyboardButton

PAD=10
FPS=60
BLACK=0,0,0
GRAY=190,190,190
LINEN=250,240,230
WHITE=255,255,255
KEYBOARD_FONT=(None,30)
KEYBOARD_BUTTON_SIZE=40,40
KEYBOARD_BG_COLOR=WHITE
KEYBOARD_BG_COLOR_CLICKED=GRAY
KEYBOARD_TEXT_COLOR=BLACK

class KeyboardCheckbox(KeyboardButton):
    def __init__(self,**kwargs):
        KeyboardButton.__init__(self,**kwargs)
        self.locked=False
        self.render_image_locked()

    def render_image_locked(self):
        check_img=pygame.image.load('check.png').convert_alpha()
        check_img_1=min(*self.size)//3
        check_img_pos=self.size[0]-check_img_1,0
        check_img=pygame.transform.smoothscale(check_img,(check_img_1,check_img_1))
        self.image_locked=self.image_org.copy()
        self.image_locked.blit(check_img,check_img_pos)

    def update(self):
        if self.clicked:
            self.image=self.image_locked
        else:
            if self.locked:
                self.image=self.image_locked
            else:
                self.image=self.image_org
class Keyboard():
    keyboard_input=[]
    keyboard_checkbox=[]
    output=False

class KeyboardCheckboxGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.info=Keyboard()

    def update(self,*args):
        mouse_x,mouse_y,mouse_clicked=args
        for s in self.sprites():
            if s.rect.collidepoint(mouse_x,mouse_y):
                if mouse_clicked==True:
                    s.clicked=True
                elif mouse_clicked==False:
                    if s.clicked:
                        s.clicked=False
                        s.locked=not s.locked
                        if s.locked:
                            self.add_checkbox_value(s.value)
                        else:
                            self.delete_checkbox_value(s.value)
            else:
                if mouse_clicked==False:
                    s.clicked=False
            s.update()

    def get_checkbox_value(self):
        return self.info.keyboard_checkbox

    def add_checkbox_value(self,value):
        self.info.keyboard_checkbox.append(value)

    def delete_checkbox_value(self,value):
        self.info.keyboard_checkbox.remove(value)

    def empty_keyboard(self):
        self.info.keyboard_checkbox=[]
        self.info.keyboard_input=[]
        self.info.output=False
