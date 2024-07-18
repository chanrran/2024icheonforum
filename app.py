import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import font_manager, rc

# 기본 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_manager.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

# GitHub에서 CSV 파일 읽기
url = 'https://raw.githubusercontent.com/chanrran/2024icheonforum/main/Caselist_240718.csv'
df = pd.read_csv(url)

# 최상단 메시지 노출
st.write("""
    ## 이 서비스는 생성형 AI 공모전의 사례제출 현황을 분석하고 인사이트를 제공하기 위해 제작되었습니다.
""")

# 데이터 요약
st.write(f"데이터를 통해 총 {df.shape[0]}건의 사례가 확인되었습니다.")

# 옵션 선택 라디오 버튼 (오른쪽)
col1, col2 = st.columns([3, 1])
with col2:
    st.subheader("옵션")
    display_option = st.radio("표/그래프 선택", ["표", "그래프"], key='display_option')

# 데이터 분석 버튼들 (왼쪽)
with col1:
    st.subheader("데이터 분석")
    btn1, btn2, btn3 = st.columns(3)

    if btn1.button("회사별 건수"):
        st.session_state.selected_button = "company"

    if btn2.button("카테고리별 건수"):
        st.session_state.selected_button = "category"

    if btn3.button("수준별 건수"):
        st.session_state.selected_button = "level"

    selected_button = st.session_state.get('selected_button', None)

    # 버튼 클릭 상태 유지 및 스타일 변경
    if selected_button == "company":
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

    if selected_button == "category":
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

    if selected_button == "level":
        level_counts = df['Level'].value_counts().sort_values(ascending=False)
        if display_option == "표":
            st.write(level_counts)
        elif display_option == "그래프":
            fig, ax = plt.subplots()
            ax.barh(level_counts.index, level_counts.values)
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
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
