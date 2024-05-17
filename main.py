from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import requests
import logging

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Initialize Jinja2Templates for rendering HTML templates
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Render dashboard.html from templates
    return templates.TemplateResponse("dashboard.html", {"request": request})


# MongoDB connection
MONGODB_URI = "mongodb+srv://ghuelteves28:ghuel@api.30rmgjh.mongodb.net/"
client = AsyncIOMotorClient(MONGODB_URI)
db = client["API"]  # Replace "your_database_name" with your actual database name
collection = db["metal_prices"]  # Collection to store metal prices
users_collection = db["users"] 



class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: User):
    # Check if the username already exists
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Store the new user in the database
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)

    return JSONResponse(status_code=201, content={"message": "User registered successfully", "user_id": str(result.inserted_id)})


@app.post("/login")
async def login(user: User):
    # Check if the username exists
    existing_user = await users_collection.find_one({"username": user.username})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if the password is correct
    if user.password != existing_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return a JSON response indicating successful login
    return JSONResponse(content={"success": True})

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoint for serving the index.html page
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint for inserting a document into the collection
@app.post("/insert-document")
async def insert_document(data: dict):
    result = await collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

# API endpoint for fetching real-time metal price
@app.get("/price")
async def get_price(metal: str, currency: str):
    price = fetch_precious_metal_price(metal, currency)
    if price is not None:
        # Store data in MongoDB
        await store_price_in_db(metal, currency, price)
        return {"metal": metal, "price": price}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch price")

# API endpoint for fetching historical metal price
@app.get("/historical-price")
async def get_historical_price(metal: str, currency: str, date: str):
    historical_price = fetch_historical_precious_metal_price(metal, currency, date)
    if historical_price is not None:
        # Store data in MongoDB
        await store_historical_price_in_db(metal, currency, date, historical_price)
        return {"metal": metal, "currency": currency, "date": date, "price": historical_price}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch historical prices")


api="goldapi-53382uslw6krrux-io" #new api change this if 

# Helper function to fetch real-time precious metal price from external API
def fetch_precious_metal_price(metal_code, currency):
    api_url = f"https://www.goldapi.io/api/{metal_code}/{currency}"

    headers = {
        "x-access-token": api

    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        price = data.get("price")
        if price is not None:
            return price
        else:
            logger.error(f"Price key not found in response data: {data}")
            return None
    else:
        logger.error(f"Error fetching real-time price: {response.status_code} - {response.text}")
        return None

# Helper function to fetch historical precious metal prices from external API
def fetch_historical_precious_metal_price(metal_code, currency, date):
    api_url = f"https://www.goldapi.io/api/{metal_code}/{currency}/{date}"

    headers = {
        "x-access-token": api
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        price = data.get("price")
        if price is not None:
            return price
        else:
            logger.error(f"Price key not found in response data: {data}")
            return None
    else:
        logger.error(f"Error fetching historical price: {response.status_code} - {response.text}")
        return None

# Store real-time metal price in MongoDB
async def store_price_in_db(metal, currency, price):
    await collection.insert_one({"metal": metal, "currency": currency, "price": price})

# Store historical metal price in MongoDB
async def store_historical_price_in_db(metal, currency, date, price):
    await collection.insert_one({"metal": metal, "currency": currency, "date": date, "price": price})
