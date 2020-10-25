import numpy as np 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def univariate_data(dataset, start_index, end_index, history_size, target_size):
  data = []
  labels = []

  start_index = start_index + history_size
  if end_index is None:
    end_index = len(dataset) - target_size

  for i in range(start_index, end_index):
    indices = range(i-history_size, i)
    data.append(np.reshape(dataset[indices], (history_size, 1)))
    labels.append(dataset[i+target_size])

  return np.array(data), np.array(labels)


def train(
        csv_path: str,
        model,
        batch_size: int = 10,
        num_epochs: int = 5,
        past_history: int = 50,
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
    val_loss = history.history['val_loss']

    return loss, val_loss
