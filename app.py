import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
data_path = 'Caselist_240718.csv'
data = pd.read_csv(data_path)

# 사이드바 필터
company = st.sidebar.selectbox('회사 선택', ['전체'] + list(data['회사'].unique()))
topic = st.sidebar.selectbox('주제 선택', ['전체'] + list(data['주제'].unique()))
level = st.sidebar.selectbox('난이도 선택', ['전체'] + list(data['난이도'].unique()))

# 필터 적용
filtered_data = data.copy()
if company != '전체':
    filtered_data = filtered_data[filtered_data['회사'] == company]
if topic != '전체':
    filtered_data = filtered_data[filtered_data['주제'] == topic]
if level != '전체':
    filtered_data = filtered_data[filtered_data['난이도'] == level]

# 메인 화면
st.title('프로젝트 대시보드')

# 그래프 생성 함수
def create_bar_chart(counts, title, xlabel, ylabel):
    counts = counts.sort_values(ascending=False)  # 내림차순 정렬
    fig, ax = plt.subplots()
    counts.plot(kind='barh', ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for i in ax.containers:
        ax.bar_label(i, label_type='edge')
    st.pyplot(fig)

# 회사별 프로젝트 수
st.header('회사별 프로젝트 수')
company_counts = filtered_data['회사'].value_counts()
create_bar_chart(company_counts, '회사별 프로젝트 수', '프로젝트 수', '회사')

# 주제별 프로젝트 수
st.header('주제별 프로젝트 수')
topic_counts = filtered_data['주제'].value_counts()
create_bar_chart(topic_counts, '주제별 프로젝트 수', '프로젝트 수', '주제')

# 난이도별 프로젝트 수
st.header('난이도별 프로젝트 수')
level_counts = filtered_data['난이도'].value_counts()
create_bar_chart(level_counts, '난이도별 프로젝트 수', '프로젝트 수', '난이도')

# 필터된 프로젝트 목록
st.header('프로젝트 목록')
st.write(filtered_data)
