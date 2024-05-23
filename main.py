from apirequsts import APIRequests


STOCK = "TSLA"
COMPANY_NAME = "Tesla"
LANGUAGE = "ru"

data = APIRequests()
stock_data = data.stock_info(STOCK)
yd_date = list(stock_data.keys())[0]
yd_price = float(stock_data[yd_date]["4. close"])

before_yd_date = list(stock_data.keys())[1]
before_yd_price = float(stock_data[before_yd_date]["4. close"])


def share_changing_info():
    percentage_change = ((yd_price - before_yd_price) / before_yd_price) * 100
    if percentage_change > 0:
        price_change = "rose"
    else:
        price_change = "fell"

    if abs(percentage_change) >= 5:
        company_news = data.check_news(COMPANY_NAME, LANGUAGE)
        intro_news = [[item["title"], item["url"]] for item in company_news]
        if LANGUAGE == "ru":
            data.telegram_message(f"Цена {STOCK} изменилась на {percentage_change:.2f}%"
                                  f"\nЧто могло повлиять на цену:")
        else:
            data.telegram_message(f"Get news! {STOCK} shares {price_change} in price by {percentage_change:.2f}%"
                                  f"\nWhat could affect the price:")
        return [data.telegram_message(f"{info[0]} {info[1]}") for info in intro_news]


share_changing_info()
