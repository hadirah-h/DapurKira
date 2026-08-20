from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

# Home page
@app.get("/")
def home():
    """Display a welcome message"""
    app_name = "DapurKira"

    return {"message": f" 👩🏻‍🍳 Welcome to {app_name}! 👩🏻‍🍳"}

