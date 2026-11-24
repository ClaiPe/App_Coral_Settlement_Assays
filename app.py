from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt

import config
from scripts.data_processing import (InvalidDataError,
                                     load_coral_data,
                                     prepare_data)
from scripts.behavior_plot import (add_category_columns,
                                   compute_percentage,
                                   plot_larval_behavior)
from scripts.figure_export import zippack_figures

PERCENTAGES_MEMORY_KEY = "percentages_computed"
GRAPH_MEMORY_KEY = "graphs_requested"


def reset_results():
    """Hide computed results when the data file or the column selection changes."""
    st.session_state[PERCENTAGES_MEMORY_KEY] = False
    st.session_state[GRAPH_MEMORY_KEY] = False


st.set_page_config(page_title="Coral Settlement Assays",
                   page_icon="🐠",
                   layout="centered")

st.title("🐠 Coral Settlement Assays")
st.caption("🌊 Visualize larval behavior proportions from your "
           "settlement assay data.")

with st.expander("📋 Expected file format"):
    cohort_column, treatment_column, age_column = config.INFO_COLUMNS
    st.markdown(f"""
    - CSV file, separated by `,` or `;`
    - Decimal separator must be `.` (for example `2.5`, not `2,5`)
    - Column names are case-sensitive; column order does not matter
    - The file must contain at least these
      {len(config.MANDATORY_COLUMNS)} columns:
        - `{cohort_column}`: cohort identifier
        - `{treatment_column}`: treatment applied
        - `{age_column}`: age of the larvae (in days)
        - `{config.REPLICATE_COLUMN}`: replicate identifier
        - `{config.TOTAL_LARVAE_REPLICATE}`: initial number of larvae
          in the replicate
        - the number of larvae observed in each behavior:
          {", ".join(f"`{column}`" for column in config.BEHAVIOR_COLUMNS)}
    - Dead larvae are computed automatically:
      `{config.TOTAL_LARVAE_REPLICATE}` minus the sum of the behavior columns
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
    behavior_groups = config.BEHAVIOR_GROUPS
    default_behavior = config.BEHAVIOR_COLUMNS
    dead_category = config.DEAD_CATEGORY
    dataframe_columns = coral_data.columns.tolist()
    behavior_options = default_behavior + [column for column in dataframe_columns
                                           if column not in default_behavior]

    with st.expander("⚙️ Define the behavior columns to use for plotting"):
        selected_groups = {}
        for category in behavior_groups:
            if category == dead_category:
                continue
            selected_groups[category] = st.multiselect(f"{category} behavior columns",
                                                      options=behavior_options,
                                                      default=behavior_groups[category],
                                                      accept_new_options=True,
                                                      on_change=reset_results)
        behavior_columns = [column for columns in selected_groups.values() for column in columns]
        selected_groups[dead_category] = behavior_groups[dead_category]

    if not behavior_columns:
        st.error("You must select at least one behavior column to plot.",
                 icon="🚫")
        st.stop()

    info_columns = config.INFO_COLUMNS
    total_larvae_per_replicate = config.TOTAL_LARVAE_REPLICATE
    replicate_column = config.REPLICATE_COLUMN
    mandatory_columns = behavior_columns + [total_larvae_per_replicate] + info_columns + [replicate_column]
    plot_colors = config.BEHAVIOR_COLORS
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
        grouped_percentage = compute_percentage(coral_data,
                                                category_columns,
                                                total_larvae_per_replicate,
                                                info_columns)
    except InvalidDataError as error:
        st.error(str(error), icon="🚫")
        st.stop()
    for warning in warnings_list:
        st.warning(warning, icon="⚠️")

    with st.expander("📊 Mean percentages per cohort, treatment and age"):
        st.dataframe(grouped_percentage.round(0))

    st.divider()
    left_column, second_column, third_column, right_column = st.columns(4)

    with left_column:
        if st.button("Generate graphs", type="primary", icon="📈"):
            st.session_state[GRAPH_MEMORY_KEY] = True

    if st.session_state.get(GRAPH_MEMORY_KEY, False):
        cohorts = grouped_percentage.index.unique(level="COHORT_ID")

        with st.spinner("🌊 Plotting larval behavior for each cohort..."):
            zip_bytes = zippack_figures(grouped_percentage,
                                        output_format, output_res, plot_colors)
            output_file_name = f"{Path(uploaded_file.name).stem}_plot.zip"

            with second_column:
                st.download_button(
                    label="Download graphs",
                    data=zip_bytes,
                    file_name=output_file_name,
                    mime="application/zip",
                    icon="📥")

            for cohort in cohorts:
                figure, _ = plot_larval_behavior(grouped_percentage, cohort, plot_colors)
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