import streamlit as st
import os
import pandas as pd
import datetime

# set streamlit
st.set_page_config(page_title="app.py", layout="wide")

# modules/viewsフォルダから関数をインポート
from modules.data_prepare import merge_csv_files
from views.for_qolo import for_qolo_result
from views.for_hospital import for_hospital_result
from views.strategy import strategy

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# 本日の日付
d_today = datetime.date.today()

# 【前準備】データETL
## rawデータを整形し、merged_data.csvを生成。
## 結果のグラフ出力は、merged_data.csvをベースに作成。
folder_path = "./data/raw"
etl_path = "./data/etl"
output_file_name = "merged_data.csv"


# データ出力
def data_etl() -> pd.DataFrame:
    df_merged = merge_csv_files(folder_path, etl_path, output_file_name)
    return df_merged


# 変換をキャッシュする
@st.cache
def convert_df(df):
    return df.to_csv().encode("utf-8")


# 画面1: Qolo
def display_for_qolo():
    """Display KPI report for Qolo view."""
    return for_qolo_result()


# 画面2: Hospital
def display_for_hospital():
    """Display KPI report for hospital view."""
    return for_hospital_result()


# 画面: HOME
def home():
    """Display home page."""
    st.header("KPI Report made by Qolo inc.")
    st.markdown("過去取得されたデータに基づいて、KPIレポートを作成します。")
    st.text("Qolo inc. output monthly KPI reports based on the past data.")
    df_merged = data_etl()
    csv = convert_df(df_merged)
    st.download_button(
        label="CSVファイルのダウンロード",
        data=csv,
        file_name=f"{d_today}_merged_data.csv",
        mime="text/csv",
    )


# 画面: Strategy
def display_strategy():
    """Display patients' strategy"""
    return strategy()


# メイン関数
def main():
    """Display results by streamlit"""

    # ロゴ表示
    img_path = f"{current_dir}/images/Qolo_logo.png"
    st.sidebar.image(img_path)

    # サイドバーセレクトボックス
    views = {
        "ホーム": home,
        "Qolo向けKPIレポート": display_for_qolo,
        "病院向けKPIレポート": display_for_hospital,
        "Optimal Strategy": display_strategy,
    }
    selected_view = st.sidebar.selectbox(label="Views", options=list(views.keys()))
    render_view = views[selected_view]
    render_view()


if __name__ == "__main__":
    main()
