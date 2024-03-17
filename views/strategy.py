# 患者個人に最適化されたリハビリ計画（を示したい）
import pathlib
import json
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from typing import Tuple

# [Attention]実行元のapp.pyの階層から見た書き方
# from modules.strategy_maker import create_tyre_combination, Strategy


# 疾患(list)・疾患レベル(dict)を返す関数
def get_disease_info() -> Tuple[list, dict]:

    # app.pyのカレントディレクトリ
    p = pathlib.Path()
    current_dir = p.cwd()
    """ -> /Users/shintaro/Desktop/Qolo/Qolo_KPI_report """

    # 疾患と疾患レベルを紐づける辞書型 作成
    jsonfile = f"{current_dir}/data/other/disease_level.json"
    with open(jsonfile, encoding="utf-8") as f:
        disease_level_dict = json.load(f)

    # 疾患リスト作成
    "入れ子構造の辞書型をノーマライズ"
    df = pd.json_normalize(disease_level_dict)
    df.to_csv(f"{current_dir}/data/other/disease_level.csv")
    col_list = df.columns.to_list()
    l_temp = []
    col_names = ["疾患", "疾患レベル"]
    for s in col_list:
        l = [x.strip() for x in s.split(".")]
        l_temp.append(l)
    df_dis = pd.DataFrame(l_temp, columns=col_names)
    disease_list = df_dis["疾患"].unique()
    """ [出力結果]
    disease_list = ['脊髄損傷' '脳卒中' '脳性麻痺' '膝関節' '神経難病' '義足' 'その他'] 
    """
    print(type(disease_list))
    print(type(disease_level_dict))

    return disease_list, disease_level_dict


# Optimal Strategy
def strategy():

    st.header("Optimal strategy")
    st.subheader("Input information")

    dis_list = get_disease_info()[0]
    dis_level_dict = get_disease_info()[1]

    """
    Input information 
    画面を6分割: 性別、身長、体重、年齢、疾患、疾患レベル
    """
    col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)
    with col_1:
        gender = st.selectbox(
            label="Gender",
            options=["Male", "Female", "Other"],
        )
    with col_2:
        height = st.number_input(
            label="Height(cm)",
            value=170.0,
            min_value=0.0,
            max_value=200.0,
            step=0.1,
            format="%.1f",
        )
    with col_3:
        weight = st.number_input(
            label="Weight(kg)",
            value=50.0,
            min_value=0.0,
            max_value=120.0,
            step=0.1,
            format="%.1f",
        )
    with col_4:
        age = st.number_input(
            label="Age",
            value=50,
            min_value=0,
            max_value=130,
            step=1,
        )
    with col_5:
        disease = st.selectbox(
            label="Disease",
            options=dis_list,
        )
    with col_6:
        selected_dict = dis_level_dict[disease]
        disease = st.selectbox(
            label="Disease Level",
            options=list(selected_dict),
        )


if __name__ == "__main__":
    strategy()
