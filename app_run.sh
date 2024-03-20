#!/bin/bash

# app.pyを実行するカレントディレクトリへ移動
# TODO: 各環境に応じて変更
cd ~/Desktop/Qolo/Qolo_KPI_report

# app.py実行メッセージ
echo "KPIレポートアプリが起動します"

# app.pyの実行
streamlit run ~/Desktop/Qolo/Qolo_KPI_report/app.py

