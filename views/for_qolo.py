import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ファイルが入っているフォルダまでのパスを文字列で取得
current_dir = os.path.dirname(__file__)


def _read_data() -> pd.DataFrame:
    """Read data."""
    # return df


def for_qolo_result() -> None:
    """Display result view."""
    # df = _read_data()


if __name__ == "__main__":
    for_qolo_result()
