SM_NAME = "BYBIT"
BASE_URL = "https://api2.bybit.com/fiat/otc/item/online"





class TRADE_ROLE:
    SELL = "1"
    BUY = "0"
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
    # AED = "AED"
    # AMD = "AMD"
    # ARS = "ARS"
    # AUD = "AUD"
    # AZN = "AZN"
    # BDT = "BDT"
    # BGN = "BGN"
    # BRL = "BRL"
    # BSD = "BSD"
    # BYN = "BYN"
    # CAD = "CAD" 
    # CLP = "CLP"
    # COP = "COP"
    # CZK = "CZK"
    # DZD = "DZD"
    # EGP = "EGP"
    # EUR = "EUR" #!
    # GBP = "GBP"
    # GEL = "GEL"
    # GHS = "GHS"
    # HKD = "HKD"
    # HUF = "HUF"
    # IDR = "IDR"
    # ILS = "ILS"
    # INR = "INR"
    # JOD = "JOD"
    # JPY = "JPY"
    # KES = "KES"
    # KGS = "KGS"
    # KHR = "KHR"
    # KWD = "KWD"
    # KZT = "KZT"#!
    # LBP = "LBP"
    # LKR = "LKR"
    # MAD = "MAD"
    # MDL = "MDL"
    # MMK = "MMK"
    # MNT = "MNT"
    # MXN = "MXN"
    # MYR = "MYR"
    # NGN = "NGN"
    # NOK = "NOK"
    # NPR = "NPR"
    # NZD = "NZD"
    # PEN = "PEN"
    # PHP = "PHP"
    # PKR = "PKR"
    # PLN = "PLN"
    # RON = "RON"
    # RSD = "RSD"
    RUB = "RUB"#!
    # SAR = "SAR"
    # SEK = "SEK"
    # THB = "THB"
    # TJS = "TJS"
    # TND = "TND"
    # TRY = "TRY"
    # TWD = "TWD"
    # UAH = "UAH"
    # USD = "USD" #!
    # UZS = "UZS"
    # VES = "VES"
    # VND = "VND"
    # ZAR = "ZAR"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}



class PAYMENTS:
    Raiffaizen = "64"
    SBP = "382"
    SBER = "582"
    TINKOFF = "581"
    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]
    
    @classmethod
    def to_dict(cls):
        return {value:key for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")}




