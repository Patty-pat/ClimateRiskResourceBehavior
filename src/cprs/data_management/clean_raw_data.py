import pandas as pd


def remove_dots_in_variable_names(df):
    """Removes dots in variable names of a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the variable names with dots.

    Returns:
        pandas.DataFrame: The DataFrame with the dots removed from the variable names.

    """
    for column in df.columns:
        new_column = column.replace(".", "")
        df = df.rename(columns={column: new_column})

    return df


def create_global_identifier_player_number(df):
    """Creates a global identifier for each player in the DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing player data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional column "PLAYER_NUM" that represents the global identifier for each player.

    """
    df["PLAYER_NUM"] = df.index + 1
    return df


def create_global_identifier_lab_session_number(df):
    """Assigns a global identifier for each lab session based on the player number.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the player number.

    Returns:
    pandas.DataFrame: The DataFrame with an additional column 'LAB_SESSION' representing the lab session number.

    """
    df["LAB_SESSION"] = pd.cut(
        df["PLAYER_NUM"],
        bins=[0, 24, 48, float("inf")],
        labels=[1, 2, 3],
    )
    return df


def create_global_identifier_group_id_all_subjects(df):
    """Creates a new column 'GROUPID_ALL' in the DataFrame 'df' to represent the global
    identifier group ID for all subjects.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data.

    Returns:
    pandas.DataFrame: The modified DataFrame with the new column added.

    """
    df["GROUPID_ALL"] = df["CS2_Forest5groupid_in_subsession"]
    df.loc[df["LAB_SESSION"] == 2, "GROUPID_ALL"] += 8
    df.loc[df["LAB_SESSION"] == 3, "GROUPID_ALL"] += 16
    cols_to_order = ["PLAYER_NUM", "LAB_SESSION", "GROUPID_ALL"]
    new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
    return df[new_columns]


def rename_relevant_participants_identifier(df):
    """Renames the relevant participants identifier columns in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the relevant participants identifier columns.

    Returns:
        pandas.DataFrame: The DataFrame with the renamed columns.

    """
    participant_vars = [col for col in df.columns if col.startswith("participant")]

    for var in participant_vars:
        new_var_name = "participant_" + var[11:]
        df = df.rename(columns={var: new_var_name})
    return df


def remove_irrelevant_and_empty_participants_identifier(df):
    """Removes irrelevant and empty columns related to participant identifiers from the
    given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: The DataFrame with the irrelevant and empty columns removed.

    """
    columns_to_drop = [
        "participant_label",
        "participant__is_bot",
        "participant__index_in_pages",
        "participant__max_page_index",
        "participant__current_app_name",
        "participant__current_page_name",
        "participant_mturk_worker_id",
        "participant_mturk_assignment_id",
        "participant_group_id",
        "participant_covid_okay",
        "participant_ceiling_group_take",
        "participant_take_ceiling",
    ]
    return df.drop(columns=columns_to_drop, errors="ignore")


def rename_rellevant_session_identifiers(df):
    """Renames relevant session identifiers in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the session identifiers.

    Returns:
        pandas.DataFrame: The DataFrame with renamed session identifiers.

    """
    session_vars = [col for col in df.columns if col.startswith("session")]

    for var in session_vars:
        new_var_name = "s_" + var[7:]
        df = df.rename(columns={var: new_var_name})

    return df


def remove_irrelevant_and_empty_session_identifiers(df):
    """Removes irrelevant and empty session identifiers from the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the session identifiers.

    Returns:
        pandas.DataFrame: The DataFrame with the specified columns dropped.

    """
    columns_to_drop = [
        "s_label",
        "s_mturk_HITId",
        "s_mturk_HITGroupId",
        "s_comment",
        "s_is_demo",
        "s_configreal_world_currency_per_point",
        "s_configparticipation_fee",
        "s_is_shock_group",
        "s_high_probability",
        "s_shock_probability_high",
        "s_shock_probability_low",
        "s_group_id",
        "s_ceiling_group_take",
        "s_configname",
        "s_code",
    ]

    # Drop the specified columns
    return df.drop(columns=columns_to_drop, errors="ignore")


def rename_rellevant_intro_to_baseline(df):
    """Renames relevant columns in the DataFrame according to specific rules.

    Args:
        df (pandas.DataFrame): The DataFrame containing the columns to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with renamed columns.

    """
    df = df.rename(columns={"CS1_Intro1playerid_in_group": "player_cubicle"})

    cs1_intro1player_vars = [
        col for col in df.columns if col.startswith("CS1_Intro1player")
    ]
    for var in cs1_intro1player_vars:
        new_var_name = "cs1_" + var[16:]
        df = df.rename(columns={var: new_var_name})

    cs1_compr_vars = [col for col in df.columns if col.startswith("CS1_compr")]
    for var in cs1_compr_vars:
        new_var_name = "cs2_compr" + var[9:]
        df = df.rename(columns={var: new_var_name})

    return df.rename(columns={"cs1_num_failed_attempts": "failed_attem1"})


def remove_irrelevant_intro_to_baseline(df):
    """Removes irrelevant columns from the DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: The DataFrame with irrelevant columns removed.

    """
    columns_to_drop = [
        "CS1_Intro1playerrole",
        "CS1_Intro1playercode",
        "CS1_Intro1playerpayoff",
        "CS1_Intro1groupid_in_subsession",
        "CS1_Intro1subsessionround_number",
    ]
    return df.drop(columns=columns_to_drop, errors="ignore")


def rename_rellevant_baseline_variables(df):
    """Renames relevant baseline variables in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the variables to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with the renamed variables.

    """
    for j in range(1, 6):
        cs2_forest_vars = [
            col for col in df.columns if col.startswith(f"CS2_Forest{j}")
        ]
        for var in cs2_forest_vars:
            new_var_name = "cs2_" + var[10:]
            df = df.rename(columns={var: new_var_name})

    return df.rename(
        columns={
            "cs2_5groupid_in_subsession": "groupid1",
            "cs2_5playerid_in_group": "memberid1",
        },
    )


def remove_irrelevant_baseline_variables(df):
    """Removes irrelevant baseline variables from the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: The DataFrame with irrelevant baseline variables removed.

    """
    df = df.drop(columns=["cs2_5playerrole", "cs2_5playerpayoff"], errors="ignore")

    for i in range(1, 5):
        drop_vars = [
            f"cs2_{i}groupid_in_subsession",
            f"cs2_{i}playerrole",
            f"cs2_{i}playerid_in_group",
            f"cs2_{i}playerpayoff",
            f"cs2_{i}playerstage_points",
            f"cs2_{i}playerpotential_payof",
        ]
        df = df.drop(columns=drop_vars, errors="ignore")
    return df


def rename_rellevant_anticipation_variables(df):
    """Renames relevant anticipation variables in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the variables to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with the renamed variables.

    """
    # Renaming variables that follow a pattern
    for j in range(1, 6):
        cs3_anti_vars = [col for col in df.columns if col.startswith(f"CS3_Anti{j}")]

        for var in cs3_anti_vars:
            new_var_name = "cs3_" + var[9:]
            df = df.rename(columns={var: new_var_name})
    # Renaming certain variables
    return df.rename(
        columns={
            "cs3_1grouphigh_probability": "high_probability",
            "cs3_5groupid_in_subsession": "groupid2",
            "cs3_5playerid_in_group": "memberid2",
            "cs3_5groupshock_probability": "group_shock_prob_high",
            "v248": "group_shock_prob_low",
            "cs3_5groupis_shock_group": "shock",
            "cs3_1playernum_failed_attempts": "failed_attem2",
        },
    )


def remove_irrelevant_anticipation_variables(df):
    """Removes irrelevant anticipation variables from the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the anticipation variables.

    Returns:
        pandas.DataFrame: The DataFrame with the irrelevant anticipation variables removed.

    """
    for i in range(1, 5):
        drop_vars_i = [
            f"cs3_{i}playerid_in_group",
            f"cs3_{i}playerrole",
            f"cs3_{i}playerpayoff",
            f"cs3_{i}playerstage_points",
            f"cs3_{i}playerpotential_payoff",
            f"cs3_{i}groupis_shock_group",
            f"cs3_{i}groupshock_probability",
        ]
        df = df.drop(columns=drop_vars_i, errors="ignore")

    for i in range(2, 6):
        drop_vars_ii = [
            f"cs3_{i}playercompr1",
            f"cs3_{i}playercompr2",
            f"cs3_{i}playercompr3",
            f"cs3_{i}playercompr4",
            f"cs3_{i}playernum_failed_attempts",
            f"cs3_{i}grouphigh_probability",
        ]
        df = df.drop(columns=drop_vars_ii, errors="ignore")

    return df.drop(
        columns=[
            "cs3_5playerrole",
            "cs3_5playerpayoff",
            "v152",
            "v176",
            "v200",
            "v224",
        ],
        errors="ignore",
    )


def rename_relevant_scarcity_variables(df):
    """Renames relevant scarcity variables in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the variables to be renamed.

    Returns:
        pandas.DataFrame: The DataFrame with the renamed variables.

    """
    for j in range(1, 6):
        cs4_shock_vars = [col for col in df.columns if col.startswith(f"CS4_Shock{j}")]
        for var in cs4_shock_vars:
            new_var_name = "cs4_" + var[9:]
            df = df.rename(columns={var: new_var_name})

    cs4_compr_vars = [col for col in df.columns if col.startswith("cs4_1playercompr")]
    for var in cs4_compr_vars:
        new_var_name = "cs4_" + var[11:]
        df = df.rename(columns={var: new_var_name})

    # Renaming certain variables
    return df.rename(
        columns={
            "cs4_1playernum_failed_attempts": "failed_attem3",
            "cs4_5groupid_in_subsession": "groupid3",
            "cs4_5playerid_in_group": "memberid3",
        },
    )


def remove_irrelevant_scarcity_variables(df):
    """Removes irrelevant scarcity variables from the given DataFrame.

    Args:
        df (DataFrame): The input DataFrame containing the scarcity variables.

    Returns:
        DataFrame: The DataFrame with the irrelevant scarcity variables removed.

    """
    for i in range(1, 5):
        drop_vars_i = [
            f"cs4_{i}playerstage_points",
            f"cs4_{i}playerpotential_payoff",
            f"cs4_{i}groupid_in_subsession",
        ]
        df = df.drop(columns=drop_vars_i, errors="ignore")

    for i in range(2, 6):
        drop_vars_ii = [
            f"cs4_{i}playercompr1",
            f"cs4_{i}playercompr2",
            f"cs4_{i}playercompr3",
            f"cs4_{i}playercompr4",
            f"cs4_{i}playernum_failed_attempts",
        ]
        df = df.drop(columns=drop_vars_ii, errors="ignore")

    drop_vars_extra = [f"cs4_{i}playerrole", f"cs4_{i}playerpayoff"] + [
        f"cs4_{i}playertake_max{j}" for i in range(1, 6) for j in range(7, -1, -1)
    ]
    return df.drop(columns=drop_vars_extra, errors="ignore")


def rename_remove_empty_questionnaire(df):
    """Renames variables that follow a specific pattern and drops empty variables from
    the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the questionnaire data.

    Returns:
        pandas.DataFrame: The DataFrame with renamed variables and dropped empty variables.

    """
    quest_vars = [col for col in df.columns if col.startswith("CS5_Quest1player")]
    for var in quest_vars:
        new_var_name = "quest_" + var[16:]
        df = df.rename(columns={var: new_var_name})

    columns_to_drop = [
        "quest_role",
        "quest_payoff",
        "quest_posrec1",
        "quest_posrec1_ifyes",
        "quest_altruism1",
        "quest_altruism1_noanswer",
        "quest_q13",
        "quest_q14",
        "quest_q15",
        "quest_q18",
        "quest_q19",
        "quest_q20",
        "quest_q21",
        "quest_q23",
        "quest_q11",
        "quest_q12",
        "quest_subject_of_studi",
        "CS5_Quest1groupid_in_subsession",
        "CS5_Quest1subsessionround_number",
    ]
    return df.drop(columns=columns_to_drop, errors="ignore")


def _clean_data(df):
    df = remove_dots_in_variable_names(df)
    df = create_global_identifier_player_number(df)
    df = create_global_identifier_lab_session_number(df)
    df = create_global_identifier_group_id_all_subjects(df)
    df = rename_relevant_participants_identifier(df)
    df = remove_irrelevant_and_empty_participants_identifier(df)
    df = rename_rellevant_session_identifiers(df)
    df = remove_irrelevant_and_empty_session_identifiers(df)
    df = rename_rellevant_intro_to_baseline(df)
    df = remove_irrelevant_intro_to_baseline(df)
    df = rename_rellevant_baseline_variables(df)
    df = remove_irrelevant_baseline_variables(df)
    df = rename_rellevant_anticipation_variables(df)
    df = remove_irrelevant_anticipation_variables(df)
    df = rename_relevant_scarcity_variables(df)
    df = remove_irrelevant_scarcity_variables(df)
    return rename_remove_empty_questionnaire(df)
