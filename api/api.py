from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from calculators.auth_service import authenticate_user
from calculators.auth_service import calculate_credit_score
from models.ml_model import get_user_prediction
router = APIRouter()
class Credentials(BaseModel):
   username: str
   password: str

@router.post("/login")
def login(credentials: Credentials):
    userScore, username, financial_health,monthly_income, total_debt, payment_history, error = authenticate_user(credentials.username, credentials.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"username": username, "credit_score": userScore, "financial_health": financial_health, "monthly_income": monthly_income, "total_debt": total_debt, "payment_history": payment_history}  # Return both username and credit score

class UserData(BaseModel):
   gross_monthly_income:float
   total_monthly_debt_payments:float
   total_credit_limit:float
   credit_history_length_months:int
   new_credit_inquiries_last_6m:int
   late_payment_count:int

class UserPredictionInput(BaseModel):
    username: str  # Accept only the username as input


@router.post("/calculate_credit_score")
def calculate_credit_score_api(user_data: UserData):
    """
    API endpoint to calculate credit score.
    Expects JSON input with user data.
    """
    try:
        # Convert Pydantic model to dictionary and calculate credit score
        credit_score = calculate_credit_score(user_data.dict())
        return {"credit_score": credit_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/predict")
def predict_user_score(input_data: UserPredictionInput):
    """
    API endpoint to get user prediction.
    Expects JSON input with username.
    """
    try:
        # Call the get_user_prediction function with the username
        result  = get_user_prediction(input_data.username)
        if result is None:
            raise HTTPException(status_code=404, detail="Prediction could not be generated for the given username.")
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  