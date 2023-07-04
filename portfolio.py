import streamlit as st
import pandas as pd
import datetime
import plotly.express as px


    ## dev start
st.title('Welcome_JY Portfolio :checkered_flag:')
st.caption('> Web, App 기반의 DashBoard를 구현합니다.')
st.divider()


    ## colunm box
st.subheader('Key word')

col1, col2, col3 = st.columns(3)
col1.metric("One.", "판매 데이터", "Data")
col2.metric("Two.", "데이터 전처리", "Table")
col3.metric("Three.", "시각화", "Graph")


    ## intro
st.write("간략한 **Sales report**를 예로 합니다.")
st.write(":blue[**SQL**]을 이용. 1차적인 Target Data를 취합하여, :blue[**Python**]으로 데이터 :blue[전 처리] **과정**을 진행 합니다.")
st.write("이후, 몇 가지 Case을 :blue[**시각화**]을 *구현* 합니다")
st.divider()



st.markdown("")
st.markdown("")
st.markdown("#### 왼쪽의 :red[Side_Bar](>)을 열어, 데이터 :red[검색 기간]을 설정할 수 있습니다.")
st.markdown("")

s_date = datetime.date(2022, 3, 1)
e_date = datetime.date(2022, 5 ,31)
min_date = datetime.date(2022, 1, 1)
max_date = datetime.date(2022, 12, 31)


## sidebar
with st.sidebar:
    with st.sidebar: 
        st.write('# 검색기간을 선택 해주세요')

    with st.sidebar:
        s_date = st.date_input("Start Date", s_date, min_value=min_date, max_value=max_date)

    with st.sidebar:
        e_date = st.date_input("End Date", e_date, min_value=min_date, max_value=max_date)


## date slider
appointment = st.slider("search period:", 
                        value=(s_date, e_date), 
                        min_value=min_date, 
                        max_value=max_date)
# st.write(s_date,e_date)

## Date - sidebar, slider -value공유 시키기
s_date = pd.to_datetime(appointment[0])
e_date = pd.to_datetime(appointment[1])
# st.write(s_date,e_date)


    ## tabs
tab1, tab2, tab3 = st.tabs(["데이터", "전처리", "시각화"])


    ## Data
df = pd.read_csv("salse_data.csv")
# tab1.write(df)

    # data convert
df['DATE'] = pd.to_datetime(df['DATE'])
df['Month'] = df['DATE'].dt.month
# df['Month'] = df['Month'].astype(str)
# tab1.write(df.dtypes)
# st.write(df)

    # Data 기간 조회하여 표시하기
filtered_df = df.loc[(df['DATE'] >= s_date)
                     & (df['DATE'] <= e_date)]

tab1.caption("품목, 거래처을 구분 값을 쿼리 취합하여도, 28만여개의 row가 있는 Data를 준비.")
tab1.write(filtered_df)
st.divider()

    ## 전처리
    # 고객 유형별 매출액
Total_df_DescrTotal = filtered_df.groupby('Descr')['Total'].sum()

    # 제품 구분별 매출수량(ST)
Total_df_TasteStickQty = filtered_df.groupby(['Month','Taste'])['Stick_Qty'].sum()

    # 제품 구분별 매출액
Total_df_TasteTotal = filtered_df.groupby('Taste')['Total'].sum()

with tab2:
    st.caption("시각화 할 Target 정보의 전처리 과정.")
    st.caption("고객 유형별 매출액")
    st.write(Total_df_DescrTotal)
    st.divider()

    st.caption("제품 구분별 매출수량(ST)")
    st.write(Total_df_TasteStickQty)
    st.divider()

    st.caption("제품 구분별 매출액")
    st.write(Total_df_TasteTotal)
    st.divider()


    ## 시각화
    # 고객 유형별 매출액
fig1 = px.pie(filtered_df, values='Total', names='Descr', title='고객 유형별 매출액')


    # 제품 구분별 매출수량(ST)
fig2 = px.bar(filtered_df, x="Month", y="Total",
             color='Taste', barmode='stack', title='월/제품 별 매출수량(ST)')

# fig2.update_layout(paper_bgcolor="white", 
#                 plot_bgcolor="white", 
#                 yaxis_gridcolor= "black",
#                 yaxis_linecolor= "black",
#                 xaxis_linecolor= "black")
# st.plotly_chart(fig2)


    # 제품 구분별 매출액
fig3 = px.pie(filtered_df, values='Total', names='Taste',title='제품 구분별 매출액')

    # tab3에 모으기
with tab3:
    st.caption("조건에 맞는 widgets에 시각화 구현")
    st.plotly_chart(fig1)
    st.divider()

    st.plotly_chart(fig2)
    st.divider()

    st.plotly_chart(fig3)
    st.divider()


with st.expander("See explanation"):
    st.write("""
        * 본 문서는 Python으로 만들어 졌습니다.
        * Data는 직접 연결 할 DB가 없어 CSV 형태로 가공하여 사용하였습니다.
        * 내용은, 실무적으로 지원할 수 있는 DashBoard 개발 과정을 설명하고자 하였습니다.
        * 대단한 개발 사항은 아니지만 개발자의 눈높이 보다는 PI 및 System 운영관리자 로써의 Perfomance를 더하는 일환으로 봐 주십시오.
        * 비교적 간단하고 빠르며, 수정 및 배포가 쉬워 현업이 가진 needs에 대응이 용이 합니다.
    """)
    st.divider()
    st.write("읽어주셔서 감사합니다.")