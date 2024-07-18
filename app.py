import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="mySUNI 생성형 AI사례 공모전 분석", layout="wide")

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={'사전평가': '난이도'})
    df = df.dropna(subset=['회사', '주제', '난이도'])
    return df

# 메인 페이지
st.title("생성형 AI사례 공모전 결과 분석")

# 데이터 로드
df = load_data()

# 사이드바 필터
st.sidebar.title("mySUNI")
st.sidebar.header("데이터 필터")
selected_company = st.sidebar.multiselect("회사 선택", options=sorted(df['회사'].unique()), default=[])
selected_topic = st.sidebar.multiselect("주제 선택", options=sorted(df['주제'].unique()), default=[])
selected_difficulty = st.sidebar.selectbox("난이도 선택", options=['전체'] + sorted(df['난이도'].unique().tolist()))

# 데이터 필터링
filtered_df = df
if selected_company:
    filtered_df = filtered_df[filtered_df['회사'].isin(selected_company)]
if selected_topic:
    filtered_df = filtered_df[filtered_df['주제'].isin(selected_topic)]
if selected_difficulty != '전체':
    filtered_df = filtered_df[filtered_df['난이도'] == selected_difficulty]

# 기본 통계
st.header("기본 통계")
col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 프로젝트 수", len(filtered_df))
col2.metric("참여 회사 수", filtered_df['회사'].nunique())
col3.metric("주제 수", filtered_df['주제'].nunique())
col4.metric("난이도 분포", ', '.join(filtered_df['난이도'].value_counts().index))

# 주제별 분석
st.header("주제별 분석")
topic_counts = filtered_df['주제'].value_counts()
fig_topic = px.pie(values=topic_counts.values, names=topic_counts.index, title='주제별 프로젝트 분포')
fig_topic.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
fig_topic.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=16),
    title_font=dict(size=24),
    legend_font=dict(size=14)
)
st.plotly_chart(fig_topic, use_container_width=True)

# 회사별 분석
st.header("회사별 분석")
company_counts = filtered_df['회사'].value_counts()
fig_company = px.bar(x=company_counts.index, y=company_counts.values, title='회사별 프로젝트 수')
fig_company.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=16),
    title_font=dict(size=24),
    xaxis_title="회사",
    yaxis_title="프로젝트 수"
)
st.plotly_chart(fig_company, use_container_width=True)

# 프로젝트 목록
st.header("프로젝트 목록")
st.dataframe(filtered_df, use_container_width=True)

# CSS 스타일링
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    .stHeader {
        background-color: #2E2E2E;
        color: white;
    }
    .stSidebar {
        background-color: #2E2E2E;
        color: white;
    }
    .stDataFrame {
        background-color: #3E3E3E;
        color: white;
    }
    .stSelectbox, .stMultiSelect {
        background-color: #3E3E3E;
        color: white;
    }
    .stMarkdown, .stHeader, .stMetric {
        font-size: 18px !important;
    }
    .stMetric .metric-value {
        font-size: 24px !important;
    }
    h1, h2, h3 {
        font-size: 32px !important;
    }
</style>
""", unsafe_allow_html=True)
