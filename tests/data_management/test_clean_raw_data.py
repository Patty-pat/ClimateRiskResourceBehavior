import pandas as pd

from src.cprs.data_management.clean_raw_data import *


def test_rename_rellevant_anticipation_variables():
    # Create a sample DataFrame
    data = {
        "CS3_Anti1SomeVar": [1, 2],
        "CS3_Anti2AnotherVar": [3, 4],
        "UnchangedVar": [5, 6],
    }
    df = pd.DataFrame(data)

    # Apply the function
    result_df = rename_rellevant_anticipation_variables(df)

    # Check if the function works as expected
    assert "cs3_SomeVar" in result_df.columns
    assert "cs3_AnotherVar" in result_df.columns
    assert "UnchangedVar" in result_df.columns
    assert "CS3_Anti1SomeVar" not in result_df.columns
    assert "CS3_Anti2AnotherVar" not in result_df.columns


def test_remove_irrelevant_anticipation_variables():
    # Create a sample DataFrame
    data = {
        "cs3_1playerid_in_group": [1, 2],
        "cs3_2playerrole": [3, 4],
        "cs3_3playerpayoff": [5, 6],
        "cs3_4playerstage_points": [7, 8],
        "cs3_5playerpotential_payoff": [9, 10],
        "cs3_5groupis_shock_group": [11, 12],
        "cs3_5groupshock_probability": [13, 14],
        "cs3_5playercompr1": [15, 16],
        "UnchangedVar": [17, 18],
    }
    df = pd.DataFrame(data)

    # Apply the function
    result_df = remove_irrelevant_anticipation_variables(df)

    # Check if the function works as expected
    assert "UnchangedVar" in result_df.columns
    assert "cs3_1playerid_in_group" not in result_df.columns
    assert "cs3_2playerrole" not in result_df.columns
