# dataset_builder.py
import json
import os
from utils.logger import logger


def save_dataset(
    questions: list,
    filename: str = "questions_dataset.json"
):
    """
    Save extracted questions into a JSON dataset.
    """

    if not questions:
        logger.warning("No questions to save")
        return

    # Ensure output directory
    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            questions,
            f,
            indent=2,
            ensure_ascii=False
        )

    logger.info(f"Dataset saved successfully at {file_path}")
