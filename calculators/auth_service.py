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
       financial_health= get_financial_health(username)
       return userScore, username,financial_health, None
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


 
# Load the CSV file
df = pd.read_csv(CSV_FILE)
 
def get_financial_health(username: str):
    """
    Calculate and return the financial health percentage for a specific user.
    """
    # Group by username to aggregate necessary metrics
    grouped = df.groupby("username").agg({
        "gross_monthly_income": "first",
        "total_monthly_debt_payments": "first",
        "total_credit_limit": "first",
        "late_payment_count": "first",
        "new_credit_inquiries_last_6m": "first",
        "score_of_last_month": "mean",
        "score_of_2_months_ago": "mean",
        "score_of_3_months_ago": "mean",
        "score_of_4_months_ago": "mean",
        "score_of_5_months_ago": "mean",
        "score_of_6_months_ago": "mean",
        "score_of_7_months_ago": "mean",
        "score_of_8_months_ago": "mean"
    }).reset_index()
 
    # Calculate average credit score
    score_columns = [
        "score_of_last_month", "score_of_2_months_ago", "score_of_3_months_ago",
        "score_of_4_months_ago", "score_of_5_months_ago", "score_of_6_months_ago",
        "score_of_7_months_ago", "score_of_8_months_ago"
    ]
    grouped["avg_credit_score"] = grouped[score_columns].mean(axis=1)
 
    # Normalize metrics to a 0-1 scale
    grouped["credit_score_norm"] = grouped["avg_credit_score"] / 850
    grouped["dti_ratio"] = grouped["total_monthly_debt_payments"] / grouped["gross_monthly_income"]
    grouped["credit_utilization"] = grouped["total_monthly_debt_payments"] / grouped["total_credit_limit"]
    grouped["late_payment_norm"] = 1 - (grouped["late_payment_count"] / grouped["late_payment_count"].max())
    grouped["inquiries_norm"] = 1 - (grouped["new_credit_inquiries_last_6m"] / grouped["new_credit_inquiries_last_6m"].max())
 
    # Calculate financial health score as weighted average
    grouped["financial_health_percent"] = (
        0.4 * grouped["credit_score_norm"] +
        0.2 * (1 - grouped["dti_ratio"]) +
        0.2 * (1 - grouped["credit_utilization"]) +
        0.1 * grouped["late_payment_norm"] +
        0.1 * grouped["inquiries_norm"]
    ) * 100
 
    # Filter for the specific user
    user_data = grouped[grouped["username"] == username]
 
    if user_data.empty:
        return f"User '{username}' not found."
    # Return the financial health percentage for the user
    financial_health = user_data["financial_health_percent"].iloc[0]
    return f"Financial Health for {username}: {financial_health:.2f}%"
 
