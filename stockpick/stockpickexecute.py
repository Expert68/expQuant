from .stockpickworker import pickstockwoker


def do_pick_stock_work(choice_symbols,benchmark,capital,stock_pickers):
    """应用stockpickworker进行选股"""
    timeseries_manager = AbuKLManager(benchmark,capital)
    stock_pick = pickstockwoker(capital,benchmark,timeseries_manager,choice_symbols,stock_pickers)
    stock_pick.fit()
    return stock_pick.choic_symbols

