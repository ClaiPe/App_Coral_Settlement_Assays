# 🦐 Coral Settlement Assays

A small Python application that turns the results of coral larval experiments
into charts. It handles two experiments, each with its own input file:

- **Settlement assay**: percent stacked bar charts showing how larvae are
  distributed between behavior categories (swimming, not swimming, settling,
  settled, "cauliflower", dead) at each larval age;
- **Competency assay**: time-course curves showing the proportion of larvae
  that are alive, settling and metamorphosed over time, with error bars.

In both cases there is one figure per cohort, with one chart per treatment.

It can be used in two ways:

- **a web app** (Streamlit): choose the experiment, upload a CSV file, choose
  the behavior columns, compute the results, generate the charts and download
  them as a ZIP;
- **a command-line script**: read a CSV file and save the charts as PNG images.

## Using the web app

The app is hosted on Streamlit Community Cloud: `https://coral-settlement.streamlit.app/`

Access is restricted: ask the maintainer to invite your e-mail address, then
sign in with that address (a code is sent by e-mail).

1. Choose your experiment: **Settlement assay** or **Competency assay**.
   Open **📋 Expected file format** to see the columns your file needs.
2. Click **Browse files** and choose your CSV file.
3. *(Optional)* Open **⚙️ Define the behavior columns to use for plotting** to
   change which columns belong to each behavior category (see below).
4. Click **Compute percentages**. Read the messages: errors are shown in red,
   warnings in orange. Open **📊 Mean results** to see the computed table.
5. Click **Generate graphs**: one figure per cohort is displayed.
6. Click **Download graphs** to get all figures in a single ZIP file.

Changing the experiment, loading another file or changing the column selection
hides the results: click **Compute percentages** again.

If the app has not been used for a while, a "This app has gone to sleep"
page may appear. Click the button to wake it up and wait a few seconds.

**Your data is not stored.** The uploaded file is processed in memory for your
session only. It is never saved on the server or added to the code repository.

## Input file format

Common rules for both experiments:

- CSV file, with `,` or `;` as separator (detected automatically).
- Decimal separator: `.` (for example `2.65`, not `2,65`).
- Column names are **not** case-sensitive (`Treatment` = `TREATMENT`). They are
  converted to lower case when the file is loaded, so the app shows them in
  lower case.
- Column order does not matter.
- Other columns are accepted but ignored, with a warning.

### Settlement assay

The following 15 columns are required:

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
| `NB_SWIMMERS` | swimming larvae (new column) |
| `NB_CCA_SETTLERS_Top` | larvae settled on top of the CCA |
| `NB_CCA_SETTLERS_BOTTOM` | larvae settled under the CCA |
| `NB_PETRI_SETTLERS` | larvae settled on the Petri dish |
| `NB_HANGERS` | hanging larvae (settling) |
| `NB_CAULIFLOWERS` | "cauliflower" larvae |

Example of ignored columns: `Scoring_Date`, `DrFM`, `Time`, `TOTAL_ALIVE`.

Files without `NB_SWIMMERS` (older files) can still be used: remove
`nb_swimmers` from the **Swimmers** category in the ⚙️ settings.

### Competency assay

The following 10 columns are required:

| Column | Content |
|---|---|
| `COHORT_ID` | cohort identifier |
| `TREATMENT` | treatment applied |
| `AGE_LARVAE` | age of the larvae (in days) |
| `NB_REPLICATES` | replicate identifier (the replicate number, not a count) |
| `TOTAL_LARVAE_SET` | initial number of larvae in the replicate |
| `NB_CCA_SETTLERS_TOP` | larvae settled on top of the CCA |
| `NB_CCA_SETTLERS_BOTTOM` | larvae settled under the CCA |
| `NB_PETRIDISH_SETTLERS` | larvae settled on the Petri dish |
| `NB_HANGERS` | hanging larvae (settling) |
| `NB_CAULIFLOWERS` | "cauliflower" larvae |

Example of ignored column: `MONITORING_DATE`.

## Behavior categories

The behavior columns are grouped into categories.

**Settlement assay**: each category is one segment of the stacked bars
(listed from the top of the bar to the bottom):

| Category | Columns (default) |
|---|---|
| Dead | computed: initial number of larvae minus all selected behavior columns |
| Swimming at the surface | `Sw_Surface` |
| Swimming at the bottom | `Sw_Bottom` |
| Not swimming at the surface | `Not_Sw_Surface` |
| Not swimming at the bottom | `Not_Sw_Bottom` |
| Swimmers | `NB_SWIMMERS` |
| Cauliflower | `NB_CAULIFLOWERS` |
| Settling | `NB_HANGERS` |
| Settled | `NB_CCA_SETTLERS_Top`, `NB_CCA_SETTLERS_BOTTOM`, `NB_PETRI_SETTLERS` |

**Competency assay**:

| Category | Columns (default) |
|---|---|
| Dead | computed: initial number of larvae minus all selected behavior columns |
| Cauliflower | `NB_CAULIFLOWERS` |
| Settling | `NB_HANGERS` |
| Settled | `NB_CCA_SETTLERS_TOP`, `NB_CCA_SETTLERS_BOTTOM`, `NB_PETRIDISH_SETTLERS` |

In the web app, the columns of each category can be changed for the current
session (for example if a column was renamed):

- a column removed from every category is no longer required; its larvae are
  counted as **dead** (a warning says so);
- a category with no column is not shown on the charts;
- other columns found in the file can be added to a category, or typed in
  (any case).

Closing or reloading the page restores the default categories.

## How the results are computed

Steps common to both experiments:

1. **Dead larvae**: for each replicate,
   `dead = initial number of larvae - (sum of the selected behavior columns)`.
2. **Invalid rows**: replicates where the number of dead larvae is negative
   (more larvae counted than set) are removed, and listed in a warning.
3. **Categories**: the columns of each category are added together.

### Settlement assay (stacked bars)

4. **Percentages per replicate**: each category is divided by the initial
   number of larvae and multiplied by 100.
5. **Mean per group**: percentages are averaged over the replicates of each
   cohort × treatment × larval age combination.
6. **Charts**: larval age on the x axis, stacked percentages (0 to 100) on the
   y axis, one legend per figure. Each category always keeps the same color.

### Competency assay (curves)

4. **Proportions per replicate** (divided by the initial number of larvae):
   - **Alive** = initial number of larvae − dead;
   - **Settling** = Settling category (`NB_HANGERS`);
   - **Metamorphosed** = Settled + Cauliflower categories.

   With the default columns, Alive = Settling + Metamorphosed: larvae that are
   still swimming are not counted in this file, so they are counted as dead.
   A curve whose categories have no column is not drawn.
5. **Mean and standard error per group** over the replicates of each
   cohort × treatment × larval age combination
   (SE = standard deviation / √number of replicates).
6. **Charts**: time in days (larval age) on the x axis, proportion of initial
   larvae (0 to 1) on the y axis, error bars = SE.

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

**Command line:** in `config.py`, set `FILE_PATH` (input file) and `CLI_ASSAY`
(`SETTLEMENT_ASSAY` or `COMPETENCY_ASSAY`, the format of that file), then run
from the project folder:

```bash
python -m scripts.coral_data_plot
```

The script draws both the stacked bars and the competency curves from the
file. The PNG images and two ZIP files (`..._behavior_plot.zip` and
`..._competency_plot.zip`) are saved in the `output/` folder.
The command line always uses the default categories from `config.py`.

**Tests:**

```bash
python -m pytest
```

## Project structure

```
app.py                       Streamlit interface (experiment choice, upload, settings, messages, charts, download)
config.py                    column names, categories, colors, settings of each experiment, output settings
scripts/
    data_processing.py       loading, column checks, dead larvae
    behavior_plot.py         categories, percentages, stacked bar charts
    time_course_plot.py      competency proportions, mean and SE, curves
    figure_export.py         saving figures, ZIP of all figures
    coral_data_plot.py       command-line script (main)
tests/                       pytest tests
.streamlit/config.toml       app theme
requirements.txt             Python dependencies with pinned versions
data/                        local input files (ignored by Git)
output/                      images created by the command-line script (ignored by Git)
```

## Configuration

All settings are in `config.py`. Column names are written in lower case.

- `SETTLEMENT_ASSAY`, `COMPETENCY_ASSAY`: names of the two experiments;
- `FILE_PATH`, `CLI_ASSAY`: input file and its experiment, for the
  command-line script;
- `INFO_COLUMNS`: cohort, treatment and age columns (common to both files);
- `ASSAY_SETTINGS`: for each experiment, the total column, the replicate
  column and the behavior categories:
  - Settlement assay: `TOTAL_LARVAL_COLUMN`, `REPLICATE_COLUMN`,
    `BEHAVIOR_GROUPS`;
  - Competency assay: `COMPETENCY_TOTAL_COLUMN`,
    `COMPETENCY_REPLICATE_COLUMN`, `COMPETENCY_GROUPS`;
- category order in `BEHAVIOR_GROUPS` is the stacking order, from the bottom
  of the bar to the top;
- `DEAD_CATEGORY`, `DEAD_COLUMN`: name of the computed "dead" category and of
  its column;
- `BEHAVIOR_COLORS`: color of each category;
- `COMPETENCY_CURVES`, `ALIVE_CURVE`, `COMPETENCY_COLORS`: curves of the
  competency assay (categories added together) and their colors;
- `OUTPUT_PATH`, `OUTPUT_FORMAT`, `OUTPUT_RES`: where and how images are saved.

## Known limitations

These points are planned but not handled yet:

- Leading or trailing spaces in values are not cleaned: `"NSW "` and `"NSW"`
  would be treated as two different treatments.
- A typo in a numeric column (for example `3. 1`) is not detected and can
  silently distort the calculations.
- Rows with missing values (NA) in the required columns are not removed
  automatically.
- The same column chosen in two categories is counted twice.
- A file with two columns whose names differ only by case (for example
  `Treatment` and `TREATMENT`) is not detected.
- Two observations at the same larval age are averaged together.

Please check your file carefully until these points are addressed.

## License

MIT, see [LICENSE](LICENSE).
