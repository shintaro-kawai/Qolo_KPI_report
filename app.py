import streamlit as st
import os

# set streamlit
st.set_page_config(page_title="app.py", layout="wide")

# modules/viewsフォルダから関数をインポート
from modules.data_prepare import merge_csv_files
from views.for_qolo import for_qolo_result
from views.for_hospital import for_hospital_result

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# データETL: Extract/Transfer/Load
# rawデータを整形し、merged_data.csvを生成。結果のグラフ出力は、merged_data.csvをベースに作成。
folder_path = "./data/raw"
etl_path = "./data/etl"
output_file_name = "merged_data.csv"
merge_csv_files(folder_path, etl_path, output_file_name)


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
    }
    selected_view = st.sidebar.selectbox(label="Views", options=list(views.keys()))
    render_view = views[selected_view]
    render_view()


if __name__ == "__main__":
    main()
