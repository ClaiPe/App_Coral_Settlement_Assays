# 🦐 Coral Settlement Assays

A small Python application that turns the results of coral larval settlement
assays into percent stacked bar charts.

For each cohort, it shows how larvae are distributed between behavior
categories (swimming, not swimming, settling, settled, "cauliflower", dead)
at each larval age, with one chart per treatment.

It can be used in two ways:

- **a web app** (Streamlit): upload a CSV file, choose the behavior columns,
  compute the percentages, generate the charts and download them as a ZIP;
- **a command-line script**: read a CSV file and save the charts as PNG images.

## Using the web app

The app is hosted on Streamlit Community Cloud: `https://coral-settlement.streamlit.app/`

Access is restricted: ask the maintainer to invite your e-mail address, then
sign in with that address (a code is sent by e-mail).

1. Click **Browse files** and choose your CSV file.
2. *(Optional)* Open **⚙️ Define the behavior columns to use for plotting** to
   change which columns belong to each behavior category (see below).
3. Click **Compute percentages**. Read the messages: errors are shown in red,
   warnings in orange. Open **📊 Mean percentages** to see the computed table.
4. Click **Generate graphs**: one figure per cohort is displayed.
5. Click **Download graphs** to get all figures in a single ZIP file.

Loading another file or changing the column selection hides the results:
click **Compute percentages** again.

If the app has not been used for a while, a "This app has gone to sleep"
page may appear. Click the button to wake it up and wait a few seconds.

**Your data is not stored.** The uploaded file is processed in memory for your
session only. It is never saved on the server or added to the code repository.

## Input file format

- CSV file, with `,` or `;` as separator (detected automatically).
- Decimal separator: `.` (for example `2.65`, not `2,65`).
- Column names are case-sensitive (`TREATMENT` is not `Treatment`).
- Column order does not matter.
- The following 14 columns are required:

| Column | Content |
|---|---|
| `COHORT_ID` | cohort identifier |
| `TREATMENT` | treatment applied |
| `AGE_LARVAE` | age of the larvae (in days) |
| `REPLICATE` | replicate identifier |
| `INITIAL_NB_LARVAE` | initial number of larvae in the replicate |
| `Sw_Surface` | larvae swimming at the surface |
| `Sw_Bottom` | larvae swimming at the bottom |
| `Not_Sw_Surface` | larvae not swimming, at the surface |
| `Not_Sw_Bottom` | larvae not swimming, at the bottom |
| `NB_CCA_SETTLERS_Top` | larvae settled on top of the CCA |
| `NB_CCA_SETTLERS_BOTTOM` | larvae settled under the CCA |
| `NB_PETRI_SETTLERS` | larvae settled on the Petri dish |
| `NB_HANGERS` | hanging larvae (settling) |
| `NB_CAULIFLOWERS` | "cauliflower" larvae |

Other columns (for example `Scoring_Date`, `DrFM`, `Time`, `TOTAL_ALIVE`)
are accepted but ignored, with a warning.

## Behavior categories

The behavior columns are grouped into categories. Each category is one
segment of the stacked bars (listed from the top of the bar to the bottom):

| Category | Columns (default) |
|---|---|
| Dead | computed: `INITIAL_NB_LARVAE` minus all selected behavior columns |
| Swimming at the surface | `Sw_Surface` |
| Swimming at the bottom | `Sw_Bottom` |
| Not swimming at the surface | `Not_Sw_Surface` |
| Not swimming at the bottom | `Not_Sw_Bottom` |
| Cauliflower | `NB_CAULIFLOWERS` |
| Settling | `NB_HANGERS` |
| Settled | `NB_CCA_SETTLERS_Top`, `NB_CCA_SETTLERS_BOTTOM`, `NB_PETRI_SETTLERS` |

In the web app, the columns of each category can be changed for the current
session (for example if a column was renamed):

- a column removed from every category is no longer required; its larvae are
  counted as **dead** (a warning says so);
- a category with no column is not shown on the charts;
- other columns found in the file can be added to a category.

Closing or reloading the page restores the default categories.

## How the charts are computed

1. **Dead larvae**: for each replicate,
   `NB_DEAD = INITIAL_NB_LARVAE - (sum of the selected behavior columns)`.
2. **Invalid rows**: replicates where `NB_DEAD` is negative (more larvae
   counted than set) are removed, and listed in a warning.
3. **Categories**: the columns of each category are added together.
4. **Percentages per replicate**: each category is divided by
   `INITIAL_NB_LARVAE` and multiplied by 100.
5. **Mean per group**: percentages are averaged over the replicates of each
   cohort × treatment × larval age combination.
6. **Charts**: one figure per cohort, one chart per treatment side by side,
   larval age on the x axis, stacked percentages (0 to 100) on the y axis,
   one legend per figure. Each category always keeps the same color.

## Errors and warnings

| Situation | Behavior |
|---|---|
| File not found, empty or unreadable | error, processing stops |
| Required column missing | error listing the missing columns |
| No behavior column selected | error, processing stops |
| Known behavior column in the file but not selected | warning: its larvae are counted as dead |
| Extra columns | warning, columns ignored |
| Negative number of dead larvae | warning listing the rows, rows removed |

## Running locally (for development)

Requirements: Python 3.12.

```bash
# create and activate an environment (conda example)
conda create -n coral-settlement python=3.12
conda activate coral-settlement

# install the dependencies (pinned versions)
pip install -r requirements.txt
```

**Web app:**

```bash
streamlit run app.py
```

**Command line:** set `FILE_PATH` in `config.py`, then run from the project
folder:

```bash
python -m scripts.coral_data_plot
```

The PNG images and a ZIP of all images are saved in the `output/` folder.
The command line always uses the default categories from `config.py`.

**Tests:**

```bash
python -m pytest
```

## Project structure

```
app.py                       Streamlit interface (upload, settings, messages, charts, download)
config.py                    column names, categories, colors, input file, output settings
scripts/
    data_processing.py       loading, column checks, dead larvae
    behavior_plot.py         categories, percentages, stacked bar charts
    figure_export.py         saving figures, ZIP of all figures
    coral_data_plot.py       command-line script (main)
    time_course_plot.py      time-course charts (in progress)
tests/                       pytest tests
.streamlit/config.toml       app theme
requirements.txt             Python dependencies with pinned versions
data/                        local input files (ignored by Git)
output/                      images created by the command-line script (ignored by Git)
```

## Configuration

All settings are in `config.py`:

- `FILE_PATH`: input file used by the command-line script;
- `INFO_COLUMNS`, `REPLICATE_COLUMN`, `TOTAL_LARVAE_REPLICATE`: names of the
  identification and total columns;
- `BEHAVIOR_GROUPS`: behavior categories and their default columns (their
  order is the stacking order, from the bottom of the bar to the top);
- `DEAD_CATEGORY`: name of the computed "dead" category;
- `BEHAVIOR_COLORS`: color of each category;
- `BEHAVIOR_COLUMNS`, `MANDATORY_COLUMNS`: computed from the settings above;
- `OUTPUT_PATH`, `OUTPUT_FORMAT`, `OUTPUT_RES`: where and how images are saved.

## Known limitations

These points are planned but not handled yet:

- Leading or trailing spaces in values are not cleaned: `"NSW "` and `"NSW"`
  would be treated as two different treatments.
- A typo in a numeric column (for example `3. 1`) is not detected and can
  silently distort the calculations.
- Rows with missing values (NA) in the required columns are not removed
  automatically.

Please check your file carefully until these points are addressed.

## License

MIT, see [LICENSE](LICENSE).
