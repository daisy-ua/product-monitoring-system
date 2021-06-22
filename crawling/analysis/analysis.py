import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 20, 10


def calculate_sale_history_stats(df):
    purchase_dates = df['purchase_date']
    delta = pd.to_datetime(purchase_dates).max() - pd.to_datetime(purchase_dates).min()
    days = int(delta.days)
    values = list(df['quantity_sold'])
    earnings = list(df['total_price'])
    sold_count = sum(values)

    if len(values) < days:
        values.extend([0] * (len(values) - days))
        earnings.extend([0] * (len(earnings) - days))

    res = pd.Series(
        [sold_count, np.mean(values),
         np.std(values), np.mean(earnings),
         np.std(earnings)
         ],
        index=['Sold_count', 'Mean_daily_sold_count',
               'Sold_count_St.Dev', 'Daily_earnings',
               'Daily_earnings_St.Dev']
    )

    return round(res, 2)


def get_category_ranking(_sales, _products):
    sales = convert_dict_to_df(_sales)
    sales = merge_category_column(sales, _products)

    sold_categories = sales.groupby('Category').apply(calculate_sale_history_stats)
    top_sold_categories = sold_categories.sort_values(
        by=['Sold_count', 'Daily_earnings', 'Mean_daily_sold_count'],
        ascending=False
    ).reset_index()

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(16, 8))

    plot = sns.barplot(
        data=top_sold_categories.iloc[0:6],
        x='Category',
        y='Sold_count')

    plot.set_xticklabels(plot.get_xticklabels(), rotation=35)
    plt.title('Model')
    plt.xlabel('Category', fontsize=18)
    plt.ylabel('Sold count', fontsize=16)
    plt.tight_layout()

    plot.figure.savefig('analysis/charts/category_ranking_chart.png')


def get_average_prices_by_category(history, products, category):
    pr_df = pd.DataFrame(products)
    pr_df = pr_df[pr_df.category.apply(lambda x: np.any(np.in1d(x, [category])))]
    ht_df = convert_dict_to_df(history)
    ht_df = merge_category_column(ht_df, products)
    ht_df = ht_df[ht_df['Category'] == category]

    if pr_df.empty or ht_df.empty:
        return False

    ax = plt.subplot()
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(16, 8))

    prices = pd.to_numeric(pr_df['price'])
    plot = sns.distplot(prices)
    plot.figure.savefig('analysis/charts/average_prices.png')
    paid_prices = pd.to_numeric(ht_df['sell_price'])
    plot = sns.distplot(paid_prices)
    ax.set_xlabel('Price', fontsize=18)
    ax.set_ylabel('', fontsize=18)
    plt.title('Model')
    plt.tight_layout()
    plot.figure.savefig('analysis/charts/average_sell_prices.png')
    return True


def get_price_prediction(product_id, history):
    df = convert_dict_to_df(history)
    df = df[df['_id'] == product_id]
    df.index = pd.to_datetime(df['purchase_date'])
    df = df.sort_index(ascending=True, axis=0)
    data = df.filter(['sell_price'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) * .8)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:training_data_len, :]

    x_train = []
    y_train = []
    for i in range(10, len(train_data)):
        x_train.append(train_data[i - 10:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build the LSTM network model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=1, epochs=1)

    test_data = scaled_data[training_data_len - 10:, :]
    x_test = []
    for i in range(10, len(test_data)):
        x_test.append(test_data[i - 10:i, 0])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # Plot/Create the data for the graph
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions

    # Visualize the data
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(16, 8))
    plt.title('Model')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Price USD ($)', fontsize=18)
    plt.plot(train['sell_price'])
    plt.plot(valid[['sell_price', 'Predictions']])
    plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    plt.savefig('analysis/charts/price_prediction.png')


def convert_dict_to_df(items):
    rows = []
    for data in items:
        data_row = data['sales']
        time = data['_id']

        for row in data_row:
            row['_id'] = time
            rows.append(row)

    return pd.DataFrame(rows)


def merge_category_column(df, products):
    categories = pd.Series([])
    pr_df = pd.DataFrame(products)
    for index, row in df.iterrows():
        category = pr_df[(pr_df['item_id'] == row['_id'])]['category'].tolist()
        categories[index] = category[0]
    df.insert(1, 'Category', categories, allow_duplicates=False)
    return df
