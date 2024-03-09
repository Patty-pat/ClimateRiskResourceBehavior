import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from cprs.config import BLD, SRC


def import_excel_nash(df):
    return pd.read_excel(SRC / "data" / "Nash.xlsx", sheet_name="Anticipation")


def plot_nash_equilibrium_and_cooperative_optimum_anticipation(df):
    # Creating subplots
    plt.figure(figsize=(8, 6))

    # Plotting connected scatter plots and line plots
    # Replace 'tot_extract' and 'Round' with the actual column names if they differ
    sns.lineplot(
        x="Round",
        y="tot_extract",
        data=df[df["Type"] == 1],
        marker="",
        label="Nash Total Group Extraction",
    )
    sns.lineplot(
        x="Round",
        y="tot_extract",
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

    plt.savefig(BLD / "graphs" / "0.Nash&Cooperative Anticipation.png")
    return df


def plot_expected_total_social_payoff_anticipation(df):
    df = df[df["Expected Total Social Payoff"].notna()]

    # Filtering data for HIGH and LOW probabilities
    df_high = df[df["hi-lo"] == "HIGH"]
    df_low = df[df["hi-lo"] == "LOW"]

    # Create the plot
    plt.figure(figsize=(8, 6))
    sns.lineplot(
        x="Take",
        y="Expected Total Social Payoff",
        data=df_high,
        marker="o",
        label="High Probability",
    )
    sns.lineplot(
        x="Take",
        y="Expected Total Social Payoff",
        data=df_low,
        marker="o",
        label="Low Probability",
    )

    # Adding an xline at 3
    plt.axvline(x=3, color="k", linestyle="--", label="Cut-off")

    # Customizing the plot
    plt.title(
        "Trade-off Between Potential Payoff Selfish vs Efficient Social Optimum by Risk Type",
    )
    plt.legend(fontsize="medium")
    plt.gca().set_facecolor("white")

    # Show or save the plot
    plt.savefig(BLD / "graphs" / "0.Tradeoff2.png")
    return df


def _plot_anticipation_nash(df):
    df = import_excel_nash(df)
    plot_nash_equilibrium_and_cooperative_optimum_anticipation(df)
    plot_expected_total_social_payoff_anticipation(df)
    return df
