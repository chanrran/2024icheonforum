import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="SK 이노베이션 포럼 대시보드", layout="wide")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv")

df = load_data()

# 사이드바
st.sidebar.title("SK 이노베이션 포럼")
st.sidebar.image("https://www.skchem.com/ko/img/logo_skchem.png", width=200)

# 메인 페이지
st.title("SK 이노베이션 포럼 대시보드")

# 1. 기본 통계
st.header("1. 기본 통계")
col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 프로젝트 수", len(df))
col2.metric("참여 회사 수", df['회사'].nunique())
col3.metric("주제 수", df['주제'].nunique())
col4.metric("사전평가 수준", df['사전평가'].nunique())

# 2. 주제별 분석
st.header("2. 주제별 분석")
fig_topic = px.pie(df, names='주제', title='주제별 프로젝트 분포')
fig_topic.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_topic, use_container_width=True)

# 3. 회사별 분석
st.header("3. 회사별 분석")
company_counts = df['회사'].value_counts()
fig_company = px.bar(company_counts, x=company_counts.index, y=company_counts.values, title='회사별 프로젝트 수')
st.plotly_chart(fig_company, use_container_width=True)

# 4. 사전평가 수준 분석
st.header("4. 사전평가 수준 분석")
fig_eval = px.pie(df, names='사전평가', title='사전평가 수준별 분포')
fig_eval.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_eval, use_container_width=True)

# 5. 워드 클라우드
st.header("5. 프로젝트 제목 워드 클라우드")
text = ' '.join(df['주제'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig_wc, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig_wc)

# 6. 프로젝트 검색 기능
st.header("6. 프로젝트 검색")
search_term = st.text_input("키워드 검색")
if search_term:
    filtered_df = df[df['주제'].str.contains(search_term, case=False) | 
                     df['성명'].str.contains(search_term, case=False) | 
                     df['회사'].str.contains(search_term, case=False)]
    st.dataframe(filtered_df)

# 7. 상세 프로젝트 정보
st.header("7. 상세 프로젝트 정보")
selected_project = st.selectbox("프로젝트 선택", df['주제'].tolist())
project_info = df[df['주제'] == selected_project].iloc[0]
st.write(f"성명: {project_info['성명']}")
st.write(f"회사: {project_info['회사']}")
st.write(f"주제: {project_info['주제']}")
st.write(f"사전평가: {project_info['사전평가']}")
if pd.notna(project_info['Playground']):
    st.markdown(f"[Playground 링크]({project_info['Playground']})")

# 9. 인터랙티브 필터링
st.header("9. 인터랙티브 필터링")
selected_company = st.multiselect("회사 선택", df['회사'].unique())
selected_topic = st.multiselect("주제 선택", df['주제'].unique())
selected_eval = st.multiselect("사전평가 수준 선택", df['사전평가'].unique())

filtered_df = df
if selected_company:
    filtered_df = filtered_df[filtered_df['회사'].isin(selected_company)]
if selected_topic:
    filtered_df = filtered_df[filtered_df['주제'].isin(selected_topic)]
if selected_eval:
    filtered_df = filtered_df[filtered_df['사전평가'].isin(selected_eval)]

st.dataframe(filtered_df)

# CSS를 사용하여 SK 브랜드 색상 적용
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stHeader {
        background-color: #EA5A24;
        color: white;
    }
    .stSidebar {
        background-color: #54565B;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
