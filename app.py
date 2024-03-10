import pandas as pd
import time
import matplotlib.pyplot as plt
import streamlit as st
import seaborn
import plotly.express as px

from views.for_qolo import for_qolo_result
from views.for_hospital import for_hospital_result


# Data preparation
def data_prepare():
    """あとでコーディング"""
    print("Hello, streamlit!")


# 画面1: Qolo
def display_for_qolo():
    """Display KPI report for Qolo view."""
    return for_qolo_result()


# 画面2: Hospital
def display_for_hospital():
    """Display KPI report for hospital view."""
    return for_hospital_result()


# HOME画面
def home():
    """Display home page."""
    st.header("KPI Report")
    st.markdown("過去取得されたデータに基づいて、KPIレポートを作成します。")
    st.text("Qolo inc. output monthly KPI reports based on the past data.")


def main():
    """Data preparation"""
    data_prepare()
    """Display results by streamlit"""
    st.set_page_config(layout="wide")
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
