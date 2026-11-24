# Parameters used to plot the coral settlement data.

FILE_PATH = "data/202510_BEM_ELH_Behavior.csv"

TOTAL_LARVAE_REPLICATE = "INITIAL_NB_LARVAE"

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

METAMORPHOSED = SETTLED + ["NB_CAULIFLOWERS"]

DEAD_CATEGORY = "Dead"

# Categories of larval behavior to plot
BEHAVIOR_GROUPS = {
    "Settled": SETTLED,
    "Settling": SETTLING,
    "Cauliflower": ["NB_CAULIFLOWERS"],
    "Not swimming at the bottom": ["Not_Sw_Bottom"],
    "Not swimming at the surface": ["Not_Sw_Surface"],
    "Swimming at the bottom": ["Sw_Bottom"],
    "Swimming at the surface": ["Sw_Surface"],
    DEAD_CATEGORY: ["NB_DEAD"]
}

BEHAVIOR_COLUMNS = [column for category, columns in BEHAVIOR_GROUPS.items()
                    if category != DEAD_CATEGORY
                    for column in columns]

MANDATORY_COLUMNS = [TOTAL_LARVAE_REPLICATE] + INFO_COLUMNS + BEHAVIOR_COLUMNS + [REPLICATE_COLUMN]

BEHAVIOR_COLORS = {
    "Settled": "#4ea06e",
    "Settling": "#d7ab5c",
    "Cauliflower": "#d489b4",
    "Not swimming at the bottom": "#6e69b7",
    "Not swimming at the surface": "#ada3ec",
    "Swimming at the bottom": "#348ab6",
    "Swimming at the surface": "#5ac2e1",
    DEAD_CATEGORY: "#807E7E"
}

OUTPUT_PATH = "./output"
OUTPUT_FORMAT = "png"
OUTPUT_RES = 150
