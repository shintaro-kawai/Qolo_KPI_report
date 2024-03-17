import os
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))


# データ準備
def _read_data() -> pd.DataFrame:
    """Read data."""
    df = pd.read_csv(os.path.join(parent_dir, "data/etl/merged_data.csv"))

    # 累積動作回数
    df_move_cumsum = df.groupby(["患者氏名"])[["起立回数"]].sum()
    df_move_cumsum = df_move_cumsum.rename(columns={"起立回数": "累積動作回数"})

    # 訓練回数
    df_train_count = df.groupby(["患者氏名"])[["患者氏名"]].count()
    df_train_count = df_train_count.rename(columns={"患者氏名": "訓練回数"})

    # 同じ患者名の行を削除
    df_nodup = df.drop_duplicates(
        subset=["患者氏名", "性別", "身長", "体重", "年齢", "疾患", "疾患レベル"]
    )
    df_patient = df_nodup[
        [
            "患者氏名",
            "性別",
            "身長",
            "体重",
            "年齢",
            "疾患",
            "疾患レベル",
            "病院ID",
            "年月",
            "Q1",
        ]
    ]

    # 疾患を番号から疾患名に置換
    df_patient = df_patient.replace(
        {
            "疾患": {
                0: "脊髄損傷",
                1: "脳卒中",
                2: "脳性麻痺",
                3: "膝関節",
                4: "神経難病",
                5: "義足",
                99: "その他",
            }
        }
    )

    # 患者情報をマージして整理
    df_patient_info = pd.merge(df_patient, df_move_cumsum, on="患者氏名")
    df_patient_info = pd.merge(df_patient_info, df_train_count, on="患者氏名")
    df_patient_info = df_patient_info.rename(
        columns={"身長": "身長[cm]", "体重": "体重[kg]"}
    )

    # 確認用
    print(df_patient_info)
    df_patient_info.to_csv(os.path.join(parent_dir, "data/other/df_patient_info.csv"))

    return df_patient_info


# 結果
def for_hospital_result() -> None:

    df = _read_data()

    # 疾患ごとの症例数・訓練回数・累積動作回数カウント
    """「疾患」もカラムに含めるために、as_index=Falseを指定"""
    df_patient_num = df.groupby(["疾患"], as_index=False)[["患者氏名"]].count()
    df_train_num = df.groupby(["疾患"], as_index=False)[["訓練回数"]].sum()
    df_move_num = df.groupby(["疾患"], as_index=False)[["累積動作回数"]].sum()

    df_disease_count = pd.merge(df_patient_num, df_train_num, on="疾患", how="inner")
    df_disease_count = pd.merge(df_disease_count, df_move_num, on="疾患", how="inner")
    df_disease_count = df_disease_count.rename(columns={"患者氏名": "症例数"})

    print(df_disease_count)

    # [2軸グラフ]訓練回数と累積動作回数
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[f"{disease_name}" for disease_name in df_disease_count["疾患"]],
            y=df_disease_count["累積動作回数"],
            yaxis="y1",
            offsetgroup=1,
            name="累積動作回数",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[f"{disease_name}" for disease_name in df_disease_count["疾患"]],
            y=df_disease_count["訓練回数"],
            yaxis="y2",
            offsetgroup=2,
            name="訓練回数",
        )
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=[f"{disease_name}" for disease_name in df_disease_count["疾患"]],
    #         y=df_disease_count["累積動作回数"],
    #         mode="markers",
    #         marker_size=df_disease_count["症例数"].values.tolist(),
    #         marker_color=(
    #             "violet",  # CSSカラー
    #             "#ee82ee",  # HTMLカラー
    #             "rgb(238, 130, 238)",  # rgb(Red, Green, Blue)
    #             "rgba(238, 130, 238, 0.2)",  # rgba(Red, Green, Blue, alpha)
    #         ),
    #     )
    # )

    # グラフ全体のレイアウト
    fig.update_layout(
        yaxis1=dict(side="left"),
        yaxis2=dict(side="right", overlaying="y", showgrid=False),
    )
    fig.update_layout(
        barmode="group",
        width=800,
        height=500,
        font_size=18,
        hoverlabel_font_size=14,
        legend=dict(x=0.9, y=-0.1, xanchor="left", yanchor="top"),
    )
    st.header("疾患ごとの累積動作回数と訓練回数")
    st.plotly_chart(fig)

    # [棒グラフ]症例数
    max_y = df_disease_count["症例数"].max() + 1
    fig2 = px.bar(
        df_disease_count,
        y="症例数",
        x="疾患",
        range_y=[0, max_y],
        orientation="v",
        width=800,
        height=500,
    )
    fig2.update_layout(
        width=800,
        height=500,
        font_size=18,
        hoverlabel_font_size=14,
    )
    st.header("疾患ごとの症例数")
    st.plotly_chart(fig2)

    # 年月ごとのデータ
    st.header("年月ごとのデータ集計")

    """
    病院ごとの症例数・訓練回数・累積動作回数カウント
    「病院ID」もカラムに含めるために、as_index=Falseを指定
    """
    yyyymm_list = df["年月"].unique()
    option_yyyymm = st.selectbox("年月", (yyyymm_list))
    df_year = df[(df["年月"] == option_yyyymm)]

    df_patient_num_2 = df_year.groupby(["病院ID"], as_index=False)[["患者氏名"]].count()
    df_train_num_2 = df_year.groupby(["病院ID"], as_index=False)[["訓練回数"]].sum()
    df_move_num_2 = df_year.groupby(["病院ID"], as_index=False)[["累積動作回数"]].sum()

    df_disease_count_2 = pd.merge(
        df_patient_num_2, df_train_num_2, on="病院ID", how="inner"
    )
    df_disease_count_2 = pd.merge(
        df_disease_count_2, df_move_num_2, on="病院ID", how="inner"
    )
    df_disease_count_2 = df_disease_count_2.rename(columns={"患者氏名": "症例数"})

    print(df_disease_count_2)

    parameter_list = [
        "症例数",
        "訓練回数",
        "累積動作回数",
    ]
    opt_para = st.selectbox("指標の種類", (parameter_list))

    # max_y = df_year[opt_para].max() + 50

    fig = px.bar(
        df_disease_count_2,
        y=opt_para,
        x="病院ID",
        # color="病院ID",
        # animation_frame="",
        # range_y=[0, max_y],
        orientation="v",
        width=800,
        height=500,
    )
    st.plotly_chart(fig)


# parameter_list = [
#     "訓練回数",
#     "累積動作回数",
# ]
# # option_parameter = st.selectbox("比較指標の種類", (parameter_list))
# max_y = df_disease_count["累積動作回数"].max() + 5

# selected_items = st.multiselect(
#     "Select parameters",
#     options=parameter_list,
#     default=parameter_list,
#     key="selected_parameters",
#     # placeholder="Please choose parameter",
# )

# if st.checkbox("All parameters ", key="check_parameters"):
#     selected_items = parameter_list


if __name__ == "__main__":
    for_hospital_result()
