from matplotlib import pyplot as plt


def compute_curve_proportions(dataframe,
                              competency_curves,
                              total_column,
                              dead_column,
                              alive_curve,
                              info_columns):
    """
    Compute the proportion of competent larvae. 
    If no data present for a curve category, this category will be ignore.

    Arguments:
    dataframe (pd.DataFrame): The DataFrame containing the data after add_category_columns()
    competency_curves (dict): Dictionnary containing the competency curves composition
    total_column (str): Reference column to compute the proportion
    dead_column (str): Reference column containing nb of dead larvae
    alive_curve (str): Name for the alive curve
    info_columns (list): columns with important info to keep

    Returns:
    A Dataframe with the proportion and the info columns
    """
    competency_table = dataframe[info_columns].copy()

    competency_table[alive_curve] = (dataframe[total_column] - dataframe[dead_column])/dataframe[total_column]

    for curve, categories in competency_curves.items():
        present_categories = [category for category in categories
                              if category in dataframe.columns]
        if not present_categories:
            continue

        curve_count = dataframe[present_categories].sum(axis=1)
        competency_table[curve] = curve_count / dataframe[total_column]

    return competency_table


def compute_curve_mean_and_se(competency_table, info_columns):
    """
    Compute proportions for competency curves.

    Arguments:
    competency_table (dataframe): dataframe containing the proportion of competent larvae.
    info_columns (list): columns with important info to keep

    Returns
    dataframe with mean proportion for each curve and the associated standard error
    """
    competency_columns = [column for column in competency_table.columns
                          if column not in info_columns]
    competency = competency_table.groupby(info_columns)[(competency_columns)].agg(["mean", "sem"])

    return competency


def plot_competency_curves(competency_table, cohort_id, color_dict):
    """
    Plot the competency curves

    Arguments:
    competency_table (pd.DataFrame): dataframe containing the proportions
    cohort_id (str): cohort identification
    color_dict (dict): dictionary mapping curves to colors

    Returns:
    fig (matplotlib.figure.Figure) containing the plots
    fig name (str).
    """
    cohort_data = competency_table.loc[cohort_id]
    treatments = cohort_data.index.unique(level="TREATMENT")

    fig, axes = plt.subplots(1, len(treatments),
                             figsize=(4 * len(treatments), 4),
                             sharey=False, squeeze=False)
    fig.subplots_adjust(wspace=0.3)
    fig.suptitle(f"[{cohort_id}] - Competency assay")

    for ax, treatment in zip(axes[0], treatments):
        treatment_data = cohort_data.loc[treatment]
        curves = treatment_data.columns.unique(level=0)
        for curve in curves:
            ax.errorbar(x=treatment_data.index,
                        y=treatment_data[curve]["mean"],
                        yerr=treatment_data[curve]["sem"],
                        label=curve,
                        color=color_dict[curve],
                        marker="o",
                        capsize=3)
        ax.set(title=treatment,
               xlabel="Time (days)",
               ylabel="Proportion of initial larvae", ylim=(0, 1))

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles,
               labels,
               loc="center left",
               bbox_to_anchor=(1, 0.5))

    fig_name = f"{cohort_id}_Competency_assay"

    return fig, fig_name


