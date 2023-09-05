import pygame

from button import KeyboardButton,KeyboardButtonGroup
from button_checkbox import KeyboardCheckbox,KeyboardCheckboxGroup

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
inform_font=pygame.font.SysFont(['方正舒体'],20)
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

def draw_status(screen,status,position):
    # 显示当前状态
    #长和高1000*500,我们设计为800*30
    display_height = display_font.get_height() + 2 * PAD
    img = pygame.Surface((700, display_height)).convert()
    img.fill(DISPLAY_BG_COLOR)
    img.blit(display_font.render(status, True, DISPLAY_TEXT_COLOR), (PAD, PAD))
    screen.blit(img, position)

def generate_items_checkbox(items,display_position):
    KEYBOARD_BUTTON_SIZE=(300,40)
    keyboard_button_grp = KeyboardCheckboxGroup()  # 初始化按钮
    #输入展示的行，表现货物的数量,item是一个list,每一个为市场的货物和其对应的价格。
    for value in items:
        keyboard_button_grp.add(KeyboardCheckbox(size=KEYBOARD_BUTTON_SIZE, value=value))
    display_height = display_font.get_height() + PAD
    x, y = display_position[0], display_position[1] + display_height  # 按钮区域的位置
    start_x=x
    for i, button in enumerate(keyboard_button_grp):
        button.rect.topleft = x, y
        x = start_x
        y += KEYBOARD_BUTTON_SIZE[1] + PAD
    return keyboard_button_grp

def generate_items(items,display_position):
    KEYBOARD_BUTTON_SIZE=(300,40)
    keyboard_button_grp = KeyboardButtonGroup()  # 初始化按钮
    #输入展示的行，表现货物的数量,item是一个list,每一个为市场的货物和其对应的价格。
    for value in items:
        keyboard_button_grp.add(KeyboardButton(size=KEYBOARD_BUTTON_SIZE, value=value))
    display_height = display_font.get_height() + PAD
    x, y = display_position[0], display_position[1] + display_height  # 按钮区域的位置
    start_x=x
    for i, button in enumerate(keyboard_button_grp):
        button.rect.topleft = x, y
        x = start_x
        y += KEYBOARD_BUTTON_SIZE[1] + PAD
    return keyboard_button_grp

def generate_items_cols(items,display_position):
    KEYBOARD_BUTTON_SIZE=(300,40)
    keyboard_button_grp = KeyboardButtonGroup()  # 初始化按钮
    #输入展示的行，表现货物的数量,item是一个list,每一个为市场的货物和其对应的价格。
    for value in items:
        keyboard_button_grp.add(KeyboardButton(size=KEYBOARD_BUTTON_SIZE, value=value))
    display_height = display_font.get_height() + PAD
    x, y = display_position[0], display_position[1] + display_height  # 按钮区域的位置
    start_y=y
    for i, button in enumerate(keyboard_button_grp):
        #只规定了左上角
        button.rect.topleft = x, y
        y = start_y
        x += KEYBOARD_BUTTON_SIZE[0] + PAD
    return keyboard_button_grp

def draw_area_keyboard(screen, keyboard_button_grp):
    # 绘按钮区域
    keyboard_button_grp.draw(screen)

def draw_area_keyboard_checkbox(screen,keyboard_button_checkbox_grp,*args):
    keyboard_button_checkbox_grp.update(*args)
    keyboard_button_checkbox_grp.draw(screen)

def draw_btm_confirm(screen,btn_confirm_grp,*args):
    btn_confirm_grp.update(*args)
    btn_confirm_grp.draw(screen)

def market_plot(screen,system_args):
    #初始化信息
    mouse_x,mouse_y,mouse_clicked=0,0,None
    bg_text=system_args['bg']
    status_text="今天是{y}年第{d}天,你在{city},当前有{money}块,目前在{market}".format(y=system_args['year'],city=system_args['city'],d=system_args['day']+1,money=system_args['role'].show_money(),market=system_args['market'].market_name)     
    market_items=system_args['market'].show_goods_list()
    item_button_grp=generate_items_checkbox(['市场货物']+market_items,(100,80))
    user_items=system_args['role'].show_goods_list()
    user_button_grp=generate_items_checkbox(['你的出租屋']+user_items,(100+300+PAD,80))
    buy_button_grp=generate_items_cols(['买入'],(100,450))
    sell_button_grp=generate_items_cols(['卖出'],(400+PAD,450))
    market_button_grp=generate_items_cols(['下一站'],(100,500))
    day_button_grp=generate_items_cols(['结束一天'],(400+PAD,500))
    item_button_grp.empty_keyboard()
    user_button_grp.empty_keyboard()
    #怎么画
    fps_clock = pygame.time.Clock()
    #进行在某个市场的结算
    while True:
        
        #初始化参数
        #判断输出
        if day_button_grp.end_of_input():
            return 'next_day',None
        if market_button_grp.end_of_input():
            return 'next_market',None
        if buy_button_grp.end_of_input():
            return 'buy',item_button_grp.get_checkbox_value()
        if sell_button_grp.end_of_input():
            return 'sell',user_button_grp.get_checkbox_value()
        
        # 判断是否最终输出
        mouse_clicked = None
        # 获取 mouse_x, mouse_y, mouse_clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

        args=mouse_x,mouse_y,mouse_clicked
        bg = pygame.image.load("bg800800.png")
        screen.fill(BLACK)
        screen.blit(bg,(0,0))
        if bg_text!='':
            text = inform_font.render(bg_text, True, (255, 255, 255))
            temp_surface = pygame.Surface(text.get_size())
            temp_surface.fill((192, 192, 192))
            temp_surface.blit(text, (0, 0))
            screen.blit(temp_surface, (0, 0))
            pygame.display.update()
            import time
            time.sleep(10)
            system_args['bg']=''
            bg_text=''
        draw_status(screen,status_text,(80,20))
        draw_area_keyboard_checkbox(screen, item_button_grp,*args)
        draw_area_keyboard_checkbox(screen, user_button_grp,*args)
        draw_btm_confirm(screen, buy_button_grp,*args)
        draw_btm_confirm(screen, sell_button_grp,*args)
        draw_btm_confirm(screen, market_button_grp,*args)
        draw_btm_confirm(screen, day_button_grp,*args)
        fps_clock.tick(FPS)
        if system_args['story']!='':
            text = inform_font.render(system_args['story'], True, (255, 255, 255))
            temp_surface = pygame.Surface(text.get_size())
            temp_surface.fill((192, 192, 192))
            temp_surface.blit(text, (0, 0))
            screen.blit(temp_surface, (0, 0))
            pygame.display.update()
            import time
            time.sleep(5)
            system_args['story']=''
        else:
            pygame.display.update()