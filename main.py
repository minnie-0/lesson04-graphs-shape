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

    # 여러 장르가 있는 경우 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    df["genre_first"] = df["genre_first"].replace("", "미상")

    # 총 관객 수를 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

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

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.48,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig1, use_container_width=True)

with st.container(border=True):
    st.markdown("### 이 그래프로 알 수 있는 것")
    st.write(
        "장르별 영화 편수의 분포를 비교해 어떤 장르의 영화가 많이 포함되어 있는지 알 수 있습니다."
    )


# ==========================================
# 2. 장르별 영화와 총 관객 트리맵
# ==========================================

st.subheader("2. 장르별 영화와 총 관객")

treemap_df = df.dropna(
    subset=["genre_first", "movieNm", "total_audi"]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

with st.container(border=True):
    st.markdown("### 이 그래프로 알 수 있는 것")
    st.write(
        "장르 안에서 영화별 총 관객 규모를 비교해 어떤 영화가 많은 관객을 모았는지 알 수 있습니다."
    )


# ==========================================
# 3. 총 관객 히스토그램
# ==========================================

st.subheader("3. 영화별 총 관객 분포")

hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="총 관객 수의 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig3, use_container_width=True)


# 가장 관객이 많은 영화
most_watched = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

most_watched_name = most_watched["movieNm"]
most_watched_audi = int(most_watched["total_audi"])


# 가장 영화가 많이 들어 있는 구간
counts, bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True
)

bin_counts = counts.value_counts().sort_index()
largest_bin = bin_counts.idxmax()

lower = int(largest_bin.left)
upper = int(largest_bin.right)


with st.container(border=True):
    st.markdown("### 이 그래프로 알 수 있는 것")

    st.write(
        f"대부분의 영화는 총 관객 약 {lower:,}명~{upper:,}명 구간에 몰려 있습니다."
    )

    st.write(
        f"가장 관객이 많은 영화는 **{most_watched_name}**으로 "
        f"총 관객은 **{most_watched_audi:,}명**입니다."
    )
