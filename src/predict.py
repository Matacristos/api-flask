import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from src.utils import univariate_data, get_test_data

def predict(
        csv_path: str,
        model,
        past_history: int = 72,
        future_target: int = 0,
        num_hours_past: int = 120
    ):

    data = pd.read_csv(csv_path, names=['Date', 'Close'])
    data = data.sort_values('Date')
    price = data[['Close']]

    # Normalize data
    min_max_scaler = MinMaxScaler()
    norm_data = min_max_scaler.fit_transform(price.values)

    _, y_test = univariate_data(norm_data,
                                int(len(norm_data) - num_hours_past),
                                None,
                                past_history,
                                future_target)

    x_test = get_test_data(norm_data,
                           int(len(norm_data) - num_hours_past),
                           past_history)
    
    original = pd.DataFrame(min_max_scaler.inverse_transform(y_test))
    predictions = pd.DataFrame(min_max_scaler.inverse_transform(model.predict(x_test)))

    ax = sns.lineplot(x=original.index, y=original[0], label="Real Data", color='royalblue')
    ax = sns.lineplot(x=predictions.index, y=predictions[0], label="Prediction", color='tomato')
    ax.set_title('Bitcoin price', size = 14, fontweight='bold')
    ax.set_xlabel("Hours", size = 14)
    ax.set_ylabel("Cost (USD)", size = 14)
    ax.set_xticklabels('', size=10)
    #ax.get_figure().savefig('../images/prediction.png')
    plt.savefig('../images/prediction.png')
    

