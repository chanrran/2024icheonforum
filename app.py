import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import rc

# 한글 폰트 설정
st.set_page_config(layout="wide")
rc('font', family='NanumGothic')

# 파일 업로드
uploaded = st.file_uploader("파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    # CSV 파일 로드
    df = pd.read_csv(uploaded)
    
    # 데이터 요약
    st.write(f"총 {df.shape[0]}건의 데이터가 확인되었습니다.")

    # 레이아웃 설정
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("데이터 분석")
        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            st.button("회사별 건수", key="company_button")
        with btn2:
            st.button("카테고리별 건수", key="category_button")
        with btn3:
            st.button("수준별 건수", key="level_button")

    with col2:
        st.subheader("옵션")
        display_option = st.radio("표/그래프 선택", ["표", "그래프"], key='display_option')

    # 회사별 건수
    if st.session_state.company_button:
        company_counts = df['Company'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(company_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots()
            ax.barh(company_counts.index, company_counts.values)
            ax.set_xlabel('건수')
            ax.set_ylabel('Company')
            ax.set_title('Company별 건수')
            for i in ax.patches:
                ax.text(i.get_width() + .3, i.get_y() + .31, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')
            st.pyplot(fig)

    # 카테고리별 건수
    if st.session_state.category_button:
        category_counts = df['Category'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(category_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots()
            ax.barh(category_counts.index, category_counts.values)
            ax.set_xlabel('건수')
            ax.set_ylabel('카테고리')
            ax.set_title('카테고리별 건수')
            for i in ax.patches:
                ax.text(i.get_width() + .3, i.get_y() + .31, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')
            st.pyplot(fig)

    # 수준별 건수
    if st.session_state.level_button:
        level_counts = df['Level'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(level_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots()
            ax.bar(level_counts.index, level_counts.values)
            ax.set_xlabel('수준')
            ax.set_ylabel('건수')
            ax.set_title('수준별 건수')
            plt.xticks(rotation=0)
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
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
