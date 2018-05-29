from .pickstockbases import Stockpickbases
import copy


# 选股工人类
class pickstockwoker(Stockpickbases):

    def __init__(self, capital, benchmark, choice_symbols, timeseries_manager, stockpickers):
        """
        选股要考虑：
        资金
        基准收益
        选股对象
        金融时间序列
        选股因子序列
        """
        self.capital = capital
        self.benchmark = benchmark
        self.choic_symbols = choice_symbols
        self.timeseries = timeseries_manager
        self.stockpicker = stockpickers
        # 在初始化选股工人的时候同时初始化选股因子
        self.init_stock_picker(stockpickers)

    # 实例化时打印选股因子序列和选股交易对象

    def __str__(self):
        return 'stock_pickers:{}\nchoice_symbols:{}'.format(self.stockpicker, self.choic_symbols)

    #初始化选股因子
    def init_stock_picker(self, stockpickers):
        #stockpicker是一个由字典组成的列表
        #stockpickers=[{'factor':xxx,'class':xxxclass}]
        """初始化选股因子从选股因子列表中获得各个选股因子"""
        if stockpickers:
            for picker in stockpickers:
                if picker is None:
                    continue

                if 'class' not in picker:
                    raise ValueError('选股因子中必须有class这个key')
                #获得picker_cp
                picker_cp = copy.deepcopy(picker)
                #将picker_cp中的类剔除掉
                fac = picker_cp.pop('class')
                #整合capital,benchmark等选股因素
                picker = class_fac(self.capital,self.benchmark,**picker_cp)

    def fit(self):
        """
        选股开始工作
        :return:
        """
        def _batch_fit():
            #如果没有选股条件，则返回所有备选股票
            if self.stockpicker is None:
                return self.choice_symbols

            inner_choice_symbols = []
            for epoch,target_symbol in enumerate(self.choice_symbols):
                add = True
                for picker in self.stockpickers:
                    timeseries = self.timeseries_manager.get_pick_stock_series(target_symbol,picker.xd,picker.min_xd)
                    #如果该股票时间序列过少，则该只股票剔除
                    if timeseries is None:
                        add = False
                        break
                    sub_add = picker.fit_pick(timeseries,target_symbol)
                    if sub_add is False:
                        #只要一个因子投了反对票，就刷出
                        add = False
                        break
                if add:
                    inner_choice_symbols.append(target_symbol)
            return inner_choice_symbols

        self.choic_symbols = _batch_fit()









