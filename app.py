import streamlit as st
import requests

BASE_URL = "https://taxifare-api-x4gzhnh2ta-uw.a.run.app"

st.write("""
         # NYC TaxiFare Predictor 🚕
         """)

st.write("""
         Please input your trip info
         """)

def get_coords(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    res = requests.get(url).json()
    if res:
        return res[0]['lat'], res[0]['lon']

p_ad = st.text_input('Pickup Address')
if p_ad:
    p_lat, p_lon = get_coords(p_ad)
  
d_ad = st.text_input('Dropoff Address')
if d_ad:
    d_lat, d_lon = get_coords(d_ad)

pas = st.slider("How many passengers?", 1, 6)
p_d = st.date_input('Trip date')
p_t = st.time_input('Trip time')
p_dt = str(p_d) + " " + str(p_t)

all_inputs = p_ad and d_ad and pas and p_dt

if all_inputs:
    new_trip = dict(
                    pickup_latitude=p_lat,
                    pickup_longitude=p_lon,
                    dropoff_latitude=d_lat,
                    dropoff_longitude=d_lon,
                    pickup_datetime=p_dt,
                    passenger_count=pas
                    )

pred_clicked = st.button('Predict!')
if pred_clicked:
    res = requests.get(BASE_URL + "/predict", params=new_trip)
    if res.status_code == 200:
        prediction = res.json()['fare']
        st.write(f"""
                # Your cab cost: {round(prediction, 2)}USD
                """)
    else:
        st.write('Sorry, something went wrong!')