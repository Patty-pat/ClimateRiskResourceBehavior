import matplotlib.pyplot as plt
import pandas as pd

from cprs.config import BLD


def load_anticipation_data(df):
    return pd.read_feather(
        BLD / "data" / "anticipation_clean.arrow",
    )  # Adjust the path and file name


def plot_individual_behavior_anticipation(df):
    """Plot individual behavior anticipation.

    This function takes a DataFrame `df` as input and plots the individual behavior anticipation
    for each group in the DataFrame. It creates a 3x8 grid of subplots, where each subplot represents
    a group. For each group, it plots the player take for each member in the group over the round number.

    Parameters:
    - df (DataFrame): The input DataFrame containing the data.

    Returns:
    - df (DataFrame): The input DataFrame.

    """
    # Unique values of GROUPID_ALL for iterating
    group_ids = df["GROUPID_ALL"].unique()

    # Create a 3x8 grid of subplots
    fig, axes = plt.subplots(3, 8, figsize=(20, 10))

    # Iterate over group_ids and plot the graphs
    for i, group_id in enumerate(group_ids):
        row = i // 8  # Calculate the row index
        col = i % 8  # Calculate the column index

        # Filter the DataFrame for the current group_id
        df_group = df[df["GROUPID_ALL"] == group_id]

        # Plot the graph: Player Take for each member in the group
        for memberid in df_group["memberid2"].unique():
            member_df = df_group[df_group["memberid2"] == memberid]
            axes[row, col].plot(
                member_df["round_num_2"],
                member_df["playertake_2"],
                label=f"Player {memberid}",
            )

        axes[row, col].set_xlabel("Round Number")
        axes[row, col].set_ylabel("Player Take")
        axes[row, col].set_title(f"Group {group_id}")

    # Remove empty subplots
    for i in range(len(group_ids), 3 * 8):
        row = i // 8  # Calculate the row index
        col = i % 8  # Calculate the column index
        fig.delaxes(axes[row, col])

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Put the legend once on the bottom
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=2)

    # Save the figure
    plt.savefig(BLD / "graphs" / "2_Individual_Beh_current_trees_anticipation.png")
    return df


def plot_group_behavior_anticipation(df):
    """Plot the group behavior anticipation graph.

    Parameters:
    - df (DataFrame): The input DataFrame containing the data.

    Returns:
    - df (DataFrame): The input DataFrame.

    This function filters the input DataFrame based on a condition, creates a grid of subplots,
    iterates over the filtered data, and plots graphs for each group. It also adjusts the spacing
    between subplots, adds a legend, and saves the figure.

    """
    # Filter the DataFrame
    df_filtered = df[df["memberid2"] == 1]

    # Unique values of GROUPID_ALL for iterating
    group_ids = df_filtered["GROUPID_ALL"].unique()

    # Create a 3x8 grid of subplots
    fig, axes = plt.subplots(3, 8, figsize=(20, 10))

    # Iterate over group_ids and plot the graphs
    for i, group_id in enumerate(group_ids):
        row = i // 8  # Calculate the row index
        col = i % 8  # Calculate the column index

        # Filter the DataFrame for the current group_id
        df_group = df_filtered[df_filtered["GROUPID_ALL"] == group_id]

        # Plot the first graph: Group Forest Stock and Total Extraction by Round
        axes[row, col].plot(
            df_group["round_num_2"],
            df_group["start_trees_2"],
            label="Group Forest Stock",
        )
        axes[row, col].plot(
            df_group["round_num_2"],
            df_group["total_group_take_2"],
            label="Group Total Extraction",
        )
        axes[row, col].set_xlabel("Round Number")
        axes[row, col].set_ylabel("Number of Trees")
        axes[row, col].set_title(f"Group {group_id}")

        # Remove empty subplots
        for i in range(len(group_ids), 3 * 8):
            row = i // 8  # Calculate the row index
            col = i % 8  # Calculate the column index
            fig.delaxes(axes[row, col])

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Put the legend once on the bottom
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=2)

    # Save the figure
    plt.savefig(BLD / "graphs" / "2_Group_Beh_remain_starting_trees_anticipation.png")
    return df


def _plot_anticipation_game_behavior(df):
    df = load_anticipation_data(df)
    plot_individual_behavior_anticipation(df)
    plot_group_behavior_anticipation(df)
    return df
