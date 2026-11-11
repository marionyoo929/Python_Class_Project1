import streamlit as st
import pandas as pd
from api import get_rest_api_data

st.title("Open API 데이터 조회")

# 화면이 열리면 바로 API를 호출한다.
try:
    rows = get_rest_api_data()
    df = pd.DataFrame(rows, columns=["id", "email", "zipcode", "lat", "lng"])
    st.dataframe(df, hide_index=True)
except Exception as e:
    st.error(f"데이터를 가져오지 못했습니다: {e}")
