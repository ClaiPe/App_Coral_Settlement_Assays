import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def percentage_sanity_check(dataframe, count_columns):
    """
    Test to check if the sum of percentages is equal to 100.

    Arguments:
    dataframe (pd.DataFrame): dataframe containing the percentages to check
    count_columns (list): list of columns containing the percentages

    Returns:
    Nothing if no weird percentage.
    If weird percentage, returns the problematic rows.
    """
    sum_percentage = dataframe[count_columns].sum(axis=1)
    wrong_sum_mask = ~np.isclose(sum_percentage, 100) # ~ inverts the mask (True becomes False, as we want the false rows)
    if wrong_sum_mask.any():
        print("---- WARNING - Some percentage sum different from 100 ----")
        print(f"rows with weird percentage:\n{dataframe[wrong_sum_mask]}")


def compute_percentage_per_row(dataframe, count_columns, total, info_columns):
    """
    Compute percentages

    Arguments:
    dataframe (pd.DataFrame): The DataFrame containing the loaded data
    count_columns (list): Columns on which to compute the percentage
    total (pd.Series): Reference column to compute the percentage
    info_columns (list): columns with important info to keep

    What it does:
    Compute percentage for each columns
    Sanity check: check if the sum of all columns is equal to 100.

    Returns:
    A Dataframe with the percentage and the info columns
    """
    percentage = dataframe[count_columns].div(dataframe[total], axis=0) * 100
    percentage_sanity_check(percentage, count_columns)

    result = pd.concat([dataframe[info_columns], percentage], axis=1)

    return result


def compute_mean_percentage(dataframe, count_columns, group_columns):
    """
    Compute mean percentage

    Arguments:
    dataframe (pd.DataFrame): dataframe containing row percentages
    count_columns (list): list of columns on which to compute the means
    group_columns (list): columns to group the rows by

    Returns:
    dataframe with mean percentage for each group
    """
    mean_percentage = dataframe.groupby(group_columns)[count_columns].mean()
    percentage_sanity_check(mean_percentage, count_columns)

    return mean_percentage


def compute_percentage(dataframe, count_columns, total_column, info_columns):
    percentage_per_replicate = compute_percentage_per_row(dataframe,
                                                          count_columns,
                                                          total_column,
                                                          info_columns)
    grouped_percentage = compute_mean_percentage(percentage_per_replicate,
                                                 count_columns,
                                                 info_columns)
    return grouped_percentage


def plot_larval_behavior(dataframe, cohort_id):
    """
    Plot the proportion of each observed behavior.

    Arguments:
    dataframe (pd.DataFrame): dataframe containing the percentages
    cohort_id (str): cohort identification

    Returns:
    fig (matplotlib.figure.Figure) containing the plots
    fig name (str).
    """
    cohort_data = dataframe.loc[cohort_id]
    treatments = cohort_data.index.unique(level="TREATMENT")

    fig, axes = plt.subplots(1, len(treatments),
                             figsize=(4 * len(treatments), 4),
                             sharey=False, squeeze=False)
    fig.suptitle(f"[{cohort_id}] - Larval Behavior")

    for ax, treatment in zip(axes[0], treatments):
        treatment_data = cohort_data.loc[treatment]
        treatment_data.plot(kind="bar", stacked=True, ax=ax,
                            legend=False)
        ax.set(title=treatment,
               xlabel="Larval age",
               ylabel="Percentage", ylim=(0, 100))

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles,
               labels,
               loc="center left",
               bbox_to_anchor=(1, 0.5))

    fig_name = f"{cohort_id}_Larval_behavior"

    return fig, fig_name