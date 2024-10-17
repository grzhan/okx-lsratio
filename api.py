import okx.TradingData as TradingData
from datetime import datetime

def get_margin_loan_ratio(target: str, period: str):
    """
    获取加密货币目标的多空比
    """
    trading_data = TradingData.TradingDataAPI(flag='0', debug=False)
    begin, end = get_time_window(period)
    return trading_data.get_margin_lending_ratio(target, begin, end, period)

def get_time_window(period: str):
    """
    根据 period 获取开始时间戳和结束时间戳
    """
    if period == '5m':
        return int((datetime.now().timestamp() - 5 * 10 * 60) * 1000), int(datetime.now().timestamp() * 1000)
    elif period == '1D':
        return int((datetime.now().timestamp() - 5 * 24 * 60 * 60) * 1000), int(datetime.now().timestamp() * 1000)

