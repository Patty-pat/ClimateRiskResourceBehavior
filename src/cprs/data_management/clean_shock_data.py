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
            "high_probability",
            "shock",
            "groupid3",
            "memberid3",
        ] + [col for col in df_main.columns if col.startswith(f"cs4_{j}")]

        df_subset = df_main[cols_to_keep]

        for col in df_subset.columns:
            if col.startswith(f"cs4_{j}"):
                df_subset = df_subset.rename(columns={col: col[5:] + "_3"})

        df_combined = pd.concat([df_combined, df_subset], ignore_index=True)
    return df_combined


def create_ROUND(df_combined):
    """Creates a new column 'ROUND' in the given DataFrame.

    Parameters:
    df_combined (pandas.DataFrame): The DataFrame to modify.

    Returns:
    pandas.DataFrame: The modified DataFrame with the new 'ROUND' column.

    """
    df_combined["ROUND"] = df_combined["subsessionround_number_3"]
    return df_combined


def create_relative_player_and_group_extraction(df_combined):
    """Calculates the relative player and group extraction values based on the given
    DataFrame.

    Parameters:
    df_combined (pandas.DataFrame): The DataFrame containing the necessary columns.

    Returns:
    pandas.DataFrame: The DataFrame with the calculated relative player and group extraction values.

    """
    df_combined["rel_playertake_3"] = (
        df_combined["playertake_3"] / df_combined["groupceiling_group_take_3"]
    )
    df_combined["rel_grouptake_3"] = df_combined["grouptotal_group_take_3"] / (
        df_combined["groupceiling_group_take_3"] * 3
    )
    return df_combined


def create_starting_number_of_trees_in_every_round(df_combined):
    """Creates the starting number of trees in every round based on the previous round's
    value.

    Args:
        df_combined (DataFrame): The combined DataFrame containing the data.

    Returns:
        DataFrame: The modified DataFrame with the starting number of trees in every round.

    """
    df_combined["start_trees_3"] = df_combined["groupcurrent_trees_3"].shift(1)
    df_combined.loc[
        (df_combined["start_trees_3"].isna()) & (df_combined["ROUND"] == 1),
        "start_trees_3",
    ] = 50
    return df_combined


def create_relative_number_of_starting_trees_in_every_round(df_combined):
    df_combined["rel_starttrees_3"] = df_combined["start_trees_3"] / 50
    return df_combined


def create_number_of_trees_other_group_member_take(df_combined):
    """Create 'othertake' and 'other_take' variables based on groupby and conditional
    sum.

    Args:
        df_combined (DataFrame): The input DataFrame containing the data.

    Returns:
        DataFrame: The modified DataFrame with the 'othertake' and 'other_take' variables added.

    """
    for i in range(1, 4):
        new_column = f"othertake{i}"

        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            "playertake_3"
        ].transform(lambda x: x[df_combined["memberid3"] != i].sum())

    for i in range(1, 4):
        new_column = f"other_take{i}"
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            f"othertake{i}"
        ].transform("max")

    df_combined["others_take_3"] = pd.NA

    for i in range(1, 4):
        df_combined.loc[df_combined["memberid3"] == i, "others_take_3"] = df_combined[
            f"other_take{i}"
        ]
    return df_combined


def rename_scarcity_variables(df_combined):
    """Renames specific columns in the given DataFrame.

    Args:
        df_combined (pandas.DataFrame): The DataFrame containing the columns to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with renamed columns.

    """
    rename_dict = {
        "participant_id_in_session": "playerid3",
        "subsessionround_number_3": "round_num_3",
        "playerplayer_history_take_3": "player_history_3",
        "grouptotal_group_take_3": "total_group_take_3",
        "groupcurrent_trees_after_take_3": "current_trees_af_3",
        "groupcurrent_trees_3": "current_trees_3",
        "groupregrowth_3": "regrowth_3",
    }

    return df_combined.rename(columns=rename_dict)


def order_sort_drop(df_combined):
    """Reorders the columns of the DataFrame, sorts it based on specific columns, drops
    intermediate columns, and sorts it again based on different columns.

    Args:
        df_combined (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: The modified DataFrame with reordered columns,
        sorted based on specific columns, and intermediate columns dropped.

    """
    cols_to_order = ["PLAYER_NUM", "LAB_SESSION", "GROUPID_ALL", "ROUND"]
    new_columns = cols_to_order + (df_combined.columns.drop(cols_to_order).tolist())
    df_combined = df_combined[new_columns]

    df_combined = df_combined.sort_values(by=["GROUPID_ALL", "ROUND", "memberid3"])

    df_combined = df_combined.drop(
        columns=[
            "playerrole_3",
            "othertake1",
            "othertake2",
            "othertake3",
            "other_take1",
            "other_take2",
            "other_take3",
        ],
    )

    return df_combined.sort_values(by=["ROUND", "GROUPID_ALL"])


def _clean_scarcity_data(df_main):
    df_combined = keep_and_append_to_long(df_main)
    df_combined = create_ROUND(df_combined)
    df_combined = create_relative_player_and_group_extraction(df_combined)
    df_combined = create_starting_number_of_trees_in_every_round(df_combined)
    df_combined = create_relative_number_of_starting_trees_in_every_round(df_combined)
    df_combined = create_number_of_trees_other_group_member_take(df_combined)
    df_combined = rename_scarcity_variables(df_combined)
    return order_sort_drop(df_combined)
