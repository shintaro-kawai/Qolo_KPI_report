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
            "アンケート結果",
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

    # 1.疾患ごとの症例数・訓練回数・累積動作回数
    st.header("疾患ごとの症例数・訓練回数・累積動作回数")

    df = _read_data()

    # 疾患ごとの症例数・訓練回数・累積動作回数カウント
    """「疾患」もカラムに含めるために、as_index=Falseを指定"""
    df_patient_num = df.groupby(["疾患"], as_index=False)[["患者氏名"]].count()
    df_train_num = df.groupby(["疾患"], as_index=False)[["訓練回数"]].sum()
    df_move_num = df.groupby(["疾患"], as_index=False)[["累積動作回数"]].sum()

    print(df_patient_num)
    print(df_train_num)
    print(df_move_num)

    df_disease_count = pd.merge(df_patient_num, df_train_num, on="疾患", how="inner")
    df_disease_count = pd.merge(df_disease_count, df_move_num, on="疾患", how="inner")
    df_disease_count = df_disease_count.rename(columns={"患者氏名": "症例数"})

    print(df_disease_count)

    parameter_list = [
        "症例数",
        "訓練回数",
        "累積動作回数",
    ]
    option_parameter = st.selectbox("比較指標の種類", (parameter_list))
    max_x = df_disease_count[option_parameter].max() + 5

    fig = px.bar(
        df_disease_count,
        x=option_parameter,
        y="疾患",
        color="疾患",
        # animation_frame="年齢",
        range_x=[0, max_x],
        orientation="h",  # 縦棒グラフはv
        width=800,
        height=500,
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    for_hospital_result()
