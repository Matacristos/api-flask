from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense, LSTM, LeakyReLU, Dropout

def get_model(num_units: int = 64, learning_rate: float = 1e-4, activation_function: str = 'sigmoid'):
    adam = Adam(lr=learning_rate)
    loss_function = 'mse'
    #batch_size = 5
    #num_epochs = 50

    # Initialize the RNN
    model = Sequential()
    model.add(LSTM(units = num_units, activation=activation_function, input_shape=(None, 1)))
    model.add(LeakyReLU(alpha=0.5))
    model.add(Dropout(0.1))
    model.add(Dense(units = 1))

    # Compiling the RNN
    model.compile(optimizer=adam, loss=loss_function)

    return model