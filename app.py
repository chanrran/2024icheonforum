import pandas as pd
import streamlit as st
from collections import Counter
import re

# 파일 업로드
uploaded = st.file_uploader("파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    # CSV 파일 로드
    df = pd.read_csv(uploaded)

    # 카테고리별 건수
    category_counts = df['카테고리'].value_counts()

    # 수준별 건수
    level_counts = df['수준'].value_counts()

    # 회사별 건수
    company_counts = df['회사'].value_counts()

    # 키워드 추출 함수
    def extract_keywords(text):
        words = re.findall(r'\b\w+\b', str(text))
        return words

    # 모든 주제에서 키워드 추출
    keywords = df['주제'].apply(extract_keywords).sum()
    keyword_counts = Counter(keywords)

    # 상위 10개 키워드
    top_keywords = keyword_counts.most_common(10)

    # Streamlit 대시보드
    st.title('데이터 분석 대시보드')

    st.subheader('카테고리별 건수')
    st.bar_chart(category_counts)

    st.subheader('수준별 건수')
    st.bar_chart(level_counts)

    st.subheader('회사별 건수')
    st.bar_chart(company_counts)

    st.subheader('주제별 키워드 분석')
    st.writ
