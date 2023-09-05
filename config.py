import numpy as np
import json

def dict2text(dict):
    text=[]
    for k,v in dict.items():
        text.append('{}:{}'.format(k,v))
    return ','.join(text)

def dict2text_list(dict):
    text=[]
    for k,v in dict.items():
        text.append('{}:售价{}'.format(k,v))
    return text

class Status:
    def __init__(self,year,city,days,configs):
        self.year=year
        self.city=city
        self.day=0
        self.markets=[Market(market_name,configs) for market_name in configs['market'].keys()]

class Goods:
    def __init__(self,good_name,min_price,max_price):
        self.good_name=good_name
        self.min_price=min_price
        self.max_price=max_price

    def get_price(self,ratio=1):
        return np.random.randint(self.min_price*ratio,self.max_price*ratio)

class Market:
    def __init__(self,market_name,configs):
        self.market_name=market_name
        self.goods_configs=configs['goods']
        self.current_commodity={}
        self.commodity_list=list(self.goods_configs.keys())

    def generate_goods(self):
        self.current_commodity_list=np.random.choice(self.commodity_list,4)
        for good in self.current_commodity_list:
            good_instance=Goods(good,self.goods_configs[good][0],self.goods_configs[good][1])
            self.current_commodity[good]=good_instance.get_price()
    
    def show_goods(self):
        return dict2text(self.current_commodity)
    
    def show_goods_list(self):
        return dict2text_list(self.current_commodity)
    
    def query_price(self,good):
        return self.current_commodity[good]
    
    def check_goods(self,good):
        return self.current_commodity.get(good,False)

class Role:
    def __init__(self,role_name):
        self.name=role_name
        self.bag=Bag()
        self.health=100

    def show_money(self):
        return self.bag.money
    
    def action(self,good_name,good_price,num,operation):
        return self.bag.check_out(good_name,good_price,num,operation)
    
    def show_goods(self):
        return ','.join([b.get_text() for b in self.bag.commodity.values()])
    
    def show_goods_list(self):
        return [b.get_text() for b in self.bag.commodity.values()]
    


class Bag:
    def __init__(self):
        self.money=1000
        self.max_money=1000
        self.count=0
        self.max_count=100
        self.commodity={}

    def check_out(self,good_name,good_price,num,operate):
        if operate=='sell':
            if self.check_good(good_name,num):
                if num>self.commodity[good_name].get_storage():
                    self.commodity[good_name].update(good_price,num,operate)
                else:
                    del self.commodity[good_name]
                self.count-=num
                self.money+=good_price*num
                return True,None
            else:
                return False,'货物不够售'

        elif operate=='buy':
            if self.check_money(good_price,num) and self.check_storage(num):
                if self.check_good(good_name,0):
                    self.commodity[good_name].update(good_price,num,operate)
                else:
                    self.commodity[good_name]=Bag_Good(good_name,good_price,num)
                self.count+=num
                self.money-=good_price*num
                return True,None
            else:
                if not self.check_money(good_price,num):
                    return False,'金钱不够'
                if not self.check_storage(num):
                    return False,'空间不足'
                
        return False,'未知操作{}'.format(operate)
    
    def check_storage(self,num):
        if self.count+num<=self.max_count:
            return True
        return False
        
    def check_money(self,good_price,num):
        if good_price*num<=self.money:
            return True
        return False
        
    def check_good(self,good_name,num):
        if self.commodity.get(good_name,False):
            if self.commodity[good_name].get_storage()>=num:
                return True
        return False
    
class Bag_Good:
    def __init__(self,good_name,price,num):
        self.name=good_name
        self.num=num
        self.avg_cost=price

    def update(self,price,num,operation):
        if operation=='sell':
            self.avg_cost=(self.avg_cost*self.num-price*num)/(self.num-num)
            self.num-=num
        elif operation=='buy':
            self.avg_cost=(self.avg_cost*self.num+price*num)/(self.num+num)
            self.num+=num
        else:
            print('unknown operation:{}'.format(operation))

    def get_storage(self):
        return self.num
    
    def get_text(self):
        return self.name+':数量:'+str(self.num)+'成本:'+str(round(self.avg_cost,2))
