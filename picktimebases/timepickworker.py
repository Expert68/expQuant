from .timepickbases import Picktimebases
import ABuSymbolPd

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



    def _day_task
