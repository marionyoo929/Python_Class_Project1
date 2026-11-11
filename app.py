import requests
import streamlit as st
import pandas as pd


def get_rest_api_data():
    url = "https://rest-api-test-self.vercel.app/api/3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    rows = []
    for item in data:
        address = item["address"]
        geo = address["geo"]
        rows.append([
            item["id"],
            item["email"],
            item["first_name"],
            item["last_name"],
            item["avatar"],
            address["street"],
            address["city"],
            address["zipcode"],
            geo["lat"],
            geo["lng"],
        ])
    return rows


st.set_page_config(layout="wide")
st.title("Open API 데이터 조회")

try:
    rows = get_rest_api_data()
    df = pd.DataFrame(rows, columns=[
        "id", "email", "first_name", "last_name", "avatar",
        "street", "city", "zipcode", "lat", "lng"
    ])
    st.dataframe(df, hide_index=True, height=420)
except Exception as e:
    st.error(f"데이터를 가져오지 못했습니다: {e}")
