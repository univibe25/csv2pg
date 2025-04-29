# registry.py
from csv2pg import transforms as T

TRANSFORMS = {
    "chronic_disease": [T.common],
    "diabetes": [T.common, T.add_patient_id],
    "health_care": [T.common],
    "heart": [T.common, T.add_patient_id],
    "penguin": [T.common],
    "titanic": [T.common, T.clean_titanic],
    "wny_health": [T.common, T.clean_wny_health],
}
