"""Tasks running the core analyses."""

from pathlib import Path
from typing import Annotated

import matplotlib.pyplot as plt
import pandas as pd
from pytask import Product, task

from cprs.config import BLD, SRC
from cprs.data_management.task_data_management import task_clean_baseline

_PRODUCTS1 = {
    "Individual1": BLD / "graphs" / "1_Individual_Beh_current_trees_baseline.png",
    "Group1": BLD / "graphs" / "1_Group_Beh_remain_starting_trees_baseline.png",
}

_PRODUCTS2 = {
    "Individual2": BLD / "graphs" / "2_Individual_Beh_current_trees_anticipation.png",
    "Group2": BLD / "graphs" / "2_Group_Beh_remain_starting_trees_anticipation.png",
}

_PRODUCTS3 = {
    "Individual3": BLD / "graphs" / "3_Individual_Beh_current_trees_shock.png",
    "Group3": BLD / "graphs" / "3_Group_Beh_remain_starting_trees_shock.png",
}

_NASH1 = {
    "Nash1": BLD / "graphs" / "0.Nash&Cooperative Baseline.png",
    "Tradeoff1": BLD / "graphs" / "0.Tradeoff1.png",
}

_NASH2 = {
    "Nash2": BLD / "graphs" / "0.Nash&Cooperative Anticipation.png",
    "Tradeoff2": BLD / "graphs" / "0.Tradeoff2.png",
}

_NASH3 = {
    "Nash3": BLD / "graphs" / "0.Nash&Cooperative Scarcity.png",
    "Tradeoff3": BLD / "graphs" / "0.Tradeoff3.png",
}


@task(after=task_clean_baseline)
def task_plot_baseline(
    path_to_data: Path = BLD / "data" / "baseline_clean.arrow",
    path_to_plot: Annotated[Path, Product] = _PRODUCTS1,
) -> None:
    df = pd.read_feather(path_to_data)
    _, ax = plt.subplots()
    df.plot(x="x", y="y", ax=ax, kind="scatter")

    plt.savefig(path_to_plot)
    plt.close()


@task(after=task_clean_baseline)
def task_plot_nash_baseline(
    path_to_data: Path = SRC / "data" / "Nash.xlsx",
    sheet_name="Nash Baseline",
    path_to_plot: Annotated[Path, Product] = _NASH1,
):
    df = pd.read_excel(path_to_data)
    _, ax = plt.subplots()
    df.plot(x="x", y="y", ax=ax, kind="scatter")

    plt.savefig(path_to_plot)
    plt.close()


# def task_plot_baseline(
# ):


# def task_plot_anticipation(
# ):


# def task_plot_scarcity(
# ):


# def task_plot_nash_baseline(
# ):


# def task_plot_nash_anticipation(
# ):


# def task_plot_nash_scarcity(
# ):
