import os
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px
import csv
import json

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))


# データ準備
def _read_data() -> pd.DataFrame:
    """Read data."""
    df = pd.read_csv(os.path.join(parent_dir, "data/etl/merged_data.csv"))
    df_move_cumsum = df.groupby(["患者氏名"])[["起立回数"]].sum()
    df_move_cumsum = df_move_cumsum.rename(columns={"起立回数": "累積動作回数"})
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
            "アンケート結果",
        ]
    ]
    df_patient_info = pd.merge(df_patient, df_move_cumsum, on="患者氏名")
    df_patient_info = df_patient_info.rename(
        columns={"身長": "身長[cm]", "体重": "体重[kg]"}
    )
    print(df_patient_info)

    return df_patient_info


# 結果
def for_qolo_result() -> None:

    # バブルチャート：患者の身長・体重に対する累積動作回数
    df = _read_data()

    st.header("患者の身長・体重に対する累積動作回数")
    show_df_Bub = st.checkbox("Show DataFrame")
    if show_df_Bub == True:
        st.write(df)

    fig = px.scatter(
        df,
        x="体重[kg]",
        y="身長[cm]",
        range_x=[30, 100],
        range_y=[130, 200],
        size="累積動作回数",
        size_max=38,
        color="年齢",
        # animation_frame="集計年",  # 集計年ごとの推移を見る
        animation_group="年齢",
    )
    st.plotly_chart(fig)

    # アンケートQ1回答の抽出
    df_q1_answer = df[["アンケート結果"]]


if __name__ == "__main__":
    for_qolo_result()
