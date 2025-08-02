import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
import os

# Suppress warnings from ARIMA to keep the output clean
warnings.filterwarnings("ignore")

CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csp.csv')

# Load the data from csp.csv
df = pd.read_csv(CSV_FILE)

# The score columns are already provided for the last 8 months.
# We list them here in chronological order for the time series model.
score_columns = [
    'score_of_8_months_ago',
    'score_of_7_months_ago',
    'score_of_6_months_ago',
    'score_of_5_months_ago',
    'score_of_4_months_ago',
    'score_of_3_months_ago',
    'score_of_2_months_ago',
    'score_of_last_month'
]

def _forecast_user_scores(user_scores):
    """
    Forecasts credit scores for a single user using an ARIMA model.
    """
    # Convert scores to float type for the model.
    train_data = user_scores.astype(float)

    # The ARIMA model can sometimes fail if the data isn't suitable.
    # A try-except block will handle these cases gracefully.
    try:
        # We use an ARIMA model with order (1, 1, 1), which is a common starting point.
        # This can be tuned for better performance if needed.
        model = ARIMA(train_data, order=(1, 1, 1))
        model_fit = model.fit()

        # Forecast the scores for the next two months.
        forecast = model_fit.forecast(steps=2)
        return forecast
    except Exception as e:
        # If forecasting fails for a user, we return None.
        # print(f"Could not process user. Reason: {e}")
        return None

def get_user_prediction(username: str):
    """
    This function receives a username and returns its prediction for that user's next two month's score.
    """
    # User data is repeated for each transaction, so we'll create a dataframe
    # with unique users to work with their scores.
    user_df = df.drop_duplicates(subset=['username']).copy()
    user_df.set_index('username', inplace=True)

    # Check if the user exists in the dataset
    if username not in user_df.index:
        return f"User '{username}' not found."

    # We select just the score columns to create our time series data for the user.
    user_scores = user_df.loc[username][score_columns]

    # Generate the forecast for the specified user
    forecasted_scores = _forecast_user_scores(user_scores)

    if forecasted_scores is not None:
        prediction = {
            "next_month_score": round(forecasted_scores.iloc[0], 2),
            "following_month_score": round(forecasted_scores.iloc[1], 2)
        }
        return prediction
    else:
        return "Could not generate a forecast for the user."
