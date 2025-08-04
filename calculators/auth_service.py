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
       user_data = user_row.iloc[0]
       userScore = calculate_credit_score(user_row.iloc[0].to_dict())
       financial_health= get_financial_health(username)
       payment_history = get_user_payment_history_ratio(username)
       print(payment_history)
       monthly_income = float(user_data['gross_monthly_income'])
       total_debt = float(user_data['total_monthly_debt_payments'])
       print(username, userScore, financial_health, monthly_income, total_debt)

       return userScore, username,financial_health,monthly_income, total_debt,payment_history, None
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
 
    # Normalize values
 
    utilization = (debt_payments / credit_limit) if credit_limit else 1
 
    credit_history_years = credit_history_length / 12
 
    # Base score
 
    score = 300
 
    # 1. Payment History (35% - fewer late payments = better)
 
    if late_payments == 0:
 
        score += 175 * 1  # Full score
 
    elif late_payments <= 2:
 
        score += 175 * 0.8
 
    elif late_payments <= 5:
 
        score += 175 * 0.5
 
    else:
 
        score += 175 * 0.2
 
    # 2. Credit Utilization (30% - lower is better)
 
    if utilization < 0.1:
 
        score += 150 * 1
 
    elif utilization < 0.3:
 
        score += 150 * 0.8
 
    elif utilization < 0.5:
 
        score += 150 * 0.5
 
    else:
 
        score += 150 * 0.2
 
    # 3. Credit History Length (15% - longer is better)
 
    if credit_history_years >= 10:
 
        score += 75 * 1
 
    elif credit_history_years >= 5:
 
        score += 75 * 0.7
 
    elif credit_history_years >= 2:
 
        score += 75 * 0.4
 
    else:
 
        score += 75 * 0.1
 
    # 4. Credit Inquiries (10% - fewer is better)
 
    if inquiries == 0:
 
        score += 50 * 1
 
    elif inquiries <= 2:
 
        score += 50 * 0.7
 
    elif inquiries <= 5:
 
        score += 50 * 0.4
 
    else:
 
        score += 50 * 0.1
 
    # 5. Credit Limit Availability (10% - higher is better)
 
    if credit_limit >= 100000:
 
        score += 50 * 1
 
    elif credit_limit >= 50000:
 
        score += 50 * 0.7
 
    elif credit_limit >= 20000:
 
        score += 50 * 0.4
 
    else:
 
        score += 50 * 0.1
 
    # Final score capping
 
    score =  min(850, max(300, int(score)))
    debt_to_income_ratio = (debt_payments / income) if income > 0 else 1
 
    # 
    return score, debt_to_income_ratio, utilization, credit_history_years
    
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
    return(int(financial_health))
 
def get_user_payment_history_ratio(username: str) -> float | None:
    """
    Calculates the payment history ratio for a specific user from the CSV file.
 
    The ratio is calculated as: on_time_payments / (on_time_payments + late_payment_count).
    A higher ratio indicates a better payment history.
 
    Args:
        username (str): The username for whom to calculate the payment history ratio.
 
    Returns:
        float: The payment history ratio for the user (between 0.0 and 1.0).
               Returns None if the user is not found or an error occurs.
    """
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Error: The file at {CSV_FILE} was not found.")
        return None
 
    # Filter for the specific user's data to improve efficiency
    user_df = df[df['username'] == username]
 
    if user_df.empty:
        # Return None if the username does not exist in the DataFrame
        return None
 
    # Define payment-related categories
    payment_categories = [
        'Mortgage', 'Auto Loan', 'Rent', 'Student Loan',
        'Credit Card Payment', 'Personal Loan'
    ]
 
    # Filter for payment transactions for that user
    payments_df = user_df[user_df['transaction_category'].isin(payment_categories)]
 
    # Count the number of on-time payments for the user
    on_time_payments_count = len(payments_df)
 
    # Get the late payment count for the user (it's the same in all their rows)
    # .iloc[0] is used to get the value from the first row of the user's data
    late_payment_count = user_df['late_payment_count'].iloc[0]
 
    # Calculate the total number of payments
    total_payments = on_time_payments_count + late_payment_count
 
    if total_payments == 0:
        # If there are no recorded payments, assume a perfect history
        return 1.0
 
    # Calculate and return the payment history ratio
    ratio = on_time_payments_count / total_payments
    return ratio