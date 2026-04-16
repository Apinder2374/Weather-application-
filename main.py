from tkinter import *
import requests
import geocoder
from dotenv import load_dotenv
import os
load_dotenv()

# ------- Getting the current lat and lon with error handling ---------------------------------------------------
try:
    g = geocoder.ip('me') # to get location through IP address. 
    if g.ok and g.latlng:
        lat, lng = g.latlng
    else:
        raise Exception("Could not get location from IP")
except Exception as e:
    print(f"Error obtaining geolocation: {e}")
    lat, lng = 0, 0  # Default to 0,0 or set fixed coordinates

# --------Getting weather details with error handling-----------------------------------------------------------
API_KEY = os.getenv("API_KEY")
link = "https://api.openweathermap.org/data/2.5/forecast?" # link to the api 
api_key = API_KEY # api key 
parameters = {"lat": lat,
              "lon": lng,
              "cnt": 4,
              "appid": api_key} # parameters 

try:
    response = requests.get(link, params=parameters) # getting the information out of the API 
    response.raise_for_status()
    data = response.json()
    weather_type = data.get("list", []) 
    if not weather_type:
        raise Exception("No weather data found")
except Exception as e:
    print(f"Error fetching weather data: {e}")
    weather_type = []

# ------- Extract data (check if weather_type is populated) ---------------------------------------------------------
weather_items = [t["weather"][0]["description"].capitalize() for t in weather_type] if weather_type else [""]*4
temp_list = [round(t["main"]["temp"] - 273.15, 2) for t in weather_type] if weather_type else [0]*4
feels_list = [round(t["main"]["feels_like"] - 273.15, 2) for t in weather_type] if weather_type else [0]*4
min_list = [round(t["main"]["temp_min"] - 273.15, 2) for t in weather_type] if weather_type else [0]*4
max_list = [round(t["main"]["temp_max"] - 273.15, 2) for t in weather_type] if weather_type else [0]*4
time_list = [t["dt_txt"][11:16] for t in weather_type] if weather_type else [""]*4

# ------ Setting up Tkinter Window -----------------------------------------------------------------
window = Tk()
window.title("Weather Application")
window.geometry("600x600")
window.config(bg="lightblue", padx=20, pady=20)

# -------- Relative Image Paths (adjust folder path accordingly) ----------------------------------------------------
image_folder = "/Users/Apinder's PC/OneDrive/Desktop/Weather Application/Weather pics/"

ClearSky_image_path = PhotoImage(file=image_folder + "ClearSkyday.png")
FewCloudsDay_image_path = PhotoImage(file=image_folder + "FewCloudsDay.png")
FewCloudsNight_image_path = PhotoImage(file=image_folder + "FewCloudsNight.png")
ScatteredClouds_image_path = PhotoImage(file=image_folder + "ScatteredClouds.png")
BrokenClouds_image_path = PhotoImage(file=image_folder + "BrokenClouds.png")
ShowerRain_image_path = PhotoImage(file=image_folder + "ShowerRain.png")
RainDay_image_path = PhotoImage(file=image_folder + "RainDay.png")
RainNight_image_path = PhotoImage(file=image_folder + "RainNight.png")
Thunderstorm_image_path = PhotoImage(file=image_folder + "Thunderstorm.png")
Snow_image_path = PhotoImage(file=image_folder + "Snow.png")
Mist_image_path = PhotoImage(file=image_folder + "Mist.png")

# ------ Mapping weather conditions to images ------------------------------------------------------
weather_images = {
    "clear sky": ClearSky_image_path,
    "few clouds": FewCloudsDay_image_path,       # Customize day/night if needed
    "scattered clouds": ScatteredClouds_image_path,
    "broken clouds": BrokenClouds_image_path,
    "shower rain": ShowerRain_image_path,
    "rain": RainDay_image_path,
    "thunderstorm": Thunderstorm_image_path,
    "snow": Snow_image_path,
    "mist": Mist_image_path,
}



# ------ Create canvas widgets dynamically -----------------------------------------------------------
canvases = []
for i in range(4):
    c = Canvas(width=100, height=100, bg="lightblue", highlightthickness=0)
    c.grid(column=i+1, row=1, pady=10)
    canvases.append(c)

# ------ Assign weather icons to canvases dynamically -----------------------------------------------
for i, weather_desc in enumerate(weather_items):
    desc_key = weather_desc.lower()
    img = None
    for key in weather_images:
        if key in desc_key:
            img = weather_images[key]
            break
    if img is None:
        img = ClearSky_image_path
    canvases[i].create_image(50, 50, image=img)

# ------ City Label --------------------------------------------------------------------------
city_label = Label(text=f"{g.state if g.ok else 'Unknown Location'}", bg="lightblue", fg="black", font=("Arial", 30))
city_label.grid(column=2, row=0, padx=10)

# ------ Header labels for columns -----------------------------------------------------------
header_texts = ["Weather", "Time", "Temperature", "Feels Like", "Minimum", "Maximum"]
for idx, text in enumerate(header_texts):
    Label(text=text, bg="lightblue", fg="black", font=("Arial", 12, "bold")).grid(column=0, row=2 + idx, pady=10, padx=10)

# ------ Weather description labels ---------------------------------------------------------
for i in range(4):
    Label(text=weather_items[i], bg="lightblue", fg="black", font=("Arial", 10)).grid(column=i+1, row=2, pady=10, padx=10)

# ------ Time labels --------------------------------------------------------------------------
for i in range(4):
    Label(text=time_list[i], bg="lightblue", fg="black", font=("Arial", 10)).grid(column=i+1, row=3, pady=10, padx=10)

# ------ Temperatures labels -------------------------------------------------------------------
def add_temp_labels(data_list, row_num):
    for i in range(4):
        Label(text=f"{data_list[i]}°C", bg="lightblue", fg="black", font=("Arial", 10)).grid(column=i+1, row=row_num, pady=10, padx=10)

add_temp_labels(temp_list, 4)
add_temp_labels(feels_list, 5)
add_temp_labels(min_list, 6)
add_temp_labels(max_list, 7)

window.mainloop()
