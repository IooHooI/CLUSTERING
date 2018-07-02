from sklearn import metrics
import pandas as pd


def metrics_with_ground_truth_labels(true_labels, predicted_labels):
    results = []
    columns = ['AR', 'MI', 'AMI', 'NMI']
    for pred in predicted_labels:
        results.append([
            metrics.adjusted_rand_score(true_labels, pred),
            metrics.mutual_info_score(true_labels, pred),
            metrics.adjusted_mutual_info_score(true_labels, pred),
            metrics.normalized_mutual_info_score(true_labels, pred)
        ])
    return pd.DataFrame(data=results, columns=columns)


def metrics_without_ground_truth_labels(Xs, predicted_labels):
    results = []
    columns = ['SC', 'CHI']
    for X, pred in zip(Xs, predicted_labels):
        results.append([
            metrics.silhouette_score(X, pred),
            metrics.calinski_harabaz_score(X, pred)
        ])
    return pd.DataFrame(data=results, columns=columns)


def metrics_report(row_names, Xs, pred_labels, true_labels):
    metrics_res = pd.concat(
        [
            metrics_with_ground_truth_labels(true_labels, pred_labels),
            metrics_without_ground_truth_labels(Xs, pred_labels)
        ],
        axis=1,
        join='inner'
    )
    metrics_res.index = row_names
    return metrics_res
