# Parameters used to plot the coral settlement data.
# Column names are written in lower case: the columns of the loaded file are
# converted to lower case, so the file can use any case.

# Names of the two experiments (keys of ASSAY_SETTINGS)
SETTLEMENT_ASSAY = "Water and Settlement assays"
COMPETENCY_ASSAY = "Competency assay"

# Input file and experiment used by the command-line script
FILE_PATH = "data/202510_BEM_ELH_Behavior.csv"
CLI_ASSAY = SETTLEMENT_ASSAY

TOTAL_LARVAL_COLUMN = "initial_nb_larvae"

INFO_COLUMNS = ["cohort_id", "treatment", "age_larvae"]

REPLICATE_COLUMN = "replicate"

SETTLED = ["settlers_top",
           "settlers_bottom",
           "settlers_petri"]

SETTLING = ["nb_hangers"]

DEAD_CATEGORY = "Dead"
DEAD_COLUMN = "nb_dead"  # computed by the code, not in the file
SETTLED_CATEGORY = "Settled"
SETTLING_CATEGORY = "Settling"
CAULIFLOWER_CATEGORY = "Cauliflower"
SWIMMERS_CATEGORY = "Swimmers"

# Categories of larval behavior to plot
BEHAVIOR_GROUPS = {
    SETTLED_CATEGORY: SETTLED,
    SETTLING_CATEGORY: ["hangers"],
    CAULIFLOWER_CATEGORY: ["cauliflowers"],
    SWIMMERS_CATEGORY: ["swimmers"],
    "Not swimming at the bottom": ["not_sw_bottom"],
    "Not swimming at the surface": ["not_sw_surface"],
    "Swimming at the bottom": ["sw_bottom"],
    "Swimming at the surface": ["sw_surface"],
    DEAD_CATEGORY: [DEAD_COLUMN]
}

BEHAVIOR_COLORS = {
    SETTLED_CATEGORY: "#4ea06e",
    SETTLING_CATEGORY: "#d7ab5c",
    CAULIFLOWER_CATEGORY: "#d489b4",
    SWIMMERS_CATEGORY: "#348ab6",
    "Not swimming at the bottom": "#6e69b7",
    "Not swimming at the surface": "#ada3ec",
    "Swimming at the bottom": "#348ab6",
    "Swimming at the surface": "#5ac2e1",
    DEAD_CATEGORY: "#807E7E"
}

# Columns of the competency assay file
COMPETENCY_TOTAL_COLUMN = TOTAL_LARVAL_COLUMN
COMPETENCY_REPLICATE_COLUMN = "nb_replicates"

COMPETENCY_SETTLED = ["nb_settlers_cca",
                      "nb_settlers_petri"]

COMPETENCY_GROUPS = {
    SETTLED_CATEGORY: COMPETENCY_SETTLED,
    SETTLING_CATEGORY: SETTLING,
    CAULIFLOWER_CATEGORY: ["nb_cauliflowers"],
    SWIMMERS_CATEGORY: ["nb_swimmers"],
    DEAD_CATEGORY: [DEAD_COLUMN]
}

# Settings of each experiment: the app picks one with the radio button
ASSAY_SETTINGS = {
    SETTLEMENT_ASSAY: {
        "total_column": TOTAL_LARVAL_COLUMN,
        "replicate_column": REPLICATE_COLUMN,
        "behavior_groups": BEHAVIOR_GROUPS
    },
    COMPETENCY_ASSAY: {
        "total_column": COMPETENCY_TOTAL_COLUMN,
        "replicate_column": COMPETENCY_REPLICATE_COLUMN,
        "behavior_groups": COMPETENCY_GROUPS
    }
}

# Competency curves
SETTLED_CURVE = "Settled"
SETTLING_CURVE = "Hangers"
SWIMMERS_CURVE = "Swimming"
CAULIFLOWER_CURVE = "Cauliflowers"

COMPETENCY_CURVES = {
    SETTLED_CURVE: [SETTLED_CATEGORY],
    SETTLING_CURVE: [SETTLING_CATEGORY],
    SWIMMERS_CURVE:  [SWIMMERS_CATEGORY],
    CAULIFLOWER_CURVE: [CAULIFLOWER_CATEGORY]
}

COMPETENCY_COLORS = {
    SETTLED_CURVE: "#4ea06e",
    SWIMMERS_CURVE: "#348ab6",
    SETTLING_CURVE: "#d7ab5c",
    CAULIFLOWER_CURVE: "#d489b4"
}

# Output parameters
OUTPUT_PATH = "./output"
OUTPUT_FORMAT = "png"
OUTPUT_RES = 150