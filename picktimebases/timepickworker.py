from .timepickbases import Picktimebases
import ABuSymbolPd
import copy

class Picktimeworker(Picktimebases):
    """择时类"""
    def __init__(self,capital,timeseries,benchmark,buy_factors,sell_factors):
        """
        :param capital: 资金类对象
        :param timeseries: 择时时间段金融时间序列
        :param benchmark: 基准收益对象
        :param buy_factors: 买入因子序列
        :param sell_factors: 卖出因子序列
        """
        self.capital = capital
        self.timeseries = timeseries
        #合并加上回测之前一年的数据，以生成特征数据
        self.combine_timeseries = ABuSymbolPd.combine_pre_kl_pd(self.timeseries,n_folds=1)
        self.benchmark = benchmark
        self.init_buy_factors(buy_factors)
        #暂时只根据日线选股，周线以及月线选股待完善
        # self.filter_long_task_factors()
        self.init_sell_factors(sell_factors)
        self.orders = list()
        #择时进度条，默认不打开
        self.task_pg = None



    def _day_task(self,today):
        """
        日任务：迭代买入卖出因子序列进行择时
        :param today: 今日的交易数据
        :return:
        """
        for sell_factor in self.sell_factors:
            #迭代卖出因子，每个卖出因子针对今日交易数据
            sell_factor.read_fit_day(today,self.orders)

        for buy_factor in self.buy_factors:
            #迭代买入因子，每个因子都对今天进行择时，如果生成order则加入self.orders
            if not buy_factor.read_fit_day(today):
                order = buy_factor.read_fit_day(today)
                if order and order.order_deal:
                    self.orders.append(order)

    def _task_attached_sell(self,today,how):
        """专属择时买入因子的择时卖出因子任务：日任务择时卖出因子"""
        for buy_factor in self.buy_factors:
            #筛选出当前买入因子锁对应的所有单子，注意这里使用buy_factor_class不是buy_factor
            factor_orders = list(filter(lambda order:order.buy_buyfactor_class == buy_factor.__class__.__name__,self.orders))

            if len(factor_orders) == 0:
                #没有下单
                continue

            #TODO不要使用字符串进行eq比对
            for sell_factor in buy_factor.sell_factors:
                if how == 'day':
                    #所有日任务都要用read_fit_day
                    sell_factor.read_fit_day(today,factor_orders)

    def _task_loop(self,today):
        """
        开始时间驱动，进行日任务
        :param today: 对于self.timeseries 进行操作，且axis=1结果为一天的交易数据
        :return:
        """
        if self.task_pg is not None:
            self.task_pg.show()

        day_cnt = today.key

        self._day_task(today)

    def fit(self,*args,**kwargs):
        """
        根据交易数据，因子等输入参数，拟合择时
        """
        self.timeseries.apply(self._task_loop,axis=1)

        if self.task_pg is not None:
            self.task_pg.close_ui_progress()

    def init_sell_factors(self,sell_factors):
        """
        通过sell_factors实例化各个卖出因子
        :param sell_factors: 该list中的元素为dict,每个dict为因子的构造元素如class，构造参数等
        :return:
        """
        self.sell_factors = list()

        if sell_factors is None:
            return

        for factor_class in sell_factors:
            if factor_class is None:
                continue

            if 'class' not in factor_class:
                #必须要有需要实例化的类的信息
                raise ValueError('必须要有需要实例化类的信息')

            factor_class_cp = copy.deepcopy(factor_class)
            #pop出类信息后剩下的窦唯类需要的参数
            class_fac = factor_class_cp.pop('class')
            #整合capital,timeseries等实例化因子对象
            factor = class_fac(self.capital,self.timeseries,self.combine_timeseries,self.benchmark,**factor_class_cp)
            #TODO:写AbuFactorSellBase
            if not isinstance(factor,AbuFactorSellBase):
                #因子对象类型检测
                raise TypeError('卖出因子的类型必须是AbuFactorSellBase')
            self.sell_factors.append(factor)

    def init_buy_factors(self,buy_factors):
        """
        通过buy_factors实例化各个买入因子
        :param buy_factors: 该list中的元素为dict,每个dict为因子的构造元素如class，构造参数等
        :return:
        """
        self.buy_factors = list()

        if buy_factors is None:
            return
        for factor_class in buy_factors:
            if factor_class is None:
                continue

            if 'class' not in factor_class:
                #必须要有需要实例化的类的信息
                raise ValueError('必须要有需要实例化类的信息')

            factor_class_cp = copy.deepcopy(factor_class)
            # pop出类信息后剩下的窦唯类需要的参数
            class_fac = factor_class_cp.pop('class')
            # 整合capital,timeseries等实例化因子对象
            factor = class_fac(self.capital, self.timeseries, self.combine_timeseries, self.benchmark,
                               **factor_class_cp)
            # TODO:写AbuFactorSellBase
            if not isinstance(factor, AbuFactorBuyBase):
                # 因子对象类型检测
                raise TypeError('卖出因子的类型必须是AbuFactorSellBase')
            self.sell_factors.append(factor)

































