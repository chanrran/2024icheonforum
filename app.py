import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="mySUNI 생성형 AI사례 공모전 분석", layout="wide")

# 데이터 로드
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv"
    df = pd.read_csv(url)
    return df

# 메인 페이지
st.title("생성형 AI사례 공모전 결과 분석")

# 데이터 로드 시도
try:
    df = load_data()
    st.success("데이터 로드 성공")
    st.write(df.head())  # 데이터 샘플 표시
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {e}")
