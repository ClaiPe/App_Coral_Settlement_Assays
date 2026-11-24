from pathlib import Path
from tqdm import tqdm

import config
from scripts.data_processing import (InvalidDataError, 
                                     load_coral_data, 
                                     prepare_data)
from scripts.behavior_plot import add_category_columns, compute_percentage, plot_larval_behavior
from scripts.figure_export import save_figure, zippack_figures


def main():
    data_file = config.FILE_PATH
    mandatory_columns = config.MANDATORY_COLUMNS
    info_columns = config.INFO_COLUMNS
    behavior_columns = config.BEHAVIOR_COLUMNS
    default_behavior = config.BEHAVIOR_COLUMNS
    total_larvae_per_replicate = config.TOTAL_LARVAE_REPLICATE
    replicate_column = config.REPLICATE_COLUMN
    behavior_groups = config.BEHAVIOR_GROUPS
    plot_colors = config.BEHAVIOR_COLORS
    output_path = config.OUTPUT_PATH
    output_format = config.OUTPUT_FORMAT
    output_res = config.OUTPUT_RES

    print(f"Loading coral data from: {data_file}")
    try:
        coral_data = load_coral_data(data_file)
        coral_data, warnings_list = prepare_data(coral_data,
                                                 mandatory_columns,
                                                 info_columns,
                                                 behavior_columns,
                                                 default_behavior,
                                                 total_larvae_per_replicate,
                                                 replicate_column)

        coral_data, category_columns = add_category_columns(coral_data, behavior_groups)

        grouped_percentage = compute_percentage(coral_data,
                                                category_columns,
                                                total_larvae_per_replicate,
                                                info_columns)
    except InvalidDataError as error:
        print(f"ERROR: {error}")
        return
    for warning in warnings_list:
        print(f"WARNING: {warning}")

    cohorts = grouped_percentage.index.unique(level="COHORT_ID")

    for cohort in tqdm(cohorts,
                       desc="Plotting larval behavior for each cohort"):
        figure, fig_name = plot_larval_behavior(grouped_percentage, cohort, plot_colors)
        save_figure(figure, fig_name,
                    output_path, output_format, output_res)

    zip_bytes = zippack_figures(grouped_percentage,
                                output_format, output_res, plot_colors)
    output_file_name = f"{Path(data_file).stem}_plot.zip"
    (Path(output_path) / output_file_name).write_bytes(zip_bytes)


if __name__ == "__main__":
    main()
