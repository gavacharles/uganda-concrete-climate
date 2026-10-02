#!/bin/sh
# Re-run every analysis step in order (used after the climate download finishes).
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python -u src/run_sites.py > results/site_run_log.txt 2>&1
.venv/bin/python -u src/adaptation.py > results/adaptation_log.txt 2>&1
.venv/bin/python -u src/run_stock.py > results/stock_run_log.txt 2>&1
.venv/bin/python -u src/figures.py > results/figures_log.txt 2>&1
