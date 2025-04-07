# ⚾ MLB 2025 Pipeline – Game Log Sync & Google Sheets Export

[![Daily Sync Status](https://github.com/cgpropz/mlb-2025-pipeline/actions/workflows/main.yml/badge.svg)](https://github.com/cgpropz/mlb-2025-pipeline/actions)

This repo automates the end-to-end process of scraping MLB game logs, merging them, and syncing them to a live **[Google Sheet](https://docs.google.com/spreadsheets/d/1X6dMVxb7vPITaONfXdrNVj0sDAKsLmxj0NYpzDfK5Gc/edit?gid=2011034577#gid=2011034577)** daily.

---

## 📋 Features

- 🕒 **Runs Daily** at 3:00 AM UTC via GitHub Actions
- 🧼 Cleans + merges player game logs
- 🧠 Fully automated data push to Google Sheets
- 🐍 Built in Python (3.9)

---

## 🚀 Usage

### 🔧 Local Setup

```bash
git clone https://github.com/cgpropz/mlb-2025-pipeline.git
cd mlb-2025-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
