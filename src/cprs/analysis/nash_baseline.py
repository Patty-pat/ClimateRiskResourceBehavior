import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from cprs.config import BLD, SRC


def import_excel_nash(df):
    return pd.read_excel(SRC / "data" / "Nash.xlsx", sheet_name="Nash Baseline")


def plot_nash_equilibrium_and_cooperative_optimum_baseline(df):
    # Creating subplots
    plt.figure(figsize=(8, 6))

    # Plotting connected scatter plots and line plots
    # Replace 'tot_extract' and 'Round' with the actual column names if they differ
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

    # Customizing the plot
    plt.title("Nash Equilibrium and Cooperative Optimum in CPR Aggregate Extraction")
    plt.legend(fontsize="small")
    plt.ylim(-5, 115)  # Adjust this range as necessary
    plt.xticks([1, 2, 3, 4, 5])  # Adjust these ticks as necessary
    plt.xlabel("Round")
    plt.ylabel("Starting Number of Trees")
    plt.legend(loc="best")

    # Remove the grids
    sns.set_style("white", {"axes.grid": False})

    plt.savefig(BLD / "graphs" / "0.Nash&Cooperative Baseline.png")
    return df


def plot_expected_total_social_payoff_baseline(df):
    # Filtering out rows where 'ExpectedTotalSocialPayoff' is NaN
    filtered_df = df[df["Expected Total Social Payoff"].notna()]

    # Create the connected scatter plot
    plt.figure(figsize=(8, 6))
    sns.lineplot(
        x="Take",
        y="Expected Total Social Payoff",
        data=filtered_df,
        marker="o",
        label="Expected Total Social Payoff",
        sort=False,
    )

    # Add an x-line at 3 with label
    plt.axvline(
        x=3,
        color="k",
        linestyle="--",
        label="Cut-off between Altruistic and Selfish",
    )

    # Customizing the plot
    plt.title(
        "Trade-off Between Potential Payoff Selfish vs Efficient Social Optimum",
        fontsize="medium",
    )
    plt.legend(fontsize="small")
    plt.gca().set_facecolor("white")

    # Show or save the plot
    plt.savefig(BLD / "graphs" / "0.Tradeoff1.png")
    return df


def _plot_baseline_nash(df):
    df = import_excel_nash(df)
    plot_nash_equilibrium_and_cooperative_optimum_baseline(df)
    plot_expected_total_social_payoff_baseline(df)
    return df
