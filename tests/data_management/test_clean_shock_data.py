import pandas as pd

from src.cprs.data_management.clean_shock_data import (
    keep_and_append_to_long,
)


# Test keep_and_append_to_long function
def test_keep_and_append_to_long_shock():
    # Creating a mock DataFrame
    data = {
        "PLAYER_NUM": [1, 2, 3],
        "LAB_SESSION": [1, 1, 1],
        "GROUPID_ALL": [1, 1, 1],
        "participant_id_in_session": [1, 2, 3],
        "groupid3": [1, 1, 1],
        "memberid3": [1, 2, 3],
        "high_probability": [1, 1, 1],
        "shock": [1, 2, 3],
        "hakenes": [7, 4, 9],
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
    assert "groupid3" in result.columns
    assert "memberid3" in result.columns
    assert "high_probability" in result.columns
    assert "shock" in result.columns
    assert "hakenes" not in result.columns
