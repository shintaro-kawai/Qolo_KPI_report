import json
import os
import glob
import pandas as pd
import re
import math
import numpy as np


# CSVファイルをマージする
def merge_csv_files(folder_path, etl_path, output_file_name):

    # header_list.jsonから読み込み
    with open("./data/other/header_list.json", "r") as f:
        header_dict = json.load(f)["column_name"]
        header_list = list(header_dict.keys())
        """各カラムの項目"""
        patient = header_list[0]  # 患者氏名
        disease = header_list[5]  # 疾患
        disease_level = header_list[6]  # 疾患レベル
        standup_num = header_list[7]  # 起立回数

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    # 読み込んだファイル名リストを作成
    filepath_list = glob.glob("./data/raw/*.csv")
    filename_list = []
    for file_name in filepath_list:
        """ex. /data/raw/0_2024-02-01-10-45-54.csv"""
        txt = re.split("[_/.]", file_name)
        filename_list.append(txt)

    df_filename = pd.DataFrame(
        filename_list,
        columns=[
            "DELETE1",
            "DELETE2",
            "DELETE3",
            "DELETE4",
            "hospital",
            "date",
            "format",
        ],
    )
    df_filename = df_filename[["hospital", "date"]]
    print(df_filename)
    df_filename.to_csv("./results/filename_list.csv", index=False)

    # CSVファイル読み込み
    df_temp = []

    for file in csv_files:

        """ファイル名の分解: 0_2024-02-01-10-45-54.csv"""
        file_text = re.split("[_.]", file)
        hospital_id = file_text[0]
        date_time = file_text[1]

        """ CSVの中身をデータフレーム化 """
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        row_num = len(df)

        """病院IDと日時のデータフレームを作成"""
        hos_list = []
        datetime_list = []
        for ii in range(row_num):
            hos_list.append(hospital_id)
            datetime_list.append(date_time)
        df_hos_id = pd.DataFrame(hos_list, columns=["hospital_id"])
        df_datetime = pd.DataFrame(datetime_list, columns=["date_time"])

        """日時から年月(yyyy-mm)を抽出して年月カラムを追加"""
        df_yyyymm = df_datetime["date_time"].str[:7]

        """病院IDと日時、年月を連結"""
        df2 = pd.concat([df, df_hos_id], axis=1)
        df3 = pd.concat([df2, df_datetime], axis=1)
        df4 = pd.concat([df3, df_yyyymm], axis=1)

        """アンケート回答を分解"""
        val_list = []
        quest_list = ["q1", "q2", "q3", "q4", "q5"]

        for i, r in df.iterrows():
            if isinstance(r["アンケート結果"], str):
                D = r["アンケート結果"]
                print(D)
                data_dict = json.loads(D)
                print(data_dict)
                print(type(data_dict))
                value_q1 = data_dict["q1"]
                value_q2 = data_dict["q2"]
                value_q3 = data_dict["q3"]
                value_q4 = data_dict["q4"]
                value_q5 = data_dict["q5"]
                print(value_q1)
                print(type(value_q1))
                val_list.append([value_q1, value_q2, value_q3, value_q4, value_q5])
            else:
                val_list.append([0, 0, 0, 0, 0])
        df_quest = pd.DataFrame(val_list, columns=quest_list)

        """アンケートQ1を文字列「1名」から数値「1」に置換"""
        df_quest = df_quest.replace({"q1": {"1名": 1, "2名": 2, "3名": 3}})
        print(df_quest)

        """アンケート回答Q1~5を連結"""
        df5 = pd.concat([df4, df_quest], axis=1)

        """CSVの中身を下に追加していく"""
        df_temp.append(df5)

    merged_df = pd.concat(df_temp, ignore_index=True, sort=False)
    print(merged_df)

    """ 全CSVファイル../data/etl/merged_data.csv を出力 """
    output_path = os.path.join(etl_path, output_file_name)

    merged_df.columns = header_list
    merged_df.to_csv(output_path, index=False)

    print(f"{len(csv_files)} CSV files merged into {output_file_name}")

    # 症例数と累積動作回数をカウント
    patient_list = merged_df[patient].unique()
    count_patient_num = len(patient_list)

    count_move_cumsum = merged_df[standup_num].sum(axis=0)

    lst_1 = [count_patient_num]
    lst_2 = [count_move_cumsum]
    df_count_result = pd.DataFrame(
        list(zip(lst_1, lst_2)), columns=["症例数", "累積動作回数"]
    )
    df_count_result.to_csv(
        "./results/count_output.csv", header=True, index=False, encoding="utf-8"
    )
    print(f"症例数は{count_patient_num}")
    print(f"累積動作回数は{count_move_cumsum}")


if __name__ == "__main__":
    folder_path = "./data/raw"  # 単体でデバッグする時 ../data/raw
    etl_path = "./data/etl"  # 単体でデバッグする時 ../data/etl
    output_file_name = "merged_data.csv"
    merge_csv_files(folder_path, etl_path, output_file_name)
