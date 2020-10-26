import numpy as np 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from utils import univariate_data


def train(
        csv_path: str,
        model,
        batch_size: int = 10,
        num_epochs: int = 5,
        past_history: int = 72,
        future_target: int = 0,
        train_split_ratio: float = 1.0,
        validation_split_ratio: float = 0.0
    ):

    data = pd.read_csv(csv_path, names=['Date', 'Close'])
    data = data.sort_values('Date')
    price = data[['Close']]

    # Normalize data
    min_max_scaler = MinMaxScaler()
    norm_data = min_max_scaler.fit_transform(price.values)

    # Data split
    train_split = int(len(norm_data) * train_split_ratio)

    x_train, y_train = univariate_data(norm_data,
                                    0,
                                    train_split,
                                    past_history,
                                    future_target)

    x_test, y_test = univariate_data(norm_data,
                                    train_split,
                                    None,
                                    past_history,
                                    future_target)

    history = model.fit(
        x_train,
        y_train,
        validation_split=validation_split_ratio,
        batch_size=batch_size,
        epochs=num_epochs,
        shuffle=False
    )

    loss = history.history['loss']
    if validation_split_ratio > 0:
        val_loss = history.history['val_loss']
        return loss, val_loss
    
    return loss, 0
