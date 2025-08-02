import pandas as pd
from sdv.metadata import MultiTableMetadata
from sdv.multi_table import HMASynthesizer

print("Starting synthetic data generation process...")

# --- Step 1: Define Seed Data In Memory ---
print("Creating seed data in memory...")

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

transactions_data = {
    'transaction_id': range(1, 11),
    'user_id': [1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
    'date': pd.to_datetime(['2023-01-05', '2023-01-10', '2023-01-15', '2023-01-20',
                            '2023-01-06', '2023-01-12', '2023-01-18', '2023-01-07',
                            '2023-01-14', '2023-01-21']),
    'amount': [-120.50, -45.00, 8000.00, -85.20, -250.00, -75.80, 5500.00, -60.00,
               -30.10, 3500.00],
    'category': ['Utilities', 'Groceries', 'Income', 'Entertainment', 'Auto', 'Groceries', 'Income', 'Utilities', 'Entertainment', 'Income']
}

score_history_data = {
    'score_id': range(1, 11),
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-01-01',
                            '2023-02-01', '2023-03-01', '2023-01-01', '2023-02-01',
                            '2023-03-01']),
    'score': [780, 785, 790,  # User 1 (Good)
              670, 665, 675,  # User 2 (Average)
              580, 570, 565]  # User 3 (High-risk)
}

# Convert dictionaries to pandas DataFrames
users_df = pd.DataFrame(users_data)
transactions_df = pd.DataFrame(transactions_data)
score_history_df = pd.DataFrame(score_history_data)

# Create the dictionary of DataFrames that SDV expects
seed_data = {
    'users': users_df,
    'transactions': transactions_df,
    'credit_score_history': score_history_df
}
print("Seed data created successfully.")

# --- Step 2: Define the Metadata ---
print("Defining metadata...")
metadata = MultiTableMetadata()
metadata.detect_from_dataframes(data=seed_data)  # Automatically detect schema

print("Metadata structure:")
print(metadata.to_dict())

# Remove manual relationship addition
# Relationships are already detected by `detect_from_dataframes()`

# Explicitly set the data types ('sdtypes') for specific columns
print("Updating column data types (sdtypes)...")
metadata.update_column(table_name='transactions', column_name='date', sdtype='datetime', datetime_format='%Y-%m-%d %H:%M:%S')
metadata.update_column(table_name='credit_score_history', column_name='date', sdtype='datetime', datetime_format='%Y-%m-%d %H:%M:%S')

print("Metadata definition complete.")

# --- Step 3: Train the Synthesizer ---
print("Training the HMASynthesizer... (This may take a moment)")
synthesizer = HMASynthesizer(metadata)
synthesizer.fit(seed_data)
print("Synthesizer training complete.")

# Generate synthetic data for individual tables

# Step 4: Generate the Synthetic Data ---
print("Generating synthetic data...")
synthetic_data = synthesizer.sample()  # No arguments needed for multi-table synthesizers
print("Synthetic data generated.")

# --- Step 5: Save the Output to CSV Files ---
synthetic_data['users'].to_csv('demo_users.csv', index=False)
synthetic_data['transactions'].to_csv('demo_transactions.csv', index=False)
synthetic_data['credit_score_history'].to_csv('demo_credit_score_history.csv', index=False)
# synthetic_users.to_csv('demo_users.csv', index=False)
# synthetic_transactions.to_csv('demo_transactions.csv', index=False)
# synthetic_score_history.to_csv('demo_credit_score_history.csv', index=False)

print("\nProcess complete! The following files have been created:")
print("- demo_users.csv")
print("- demo_transactions.csv")
print("- demo_credit_score_history.csv")