from abc import ABCMeta


class Stockpickbases(metaclass=ABCMeta):

    def fit(self, *args, **kwargs):
        """
        选股开始时要做的
        """
        pass

    def init_stock_picker(self, *args, **kwargs):
        """初始化选股参数"""
        pass
