from abc import ABCMeta


class Picktimebases(metaclass=ABCMeta):
    def fit(self,*args,**kwargs):
        pass

    def init_buy_factors(self,*args,**kwargs):
        pass

    def init_sell_factors(self,*args,**kwargs):
        pass

