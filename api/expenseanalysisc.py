from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os

router = APIRouter()
CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csp.csv') # Update with actual path

@router.get("/api/expenses")
def get_expenses(username: str = Query(..., description="Username to fetch expense data for")):
    try:
        df = pd.read_csv(CSV_FILE)

        # Filter data for the given username
        user_df = df[df["username"] == username]

        if user_df.empty:
            raise HTTPException(status_code=404, detail="No data found for user")

        # Aggregate category-wise spending
        category_data = (
            user_df.groupby("transaction_category")["transaction_amount"]
            .sum()
            .abs()
            .reset_index()
        )

        total = category_data["transaction_amount"].sum()

        categories = []
        for _, row in category_data.iterrows():
            categories.append({
                "name": row["transaction_category"],
                "amount": float(row["transaction_amount"]),
                "percentage": round((row["transaction_amount"] / total) * 100, 2),
                "color": "#3b82f6",  # You can customize colors
                "trend": "stable",   # Placeholder
                "trendValue": 0      # Placeholder
            })

        # Monthly trend
        user_df["month"] = pd.to_datetime(user_df["transaction_date"]).dt.strftime("%b")
        monthly_data = (
            user_df.groupby("month")["transaction_amount"]
            .sum()
            .abs()
            .reset_index()
            .rename(columns={"transaction_amount": "amount"})
            .to_dict(orient="records")
        )

        return {
            "categories": categories,
            "monthly": monthly_data,
            "total": float(total)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
