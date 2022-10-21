def GetBankCode(name: str):
    bank_name = {
        "BOT": "001",
        "BBL": "002",
        "KBANK": "004",
        "KTB": "006",
        "TTB": "011",
        "SCB": "014",
        "CIMBT": "022",
        "UOBT": "024",
        "BAY": "025",
        "GSB": "030",
        "GHB": "033",
        "BAAC": "034",
        "ISBT": "066",
        "KKP": "069",
        "TCD": "071",
        "LHB": "073",
    }
    return bank_name[name]


def GetBankName(code: str):
    bank_code = {
        "001": "BOT",
        "002": "BBL",
        "004": "KBANK",
        "006": "KTB",
        "011": "TTB",
        "014": "SCB",
        "022": "CIMBT",
        "024": "UOBT",
        "025": "BAY",
        "030": "GSB",
        "033": "GHB",
        "034": "BAAC",
        "066": "ISBT",
        "069": "KKP",
        "071": "TCD",
        "073": "LHB"
    }
    return bank_code[code]
