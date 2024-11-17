import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from cprs.config import BLD, SRC


def import_excel_nash(df):
    """Imports an Excel file containing Nash baseline data.

    Parameters:
    - df: DataFrame
        The DataFrame to store the imported data.

    Returns:
    - DataFrame
        The imported data as a DataFrame.

    """
    return pd.read_excel(SRC / "data" / "Nash.xlsx", sheet_name="Nash Baseline")


def plot_nash_equilibrium_and_cooperative_optimum_baseline(df):
    """Plots the Nash Equilibrium and Cooperative Optimum in CPR Aggregate Extraction.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the data for plotting.

    Returns:
        pandas.DataFrame: The input DataFrame.

    """
    plt.figure(figsize=(8, 6))

    sns.lineplot(
        x="Round",
        y=" tot_extract",
        data=df[df["Type"] == 1],
        marker="",
        label="Nash Total Group Extraction",
    )
    sns.lineplot(
        x="Round",
        y=" tot_extract",
        data=df[df["Type"] == 5],
        marker="",
        label="Cooperative Optimum Total Group Extraction",
    )
    sns.lineplot(
        x="Round",
        y="Start_Stock",
        data=df[df["Type"] == 1],
        marker="o",
        color="black",
        label="Nash Equilibrium",
    )
    sns.lineplot(
        x="Round",
        y="Start_Stock",
        data=df[df["Type"] == 5],
        marker="o",
        color="maroon",
        label="Cooperative Optimum",
    )

    plt.title("Nash Equilibrium and Cooperative Optimum in CPR Aggregate Extraction")
    plt.legend(fontsize="small")
    plt.ylim(-5, 115)  # Adjust this range as necessary
    plt.xticks([1, 2, 3, 4, 5])  # Adjust these ticks as necessary
    plt.xlabel("Round")
    plt.ylabel("Starting Number of Trees")
    plt.legend(loc="best")

    sns.set_style("white", {"axes.grid": False})

    plt.savefig(BLD / "graphs" / "0.Nash&Cooperative Baseline.png")
    return df


def plot_expected_total_social_payoff_baseline(df):
    """Plots the expected total social payoff against the 'Take' variable in the given
    DataFrame.

    Parameters:
    df (DataFrame): The input DataFrame containing the data to be plotted.

    Returns:
    DataFrame: The original DataFrame.

    """
    filtered_df = df[df["Expected Total Social Payoff"].notna()]

    plt.figure(figsize=(8, 6))
    sns.lineplot(
        x="Take",
        y="Expected Total Social Payoff",
        data=filtered_df,
        marker="o",
        label="Expected Total Social Payoff",
        sort=False,
    )

    plt.axvline(
        x=3,
        color="k",
        linestyle="--",
        label="Cut-off between Altruistic and Selfish",
    )

    plt.title(
        "Trade-off Between Potential Payoff Selfish vs Efficient Social Optimum",
        fontsize="medium",
    )
    plt.legend(fontsize="small")
    plt.gca().set_facecolor("white")

    plt.savefig(BLD / "graphs" / "0.Tradeoff1.png")
    return df


def _plot_baseline_nash(df):
    df = import_excel_nash(df)
    plot_nash_equilibrium_and_cooperative_optimum_baseline(df)
    plot_expected_total_social_payoff_baseline(df)
    return df
