"""Tasks for managing the data."""
from pathlib import Path

import pandas as pd
from pytask import task

from cprs.config import BLD, DATA
from cprs.data_management.clean_anticipation_data import _clean_anticipation_data
from cprs.data_management.clean_baseline_data import _clean_baseline_data
from cprs.data_management.clean_questionnaire import _clean_questionnaire_data
from cprs.data_management.clean_raw_data import _clean_data
from cprs.data_management.clean_shock_data import _clean_scarcity_data
from cprs.data_management.merge_clean_all_parts import _merging_all_cleaned_subfiles

_DEPENDENCIES = {
    "base": BLD / "data" / "baseline_clean.arrow",
    "anti": BLD / "data" / "anticipation_clean.arrow",
    "scarcity": BLD / "data" / "scarcity_clean.arrow",
    "quest": BLD / "data" / "questionnaire_clean.arrow",
}


@task
def task_clean_data(
    raw_file=Path(DATA / "all_apps_wide_2024-01-18.csv").resolve(),
    produces=BLD / "data" / "data_clean.arrow",
):
    df = pd.read_csv(raw_file)
    clean = _clean_data(df)  # Pass the DataFrame variable to the clean_data function
    clean.to_feather(produces)


@task(after=task_clean_data)
def task_clean_baseline(
    depends=Path(BLD / "data" / "data_clean.arrow"),
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
def task_clean_shock(
    depends=BLD / "data" / "data_clean.arrow",
    produces=BLD / "data" / "scarcity_clean.arrow",
):
    clean_data = pd.read_feather(depends)
    clean = _clean_scarcity_data(clean_data)  # Pass the clean DataFrame
    clean.to_feather(produces)


@task(after=task_clean_shock)
def task_clean_questionnaire(
    depends=BLD / "data" / "data_clean.arrow",
    produces=BLD / "data" / "questionnaire_clean.arrow",
):
    clean_data = pd.read_feather(depends)
    clean = _clean_questionnaire_data(clean_data)  # Pass the clean DataFrame
    clean.to_feather(produces)


@task(after=task_clean_questionnaire)
def task_merge_all_sub_datafiles(
    depends=_DEPENDENCIES,
    produces=BLD / "data" / "ALL_CLEANED.arrow",
):
    base_df = pd.read_feather(depends["base"])
    anti_df = pd.read_feather(depends["anti"])
    scarcity_df = pd.read_feather(depends["scarcity"])
    quest_df = pd.read_feather(
        depends["quest"],
    )  # Add 'quest' to _DEPENDENCIES if it's a separate file

    merged_df = _merging_all_cleaned_subfiles(base_df, anti_df, scarcity_df, quest_df)

    merged_df.to_feather(produces)
