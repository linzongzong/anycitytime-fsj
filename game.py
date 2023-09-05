import sys
import pygame

def show_box(screen,text):
    color=(255,255,255)
    pygame.draw.rect(screen,color,pygame.Rect(200,150,200,100))
    pygame.display.update()
    f = pygame.font.SysFont(['方正舒体','microsoftsansserif'],20)
    screen.blit(f.render(text,True,(0,0,0)),(200,150))
    pygame.display.update()


def table_list(screen,data):
    row=10
    f = pygame.font.SysFont(['方正舒体','microsoftsansserif'],20)
    for idx,d in enumerate(data):
        content=f.render("{}".format(d),True,(255,0,0),(0,0,0))
        textRect =content.get_rect()
        textRect.center = (100+idx*row,50)
        screen.bilt(textRect,content)

def run_process(screen):
    face = pygame.Surface((50,50),flags=pygame.HWSURFACE)
    face.fill(color='white')
    table_list(screen,['预算:100','手机:1','手表:2'])

def init_window(screen):
    f = pygame.font.SysFont(['方正舒体','microsoftsansserif'],50)
    text = f.render("上海浮生记",True,(255,0,0),(0,0,0))
    textRect =text.get_rect()
    textRect.center = (300,200)
    screen.blit(text,textRect)
    year=InputBox(pygame.Rect(100, 250, 2, 30))
    city=InputBox(pygame.Rect(320, 250, 2, 30))
    #play_button = Button('Play', RED, None, 350, centered_x=True)
    while True:
        # 循环获取事件，监听事件
        for event in pygame.event.get():
            # 判断用户是否点了关闭按钮
            if event.type == pygame.QUIT:
                #卸载所有pygame模块
                pygame.quit()
                #终止程序
                sys.exit()
            show_box(screen,'hello')
            if event.type==pygame.MOUSEBUTTONDOWN:
                run_process()
            year.dealEvent(event)
            city.dealEvent(event)
            #play_button.dealEvent(event)
        year.draw(screen)
        city.draw(screen)
        pygame.display.flip() #更新屏幕内容


if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((600,400))
    pygame.display.set_caption('上海浮生记')
    print("获取系统中所有可用字体",pygame.font.get_fonts())
    init_window(screen)
    #run_process()
    