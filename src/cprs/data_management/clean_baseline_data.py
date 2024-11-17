import pandas as pd


def keep_and_append_to_long(df_main):
    """Transforming data from wide to long from the input DataFrame to a new DataFrame,
    keeping only relevant variables.

    Parameters:
    - df_main (pandas.DataFrame): The main DataFrame containing the data.

    Returns:
    - df_combined (pandas.DataFrame): The combined DataFrame with the selected columns and appended to create long data.

    """
    df_combined = pd.DataFrame()

    for j in range(1, 6):
        cols_to_keep = [
            "PLAYER_NUM",
            "LAB_SESSION",
            "GROUPID_ALL",
            "participant_id_in_session",
            "groupid1",
            "memberid1",
        ] + [col for col in df_main.columns if col.startswith(f"cs2_{j}")]

        df_subset = df_main[cols_to_keep]

        for col in df_subset.columns:
            if col.startswith(f"cs2_{j}"):
                df_subset = df_subset.rename(columns={col: col[5:] + "_1"})

        df_combined = pd.concat([df_combined, df_subset], ignore_index=True)

    return df_combined


def create_ROUND(df_combined):
    """Create a new column 'ROUND' in the given DataFrame.

    Parameters:
    df_combined (pandas.DataFrame): The DataFrame containing the data.

    Returns:
    pandas.DataFrame: The DataFrame with the 'ROUND' column added.

    """
    df_combined["ROUND"] = df_combined["subsessionround_number_1"]
    return df_combined


def create_relative_player_harvest_in_baseline(df_combined):
    df_combined["relative_playertake_1"] = df_combined["playertake_1"] / 7
    return df_combined


def create_relative_group_harvest_in_baseline(df_combined):
    """Calculates the relative group take for each entry in the given DataFrame.

    Parameters:
    df_combined (pandas.DataFrame): The DataFrame containing the data.

    Returns:
    pandas.DataFrame: The DataFrame with the calculated relative group take.

    """
    df_combined["relative_grouptake_1"] = df_combined["grouptotal_group_take_1"] / 21
    return df_combined


def create_starting_number_of_trees_in_each_round(df_combined):
    """Creates the starting number of trees in each round based on the previous round's
    value.

    Args:
        df_combined (DataFrame): The combined DataFrame containing the data.

    Returns:
        DataFrame: The modified DataFrame with the new column 'start_trees_1' added.

    """
    df_combined["start_trees_1"] = df_combined["groupcurrent_trees_1"].shift(1)
    df_combined.loc[
        (df_combined["start_trees_1"].isna()) & (df_combined["ROUND"] == 1),
        "start_trees_1",
    ] = 100
    return df_combined


def create_relative_starting_trees(df_combined):
    df_combined["rel_starttrees_1"] = df_combined["start_trees_1"] / 100
    return df_combined


def create_other_group_members_harvest(df_combined):
    """Create 'othertake' and 'other_take' variables based on groupby and sum/max
    operations.

    Args:
        df_combined (pandas.DataFrame): The input DataFrame containing the data.

    Returns:
        pandas.DataFrame: The DataFrame with the 'othertake' and 'other_take' variables added.

    """
    for i in range(1, 4):
        # Define a new column name
        new_column = f"othertake{i}"

        # Apply the conditional sum grouped by 'GROUPID_ALL' and 'ROUND'
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            "playertake_1"
        ].transform(lambda x: x[df_combined["memberid1"] != i].sum())

    for i in range(1, 4):
        new_column = f"other_take{i}"
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            f"othertake{i}"
        ].transform("max")

    df_combined["others_take_1"] = pd.NA

    for i in range(1, 4):
        df_combined.loc[df_combined["memberid1"] == i, "others_take_1"] = df_combined[
            f"other_take{i}"
        ]

    return df_combined


def rename_variables_baseline(df_combined):
    """Renames specific columns in the given DataFrame.

    Args:
        df_combined (pandas.DataFrame): The DataFrame containing the columns to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with renamed columns.

    """
    rename_dict = {
        "participant_id_in_session": "playerid1",
        "subsessionround_number_1": "round_num_1",
        "playerplayer_history_take_1": "player_history_1",
        "grouptotal_group_take_1": "total_group_take_1",
        "groupcurrent_trees_after_take_1": "current_trees_af_1",
        "groupcurrent_trees_1": "current_trees_1",
        "groupregrowth_1": "regrowth_1",
    }

    return df_combined.rename(columns=rename_dict)


def order_sort_drop(df_combined):
    """Reorders the columns of the DataFrame, sorts it based on specific columns, and
    drops intermediate columns.

    Args:
        df_combined (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: The modified DataFrame with reordered columns,
        sorted based on specific columns, and intermediate columns dropped.

    """
    cols_to_order = ["PLAYER_NUM", "LAB_SESSION", "GROUPID_ALL", "ROUND"]
    new_columns = cols_to_order + (df_combined.columns.drop(cols_to_order).tolist())
    df_combined = df_combined[new_columns]

    df_combined = df_combined.sort_values(by=["GROUPID_ALL", "ROUND", "memberid1"])

    df_combined = df_combined.drop(
        columns=[
            "othertake1",
            "othertake2",
            "othertake3",
            "other_take1",
            "other_take2",
            "other_take3",
        ],
    )
    df_combined.sort_values(by=["ROUND", "GROUPID_ALL"])

    return df_combined


def _clean_baseline_data(df_main):
    df_combined = keep_and_append_to_long(df_main)
    df_combined = create_ROUND(df_combined)
    df_combined = create_relative_player_harvest_in_baseline(df_combined)
    df_combined = create_relative_group_harvest_in_baseline(df_combined)
    df_combined = create_starting_number_of_trees_in_each_round(df_combined)
    df_combined = create_relative_starting_trees(df_combined)
    df_combined = create_other_group_members_harvest(df_combined)
    df_combined = rename_variables_baseline(df_combined)
    return order_sort_drop(df_combined)
