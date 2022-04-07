# TablesExtractor

Tool for extracting tables from PDF documents.

# Installation

1. Install python packages: `pip install -r requirements.txt`.
2. Prepare tensorflow models:
```bash
cd tables_extractor/models
bash download_model.sh matroshenko TablesDetector v3.0.0 tables_detector_v3
bash download_model.sh matroshenko TableAnalyzer v2.0.0 splerge_model_v1
unzip tables_detector_v3.zip -d tables_detector_v3
unzip splerge_model_v1.zip -d splerge_model_v1
```

# Usage

To export tables from PDF document to HTML format use script `export_tables_to_html.py`.
Run with `--help` to view usage info.