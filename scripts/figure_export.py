from pathlib import Path
import io
import zipfile

import matplotlib.pyplot as plt


def save_figure(fig, fig_name, save_dir, output_format="png", res=150):
    """
    Save a figure in the output directory

    Arguments:
    fig (matplotlib.figure.Figure): figure to save
    fig_name (str): name of output file
    save_dir (str): directory to save the output fig.
    output_format (str): output format
    res (int): output resolution

    Returns:
    None
    """
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)

    fig.savefig(save_path / f"{fig_name}.{output_format}",
                dpi=res,
                bbox_inches="tight")
    plt.close(fig)


def zippack_figures(dataframe, plot_function, plot_colors, output_format="png", output_res=150):
    """
    Create a zip containing plots depending on the plot function selected.

    Arguments:
    dataframe (pd.DataFrame): dataframe containing the computed percentages necessary to plot larval behavior
    plot_function (function): function to plot the data
    output_format (str): format for the output plot
    output_res (int): resolution of the output plot
    plot_colors (dict): dictionary mapping behavior categories to colors

    Returns:
    zip file containing the plots
    """
    zip_buffer = io.BytesIO()
    cohorts = dataframe.index.unique(level="cohort_id")
        
    with zipfile.ZipFile(zip_buffer, "w") as archive:
        for cohort in cohorts:
            figure, fig_name = plot_function(dataframe, cohort, plot_colors)
            figure_buffer = io.BytesIO()
            figure.savefig(figure_buffer,
                        format=output_format,
                        dpi=output_res,
                        bbox_inches="tight")
            plt.close(figure)

            archive.writestr(f"{fig_name}.{output_format}", figure_buffer.getvalue())

    zip_bytes = zip_buffer.getvalue()
    return zip_bytes