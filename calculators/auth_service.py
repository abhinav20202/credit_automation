import pandas as pd
import os

CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csp.csv')

def authenticate_user(username: str, password: str):
   try:
       df = pd.read_csv(CSV_FILE)
   except FileNotFoundError:
       return None, "CSV file not found"
   user_row = df[(df['username'] == username) & (df['password'] == password)]
   if not user_row.empty:
       userScore = calculate_credit_score(user_row.iloc[0].to_dict())
       return userScore, username, None
   else:
       return None, "Invalid username or password"


def calculate_credit_score(user_data: dict) -> int:
    """
    Calculate the credit score based on user data.
    :param user_data: Dictionary containing user information.
    :return: Calculated credit score (integer).
    """
    # Extract relevant data
    income = user_data.get('gross_monthly_income', 0)
    debt_payments = user_data.get('total_monthly_debt_payments', 0)
    credit_limit = user_data.get('total_credit_limit', 0)
    credit_history_length = user_data.get('credit_history_length_months', 0)
    late_payments = user_data.get('late_payment_count', 0)
    inquiries = user_data.get('new_credit_inquiries_last_6m', 0)

    # Calculate debt-to-income ratio
    debt_to_income_ratio = (debt_payments / income) if income > 0 else 1

    # Calculate credit utilization
    credit_utilization = (debt_payments / credit_limit) if credit_limit > 0 else 1

    # Base score
    score = 900  # Start with a perfect score

    # Adjust score based on factors
    score -= debt_to_income_ratio * 100  # Penalize high debt-to-income ratio
    score -= credit_utilization * 100  # Penalize high credit utilization
    score -= late_payments * 50  # Penalize late payments
    score -= inquiries * 10  # Penalize recent credit inquiries
    score += credit_history_length * 2  # Reward longer credit history

    # Ensure score is within range
    score = max(300, min(850, int(score)))  # Credit scores typically range from 300 to 850

    return score, credit_utilization, debt_to_income_ratio      