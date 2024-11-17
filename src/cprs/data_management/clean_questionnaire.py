def keep_only_questionnaires_from_clean_data(df_main):
    """Filter the given DataFrame to keep only the columns related to questionnaires.

    Args:
        df_main (pandas.DataFrame): The main DataFrame containing the data.

    Returns:
        pandas.DataFrame: The filtered DataFrame with only the relevant columns.

    """
    for j in range(1, 6):
        columns_to_keep = (
            [col for col in df_main.columns if col.startswith(f"cs2_compr{j}")]
            + [col for col in df_main.columns if col.startswith(f"cs3_compr{j}")]
            + [col for col in df_main.columns if col.startswith(f"cs4_compr{j}")]
            + [
                "PLAYER_NUM",
                "LAB_SESSION",
                "GROUPID_ALL",
                "failed_attem1",
                "failed_attem2",
                "failed_attem3",
                "participant_id_in_session",
                "player_cubicle",
                "groupid1",
                "groupid2",
                "groupid3",
            ]
            + [col for col in df_main.columns if col.startswith("quest_")]
        )

        df_main = df_main[columns_to_keep]

    return df_main


def create_binary_social_optimum_strategy(df_main):
    """Create binary columns for social optimum strategy based on questionnaire
    responses.

    Args:
        df_main (pandas.DataFrame): The main DataFrame containing the questionnaire data.

    Returns:
        pandas.DataFrame: The main DataFrame with additional binary columns for social optimum strategy.

    """
    df_main["social_optimum1"] = df_main["quest_optimumN"].apply(
        lambda x: 1 if x == 3 else 0,
    )
    df_main["social_optimum2"] = df_main["quest_optimumA"].apply(
        lambda x: 1 if x == 3 else 0,
    )
    df_main["social_optimum3"] = df_main["quest_optimumS"].apply(
        lambda x: 1 if x == 3 else 0,
    )

    return df_main


def create_binary_nash_socially_acceptable(df_main):
    """Create binary variables for Nash strategy and socially acceptable perception.

    Args:
        df_main (pandas.DataFrame): The main dataframe containing the questionnaire data.

    Returns:
        pandas.DataFrame: The main dataframe with additional binary variables.

    """
    df_main["nash_strategy"] = df_main["quest_strategy"].apply(
        lambda x: 1 if x == 5 else 0,
    )
    df_main["prosocial_perception"] = df_main["quest_slider_guess"].apply(
        lambda x: 1 if x > 26.3 else 0,
    )
    df_main["social_appropriate"] = df_main["quest_soc_approp_pos"].apply(
        lambda x: 1 if x >= 2 else 0,
    )
    df_main["social_appropriate"] = df_main["quest_soc_approp_neg"].apply(
        lambda x: 1 if x < 2 else 0,
    )
    df_main["prosocial_perception"] = df_main["quest_slider_guess"].apply(
        lambda x: 1 if x > 26.3 else 0,
    )

    return df_main


def recode_eai_questions(df_main):
    """Recodes the EAI (Emotional Awareness and Insight) questions in the given
    DataFrame.

    Args:
        df_main (pandas.DataFrame): The DataFrame containing the EAI questions.

    Returns:
        pandas.DataFrame: The DataFrame with the EAI questions recoded.

    """
    for col in [
        "quest_eai_7",
        "quest_eai_8",
        "quest_eai_9",
        "quest_eai_10",
        "quest_eai_13",
        "quest_eai_14",
        "quest_eai_17",
        "quest_eai_18",
        "quest_eai_19",
        "quest_eai_20",
    ]:
        df_main[col] = df_main[col].apply(lambda x: 8 - x)

    return df_main


def create_global_environmental_attitude_average_individual_score(df_main):
    """Calculates the global environmental attitude average individual score for each
    row in the given DataFrame.

    Args:
        df_main (pandas.DataFrame): The DataFrame containing the questionnaire data.

    Returns:
        pandas.DataFrame: The DataFrame with the calculated global environmental attitude average individual score.

    """
    score_columns = [
        "quest_eai_" + str(i) for i in range(1, 25)
    ]  # Adjust if the range is different
    df_main["score"] = df_main[score_columns].sum(axis=1)
    df_main["GEA"] = df_main["score"] / 24

    return df_main


def create_group_average_global_environmental_attitude_average_score(df_main):
    """Calculate the group average global environmental attitude average score.

    This function takes a DataFrame 'df_main' as input and performs the following steps:
    1. Creates a binary variable 'pro_env' based on the 'GEA' column.
    2. Computes the group average 'GEA' score using the 'GROUPID_ALL' column.
    3. Creates a binary variable 'group_pro_env' based on the group average 'GEA' score.

    Parameters:
    - df_main (DataFrame): The main DataFrame containing the data.

    Returns:
    - df_main (DataFrame): The main DataFrame with the additional columns 'pro_env', 'GEA_gav', and 'group_pro_env'.

    """
    df_main["pro_env"] = df_main["GEA"].apply(lambda x: 1 if x > 4 else 0)
    df_main["GEA_gav"] = df_main.groupby("GROUPID_ALL")["GEA"].transform("mean")
    df_main["group_pro_env"] = df_main["GEA_gav"].apply(lambda x: 1 if x > 4 else 0)

    return df_main


def rename_global_preference_survey(df_main):
    """Renames the columns of the given DataFrame to match the global preference survey
    column names.

    Args:
        df_main (pandas.DataFrame): The DataFrame containing the survey data.

    Returns:
        pandas.DataFrame: The DataFrame with renamed columns.

    """
    # Risk Preferences
    df_main = df_main.rename(columns={"quest_gps71": "RISK"})

    # Time Preferences
    df_main = df_main.rename(columns={"quest_gps72_a": "TIME"})

    # Altruistic Preferences
    df_main = df_main.rename(columns={"quest_gps72_d": "ALTRUISM"})

    # Negative Reciprocity
    negrec_components = ["quest_gps72_b", "quest_gps72_c", "quest_gps73_b"]
    df_main["NEGREC"] = df_main[negrec_components].mean(axis=1)

    # Positive Reciprocity
    df_main = df_main.rename(columns={"quest_gps73_a": "POREC"})

    # Trust
    return df_main.rename(columns={"quest_gps73_c": "TRUST"})


def mapping_values_of_highest_education(df_main):
    """Maps the values of the 'quest_highest_ed' column in the given DataFrame to
    numerical values.

    Args:
        df_main (pandas.DataFrame): The DataFrame containing the 'quest_highest_ed' column.

    Returns:
        pandas.DataFrame: The DataFrame with a new column 'highest_ed' containing the mapped values.

    """
    education_map = {
        "Schulabschluss": 1,
        "Ausbildung": 2,
        "Bachelor-Abschluss": 3,
        "Master-Abschluss": 4,
        "Promotion (PhD.)": 5,
        "Sonstige": 0,
    }

    df_main["highest_ed"] = df_main["quest_highest_ed"].map(education_map)

    return df_main


def rename_climate_shock_perception_questions(df_main):
    """Renames the columns related to climate shock perception questions in the given
    DataFrame.

    Args:
        df_main (pandas.DataFrame): The DataFrame containing the questionnaire data.

    Returns:
        pandas.DataFrame: The DataFrame with the renamed columns.

    """
    return df_main.rename(
        columns={
            "quest_q30": "climate_shock_concer",
            "quest_q32": "climate_shock_impact",
            "quest_q33": "climate_shock_cause",
            "quest_q59": "climate_shock_main_increased_risk_reason",
        },
    )


def recode_study_field_related_to_environment(df_main):
    """Recodes the 'quest_study_field' column in the given DataFrame to represent
    whether it is related to the environment or not.

    Parameters:
        df_main (pandas.DataFrame): The DataFrame containing the 'quest_study_field' column.

    Returns:
        pandas.DataFrame: The DataFrame with the 'quest_study_field' column recoded and a new column 'quest_study_field_label' added.

    """
    df_main.loc[df_main["quest_study_field"] == 3, "quest_study_field"] = 2
    field_labels = {1: "1: Yes Related", 2: "2: Not Related"}
    df_main["quest_study_field_label"] = df_main["quest_study_field"].map(field_labels)

    return df_main


def _clean_questionnaire_data(df_main):
    df_main = keep_only_questionnaires_from_clean_data(df_main)
    df_main = create_binary_social_optimum_strategy(df_main)
    df_main = create_binary_nash_socially_acceptable(df_main)
    df_main = recode_eai_questions(df_main)
    df_main = create_global_environmental_attitude_average_individual_score(df_main)
    df_main = create_group_average_global_environmental_attitude_average_score(df_main)
    df_main = rename_global_preference_survey(df_main)
    df_main = mapping_values_of_highest_education(df_main)
    df_main = rename_climate_shock_perception_questions(df_main)
    return recode_study_field_related_to_environment(df_main)
