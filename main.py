import sqlite3
import pandas as pd
import numpy as np
import datetime as dt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from flask import Flask
from flask import Flask, render_template, request

# Создаем базу данных
conn = sqlite3.connect('menstrual.db')

# Создаем таблицу "periods"
conn.execute('''CREATE TABLE IF NOT EXISTS periods
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             start_date TEXT NOT NULL,
             end_date TEXT NOT NULL,
             cycle_length INTEGER NOT NULL,
             period_length INTEGER NOT NULL);''')
def add_period(start_date, end_date, cycle_length, period_length):
    conn = sqlite3.connect('menstrual.db')
    conn.execute("INSERT INTO periods (start_date, end_date, cycle_length, period_length) \
                  VALUES (?, ?, ?, ?)", (start_date, end_date, cycle_length, period_length))
    conn.commit()
def calculate_periods():
    conn = sqlite3.connect('menstrual.db')
    df = pd.read_sql_query("SELECT * from periods", conn)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['period_length'] = pd.to_numeric(df['period_length'])
    df['cycle_length'] = pd.to_numeric(df['cycle_length'])
    df['next_period_start_date'] = df['start_date'] + pd.to_timedelta(df['cycle_length'], unit='D')
    df['ovulation_date'] = df['next_period_start_date'] - pd.to_timedelta(14, unit='D')
    df['pms_start_date'] = df['next_period_start_date'] - pd.to_timedelta(7, unit='D')
    return df
def create_model():
    model = Sequential()
    model.add(Dense(128, input_dim=3, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))

    optimizer = Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model
def train_model():
    conn = sqlite3.connect('menstrual.db')
    df = pd.read_sql_query("SELECT * from periods", conn)
    X = df[['cycle_length', 'period_length', 'prev_period_length']]
    y = df[['ovulation_date', 'pms_start_date', 'next_period_start_date']]
    model = create_model()
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    history = model.fit(X, y, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    return model, history
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    cycle_length = int(request.form['cycle_length'])
    period_length = int(request.form['period_length'])
    last_period_start = request.form['last_period_start']

    # Perform period date calculations using the Python code from step 6

    result = "Period start: " + period_start.strftime('%Y-%m-%d') + "<br>"
    result += "Ovulation start: " + ovulation_start.strftime('%Y-%m-%d') + "<br>"
    result += "PMS start: " + pms_start.strftime('%Y-%m-%d') + "<br>"

    return result