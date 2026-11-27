from pathlib import Path
from tqdm import tqdm

import config
from scripts.data_processing import (InvalidDataError,
                                     get_behavior_columns,
                                     load_coral_data,
                                     prepare_data)
from scripts.behavior_plot import (add_category_columns,
                                   compute_percentage,
                                   plot_larval_behavior)
from scripts.time_course_plot import (compute_curve_proportions,
                                      compute_curve_mean_and_se,
                                      plot_competency_curves)
from scripts.figure_export import save_figure, zippack_figures


def main():
    data_file = config.FILE_PATH
    settings = config.ASSAY_SETTINGS[config.CLI_ASSAY]
    info_columns = config.INFO_COLUMNS
    total_larvae_per_replicate = settings["total_column"]
    replicate_column = settings["replicate_column"]
    behavior_groups = settings["behavior_groups"]
    behavior_columns = get_behavior_columns(behavior_groups,
                                            config.DEAD_CATEGORY)
    default_behavior = behavior_columns
    mandatory_columns = (info_columns + behavior_columns
                         + [total_larvae_per_replicate, replicate_column])
    behavior_colors = config.BEHAVIOR_COLORS

    # Competency curves
    competency_curves = config.COMPETENCY_CURVES
    competency_colors = config.COMPETENCY_COLORS

    # Output parameters
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

        # For competency curves
        competency_proportions = compute_curve_proportions(coral_data,
                                                           competency_curves,
                                                           total_larvae_per_replicate,
                                                           info_columns)
        competency_table = compute_curve_mean_and_se(competency_proportions, info_columns)
        
    except InvalidDataError as error:
        print(f"ERROR: {error}")
        return
    for warning in warnings_list:
        print(f"WARNING: {warning}")

    cohorts = grouped_percentage.index.unique(level="cohort_id")

    for cohort in tqdm(cohorts,
                       desc="Plotting larval behavior for each cohort"):
        figure, fig_name = plot_larval_behavior(grouped_percentage, cohort, behavior_colors)
        save_figure(figure, fig_name,
                    output_path, output_format, output_res)
    zip_bytes = zippack_figures(grouped_percentage,
                                plot_larval_behavior,
                                behavior_colors,
                                output_format, output_res)
    output_file_name = f"{Path(data_file).stem}_behavior_plot.zip"
    (Path(output_path) / output_file_name).write_bytes(zip_bytes)

    for cohort in tqdm(cohorts,
                       desc="Plotting competency assay curves for each cohort"):
        figure, fig_name = plot_competency_curves(competency_table, cohort, competency_colors)
        save_figure(figure, fig_name,
                            output_path, output_format, output_res)
    zip_bytes = zippack_figures(competency_table,
                                plot_competency_curves,
                                competency_colors,
                                output_format, output_res)
    output_file_name = f"{Path(data_file).stem}_competency_plot.zip"
    (Path(output_path) / output_file_name).write_bytes(zip_bytes)


if __name__ == "__main__":
    main()
