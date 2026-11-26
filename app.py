from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt

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
from scripts.figure_export import zippack_figures

PERCENTAGES_MEMORY_KEY = "percentages_computed"
GRAPH_MEMORY_KEY = "graphs_requested"


def reset_results():
    """Hide computed results when the experiment, data file or the column selection changes."""
    st.session_state[PERCENTAGES_MEMORY_KEY] = False
    st.session_state[GRAPH_MEMORY_KEY] = False


st.set_page_config(page_title="Coral Settlement Assays",
                   page_icon="🐠",
                   layout="centered")

st.title("🐠 Coral Settlement Assays")
st.caption("🌊 Visualize larval behavior evolution and competency from your "
           "settlement and competency assays data.")

assay = st.radio("Choose your experiment",
                 options=[config.SETTLEMENT_ASSAY, config.COMPETENCY_ASSAY],
                 horizontal=True,
                 index=None,
                 on_change=reset_results)

if assay is None:
    st.stop()

# Settings of the chosen experiment
settings = config.ASSAY_SETTINGS[assay]
info_columns = config.INFO_COLUMNS
total_larvae_per_replicate = settings["total_column"]
replicate_column = settings["replicate_column"]
behavior_groups = settings["behavior_groups"]
dead_category = config.DEAD_CATEGORY
default_behavior = get_behavior_columns(behavior_groups, dead_category)
nb_mandatory_columns = (len(info_columns) + len(default_behavior)
                        + 2)  # + replicate and total columns

with st.expander("📋 Expected file format"):
    cohort_column, treatment_column, age_column = info_columns
    st.markdown(f"""
    - CSV file, separated by `,` or `;`
    - Decimal separator must be `.` (for example `2.5`, not `2,5`)
    - Column names are not case-sensitive (`Treatment` = `TREATMENT`); column order does not matter
    - The file must contain at least these
    {nb_mandatory_columns} columns:
        - `{cohort_column}`: cohort identifier
        - `{treatment_column}`: treatment applied
        - `{age_column}`: age of the larvae (in days)
        - `{replicate_column}`: replicate identifier
        - `{total_larvae_per_replicate}`: initial number of larvae
        in the replicate
        - the number of larvae observed in each behavior:
        {", ".join(f"`{column}`" for column in default_behavior)}
    - Dead larvae are computed automatically:
    `{total_larvae_per_replicate}` minus the sum of the behavior columns
    - Other columns are accepted but ignored
    - The behavior columns can be changed after uploading the file
    (⚙️ settings below)
    """)

uploaded_file = st.file_uploader("📂 Choose your data file (CSV)", type="csv",
                                 on_change=reset_results)

if uploaded_file is not None:
    st.success(f"File received: {uploaded_file.name}", icon="✅")

    try:
        coral_data = load_coral_data(uploaded_file)
    except InvalidDataError as error:
        st.error(str(error), icon="🚫")
        st.stop()

    # Columns options the user can select as larval behavior
    dataframe_columns = coral_data.columns.tolist()
    behavior_options = default_behavior + [column for column in dataframe_columns
                                        if column not in default_behavior]

    with st.expander("⚙️ Define the behavior columns to use for plotting"):
        selected_groups = {}
        for category in behavior_groups:
            if category == dead_category:
                continue
            selected_columns = st.multiselect(f"{category} behavior columns",
                                              options=behavior_options,
                                              default=behavior_groups[category],
                                              accept_new_options=True,
                                              on_change=reset_results)
            # Columns typed by the user: same lower case as the file columns
            selected_groups[category] = [column.lower()
                                         for column in selected_columns]
        behavior_columns = [column for columns in selected_groups.values() for column in columns]
        selected_groups[dead_category] = behavior_groups[dead_category]

    if not behavior_columns:
        st.error("You must select at least one behavior column to plot.",
                icon="🚫")
        st.stop()

    mandatory_columns = behavior_columns + [total_larvae_per_replicate] + info_columns + [replicate_column]

    output_format = config.OUTPUT_FORMAT
    output_res = config.OUTPUT_RES

    if st.button("Compute percentages", type="primary", icon="📊"):
        st.session_state[PERCENTAGES_MEMORY_KEY] = True

    if not st.session_state.get(PERCENTAGES_MEMORY_KEY, False):
        st.stop()

    try:
        coral_data, warnings_list = prepare_data(coral_data,
                                                    mandatory_columns,
                                                    info_columns,
                                                    behavior_columns,
                                                    default_behavior,
                                                    total_larvae_per_replicate,
                                                    replicate_column)
        coral_data, category_columns = add_category_columns(coral_data, selected_groups)

        if assay == config.SETTLEMENT_ASSAY:
            result_table = compute_percentage(coral_data,
                                              category_columns,
                                              total_larvae_per_replicate,
                                              info_columns)
            plot_function = plot_larval_behavior
            plot_colors = config.BEHAVIOR_COLORS
            nb_digits = 0
        else:
            competency_proportions = compute_curve_proportions(coral_data,
                                                               config.COMPETENCY_CURVES,
                                                               total_larvae_per_replicate,
                                                               config.DEAD_COLUMN,
                                                               config.ALIVE_CURVE,
                                                               info_columns)
            result_table = compute_curve_mean_and_se(competency_proportions, info_columns)
            plot_function = plot_competency_curves
            plot_colors = config.COMPETENCY_COLORS
            nb_digits = 2
    except InvalidDataError as error:
        st.error(str(error), icon="🚫")
        st.stop()
    for warning in warnings_list:
        st.warning(warning, icon="⚠️")

    with st.expander("📊 Mean results per cohort, treatment and age"):
        st.dataframe(result_table.round(nb_digits))

    st.divider()
    left_column, second_column, third_column, right_column = st.columns(4)

    with left_column:
        if st.button("Generate graphs", type="primary", icon="📈"):
            st.session_state[GRAPH_MEMORY_KEY] = True

    if st.session_state.get(GRAPH_MEMORY_KEY, False):
        cohorts = result_table.index.unique(level="cohort_id")

        with st.spinner("🌊 Plotting results for each cohort..."):
            zip_bytes = zippack_figures(result_table,
                                        plot_function,
                                        plot_colors,
                                        output_format, output_res)
            output_file_name = f"{Path(uploaded_file.name).stem}_plot.zip"

            with second_column:
                st.download_button(
                    label="Download graphs",
                    data=zip_bytes,
                    file_name=output_file_name,
                    mime="application/zip",
                    icon="📥")

            for cohort in cohorts:
                figure, _ = plot_function(result_table, cohort, plot_colors)
                st.pyplot(figure)
                plt.close(figure)

    else:
        with second_column:
            st.download_button(label="Download graphs",
                            data=b"", 
                            file_name="no_graph.zip",
                            icon="📥",
                            disabled=True,
                            help="Generate the graphs first")