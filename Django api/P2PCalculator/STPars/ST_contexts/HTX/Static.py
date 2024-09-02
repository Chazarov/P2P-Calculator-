SM_NAME = "HTX"
BASE_URL = "https://www.htx.com/-/x/otc/v1/data/trade-market?"





class TRADE_ROLE:
    SELL = "sell"
    BUY = "buy"
    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}
    


class PREFERENCES:
    NUMBER_OF_PAGES_TO_PARSE = 10
    NUMBER_OF_UNITS_PER_PAGE = 10
    TIMEOUT = 3
    UPDATE_RATE = 0.1



class TOKENS:
    USDT = "2"
    BTC = "1"
    ETH = "3"
    USDD = "62"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}



class CURRENCIES:
    RUB = "11"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}



class PAYMENTS:
    Raiffaizen = "36"
    SBP = "69"
    SBER = "29"
    TINKOFF = "28"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}




