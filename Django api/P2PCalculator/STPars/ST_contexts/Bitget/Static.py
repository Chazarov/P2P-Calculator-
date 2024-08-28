SM_NAME = "BITGET"
BASE_URL = "https://api.bitget.com/api/p2p/v1/merchant/orderList"
RELATIVE_URL = "/api/p2p/v1/merchant/orderList"





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
    NUMBER_OF_PAGES_TO_PARSE = 1
    NUMBER_OF_UNITS_PER_PAGE = 200



class TOKENS:
    USDT = "USDT"
    BTC = "BTC"
    ETH = "ETH"
    USDC = "USDC"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}



class CURRENCIES:
    RUB = "RUB"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}



class PAYMENTS:
    Raiffaizen = "96"
    SBP = "258"
    SBER = "415"
    TINKOFF = "229"
    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}




