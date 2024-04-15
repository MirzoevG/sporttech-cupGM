import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import warnings
import logging


tf.get_logger().setLevel('ERROR')

# Отключение предупреждений
warnings.filterwarnings("ignore")

def load_data_from_jsonl(jsonl_file):
    data = []
    with open(jsonl_file, 'r') as file:
        try:
            for line in file:
                data.append(eval(line))  # Предполагая, что jsonl содержит допустимый JSON
        except:
            pass
    df = pd.DataFrame(data)
    df = df.dropna()  # Удаление строк с пропущенными значениями
    return df

# Загрузка данных
viborka_df = load_data_from_jsonl('viborka.jsonl')

# Отобразим первые несколько строк для проверки
#print(viborka_df.head())



X = viborka_df.drop('cheater_value', axis=1)  # Признаки
y = viborka_df['cheater_value']  # Целевая переменная

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Определение модели
model = keras.Sequential()
model.add(keras.layers.Dense(30, input_shape=(X_train.shape[1],), activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))

optimizer = keras.optimizers.Adam(learning_rate = 0.05)

# Компиляция модели
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
history = model.fit(X_train, y_train, epochs=100, batch_size=128, verbose=1)
loss, accuracy = model.evaluate(X_test, y_test)


# Оценка модели на тестовых данных
loss, accuracy = model.evaluate(X_test, y_test)
#print(f'Точность модели на тестовых данных: {accuracy:.4f}')

# Сохранение модели
model.save('fraud_detection_model.h5')
print('Модель сохранена успешно.')
