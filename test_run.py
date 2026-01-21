from core.file_loader import load_file
from core.text_cleaner import clean_text
from core.question_parser import extract_questions
from core.output_formatter import format_output
from dataset_builder import save_dataset
from utils.logger import logger


def main():
    # 1️⃣ Input file path (pdf / txt / image)
    FILE_PATH = "image.png"

    logger.info("Starting question extraction pipeline")
    logger.info(f"Input file: {FILE_PATH}")

    # 2️⃣ Load file
    raw_text = load_file(FILE_PATH)
    logger.info("File loaded successfully")

    print("\n===== RAW TEXT =====")
    print(raw_text[:500])

    # 3️⃣ Clean text
    cleaned_text = clean_text(raw_text)
    logger.info("Text cleaned successfully")

    print("\n===== CLEANED TEXT =====")
    print(cleaned_text[:500])

    # 4️⃣ Extract questions
    questions = extract_questions(cleaned_text)
    logger.info(f"Total questions extracted: {len(questions)}")

    print("\n===== QUESTIONS =====")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['question']}")

    # 5️⃣ Format questions (standard structure)
    formatted_questions = []
    for q in questions:
        formatted_questions.append(format_output( question=q["question"],
        q_type=q.get("type", "unknown"),
        difficulty=q.get("difficulty", "unknown"),
        source=FILE_PATH))

    # 6️⃣ Save dataset
    save_dataset(formatted_questions, filename="questions_dataset.json")
    logger.info("Dataset saved as questions_dataset.json")

    print("\n✅ Dataset saved successfully: questions_dataset.json")


if __name__ == "__main__":
    main()
