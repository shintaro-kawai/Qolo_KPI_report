import json
import os
import glob
import pandas as pd
import csv


# CSVファイルをマージする
def merge_csv_files(folder_path, etl_path, output_file_name):

    # header_list.jsonから読み込み
    with open("./data/other/header_list.json", "r") as f:
        header_dict = json.load(f)["column_name"]
        header_list = list(header_dict.keys())
        patient = header_list[0]  # 患者氏名
        disease = header_list[5]  # 疾患
        standup_num = header_list[7]  # 起立回数

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    # CSVファイル読み込み
    df_temp = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_temp.append(df)

    merged_df = pd.concat(df_temp, ignore_index=True, sort=False)

    # ../data/etl/merged_data.csv を出力
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

    # 読み込んだファイル名リストを作成
    filepath_list = glob.glob("./data/raw/*.csv")
    filename_list = []
    for file_name in filepath_list:
        filename_list.append(
            file_name[5:]
        )  # この数字はpathが現れるように使用する環境に合わせて調整

    df_filename = pd.DataFrame(filename_list, columns=["file_name"])
    df_filename.to_csv("./results/filename_list.csv", index=False)


if __name__ == "__main__":
    folder_path = "../data/raw"
    etl_path = "../data/etl"
    output_file_name = "merged_data.csv"
    merge_csv_files(folder_path, etl_path, output_file_name)
