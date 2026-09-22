import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 분포와 관계를 중심으로 살펴봅니다."
)


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_URL,
        dtype={
            "movieCd": str,
            "openDt": str
        }
    )

    # 장르가 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    df["genre_first"] = df["genre_first"].replace("", "미상")

    return df


try:
    df = load_data()

except Exception:
    st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
    st.stop()


# ==========================================
# 1. 장르별 영화 편수
# ==========================================

st.subheader("1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.48,
    title="장르별 영화 편수"
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 그래프 설명
# ==========================================

with st.container(border=True):
    st.markdown("### 이 그래프로 알 수 있는 것")
    st.write(
        "장르별 영화 편수의 분포를 비교해 어떤 장르의 영화가 많이 포함되어 있는지 알 수 있습니다."
    )
