import pandas as pd
import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt

# 파일 업로드
uploaded = st.file_uploader("파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    # CSV 파일 로드
    df = pd.read_csv(uploaded)
    
    # 데이터프레임 내용 출력
    st.write(df.head(10))

    # 열 이름을 적절히 설정 (필요한 경우)
    df.columns = ['Company', 'Title', 'Category', 'Level'] + [f'Unnamed: {i}' for i in range(len(df.columns) - 4)]

    # 데이터프레임 열 이름 출력
    st.write("수정된 열 이름:", df.columns.tolist())

    # 필요한 열이 있는지 확인
    if 'Company' in df.columns and 'Title' in df.columns and 'Category' in df.columns and 'Level' in df.columns:
        # 회사별 건수
        company_counts = df['Company'].value_counts().sort_values(ascending=False)

        # 수준별 건수
        level_counts = df['Level'].value_counts()

        # 키워드 추출 함수
        def extract_keywords(text):
            words = re.findall(r'\b\w+\b', str(text))
            return words

        # 모든 카테고리에서 키워드 추출 (NaN 값 제거)
        keywords = df['Category'].dropna().apply(extract_keywords).sum()
        keyword_counts = Counter(keywords)

        # 상위 10개 키워드
        top_keywords = keyword_counts.most_common(10)

        # Streamlit 대시보드
        st.title('데이터 분석 대시보드')

        st.subheader('Company별 건수')
        fig, ax = plt.subplots()
        ax.barh(company_counts.index, company_counts.values)
        ax.set_xlabel('건수')
        ax.set_ylabel('Company')
        ax.set_title('Company별 건수')
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y() + .31, 
                    str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')
        st.pyplot(fig)

        st.subheader('수준별 건수')
        fig, ax = plt.subplots()
        ax.bar(level_counts.index, level_counts.values)
        ax.set_xlabel('수준')
        ax.set_ylabel('건수')
        ax.set_title('수준별 건수')
        plt.xticks(rotation=0)
        st.pyplot(fig)

        st.subheader('카테고리별 키워드 분석')
        st.write(pd.DataFrame(top_keywords, columns=['키워드', '빈도수']))
    else:
        st.error("CSV 파일에 필요한 열(Company, Title, Category, Level)이 없습니다.")
