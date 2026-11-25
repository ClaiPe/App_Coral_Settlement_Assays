# Parameters used to plot the coral settlement data.

FILE_PATH = "data/202510_BEM_ELH_Behavior.csv"

TOTAL_LARVAL_COLUMN = "INITIAL_NB_LARVAE"

INFO_COLUMNS = ["COHORT_ID", "TREATMENT", "AGE_LARVAE"]

REPLICATE_COLUMN = "REPLICATE"

BEHAVIOR_COLUMNS = ["Sw_Surface",
                    "Sw_Bottom",
                    "Not_Sw_Surface",
                    "Not_Sw_Bottom",
                    "NB_CCA_SETTLERS_Top",
                    "NB_CCA_SETTLERS_BOTTOM",
                    "NB_PETRI_SETTLERS",
                    "NB_HANGERS",
                    "NB_CAULIFLOWERS"]

SETTLED = ["NB_CCA_SETTLERS_Top",
           "NB_CCA_SETTLERS_BOTTOM",
           "NB_PETRI_SETTLERS"]

SETTLING = ["NB_HANGERS"]

DEAD_CATEGORY = "Dead"
SETTLED_CATEGORY = "Settled"
SETTLING_CATEGORY = "Settling"
CAULIFLOWER_CATEGORY = "Cauliflower"

# Categories of larval behavior to plot
BEHAVIOR_GROUPS = {
    SETTLED_CATEGORY: SETTLED,
    SETTLING_CATEGORY: SETTLING,
    CAULIFLOWER_CATEGORY: ["NB_CAULIFLOWERS"],
    "Not swimming at the bottom": ["Not_Sw_Bottom"],
    "Not swimming at the surface": ["Not_Sw_Surface"],
    "Swimming at the bottom": ["Sw_Bottom"],
    "Swimming at the surface": ["Sw_Surface"],
    DEAD_CATEGORY: ["NB_DEAD"]
}

BEHAVIOR_COLUMNS = [column for category, columns in BEHAVIOR_GROUPS.items()
                    if category != DEAD_CATEGORY
                    for column in columns]

MANDATORY_COLUMNS = [TOTAL_LARVAL_COLUMN] + INFO_COLUMNS + BEHAVIOR_COLUMNS + [REPLICATE_COLUMN]

BEHAVIOR_COLORS = {
    SETTLED_CATEGORY: "#4ea06e",
    SETTLING_CATEGORY: "#d7ab5c",
    CAULIFLOWER_CATEGORY: "#d489b4",
    "Not swimming at the bottom": "#6e69b7",
    "Not swimming at the surface": "#ada3ec",
    "Swimming at the bottom": "#348ab6",
    "Swimming at the surface": "#5ac2e1",
    DEAD_CATEGORY: "#807E7E"
}

# Competency assay
METAMORPHOSED_CURVE = "Metamorphosed"
ALIVE_CURVE = "Alive"
SETTLING_CURVE = "Settling"

COMPETENCY_CURVES = {
    SETTLING_CURVE: [SETTLING_CATEGORY],
    METAMORPHOSED_CURVE: [SETTLED_CATEGORY, CAULIFLOWER_CATEGORY]
}

COMPETENCY_COLORS = {
    METAMORPHOSED_CURVE: "#353434",
    ALIVE_CURVE: "#f7b63d",
    SETTLING_CURVE: "#F06A6A"
}

# Output parameters
OUTPUT_PATH = "./output"
OUTPUT_FORMAT = "png"
OUTPUT_RES = 150
