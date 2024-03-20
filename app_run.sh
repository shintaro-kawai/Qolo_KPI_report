#!/bin/bash

# app.pyを実行するカレントディレクトリへ移動
# TODO: 各環境に応じて変更\
DIR="/Users/shintaro/Desktop/Qolo/Qolo_KPI_report"
cd $DIR

# app.py実行メッセージ
echo "KPIレポートアプリを起動します"
echo "run $DIR/app.py"

# app.pyの実行
# STREAMLIT=`which streamlit`
# echo $STREAMLIT
/Users/shintaro/.pyenv/shims/streamlit run "$DIR/app.py"

