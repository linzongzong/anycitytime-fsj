import pygame
from pygame import Rect
pygame.init() 
SCREEN_SIZE = 800,800 # 屏幕大小
 
# 一些常用颜色
WHITE = 255, 255, 255
GRAY = 190, 190, 190
BLACK = 0, 0, 0
LINEN = 250, 240, 230
DARKSLATEGRAY = 47, 79, 79
 
PAD = 10 # 各物块，按钮之间的 padding
FPS = 60 # pygame显示的fps
 
#DISPLAY_FONT = (None, 40) # 显示打印文字的字体
display_font=pygame.font.SysFont(['方正舒体'],20)
DISPLAY_BG_COLOR = LINEN  # 显示打印文字区域的背景色
DISPLAY_TEXT_COLOR = DARKSLATEGRAY # 打印文字的颜色
 
KEYBOARD_FONT = (None, 30) # 按钮字体
KEYBOARD_FONT = (None, 30) # 按钮字体
KEYBOARD_FONT = (None, 30) # 按钮字体
KEYBOARD_FONT = (None, 30) # 按钮字体
KEYBOARD_BUTTON_SIZE = 40, 100 # 按钮大小
KEYBOARD_BG_COLOR = WHITE # 按钮背景色
KEYBOARD_BG_COLOR_CLICKED = GRAY # 按钮被选中时的背景色
KEYBOARD_TEXT_COLOR = BLACK # 按钮文字颜色

class KeyboardButton(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        # 创建按钮时需要有多个参数
        # size ：按钮的大小
        # value ：按钮的显示值
        # id : 按钮的id
        pygame.sprite.Sprite.__init__(self)
        self.size = kwargs.get('size')
        self.value = kwargs.get('value')
        if kwargs.get('id'):
            self.id = kwargs.get('id')
        else :
            # 若没有id，则我们默认self.value为按钮的self.id
            self.id = self.value
        self.clicked = False # 按钮是否被选中
        self.render_image() # 渲染按钮显示图像
 
    def render_image(self):
        # 主要渲染两个图像：
        # self.image_org为原始图像
        # self.image_clicked为选中时的图像
        w, h = display_font.size(self.value)
        # 初始化Surface
        self.rect = Rect(0, 0, *self.size)
        self.image_org = pygame.Surface(self.size).convert()
        self.image_org.fill(KEYBOARD_BG_COLOR)
        # 居中渲染self.value
        self.image_org.blit(display_font.render(self.value, True, KEYBOARD_TEXT_COLOR),
                            ((self.size[0] - w) // 2, (self.size[1] - h) // 2))
        self.image_clicked = self.image_org.copy()
        self.image_clicked.fill(KEYBOARD_BG_COLOR_CLICKED)
        self.image_clicked.blit(display_font.render(self.value, True, KEYBOARD_TEXT_COLOR),
                                ((self.size[0] - w) // 2, (self.size[1] - h) // 2))
        self.image = self.image_org
 
    def update(self):
        # 根据该按钮是否被选中决定显示图像
        if self.clicked:
            self.image = self.image_clicked
        else:
            self.image = self.image_org

class Keyboard():
    keyboard_input = [] # 存放input
    output = False # 是否最终输出

class KeyboardButtonGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.info=Keyboard()

    def update(self, *args):
        mouse_x, mouse_y, mouse_clicked = args
        for s in self.sprites():
            if s.rect.collidepoint(mouse_x, mouse_y):
                # 鼠标触碰按钮
                # 若鼠标按下
                if mouse_clicked == True:
                    s.clicked = True
                # 若鼠标按上
                elif mouse_clicked == False:
                    if s.clicked:
                        # 若鼠标按上且之前按下时点击的该按钮
                        s.clicked = False
                        self.add_input(s.id)
            else:
                if mouse_clicked == False:
                    s.clicked = False
            s.update() # 更新按钮的显示

    def empty_keyboard(self):
        # 初始化Keyboard中的变量
        self.info.keyboard_input = []
        self.info.output = False
    
    def add_input(self,value):
        self.info.keyboard_input.append(value)
        self.info.output=True
    
    def end_of_input(self):
        return self.info.output