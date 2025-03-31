import requests
import json

cuisines = [
    "African",
    "Asian",
    "American",
    "British",
    "Cajun",
    "Caribbean",
    "Chinese",
    "Eastern European", 
    "European",
    "French",
    "German",
    "Greek",
    "Indian",
    "Irish",
    "Italian",
    "Japanese",
    "Jewish",
    "Korean",
    "Latin American",
    "Mediterranean",
    "Mexican",
    "Middle Eastern",
    "Nordic",
    "Southern",
    "Spanish",
    "Thai",
    "Vietnamese",
]
apiKey = ""
URL = "https://api.spoonacular.com/recipes/complexSearch?apiKey={apiKey}&addRecipeNutrition=True&addRecipeInstructions=True"
cuisine = "Vietnamese"

number=100
offset=0
totalResults = 1

while offset<totalResults:
    response = requests.get(f"{URL}&cuisine={cuisine}&number={number}&offset={offset}")
    data = response.json()
    totalResults = data["totalResults"]
    offset+=number

    with open(f"recipies_{cuisine.lower()}_{offset}.json","w") as f:
        json.dump(data,f,indent=4)
