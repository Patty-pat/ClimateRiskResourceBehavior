import pandas as pd


def _merging_all_cleaned_subfiles(base_df, anti_df, scarcity_df, quest_df):
    """Merges all cleaned subfiles into a single dataframe.

    Args:
        base_df (pandas.DataFrame): The base dataframe.
        anti_df (pandas.DataFrame): The anti dataframe.
        scarcity_df (pandas.DataFrame): The scarcity dataframe.
        quest_df (pandas.DataFrame): The quest dataframe.

    Returns:
        pandas.DataFrame: The merged dataframe containing all the cleaned subfiles.

    """
    merged_df = pd.merge(
        base_df,
        anti_df,
        on=["PLAYER_NUM", "GROUPID_ALL", "ROUND", "LAB_SESSION"],
        how="left",
    )

    merged_df = pd.merge(
        merged_df,
        scarcity_df,
        on=["PLAYER_NUM", "GROUPID_ALL", "ROUND", "LAB_SESSION"],
        how="left",
    )

    return pd.merge(
        merged_df,
        quest_df,
        on=[
            "PLAYER_NUM",
            "GROUPID_ALL",
            "LAB_SESSION",
            "groupid1",
            "groupid2",
            "groupid3",
        ],
        how="left",
    )
