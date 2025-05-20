# test_suite.py

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
        field_wise[key]["total"] += 1

        if expected[key] == pred_value:
            correct += 1
            field_wise[key]["correct"] += 1

    return correct / total * 100, field_wise

def main():
    with open("ground_truths.json", "r") as f:
        ground_truths = json.load(f)

    total_accuracy = 0
    total_cases = len(ground_truths)
    overall_field_stats = {}

    for entry in ground_truths:
        image_path = os.path.join("data", entry["image"])
        expected = entry["expected"]

        print(f"\n🔍 Testing: {entry['image']}")

        extracted_text = extract_data_from_image(image_path)
        predicted = parse_extracted_data(extracted_text)

        acc, field_stats = evaluate_accuracy(expected, predicted)
        total_accuracy += acc
        print(f"  ➤ Accuracy: {acc:.2f}%")

        for field, stat in field_stats.items():
            overall = overall_field_stats.setdefault(field, {"correct": 0, "total": 0})
            overall["correct"] += stat["correct"]
            overall["total"] += stat["total"]

    avg_accuracy = total_accuracy / total_cases
    print("\n📊 Final Benchmark Report")
    print(f"✅ Average Accuracy Across {total_cases} Receipts: {avg_accuracy:.2f}%")

    for field, stat in overall_field_stats.items():
        field_acc = (stat["correct"] / stat["total"]) * 100
        print(f"  - {field}: {field_acc:.2f}% correct")

if __name__ == "__main__":
    main()
