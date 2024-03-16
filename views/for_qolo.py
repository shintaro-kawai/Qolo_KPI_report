# Qolo向けKPIレポート　グラフ出力

import os
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))


# データ準備
def _read_data() -> pd.DataFrame:

    # 患者ベースのdf作成
    df = pd.read_csv(os.path.join(parent_dir, "data/etl/merged_data.csv"))
    """患者氏名ごとに起立回数を合計"""
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
            "病院ID",
            "日時",
            "Q1",
        ]
    ]
    df_patient_info = pd.merge(df_patient, df_move_cumsum, on="患者氏名")
    df_patient_info = df_patient_info.rename(
        columns={"身長": "身長[cm]", "体重": "体重[kg]"}
    )
    print(df_patient_info)

    # 拠点ベースのdf作成
    df_place = df.groupby(["病院ID"], as_index=False)[["起立回数"]].sum()
    """
    "病院ID"もカラムに含めるために、as_index=Falseにする。
    例) df_patient_num = df.groupby(["疾患"], as_index=False)[["患者氏名"]].count()
    """
    df_place = df_place.rename(columns={"起立回数": "累積動作回数"})
    df_place_move = df_place[["病院ID", "累積動作回数"]]
    print(df_place_move)

    return df_patient_info, df_place_move


# 結果
def for_qolo_result() -> None:

    df = _read_data()

    # [バブルチャート]患者の身長・体重に対する累積動作回数
    df_bubble = df[0]

    st.header("患者の身長・体重に対する累積動作回数")
    show_df_Bub = st.checkbox("Show DataFrame for Cumulative Number")
    if show_df_Bub == True:
        st.write(df_bubble)

    fig1 = px.scatter(
        df_bubble,
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
    st.plotly_chart(fig1)

    # [縦棒グラフ]拠点ごとの合計動作回数
    df_bar = df[1]
    # df_bar_1 = df_bar["病院ID"].astype(str)
    # df_bar_2 = df_bar["累積動作回数"]
    # df_bar = pd.merge(df_bar_1, df_bar_2)

    st.header("拠点ごとの合計動作回数")
    show_df_Bar = st.checkbox("Show DataFrame for Total Moving Counts in Each Hospital")
    if show_df_Bar == True:
        st.write(df_bar)

    max_x = len(df_bar)

    fig2 = px.bar(
        df_bar,
        x="病院ID",
        y="累積動作回数",
        # color="疾患",
        # animation_frame="年齢",
        range_x=[0, max_x],
        orientation="v",
        width=800,
        height=500,
    )
    st.plotly_chart(fig2)


if __name__ == "__main__":
    for_qolo_result()
