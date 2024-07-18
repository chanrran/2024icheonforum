import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import font_manager, rc
import urllib.request

# 페이지 설정
st.set_page_config(layout="wide")

# GitHub에서 폰트 파일 다운로드 및 설정
font_url = 'https://raw.githubusercontent.com/chanrran/2024icheonforum/main/NanumGothic-Regular.ttf'
font_path = 'NanumGothic-Regular.ttf'
urllib.request.urlretrieve(font_url, font_path)

font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

# GitHub에서 CSV 파일 읽기
url = 'https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv'
df = pd.read_csv(url)

# mySUNI ID 열을 제거
df = df.drop(columns=['mySUNI ID'], errors='ignore')

# 스타일 설정
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #f39c12;
        text-align: center;
        margin-bottom: 1rem;
    }
    .data-summary {
        font-size: 1.2rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-size: 1rem;
        margin: 5px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 및 설명
st.markdown('<div class="main-title">생성형 AI 공모전 사례 분석 서비스</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">이 서비스는 생성형 AI 공모전의 사례제출 현황을 분석하고 인사이트를 제공하기 위해 제작되었습니다.</div>', unsafe_allow_html=True)
st.markdown(f'<div class="data-summary">데이터를 통해 총 {df.shape[0]}건의 사례가 확인되었습니다.</div>', unsafe_allow_html=True)

# 옵션 선택 (상단으로 이동)
st.subheader("분석 옵션")
display_option = st.radio("표시 방식 선택:", ["표", "그래프"], key='display_option', horizontal=True)

# 데이터 분석 기능
st.subheader("데이터 분석")

def plot_barh_with_labels(counts, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(counts.index, counts.values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for i, v in enumerate(counts.values):
        ax.text(v + 0.1, i, str(v), va='center')
    ax.invert_yaxis()
    return fig

def show_data(data, title, x_label):
    if display_option == "표":
        st.write(data)
    elif display_option == "그래프":
        fig = plot_barh_with_labels(data, x_label, '', title)
        st.pyplot(fig)

if st.button("회사별 건수"):
    company_counts = df['Company'].value_counts().sort_values(ascending=False)
    show_data(company_counts, '회사별 건수', '건수')

if st.button("카테고리별 건수"):
    category_counts = df['Category'].value_counts().sort_values(ascending=False)
    show_data(category_counts, '카테고리별 건수', '건수')

if st.button("수준별 건수"):
    level_counts = df['Level'].value_counts().sort_values(ascending=False)
    show_data(level_counts, '수준별 건수', '건수')

if st.button("주요 키워드 추출"):
    keywords = df['Category'].dropna().apply(lambda x: re.findall(r'\b\w+\b', str(x))).sum()
    keyword_counts = Counter(keywords)
    top_keywords = keyword_counts.most_common(10)
    st.write(pd.DataFrame(top_keywords, columns=['키워드', '빈도수']))

if st.button("Wordcloud 만들기"):
    text = ' '.join(df['Title'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# 상세 검색 기능
st.subheader("상세 검색")
search_keyword = st.text_input("검색어를 입력하세요 (키워드, 회사명, 주제, 수준):")

if search_keyword:
    filtered_df = df[
        df.apply(lambda row: row.astype(str).str.contains(search_keyword, case=False).any(), axis=1)
    ]
    st.write(f"총 {filtered_df.shape[0]}건의 사례가 검색되었습니다.")
    st.dataframe(filtered_df[['Company', 'Title', 'Category', 'Level']])
