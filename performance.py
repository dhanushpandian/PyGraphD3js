from sklearn.metrics import precision_score, recall_score, f1_score

# Ground Truth (Expected relevant results)
ground_truth = {
    "COVID-19 treatments": {"Remdesivir", "Dexamethasone", "Tocilizumab"},
    "Cancer drugs": {"Paclitaxel", "Cisplatin"}
}

# Retrieved Results (Actual results from the system)
retrieved_results = {
    "COVID-19 treatments": {"Remdesivir", "Hydroxychloroquine", "Dexamethasone"},
    "Cancer drugs": {"Cisplatin", "Methotrexate"}
}

# Compute Precision, Recall, and F1-score
precision_list, recall_list, f1_list = [], [], []

for query in ground_truth:
    relevant_retrieved = len(ground_truth[query] & retrieved_results[query])  # Intersection
    total_retrieved = len(retrieved_results[query])  # Retrieved results
    total_relevant = len(ground_truth[query])  # Ground truth results
    
    precision = relevant_retrieved / total_retrieved if total_retrieved else 0
    recall = relevant_retrieved / total_relevant if total_relevant else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0
    
    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1)

# Average Scores
avg_precision = sum(precision_list) / len(precision_list)
avg_recall = sum(recall_list) / len(recall_list)
avg_f1 = sum(f1_list) / len(f1_list)

# Print results
print(f"Precision: {avg_precision:.2f}")
print(f"Recall: {avg_recall:.2f}")
print(f"F1-score: {avg_f1:.2f}")
