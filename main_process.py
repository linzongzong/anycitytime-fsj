from config import Role,Status
import yaml
import os
from fsj_llm import initial_generate,model_story_generate,background_generate
from day_screen import market_plot
import pygame
SCREEN_SIZE = 800, 800

def main(role_name):
    days=40
    role=Role(role_name)
    value=input('请输入年代和城市,并用逗号隔开（不想输入直接回车）:')
    if value!='':
        year=value.split(',')[0]
        city=value.split(',')[1]
        initial_generate(value.split(','))
        bg=background_generate(value.split(','))
        file='llm_data.yaml'
    else:
        year='2000'
        city='北京'
        file='env_config.yaml'
        bg='一个背景离乡的北漂，要在北京的40天内赚够足够的金钱偿还债务，同时还要小心在北京遇到的各种事件并设法生存下来的故事。'
    curPath= os.getcwd()
    yamlPath = os.path.join(curPath, file)
    with open(yamlPath, 'r', encoding='utf-8') as f:
        config_file=yaml.safe_load(f)
    status=Status(year,city,days,config_file)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    story=""
    for d in range(days):
        nextday=False
        for market in status.markets:
            market.generate_goods()
            finish=False
            while not finish:
                args={'day':d,'role':role,'status':status,'market':market,'year':year,'city':city,'story':story,'bg':bg}
                op_flag,op_info=market_plot(screen,args)
                bg=''
                story=""
                if op_flag=='next_market':
                    finish=True
                elif op_flag=='next_day':
                    finish=True
                    nextday=True
                else:
                    for good_item in op_info:
                        good=good_item.split(':')[0]
                        op=op_flag
                        num=1
                        if not market.check_goods(good):
                            story='市场不存在货物{},交易失败!'.format(good)
                        else:
                            price=market.query_price(good)
                            story,checkout_price=model_story_generate(year,city,market.market_name,good,num,int(price),op)
                            trade_res,trade_msg=role.action(good,int(checkout_price),int(num),op)
                            if trade_res:
                                story+="交易成功!"
                            else:
                                story+="{},交易失败!".format(trade_msg)
            if nextday:
                break
    pygame.quit()
if __name__=='__main__':
    main('zanelin')