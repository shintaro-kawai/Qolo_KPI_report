# Qolo_KPI_report
Make KPI reports for Qolo and hospitals

## KPIレポートの内容
- 病院向けのグラフ
  - [ ] 患者の身長・体重に対する動作回数（バブルチャート）
  - [ ] 対応スタッフ数に対する合計動作回数
- Qolo向けのグラフ
  - [ ] 拠点ごとの合計動作回数
  - [ ] 疾患ごとの症例数・訓練回数・動作回数（複数項目の棒グラフ）
  - [ ] 各機体の累積動作量

## Project structure
<pre>
.
├── LICENSE
├── README.md
├── app.py
├── data
│   ├── etl
│   │   └── merged_data.csv
│   ├── other
│   │   ├── df_patient_info.csv
│   │   ├── disease_level.json
│   │   └── header_list.json
│   └── raw
├── images
│   └── Qolo_logo.png
├── modules
│   └── data_prepare.py
├── requirements.txt
├── results
│   ├── count_output.csv
│   └── filename_list.csv
└── views
    ├── for_hospital.py
    └── for_qolo.py
</pre>