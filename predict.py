import numpy as np 
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

from utils import univariate_data

def predict(
        csv_path: str,
        model,
        past_history: int = 50,
        future_target: int = 0
    ):

    data = pd.read_csv(csv_path, names=['Date', 'Close'])
    data = data.sort_values('Date')
    price = data[['Close']]

    # Normalize data
    min_max_scaler = MinMaxScaler()
    norm_data = min_max_scaler.fit_transform(price.values)

    x_test, y_test = univariate_data(norm_data,
                                    len(norm_data) - past_history,
                                    None,
                                    past_history,
                                    future_target)
    
    original = pd.DataFrame(min_max_scaler.inverse_transform(y_test))
    predictions = pd.DataFrame(min_max_scaler.inverse_transform(model.predict(x_test)))

    ax = sns.lineplot(x=original.index, y=original[0], label="Real Data", color='royalblue')
    ax = sns.lineplot(x=predictions.index, y=predictions[0], label="Prediction", color='tomato')
    ax.set_title('Bitcoin price', size = 14, fontweight='bold')
    ax.set_xlabel("Hours", size = 14)
    ax.set_ylabel("Cost (USD)", size = 14)
    ax.set_xticklabels('', size=10)
    ax.save_fig('./images/prediction.png')
    

