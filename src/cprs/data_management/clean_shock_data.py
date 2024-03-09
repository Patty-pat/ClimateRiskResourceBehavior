import pandas as pd


def keep_and_append_to_long(df_main):
    df_combined = pd.DataFrame()

    for j in range(1, 6):
        # Define columns to keep
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

        # Keep only the selected columns
        df_subset = df_main[cols_to_keep]

        # Rename columns by appending '_1' to each of the selected 'cs2_{j}' columns
        for col in df_subset.columns:
            if col.startswith(f"cs4_{j}"):
                df_subset = df_subset.rename(columns={col: col[5:] + "_3"})

        df_combined = pd.concat([df_combined, df_subset], ignore_index=True)

    return df_combined


def create_new_variables(df_combined):
    # Creating new columns
    df_combined["ROUND"] = df_combined["subsessionround_number_3"]
    df_combined["rel_playertake_3"] = (
        df_combined["playertake_3"] / df_combined["groupceiling_group_take_3"]
    )
    df_combined["rel_grouptake_3"] = df_combined["grouptotal_group_take_3"] / (
        df_combined["groupceiling_group_take_3"] * 3
    )

    # Create start trees
    df_combined["start_trees_3"] = df_combined["groupcurrent_trees_3"].shift(1)
    # Replace NaN values in start_trees_1 with 50
    df_combined.loc[
        (df_combined["start_trees_3"].isna()) & (df_combined["ROUND"] == 1),
        "start_trees_3",
    ] = 50

    df_combined["rel_starttrees_3"] = df_combined["start_trees_3"] / 50

    # Then, create the 'othertake' variables using groupby and sum
    # We use a loop to iterate over the different member IDs
    for i in range(1, 4):
        # Define a new column name
        new_column = f"othertake{i}"

        # Apply the conditional sum grouped by 'GROUPID_ALL' and 'ROUND'
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            "playertake_3"
        ].transform(lambda x: x[df_combined["memberid3"] != i].sum())

    # Create 'other_take' variables using groupby and max
    for i in range(1, 4):
        new_column = f"other_take{i}"
        df_combined[new_column] = df_combined.groupby(["GROUPID_ALL", "ROUND"])[
            f"othertake{i}"
        ].transform("max")

    # Initialize the 'others_take_1' column with NaNs (pandas' equivalent to Stata's ".")
    df_combined["others_take_3"] = pd.NA

    # Populate 'others_take_1' based on memberid1
    for i in range(1, 4):
        df_combined.loc[df_combined["memberid3"] == i, "others_take_3"] = df_combined[
            f"other_take{i}"
        ]

    rename_dict = {
        "participant_id_in_session": "playerid3",
        "subsessionround_number_3": "round_num_3",
        "playerplayer_history_take_3": "player_history_3",
        "grouptotal_group_take_3": "total_group_take_3",
        "groupcurrent_trees_after_take_3": "current_trees_af_3",
        "groupcurrent_trees_3": "current_trees_3",
        "groupregrowth_3": "regrowth_3",
    }

    # Renaming the columns
    return df_combined.rename(columns=rename_dict)


def order_sort_drop(df_combined):
    # Reorder ROUND after GROUPID
    cols_to_order = ["PLAYER_NUM", "LAB_SESSION", "GROUPID_ALL", "ROUND"]
    new_columns = cols_to_order + (df_combined.columns.drop(cols_to_order).tolist())
    df_combined = df_combined[new_columns]

    # Sorting the DataFrame for the following operations
    df_combined = df_combined.sort_values(by=["GROUPID_ALL", "ROUND", "memberid3"])

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


def _clean_shock_data(df_main):
    df_combined = keep_and_append_to_long(df_main)
    df_combined = create_new_variables(df_combined)
    return order_sort_drop(df_combined)
