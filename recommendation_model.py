import csv
from collections import Counter, defaultdict
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent / "student_dataset.csv"

field_mode_counts = defaultdict(Counter)
global_mode_counts = Counter()
is_initialized = False


def _initialize_model():
    global is_initialized

    if not DATASET_PATH.exists():
        is_initialized = False
        return

    field_mode_counts.clear()
    global_mode_counts.clear()

    with DATASET_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            field = (row.get("Field") or "").strip()
            mode = (row.get("Recommended_Learning_Mode") or "").strip()
            if not field or not mode:
                continue
            field_mode_counts[field.lower()][mode] += 1
            global_mode_counts[mode] += 1

    is_initialized = bool(global_mode_counts)


_initialize_model()

# Prediction function
def predict_roadmap(field_name):
    if not is_initialized:
        return "Error: Recommendation model is unavailable because dataset could not be loaded."

    field_name = (field_name or "").strip().lower()
    if not field_name:
        return "Error: Field is required."

    if field_name in field_mode_counts and field_mode_counts[field_name]:
        return field_mode_counts[field_name].most_common(1)[0][0]

    if global_mode_counts:
        # Fallback to the most frequent learning mode in dataset.
        return global_mode_counts.most_common(1)[0][0]

    return f"Error: Field '{field_name}' not found in dataset."
