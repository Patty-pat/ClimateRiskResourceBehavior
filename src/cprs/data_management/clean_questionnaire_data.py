import pandas as pd

from cprs.config import BLD


def load_clean_data(df_main):
    return pd.read_feather(BLD / "data" / "data_clean.arrow")


def keep_only_questionnaires_from_clean_data(df_main):
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
    score_columns = [
        "quest_eai_" + str(i) for i in range(1, 25)
    ]  # Adjust if the range is different
    df_main["score"] = df_main[score_columns].sum(axis=1)
    df_main["GEA"] = df_main["score"] / 24

    return df_main


def create_group_average_global_environmental_attitude_average_score(df_main):
    # Create binary variable 'pro_env' based on 'GEA'
    df_main["pro_env"] = df_main["GEA"].apply(lambda x: 1 if x > 4 else 0)

    # Compute group average 'GEA' score
    df_main["GEA_gav"] = df_main.groupby("GROUPID_ALL")["GEA"].transform("mean")

    # Create binary variable 'group_pro_env' based on 'GEA_gav'
    df_main["group_pro_env"] = df_main["GEA_gav"].apply(lambda x: 1 if x > 4 else 0)

    return df_main


def rename_global_preference_survey(df_main):
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
    education_map = {
        "Schulabschluss": 1,
        "Ausbildung": 2,
        "Bachelor-Abschluss": 3,
        "Master-Abschluss": 4,
        "Promotion (PhD.)": 5,
        "Sonstige": 0,
    }

    # Create a new column 'highest_ed' with mapped values
    df_main["highest_ed"] = df_main["quest_highest_ed"].map(education_map)

    return df_main


def rename_climate_shock_perception_questions(df_main):
    return df_main.rename(
        columns={
            "quest_q30": "climate_shock_concer",
            "quest_q32": "climate_shock_impact",
            "quest_q33": "climate_shock_cause",
            "quest_q59": "climate_shock_main_increased_risk_reason",
        },
    )


def recode_study_field_related_to_environment(df_main):
    df_main.loc[df_main["quest_study_field"] == 3, "quest_study_field"] = 2
    # Mapping 'quest_study_field' values to labels
    field_labels = {1: "1: Yes Related", 2: "2: Not Related"}
    df_main["quest_study_field_label"] = df_main["quest_study_field"].map(field_labels)

    return df_main


def _clean_questionnaire_data(df):
    df_main = load_clean_data(df_main)
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
