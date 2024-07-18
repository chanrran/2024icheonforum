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
    df = pd.read_csv("https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv")
    # NaN 값을 가진 행 제거
    df = df.dropna()
    # '사전평가' 컬럼명을 '난이도'로 변경
    df = df.rename(columns={'사전평가': '난이도'})
    return df

df = load_data()

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
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전체 프로젝트 수", len(filtered_df))
    col2.metric("참여 회사 수", filtered_df['회사'].nunique())
    col3.metric("주제 수", filtered_df['주제'].nunique())
    # '난이도' 컬럼의 데이터 타입 확인 및 처리
    if pd.api.types.is_numeric_dtype(filtered_df['난이도']):
        col4.metric("평균 난이도", filtered_df['난이도'].mean().round(2))
    else:
        col4.metric("난이도 분포", ', '.join(filtered_df['난이도'].value_counts().index))

with tab2:
    st.header("주제별 분석")
    topic_counts = filtered_df['주제'].value_counts()
    if not topic_counts.empty:
        fig_topic = px.pie(values=topic_counts.values, names=topic_counts.index, title='주제별 프로젝트 분포')
        fig_topic.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_topic, use_container_width=True)
    else:
        st.write("주제별 분석을 위한 데이터가 충분하지 않습니다.")

with tab3:
    st.header("회사별 분석")
    company_counts = filtered_df['회사'].value_counts()
    if not company_counts.empty:
        fig_company = px.bar(x=company_counts.index, y=company_counts.values, title='회사별 프로젝트 수')
        fig_company.update_layout(xaxis_title="회사", yaxis_title="프로젝트 수")
        st.plotly_chart(fig_company, use_container_width=True)
    else:
        st.write("회사별 분석을 위한 데이터가 충분하지 않습니다.")

with tab4:
    st.header("프로젝트 제목 워드 클라우드")
    if not filtered_df.empty:
        text = ' '.join(filtered_df['주제'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig_wc, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig_wc)
    else:
        st.write("워드 클라우드 생성을 위한 데이터가 충분하지 않습니다.")

# 프로젝트 목록
st.header("프로젝트 목록")
if st.checkbox("프로젝트 목록 표시"):
    st.dataframe(filtered_df)

# 상세 프로젝트 정보
st.header("상세 프로젝트 정보")
if not filtered_df.empty:
    selected_project = st.selectbox("프로젝트 선택", filtered_df['주제'].tolist())
    project_info = filtered_df[filtered_df['주제'] == selected_project].iloc[0]
    st.write(f"성명: {project_info['성명']}")
    st.write(f"회사: {project_info['회사']}")
    st.write(f"주제: {project_info['주제']}")
    st.write(f"난이도: {project_info['난이도']}")
    if pd.notna(project_info['Playground']) and project_info['Playground'] != '':
        st.markdown(f"[Playground 링크]({project_info['Playground']})")
else:
    st.write("상세 정보를 표시할 프로젝트가 없습니다.")

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
