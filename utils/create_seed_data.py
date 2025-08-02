import pandas as pd
import numpy as np

# --- Create seed_users.csv ---
users_data = {
    'user_id': [1, 2, 3],
    'username': ['user1', 'user2', 'user3'],
    'password': ['password', 'password', 'password'],
    'gross_monthly_income': [20000, 30000, 40000],
    'total_monthly_debt_payments': [2500, 3500, 4500],
    'total_credit_limit': [100000, 150000, 120000],
    'credit_history_length_months': [24, 36, 12],
    'new_credit_inquiries_last_6m': [2, 1, 3],
    'late_payment_count': [0, 1, 2]
}
users_df = pd.DataFrame(users_data)
users_df.to_csv('seed_users.csv', index=False)
print("seed_users.csv created.")

# --- Create seed_transactions.csv ---
transactions_data = {
    'transaction_id': range(1, 11),
    'user_id': [1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
    'date': pd.to_datetime(['2023-01-05', '2023-01-10', '2023-01-15', '2023-01-20',
                            '2023-01-06', '2023-01-12', '2023-01-18', '2023-01-07',
                            '2023-01-14', '2023-01-21']),
    'amount': [-120.50, -45.00, 5000.00, -85.20, -250.00, -75.80, 7500.00, -60.00,
               -30.10, 4200.00],
    'category': ['groceries', 'transport', 'salary', 'entertainment', 'groceries',
                 'transport', 'salary', 'groceries', 'transport', 'salary']
}
transactions_df = pd.DataFrame(transactions_data)
transactions_df.to_csv('seed_transactions.csv', index=False)
print("seed_transactions.csv created.")

# --- Create seed_credit_score_history.csv ---
score_history_data = {
    'score_id': range(1, 10),
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-01-01',
                            '2023-02-01', '2023-03-01', '2023-01-01', '2023-02-01',
                            '2023-03-01']),
    'score': [750, 760, 770, 680, 690, 700, 620, 630, 640]
}
score_history_df = pd.DataFrame(score_history_data)
score_history_df.to_csv('seed_credit_score_history.csv', index=False)
print("seed_credit_score_history.csv created.")