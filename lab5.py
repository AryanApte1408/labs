# # lab5.py — Lab 5: The What to Wear Bot
# import os
# import requests
# import streamlit as st
# from openai import OpenAI

# # ========================= Helpers =========================
# def _get_openai_api_key() -> str | None:
#     try:
#         return st.secrets["OPENAI_API_KEY"]
#     except Exception:
#         pass
#     try:
#         from dotenv import load_dotenv
#         load_dotenv()
#     except Exception:
#         pass
#     return os.getenv("OPENAI_API_KEY")

# def _get_openweather_api_key() -> str | None:
#     try:
#         return st.secrets["OPENWEATHER_API_KEY"]
#     except Exception:
#         pass
#     return os.getenv("OPENWEATHER_API_KEY")

# def get_current_weather(location: str, API_key: str) -> dict:
#     """Fetch weather data from OpenWeather API for a given city."""
#     if "," in location:
#         location = location.split(",")[0].strip()

#     url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_key}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return {"error": f"Failed to fetch weather for {location}: {response.text}"}

#     data = response.json()
#     try:
#         temp = data['main']['temp'] - 273.15
#         feels_like = data['main']['feels_like'] - 273.15
#         temp_min = data['main']['temp_min'] - 273.15
#         temp_max = data['main']['temp_max'] - 273.15
#         humidity = data['main']['humidity']
#         description = data['weather'][0]['description']
#     except KeyError:
#         return {"error": f"Unexpected response format: {data}"}

#     return {
#         "location": location,
#         "temperature": round(temp, 2),
#         "feels_like": round(feels_like, 2),
#         "temp_min": round(temp_min, 2),
#         "temp_max": round(temp_max, 2),
#         "humidity": humidity,
#         "description": description,
#     }

# # ========================= App Config =========================
# st.set_page_config(page_title="Lab 5 — What to Wear Bot", layout="centered")
# st.title("Lab 5 — The What to Wear Bot")

# # ========================= API Keys =========================
# openai_api_key = _get_openai_api_key()
# weather_api_key = _get_openweather_api_key()

# if not openai_api_key or not weather_api_key:
#     st.error("Missing API keys. Please add `OPENAI_API_KEY` and `OPENWEATHER_API_KEY` to Streamlit Secrets.")
#     st.stop()

# client = OpenAI(api_key=openai_api_key)

# # ========================= UI =========================
# city = st.text_input("Enter a city:", "Syracuse, NY")

# if st.button("Get Clothing Suggestion"):
#     weather = get_current_weather(city, weather_api_key)

#     if "error" in weather:
#         st.error(weather["error"])
#         st.stop()

#     st.write(f"**Weather in {weather['location']}**")
#     st.write(
#         f"{weather['temperature']}°C (feels like {weather['feels_like']}°C), "
#         f"low {weather['temp_min']}°C / high {weather['temp_max']}°C, "
#         f"humidity {weather['humidity']}%, conditions: {weather['description']}"
#     )

#     # Ask the LLM for clothing & picnic advice
#     prompt = f"""
#     The weather today in {weather['location']} is:
#     - Temperature: {weather['temperature']}°C
#     - Feels like: {weather['feels_like']}°C
#     - Low: {weather['temp_min']}°C, High: {weather['temp_max']}°C
#     - Humidity: {weather['humidity']}%
#     - Conditions: {weather['description']}

#     Based on this, suggest what clothes someone should wear today,
#     and whether it’s a good day for a picnic.
#     """

#     with st.spinner("Thinking..."):
#         resp = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#         )
#         suggestion = resp.choices[0].message.content

#     st.subheader("👕 Clothing & Picnic Suggestion")
#     st.write(suggestion)


# lab5.py — Lab 5: The What to Wear Bot (GPT-5-nano + Gemini 2.5-pro)
import os
import requests
import streamlit as st
from openai import OpenAI
import google.generativeai as genai

# ========================= Helpers =========================
def _get_openai_api_key() -> str | None:
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")

def _get_openweather_api_key() -> str | None:
    try:
        return st.secrets["OPENWEATHER_API_KEY"]
    except Exception:
        return os.getenv("OPENWEATHER_API_KEY")

def _get_gemini_api_key() -> str | None:
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")

def get_current_weather(location: str, API_key: str) -> dict:
    """Fetch weather data from OpenWeather API for a given city."""
    if "," in location:
        location = location.split(",")[0].strip()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch weather for {location}: {response.text}"}

    data = response.json()
    try:
        temp = data['main']['temp'] - 273.15
        feels_like = data['main']['feels_like'] - 273.15
        temp_min = data['main']['temp_min'] - 273.15
        temp_max = data['main']['temp_max'] - 273.15
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
    except KeyError:
        return {"error": f"Unexpected response format: {data}"}

    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": humidity,
        "description": description,
    }

# ========================= App Config =========================
st.set_page_config(page_title="Lab 5 — What to Wear Bot", layout="centered")
st.title("Lab 5 — The What to Wear Bot")

# ========================= API Keys =========================
openai_api_key = _get_openai_api_key()
weather_api_key = _get_openweather_api_key()
gemini_api_key = _get_gemini_api_key()

if not weather_api_key:
    st.error("Missing OPENWEATHER_API_KEY in secrets.")
    st.stop()

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# ========================= UI =========================
llm_choice = st.selectbox("Choose an LLM:", ["OpenAI (GPT-5-nano)", "Gemini (Gemini-2.5-pro)"])
city = st.text_input("Enter a city:", "Syracuse, NY")

if st.button("Get Clothing Suggestion"):
    weather = get_current_weather(city, weather_api_key)

    if "error" in weather:
        st.error(weather["error"])
        st.stop()

    st.write(f"**Weather in {weather['location']}**")
    st.write(
        f"{weather['temperature']}°C (feels like {weather['feels_like']}°C), "
        f"low {weather['temp_min']}°C / high {weather['temp_max']}°C, "
        f"humidity {weather['humidity']}%, conditions: {weather['description']}"
    )

    prompt = f"""
    The weather today in {weather['location']} is:
    - Temperature: {weather['temperature']}°C
    - Feels like: {weather['feels_like']}°C
    - Low: {weather['temp_min']}°C, High: {weather['temp_max']}°C
    - Humidity: {weather['humidity']}%
    - Conditions: {weather['description']}

    Based on this, suggest what clothes someone should wear today,
    and whether it’s a good day for a picnic.
    """

    suggestion = None
    with st.spinner("Thinking..."):
        if "OpenAI" in llm_choice and openai_client:
            resp = openai_client.chat.completions.create(
                model="gpt-5-nano",
                messages=[{"role": "user", "content": prompt}],
            )
            suggestion = resp.choices[0].message.content

        elif "Gemini" in llm_choice and gemini_api_key:
            model = genai.GenerativeModel("gemini-2.5-pro")
            resp = model.generate_content(prompt)
            suggestion = resp.text

        else:
            st.error("No valid API key for the chosen LLM.")

    if suggestion:
        st.subheader("👕 Clothing & Picnic Suggestion")
        st.write(suggestion)
