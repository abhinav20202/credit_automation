from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router
from api.expenseanalysisc import router as expense_router

app = FastAPI()


#CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(expense_router)
 