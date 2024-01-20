import streamlit as st
from streamlit_js_eval import get_geolocation, get_page_location, get_cookie, set_cookie

st.code("""https://aghasemi-streamlit-js-eval-example-yleu91.streamlit.app/""")
# save the location
if 'location' not in st.session_state:
    st.session_state.location = None

st.write(st.session_state)
st.write("Cookie location is:", get_cookie('location'))


page_location = get_page_location()
st.write("Your page location is:", page_location)
def print_star():
    st.write("🌟")

btn_get_geolocation = st.button("Get geolocation", key="btn_get_geolocation", on_click=print_star)

if btn_get_geolocation:
    location = get_geolocation()
    st.write("Your location is:", location)


    set_cookie('location', location, 1)
    st.write("Cookie set")

    st.write("Cookie location is:", get_cookie('location'))

