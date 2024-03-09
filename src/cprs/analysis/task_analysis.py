"""Tasks running the core analyses."""

import pandas as pd
from pytask import task

from cprs.analysis.nash_anticipation import _plot_anticipation_nash
from cprs.analysis.nash_baseline import _plot_baseline_nash
from cprs.analysis.nash_scarcity import _plot_scarcity_nash
from cprs.analysis.plot_anticipation_results import _plot_anticipation_game_behavior
from cprs.analysis.plot_baseline_results import _plot_baseline_game_behavior
from cprs.analysis.plot_scarcity_results import _plot_scarcity_game_behavior
from cprs.config import BLD, SRC

_PRODUCTS1 = {
    "Individual1": BLD / "graphs" / "1_Individual_Beh_current_trees_baseline.png",
    "Group2": BLD / "graphs" / "1_Group_Beh_remain_starting_trees_baseline.png",
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
    "Nash2": BLD / "graphs" / "0.Nash&Cooperative Scarcity.png",
    "Tradeoff2": BLD / "graphs" / "0.Tradeoff3.png",
}


@task
def task_plot_baseline(
    depends_on=BLD / "data" / "baseline_clean.arrow",
    produces=_PRODUCTS1,
):
    df = pd.read_feather(depends_on)
    _plot_baseline_game_behavior(df)


@task
def task_plot_anticipation(
    depends_on=BLD / "data" / "anticipation_clean.arrow",
    produces=_PRODUCTS2,
):
    df = pd.read_feather(depends_on)
    _plot_anticipation_game_behavior(df)


@task
def task_plot_scarcity(
    depends_on=BLD / "data" / "scarcity_clean.arrow",
    produces=_PRODUCTS3,
):
    df = pd.read_feather(depends_on)
    _plot_scarcity_game_behavior(df)


@task
def task_plot_nash_baseline(
    depends_on=SRC / "data" / "Nash.xlsx",
    sheet_name="Nash Baseline",
    produces=_NASH1,
):
    df = pd.read_excel(depends_on)
    _plot_baseline_nash(df)


@task
def task_plot_nash_anticipation(
    depends_on=SRC / "data" / "Nash.xlsx",
    sheet_name="Anticipation",
    produces=_NASH2,
):
    df = pd.read_excel(depends_on)
    _plot_anticipation_nash(df)


@task
def task_plot_nash_scarcity(
    depends_on=SRC / "data" / "Nash.xlsx",
    sheet_name="Scarcity",
    produces=_NASH3,
):
    df = pd.read_excel(depends_on)
    _plot_scarcity_nash(df)
