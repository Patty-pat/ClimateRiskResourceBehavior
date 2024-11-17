import pandas as pd

from src.cprs.data_management.clean_baseline_data import *


def test_keep_and_append_to_long_baseline():
    # Creating a mock DataFrame
    data = {
        "PLAYER_NUM": [1, 2, 3],
        "LAB_SESSION": [1, 1, 1],
        "GROUPID_ALL": [1, 1, 1],
        "participant_id_in_session": [1, 2, 3],
        "groupid1": [1, 1, 1],
        "memberid1": [1, 2, 3],
        "tatur": [7, 4, 9],
        # Add other mock data as needed
    }
    df_main = pd.DataFrame(data)

    # Call the function
    result = keep_and_append_to_long(df_main)

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert "PLAYER_NUM" in result.columns
    assert "LAB_SESSION" in result.columns
    assert "GROUPID_ALL" in result.columns
    assert "participant_id_in_session" in result.columns
    assert "groupid1" in result.columns
    assert "memberid1" in result.columns
    assert "tatur" not in result.columns


def test_create_ROUND():
    data = {"subsessionround_number_1": [1, 2, 3]}
    df_combined = pd.DataFrame(data)

    result = create_ROUND(df_combined)

    assert "ROUND" in result.columns
    assert all(result["ROUND"] == result["subsessionround_number_1"])
