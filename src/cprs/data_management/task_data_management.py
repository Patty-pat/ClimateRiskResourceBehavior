"""Tasks for managing the data."""
from pathlib import Path

import pandas as pd
from pytask import task

from cprs.config import BLD, DATA
from cprs.data_management.clean_anticipation_data import _clean_anticipation_data
from cprs.data_management.clean_baseline_data import _clean_baseline_data
from cprs.data_management.clean_data import _clean_data
from cprs.data_management.clean_scarcity_data import _clean_scarcity_data


@task
def task_clean_data(
    raw_file=Path(DATA / "all_apps_wide_2024-01-18.csv"),
    produces=BLD / "data" / "data_clean.arrow",
):
    pd.read_csv(raw_file)
    clean = _clean_data(raw_file)  # Pass the raw DataFrame directly
    clean.to_feather(produces)


@task(after=task_clean_data)
def task_clean_baseline(
    depends=BLD / "data" / "data_clean.arrow",
    produces=BLD / "data" / "baseline_clean.arrow",
):
    clean_data = pd.read_feather(depends)
    clean = _clean_baseline_data(clean_data)  # Pass the clean DataFrame
    clean.to_feather(produces)


@task(after=task_clean_baseline)
def task_clean_anticipation(
    depends=BLD / "data" / "data_clean.arrow",
    produces=BLD / "data" / "anticipation_clean.arrow",
):
    clean_data = pd.read_feather(depends)
    clean = _clean_anticipation_data(clean_data)  # Pass the clean DataFrame
    clean.to_feather(produces)


@task(after=task_clean_anticipation)
def task_clean_scarcity(
    depends=BLD / "data" / "data_clean.arrow",
    produces=BLD / "data" / "scarcity_clean.arrow",
):
    clean_data = pd.read_feather(depends)
    clean = _clean_scarcity_data(clean_data)  # Pass the clean DataFrame
    clean.to_feather(produces)
