# Justice by the Numbers — Karnataka HC

A public-facing civic dashboard by Lawgorithm.

## How to run locally

1. Install Python 3.10+
2. Open Terminal, go to this folder: `cd justice-dashboard`
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Browser opens automatically at http://localhost:8501

## How to update data

1. Open Google Colab → upload `data_prep.py` → run it
2. Download `processed_cases.csv` and `cohort_stats.csv`
3. Replace the files in the `data/` folder
4. Push to GitHub → dashboard auto-redeploys in ~2 minutes

## Files

- `app.py` — main dashboard
- `data/processed_cases.csv` — cleaned case data
- `data/cohort_stats.csv` — pre-computed cohort analysis
- `requirements.txt` — Python packages needed
