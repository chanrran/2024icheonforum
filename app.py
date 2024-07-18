import pandas as pd
import streamlit as st
from io import BytesIO
from collections import Counter
import re

# 파일 업로드
uploaded = st.file_uploader("파일을 업로드하세요", type=["xlsx"])

if uploaded is not None:
    # 엑셀 파일 로드
    df = pd.read_excel(BytesIO(uploaded.read()))

    # 데이터프레임 열 이름 출력
    st.write("엑셀 파일의 열 이름:", df.columns.tolist())

    # 필요한 열이 있는지 확인
    if 'Company' in df.columns and 'Title' in df.columns and 'Category' in df.columns and 'Level' in df.columns:
        # 회사별 건수
        company_counts = df['Company'].value_counts()

        # 수준별 건수
        level_counts = df['Level'].value_counts()

        # 키워드 추출 함수
        def extract_keywords(text):
            words = re.findall(r'\b\w+\b', str(text))
            return words

        # 모든 카테고리에서 키워드 추출
        keywords = df['Category'].apply(extract_keywords).sum()
        keyword_counts = Counter(keywords)

        # 상위 10개 키워드
        top_keywords = keyword_counts.most_common(10)

        # Streamlit 대시보드
        st.title('데이터 분석 대시보드')

        st.subheader('회사별 건수')
        st.bar_chart(company_counts)

        st.subheader('수준별 건수')
        st.bar_chart(level_counts)

        st.subheader('카테고리별 키워드 분석')
        st.write(pd.DataFrame(top_keywords, columns=['키워드', '빈도수']))
    else:
        st.error("엑셀 파일에 필요한 열(Company, Title, Category, Level)이 없습니다.")
