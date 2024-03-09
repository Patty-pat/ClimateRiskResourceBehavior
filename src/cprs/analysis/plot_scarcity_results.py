import matplotlib.pyplot as plt
import pandas as pd

from cprs.config import BLD


def load_shock_data(df):
    return pd.read_feather(
        BLD / "data" / "scarcity_clean.arrow",
    )  # Adjust the path and file name


def plot_individual_behavior_shock(df):
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
        for memberid in df_group["memberid3"].unique():
            member_df = df_group[df_group["memberid3"] == memberid]
            axes[row, col].plot(
                member_df["round_num_3"],
                member_df["playertake_3"],
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
    plt.savefig(BLD / "graphs" / "3_Individual_Beh_current_trees_shock.png")
    return df


def plot_group_behavior_shock(df):
    # Filter the DataFrame
    df_filtered = df[df["memberid3"] == 1]

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
            df_group["round_num_3"],
            df_group["start_trees_3"],
            label="Group Forest Stock",
        )
        axes[row, col].plot(
            df_group["round_num_3"],
            df_group["total_group_take_3"],
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
    plt.savefig(BLD / "graphs" / "3_Group_Beh_remain_starting_trees_shock.png")
    return df


def _plot_scarcity_game_behavior(df):
    df = load_shock_data(df)
    plot_individual_behavior_shock(df)
    plot_group_behavior_shock(df)
    return df
