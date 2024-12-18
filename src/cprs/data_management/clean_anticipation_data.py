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
            "participant_high_probability",
            "participant_is_shock_group",
            "high_probability",
            "shock",
            "groupid2",
            "memberid2",
        ] + [col for col in df_main.columns if col.startswith(f"cs3_{j}")]

        df_subset = df_main[cols_to_keep]

        for col in df_subset.columns:
            if col.startswith(f"cs3_{j}"):
                df_subset = df_subset.rename(columns={col: col[5:] + "_2"})

        df_combined = pd.concat([df_combined, df_subset], ignore_index=True)

    return df_combined


def create_new_variables(df_combined):
    """Creates new variables based on the produced long data frame.

    Args:
        df_combined (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: The modified DataFrame with new variables.

    """
    df_combined["ROUND"] = df_combined["subsessionround_number_2"]
    df_combined["relative_playertake_2"] = df_combined["playertake_2"] / 7
    df_combined["relative_grouptake_2"] = df_combined["grouptotal_group_take_2"] / 21

    df_combined["start_trees_2"] = df_combined["groupcurrent_trees_2"].shift(1)
    df_combined.loc[
        (df_combined["start_trees_2"].isna()) & (df_combined["ROUND"] == 1),
        "start_trees_2",
    ] = 100

    df_combined["rel_starttrees_2"] = df_combined["start_trees_2"] / 100

    for i in range(1, 4):
        new_column = f"othertake{i}"

        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            "playertake_2"
        ].transform(lambda x: x[df_combined["memberid2"] != i].sum())

    for i in range(1, 4):
        new_column = f"other_take{i}"
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            f"othertake{i}"
        ].transform("max")

    df_combined["others_take_2"] = pd.NA

    for i in range(1, 4):
        df_combined.loc[df_combined["memberid2"] == i, "others_take_2"] = df_combined[
            f"other_take{i}"
        ]

    return df_combined


def rename_anticipation_variables(df_combined):
    """Renames specific columns in the given DataFrame.

    Args:
        df_combined (pandas.DataFrame): The DataFrame containing the columns to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with renamed columns.

    """
    rename_dict = {
        "participant_id_in_session": "playerid2",
        "subsessionround_number_2": "round_num_2",
        "playerplayer_history_take_2": "player_history_2",
        "grouptotal_group_take_2": "total_group_take_2",
        "groupcurrent_trees_after_take_2": "current_trees_af_2",
        "groupcurrent_trees_2": "current_trees_2",
        "groupregrowth_2": "regrowth_2",
    }
    return df_combined.rename(columns=rename_dict)


def order_sort_drop(df_combined):
    """Reorders the columns of the DataFrame `df_combined` to have "ROUND" after
    "GROUPID", sorts the DataFrame by "GROUPID_ALL", "ROUND", and "memberid2", drops
    intermediate columns, and sorts the DataFrame by "ROUND" and "GROUPID_ALL".

    Parameters:
        df_combined (pandas.DataFrame): The input DataFrame to be processed.

    Returns:
        pandas.DataFrame: The processed DataFrame with reordered columns, sorted by specified columns,
                          and with intermediate columns dropped.

    """
    # Reorder ROUND after GROUPID
    cols_to_order = ["PLAYER_NUM", "LAB_SESSION", "GROUPID_ALL", "ROUND"]
    new_columns = cols_to_order + (df_combined.columns.drop(cols_to_order).tolist())
    df_combined = df_combined[new_columns]

    # Sorting the DataFrame for the following operations
    df_combined = df_combined.sort_values(by=["GROUPID_ALL", "ROUND", "memberid2"])

    # Dropping intermediate columns
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

    # Sorting the DataFrame
    return df_combined.sort_values(by=["ROUND", "GROUPID_ALL"])


def _clean_anticipation_data(df_main):
    df_combined = keep_and_append_to_long(df_main)
    df_combined = create_new_variables(df_combined)
    df_combined = rename_anticipation_variables(df_combined)
    return order_sort_drop(df_combined)
