import pandas as pd


def _keep_and_append_to_long(df_main):
    df_combined = pd.DataFrame()

    for j in range(1, 6):
        # Define columns to keep
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

        # Keep only the selected columns
        df_subset = df_main[cols_to_keep]

        # Rename columns by appending '_1' to each of the selected 'cs2_{j}' columns
        for col in df_subset.columns:
            if col.startswith(f"cs3_{j}"):
                df_subset = df_subset.rename(columns={col: col[5:] + "_2"})

        return pd.concat([df_combined, df_subset], ignore_index=True)
    return None


def _create_new_variables(df_combined):
    # Creating new columns
    df_combined["ROUND"] = df_combined["subsessionround_number_2"]
    df_combined["relative_playertake_2"] = df_combined["playertake_2"] / 7
    df_combined["relative_grouptake_2"] = df_combined["grouptotal_group_take_2"] / 21

    # Create start trees
    df_combined["start_trees_2"] = df_combined["groupcurrent_trees_2"].shift(1)
    # Replace NaN values in start_trees_1 with 100
    df_combined.loc[
        (df_combined["start_trees_2"].isna()) & (df_combined["ROUND"] == 1),
        "start_trees_2",
    ] = 100

    df_combined["rel_starttrees_2"] = df_combined["start_trees_2"] / 100

    # Then, create the 'othertake' variables using groupby and sum
    # We use a loop to iterate over the different member IDs
    for i in range(1, 4):
        # Define a new column name
        new_column = f"othertake{i}"

        # Apply the conditional sum grouped by 'GROUPID_ALL' and 'ROUND'
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            "playertake_2"
        ].transform(lambda x: x[df_combined["memberid2"] != i].sum())

    # Create 'other_take' variables using groupby and max
    for i in range(1, 4):
        new_column = f"other_take{i}"
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            f"othertake{i}"
        ].transform("max")

    # Initialize the 'others_take_1' column with NaNs (pandas' equivalent to Stata's ".")
    df_combined["others_take_2"] = pd.NA

    # Populate 'others_take_1' based on memberid1
    for i in range(1, 4):
        df_combined.loc[df_combined["memberid2"] == i, "others_take_2"] = df_combined[
            f"other_take{i}"
        ]

    return df_combined


def _rename_anticipation_variables(df_combined):
    rename_dict = {
        "participant_id_in_session": "playerid2",
        "subsessionround_number_2": "round_num_2",
        "playerplayer_history_take_2": "player_history_2",
        "grouptotal_group_take_2": "total_group_take_2",
        "groupcurrent_trees_after_take_2": "current_trees_af_2",
        "groupcurrent_trees_2": "current_trees_2",
        "groupregrowth_2": "regrowth_2",
    }
    # Renaming the columns
    return df_combined.rename(columns=rename_dict)


def _order_sort_drop(df_combined):
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


def clean_anticipation_data(df_main):
    df_combined = _keep_and_append_to_long(df_main)
    df_combined = _create_new_variables(df_combined)
    df_combined = _rename_anticipation_variables(df_combined)
    df_combined = _order_sort_drop(df_combined)
