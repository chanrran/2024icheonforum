import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import font_manager, rc
import urllib.request

# GitHub에서 폰트 파일 다운로드 및 설정
font_url = 'https://raw.githubusercontent.com/chanrran/2024icheonforum/main/NanumGothic-Regular.ttf'
font_path = 'NanumGothic-Regular.ttf'
urllib.request.urlretrieve(font_url, font_path)

font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

# GitHub에서 CSV 파일 읽기
url = 'https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv'
df = pd.read_csv(url)

# 최상단 메시지 노출
st.markdown(f"""
    <style>
        .main-title {{
            font-size: 2rem;
            font-weight: bold;
            color: #f39c12;
            text-align: center;
        }}
        .data-summary {{
            font-size: 1.2rem;
            color: #ffffff;
            text-align: center;
            margin-bottom: 20px;
        }}
        .options-box {{
            background-color: #34495e;
            padding: 20px;
            border-radius: 10px;
        }}
        .button-container {{
            display: flex;
            justify-content: space-around;
        }}
        .stButton>button {{
            background-color: #3498db;
            color: white;
            font-size: 1rem;
            margin: 5px;
        }}
        .stButton>button:hover {{
            background-color: #2980b9;
        }}
    </style>
    <div class="main-title">
        이 서비스는 생성형 AI 공모전의 사례제출 현황을 분석하고 인사이트를 제공하기 위해 제작되었습니다.
    </div>
    <div class="data-summary">
        데이터를 통해 총 {df.shape[0]}건의 사례가 확인되었습니다.
    </div>
""", unsafe_allow_html=True)

# 옵션 선택 라디오 버튼 (오른쪽)
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown('<div class="options-box">', unsafe_allow_html=True)
    st.subheader("옵션")
    display_option = st.radio("표/그래프 선택", ["표", "그래프"], key='display_option')
    st.markdown('</div>', unsafe_allow_html=True)

# 데이터 분석 버튼들 (왼쪽)
with col1:
    st.subheader("데이터 분석")
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("회사별 건수"):
        st.session_state.selected_button = "company"

    if st.button("카테고리별 건수"):
        st.session_state.selected_button = "category"

    if st.button("수준별 건수"):
        st.session_state.selected_button = "level"
    st.markdown('</div>', unsafe_allow_html=True)

    selected_button = st.session_state.get('selected_button', None)

    # 버튼 클릭 상태 유지 및 스타일 변경
    def plot_barh_with_labels(ax, counts, xlabel, ylabel, title):
        ax.barh(counts.index, counts.values)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y() + .3, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')
        ax.invert_yaxis()

    if selected_button == "company":
        company_counts = df['Company'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(company_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_barh_with_labels(ax, company_counts, '건수', 'Company', 'Company별 건수')
            st.pyplot(fig)

    if selected_button == "category":
        category_counts = df['Category'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(category_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_barh_with_labels(ax, category_counts, '건수', '카테고리', '카테고리별 건수')
            st.pyplot(fig)

    if selected_button == "level":
        level_counts = df['Level'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(level_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots(figsize=(10, 8))
            plot_barh_with_labels(ax, level_counts, '건수', '수준', '수준별 건수')
            st.pyplot(fig)

# 주요 키워드 추출
if st.button("주요 키워드 추출"):
    keywords = df['Category'].dropna().apply(lambda x: re.findall(r'\b\w+\b', str(x))).sum()
    keyword_counts = Counter(keywords)
    top_keywords = keyword_counts.most_common(10)
    st.write(pd.DataFrame(top_keywords, columns=['키워드', '빈도수']))

# Wordcloud 만들기
if st.button("Wordcloud 만들기"):
    text = ' '.join(df['Title'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
