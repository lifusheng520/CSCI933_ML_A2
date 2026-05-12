"""
Evaluation scaffold.

This script creates a CSV template for evaluation results.
Students should extend it to run both baseline and RAG systems and then
manually or semi-automatically score the outputs.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List

from config import RESULTS_DIR, QUESTIONS_DIR

QUESTIONS_PATH = RESULTS_DIR / "instructor_questions.json"
OUTPUT_PATH = RESULTS_DIR / "evaluation_results_template.csv"


def load_questions(path: Path = QUESTIONS_PATH) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Question file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_evaluation_template(input) -> None:

    fieldnames = [
        "question_id",
        "question",
        "question_type",
        "expected_focus",
        "system",
        "retrieved_passages",
        "generated_response",
        "correctness_score",
        "grounding_score",
        "retrieval_relevance_score",
        "usefulness_score",
        "style_quality_score",
        "comments",
    ]

    with open(QUESTIONS_DIR/"instructor_questions.json", 'r', encoding='utf-8') as f:
        instructor_questions = {item["question"]: item for item in json.load(f)}

    with open(input, 'r', encoding='utf-8') as f:
        retrieval_history = json.load(f)

    # create list to record evaluation
    rows = []

    for i, entry in enumerate(retrieval_history, start=1):
        # get query type and expected focus
        query = entry.get("query")
        query_info = instructor_questions.get(query, {})

        # keep play, speaker, and text fields in retrieved passages
        passages = []
        for ev in entry.get("retrieved_evidence", []):
            passages.append({
                "play": ev.get("play"),
                "speakers": ev.get("speakers"),
                "text": ev.get("text"),
                "scene_summary": ev.get("scene_summary")
            })

        passages_json_list = json.dumps(passages, ensure_ascii=False)

        # Build the evaluation row
        row = {
            "question_id": f"Q{i:02d}",
            "question": entry.get("query"),
            "question_type": query_info.get("type", ""),
            "expected_focus": query_info.get("expected_focus", ""),
            "system": "",
            "retrieved_passages": passages_json_list,
            "generated_response": entry.get("answer"),
            "correctness_score": "",
            "grounding_score": "",
            "retrieval_relevance_score": "",
            "usefulness_score": "",
            "style_quality_score": "",
            "comments": ""
        }
        rows.append(row)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote evaluation template to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_evaluation_template("../results/answers/retrieval_history.json")
