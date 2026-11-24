# Parameter used to plot the coral settlement data.

FILE_PATH = "data/202603_GFASC_FEF_Settlement_Assays.csv"

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

MANDATORY_COLUMNS = [TOTAL_LARVAE_REPLICATE] + INFO_COLUMNS + BEHAVIOR_COLUMNS + [REPLICATE_COLUMN]

SETTLED = ["NB_CCA_SETTLERS_Top",
           "NB_CCA_SETTLERS_BOTTOM",
           "NB_PETRI_SETTLERS"]

SETTLING = ["NB_HANGERS"]

METAMORPHOSED = SETTLED + ["NB_CAULIFLOWERS"]

OUTPUT_PATH = "./output"
OUTPUT_FORMAT = "png"
OUTPUT_RES = 150
