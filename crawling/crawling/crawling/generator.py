import datetime
import random


def generate_sale_history(product_id, product_price):
    purchase_num = random.randint(1, 200)
    sales = []
    dates = []

    for _ in range(purchase_num):
        dates.append(get_random_date())

    product_price = float(product_price)
    price = product_price
    is_price_changed = False
    sale_days_num = 10
    curr_day_num = 0

    for date in sorted(dates):

        if curr_day_num > sale_days_num:
            is_price_changed = bool(random.randint(0, 1))

        if curr_day_num > sale_days_num and not is_price_changed:
            price = product_price
            sale_days_num = random.randint(3, 30)
            curr_day_num = 0

        if is_price_changed:
            is_price_changed = False
            delta_price = product_price * 0.3
            price = random.uniform(product_price - delta_price, product_price + delta_price)
            price = float("{:.2f}".format(price))
            sale_days_num = random.randint(3, 30)
            curr_day_num = 0

        quantity = random.randint(1, 2)
        total_price = price * quantity
        curr_day_num += 1

        sales.append({
            'purchase_date': str(date),
            'quantity_sold': quantity,
            'sell_price': price,
            'total_price': total_price
        })

    return {
        '_id': product_id,
        'sales': sales
    }


def get_random_date():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_dates = random.randrange(days_between_dates)

    return start_date + datetime.timedelta(days=random_number_of_dates)
