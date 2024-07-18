import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="mySUNI 생성형 AI사례 공모전 분석", layout="wide")

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv")
        # NaN 값을 가진 행 제거
        df = df.dropna()
        # '사전평가' 컬럼명을 '난이도'로 변경
        df = df.rename(columns={'사전평가': '난이도'})
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

# 데이터가 비어있는지 확인
if df.empty:
    st.warning("데이터를 불러오는 데 실패했습니다. 잠시 후 다시 시도해주세요.")
    st.stop()

# 사이드바 설정
st.sidebar.title("mySUNI")
st.sidebar.header("데이터 필터")

# 사이드바 필터
selected_company = st.sidebar.multiselect("회사 선택", df['회사'].unique())
selected_topic = st.sidebar.multiselect("주제 선택", df['주제'].unique())
selected_difficulty = st.sidebar.selectbox("난이도 선택", ['전체'] + list(df['난이도'].unique()))

# 데이터 필터링
filtered_df = df
if selected_company:
    filtered_df = filtered_df[filtered_df['회사'].isin(selected_company)]
if selected_topic:
    filtered_df = filtered_df[filtered_df['주제'].isin(selected_topic)]
if selected_difficulty != '전체':
    filtered_df = filtered_df[filtered_df['난이도'] == selected_difficulty]

# 메인 페이지
st.title("생성형 AI사례 공모전 결과 분석")
st.write("이 대시보드는 생성형 AI사례 공모전의 결과 데이터를 분석하고 시각화합니다.")

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["기본 통계", "주제 분석", "회사별 분석", "워드 클라우드"])

with tab1:
    st.header("기본 통계")
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("전체 프로젝트 수", len(filtered_df))
        col2.metric("참여 회사 수", filtered_df['회사'].nunique())
        col3.metric("주제 수", filtered_df['주제'].nunique())
        if pd.api.types.is_numeric_dtype(filtered_df['난이도']):
            col4.metric("평균 난이도", filtered_df['난이도'].mean().round(2))
        else:
            col4.metric("난이도 분포", ', '.join(filtered_df['난이도'].value_counts().index))
    else:
        st.write("표시할 데이터가 없습니다.")

# 나머지 탭들의 코드는 이전과 동일하게 유지...

# CSS를 사용하여 mySUNI 브랜드 색상 적용
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stHeader {
        background-color: #00A6D4;
        color: white;
    }
    .stSidebar {
        background-color: #003A59;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
