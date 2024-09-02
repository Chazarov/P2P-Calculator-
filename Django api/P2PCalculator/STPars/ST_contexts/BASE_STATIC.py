
USER_NAME = "user_name"
USER_ID = "user_id"
PRICE = "price"
MIN_AMOUNT = "min_amount"
ADV_ID = "adv_id"




class PAYMENTS:
    Raiffaizen = "Raiffaizen"
    SBP = "SBP"
    SBER = "SBER"
    TINKOFF = "TINKOFF"

    @classmethod
    def to_list(cls):
        return [value for key, value in cls.__dict__.items() if isinstance(value, str) and not key.startswith("__")]



