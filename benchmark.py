# benchmark.py

import json
import os
from main import extract_data_from_image, parse_extracted_data

def evaluate_accuracy(expected, predicted):
    correct = 0
    total = 0
    field_wise = {}

    for key in expected:
        total += 1
        field_wise.setdefault(key, {"correct": 0, "total": 0})

        pred_value = predicted.get(key, None)
        if expected[key] == pred_value:
            correct += 1
            field_wise[key]["correct"] += 1
        field_wise[key]["total"] += 1

    return correct / total * 100, field_wise

def run_benchmark(ground_truth_path="ground_truths.json", data_folder="data"):
    with open(ground_truth_path, "r") as f:
        ground_truths = json.load(f)

    results = []
    total_accuracy = 0
    total_cases = len(ground_truths)
    overall_field_stats = {}

    for entry in ground_truths:
        image_path = os.path.join(data_folder, entry["image"])
        expected = entry["expected"]

        extracted_text = extract_data_from_image(image_path)
        predicted = parse_extracted_data(extracted_text)

        acc, field_stats = evaluate_accuracy(expected, predicted)
        total_accuracy += acc

        for field, stat in field_stats.items():
            overall = overall_field_stats.setdefault(field, {"correct": 0, "total": 0})
            overall["correct"] += stat["correct"]
            overall["total"] += stat["total"]

        results.append({
            "image": entry["image"],
            "accuracy": acc
        })

    avg_accuracy = total_accuracy / total_cases
    return avg_accuracy, overall_field_stats, results
