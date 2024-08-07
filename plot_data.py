import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

def fetch_data_as_dict(db_path: str, table: str):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM {table}")

    rows = cursor.fetchall()

    data = [dict(row) for row in rows]

    db.close()

    return data

def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data)):
        end_ix = i + n_steps
        if end_ix > len(data)-1:
            break
        seq_x, seq_y = data[i:end_ix], data[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def frequency():
    numbers = fetch_data_as_dict("data.db", "numbers")
    frequencies = [0] + [0 for i in range(1,76)]
    for entry in numbers:
        if int(entry["year"]) >= 2024: # Change to filter by year, date, etc
            for i in range(1,6): # change range to filter by number: n1, n2, n3, etc
                index = int(entry[f"n{i}"])
                frequencies[index] += 1
    sum = 0
    for num in frequencies:
        sum += num
    print(sum)
    frequencies.pop(0)
    values = list(range(1,76))
    plt.plot(values,frequencies)
    plt.show()

def binary():
    numbers = fetch_data_as_dict("data.db", "numbers")
    num = 19 # change to determine if played or not
    year = 2024 # change to determine year
    
    total_draws = []
    for entry in numbers:
        if int(entry["year"]) == year:
            draws = []
            for i in range(1,6):
                draws.append(int(entry[f"n{i}"]))
            total_draws.append(draws)
    total_draws_y = [255 for i in range(0,len(total_draws))]
    for i, draws in enumerate(total_draws):
        if num in draws:
            total_draws_y[i] = 1
        else:
            total_draws_y[i] = 0
    total_draws = list(range(1,len(total_draws)+1))
    plt.plot(total_draws, total_draws_y)
    plt.show()


def predict():
    year = 2024

    numbers = fetch_data_as_dict("data.db","numbers")
    data = []
    for entry in numbers:
        if int(entry["year"]) == year:
            draws = []
            for i in range(1,6):
                draws.append(int(entry[f"n{i}"]))
            data.append(draws)

    data = np.array(data)

    n_steps = 2

    count = 100
    sums = [0] * 5

    for i in range(0, count):
        X, y = create_sequences(data, n_steps)

        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(n_steps, data.shape[1])))
        model.add(Dense(data.shape[1]))
        model.compile(optimizer='adam', loss='mse')

        model.fit(X, y, epochs=200, verbose=0)

        input_sequence = np.array([data[-n_steps:]])
        next_row = model.predict(input_sequence, verbose=0)
        next_row_list = next_row[0].tolist()

        rounded_rows = [round(num) for num in next_row_list]
        #print(rounded_rows)
        
        for j, sum in enumerate(sums):
            sums[j] += next_row_list[j]
            #print(sum)
        
    average = [sums[i]/count for i in range(0,5)]
    average = [round(num) for num in average]
    print(f"Average: {average}")





if __name__ == "__main__":
    predict()