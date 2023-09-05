#coding=utf-8
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import json
import yaml
import re
#输入你的llm model by openai 
#initial_api_key
model='xx'


def json2yaml(json,group):
    return yaml.dump({group:json})

def good_initial_generate(value):
    text="""
    请以:形式告诉我想要的东西和市面上的价格的平均值,高低价格都有,最低个位数,用json表示
    Q:请告诉我2000年北京售卖的东西以及其价格区间
    A:{"大哥大":[100,2000],"VCD":[1,10],"走私汽车":[50000,100000],"香烟":[10,200]}
    Q:"""
    text_value="请告诉我{year}年{location}街头售卖的有时代感的品牌的东西以及其价格\nA:".format(year=value[0],location=value[1])
    msg = HumanMessage(content=text+text_value)
    res=model(messages=[msg]).content
    while('无法' in res):
        res=model(messages=[msg]).content
    goods_res=json.loads(res.split('\n')[0])
    print(goods_res)
    return goods_res

def market_initial_generate(value):
    text="""
    请回答4个指定年代的城市中著名的线下商品交易市场地点,并用中文逗号隔开
    Q:请给出2000年北京主要的交易地点
    A:西直门,公主坟,积水潭,北京站
    Q:"""
    text_value="请给出{year}年{location}主要的交易地点\nA:".format(year=value[0],location=value[1])
    msg = HumanMessage(content=text+text_value)
    res=model(messages=[msg]).content
    while('无法' in res):
        res=model(messages=[msg]).content
    output={}
    for idx,r in enumerate(res.split(',')):
        output[r]=str(idx+1)
    print(output)
    return output

def background_generate(value):
    text="""
    请根据年代和地点编写故事,你是一个外来的人来当地,通过买卖物品挣钱,并携带1000元的背景故事
    Q:2000年的北京
    A:你来自农村,由于早年辍学求生活,向村长借了1000元出来闯荡
    Q:"""
    text_value="{year}年的{location}\nA:".format(year=value[0],location=value[1])
    msg = HumanMessage(content=text+text_value)
    res=model(messages=[msg]).content
    return res


def initial_generate(value):
    res={}
    res['goods']=good_initial_generate(value)
    res['market']=market_initial_generate(value)
    filename='llm_data.yaml'
    import os
    if os.path.exists('./{}'.format(filename)):
        os.remove(filename)
    file=open(filename,"w",encoding='utf-8')
    yaml.dump(res,file,allow_unicode=True)

def model_story_generate(year,city,market,item,num,price,op):
    text="""
    请帮我设计一段故事,结合年代时间和地点特色,描述我在街头买卖物品时遇到的情况,并按规定的事情,对应的价格变化,以及最后的价格返回,要求编撰的故事和价格的变化是能够在逻辑上对应上的。
    Q:在2000年北京东直门,出售1个运动鞋,原有卖出价是200元
    A:遇到急需要运动鞋的中学生,卖出价格上升,卖出价是400元
    Q:在2010年上海外滩,出售1个随身听,原有卖出价是50元
    A:随身听电池没电了,卖出价格下降,卖出价是30元
    Q:在1990年深圳华强北,购买1个大哥大,原有买入价是10000元
    A:偶遇大促销,买入价格急剧下降,买入价是5000元
    Q:在1990年深圳华强北,购买1个电子计算器,原有买入价是1000元
    A:老板坐地起价,买入价格急剧上升,买入价是2000元
    Q:"""
    if op=='sell':
        text_value="在{year}年{city}{market}出售{num}个{item},原有卖出价是{price}\nA:".format(year=year,city=city,market=market,item=item,num=num,price=price)
    elif op=='buy':
        text_value="在{year}年{city}{market}购买{num}个{item},原有买入价是{price}\nA:".format(year=year,city=city,market=market,item=item,num=num,price=price)
    res='无法'
    print('story:',res)
    out_price=price
    count=0
    while ('无法' in res) and count<4:
        msg = HumanMessage(content=text+text_value)
        res=model(messages=[msg]).content
        try:
            out_price=int(re.findall('(\d+)',res)[-1])
        except:
            res='无法'
            count+=1
    print(res)
    if int(out_price)==int(price):
        if op=='buy':
            action='购入'
        elif op=='sell':
            action='售出'
        return '成功{}'.format(action),int(out_price)
    return res,out_price

if __name__ == '__main__':
    #value=['1995','成都']
    #print(initial_generate(value))
    res=background_generate(['2000','上海'])
    print(res)