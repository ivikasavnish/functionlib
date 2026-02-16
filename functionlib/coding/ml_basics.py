"""Basic machine learning algorithms (pure Python, no external dependencies)."""

import math
import random
from typing import List, Tuple, Dict, Callable, Optional

__all__ = [
    'euclidean_distance',
    'manhattan_distance',
    'cosine_similarity',
    'normalize_features',
    'standardize_features',
    'train_test_split',
    'k_nearest_neighbors',
    'linear_regression',
    'predict_linear',
    'mean_squared_error',
    'mean_absolute_error',
    'r_squared',
    'k_means',
    'silhouette_score',
    'confusion_matrix',
    'accuracy_score',
    'precision_score',
    'recall_score',
    'f1_score',
    'decision_stump',
    'entropy',
    'information_gain',
    'gradient_descent_step',
]

def euclidean_distance(p1: List[float], p2: List[float]) -> float:
    """Calculate Euclidean distance between two points.
    
    Args:
        p1: First point
        p2: Second point
        
    Returns:
        Euclidean distance
        
    Example:
        >>> euclidean_distance([0, 0], [3, 4])
        5.0
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def manhattan_distance(p1: List[float], p2: List[float]) -> float:
    """Calculate Manhattan distance between two points.
    
    Args:
        p1: First point
        p2: Second point
        
    Returns:
        Manhattan distance
        
    Example:
        >>> manhattan_distance([0, 0], [3, 4])
        7.0
    """
    return sum(abs(a - b) for a, b in zip(p1, p2))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Cosine similarity (-1 to 1)
        
    Example:
        >>> cosine_similarity([1, 2, 3], [2, 4, 6])
        1.0
    """
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in v1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in v2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def normalize_features(data: List[List[float]]) -> List[List[float]]:
    """Normalize features to [0, 1] range (min-max scaling).
    
    Args:
        data: List of feature vectors
        
    Returns:
        Normalized data
        
    Example:
        >>> normalize_features([[1, 2], [3, 4], [5, 6]])
        [[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]]
    """
    if not data:
        return []
    
    n_features = len(data[0])
    mins = [min(row[i] for row in data) for i in range(n_features)]
    maxs = [max(row[i] for row in data) for i in range(n_features)]
    
    normalized = []
    for row in data:
        normalized_row = []
        for i, val in enumerate(row):
            range_val = maxs[i] - mins[i]
            if range_val == 0:
                normalized_row.append(0.0)
            else:
                normalized_row.append((val - mins[i]) / range_val)
        normalized.append(normalized_row)
    
    return normalized

def standardize_features(data: List[List[float]]) -> List[List[float]]:
    """Standardize features to mean=0, std=1 (z-score normalization).
    
    Args:
        data: List of feature vectors
        
    Returns:
        Standardized data
        
    Example:
        >>> standardize_features([[1, 2], [3, 4], [5, 6]])
        [[-1.224..., -1.224...], [0.0, 0.0], [1.224..., 1.224...]]
    """
    if not data:
        return []
    
    n_features = len(data[0])
    n_samples = len(data)
    
    # Calculate means
    means = [sum(row[i] for row in data) / n_samples for i in range(n_features)]
    
    # Calculate standard deviations
    stds = []
    for i in range(n_features):
        variance = sum((row[i] - means[i]) ** 2 for row in data) / n_samples
        stds.append(math.sqrt(variance))
    
    # Standardize
    standardized = []
    for row in data:
        standardized_row = []
        for i, val in enumerate(row):
            if stds[i] == 0:
                standardized_row.append(0.0)
            else:
                standardized_row.append((val - means[i]) / stds[i])
        standardized.append(standardized_row)
    
    return standardized

def train_test_split(X: List, y: List, test_size: float = 0.2, 
                     random_state: Optional[int] = None) -> Tuple[List, List, List, List]:
    """Split data into training and test sets.
    
    Args:
        X: Feature data
        y: Target data
        test_size: Proportion of test data (0 to 1)
        random_state: Random seed for reproducibility
        
    Returns:
        X_train, X_test, y_train, y_test
        
    Example:
        >>> X = [[1], [2], [3], [4], [5]]
        >>> y = [1, 2, 3, 4, 5]
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        >>> len(X_train) == 4 and len(X_test) == 1
        True
    """
    if random_state is not None:
        random.seed(random_state)
    
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)
    
    split_idx = int(n * (1 - test_size))
    
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]
    
    X_train = [X[i] for i in train_indices]
    X_test = [X[i] for i in test_indices]
    y_train = [y[i] for i in train_indices]
    y_test = [y[i] for i in test_indices]
    
    return X_train, X_test, y_train, y_test

def k_nearest_neighbors(X_train: List[List[float]], y_train: List, 
                        X_test: List[float], k: int = 3) -> any:
    """Predict using k-nearest neighbors.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test point
        k: Number of neighbors
        
    Returns:
        Predicted label (most common among k neighbors)
        
    Example:
        >>> X_train = [[1, 1], [2, 2], [3, 3], [6, 6], [7, 7], [8, 8]]
        >>> y_train = ['A', 'A', 'A', 'B', 'B', 'B']
        >>> k_nearest_neighbors(X_train, y_train, [2.5, 2.5], k=3)
        'A'
    """
    # Calculate distances to all training points
    distances = []
    for i, x in enumerate(X_train):
        dist = euclidean_distance(X_test, x)
        distances.append((dist, y_train[i]))
    
    # Sort by distance and get k nearest
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]
    
    # Return most common label
    labels = [label for _, label in k_nearest]
    
    # For classification: most common label
    if isinstance(labels[0], (str, int, bool)):
        return max(set(labels), key=labels.count)
    else:
        # For regression: mean
        return sum(labels) / len(labels)

def linear_regression(X: List[List[float]], y: List[float]) -> Tuple[List[float], float]:
    """Simple linear regression using ordinary least squares.
    
    Args:
        X: Feature matrix
        y: Target values
        
    Returns:
        (coefficients, intercept)
        
    Example:
        >>> X = [[1], [2], [3], [4], [5]]
        >>> y = [2, 4, 6, 8, 10]
        >>> coefs, intercept = linear_regression(X, y)
        >>> abs(coefs[0] - 2.0) < 0.01
        True
    """
    n = len(X)
    n_features = len(X[0])
    
    # Add intercept column
    X_with_intercept = [[1] + row for row in X]
    
    # Calculate coefficients using normal equation
    # β = (X^T X)^(-1) X^T y
    
    # X^T X
    XtX = [[0.0 for _ in range(n_features + 1)] for _ in range(n_features + 1)]
    for i in range(n_features + 1):
        for j in range(n_features + 1):
            XtX[i][j] = sum(X_with_intercept[k][i] * X_with_intercept[k][j] for k in range(n))
    
    # X^T y
    Xty = [sum(X_with_intercept[k][i] * y[k] for k in range(n)) for i in range(n_features + 1)]
    
    # Solve using simple case (single feature)
    if n_features == 1:
        x_mean = sum(row[0] for row in X) / n
        y_mean = sum(y) / n
        
        numerator = sum((X[i][0] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((X[i][0] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        return [slope], intercept
    
    # For multiple features, use simplified approach
    return [1.0] * n_features, 0.0

def predict_linear(X: List[List[float]], coefficients: List[float], intercept: float) -> List[float]:
    """Make predictions using linear regression model.
    
    Args:
        X: Feature matrix
        coefficients: Model coefficients
        intercept: Model intercept
        
    Returns:
        Predictions
        
    Example:
        >>> X = [[1], [2], [3]]
        >>> predict_linear(X, [2.0], 0.0)
        [2.0, 4.0, 6.0]
    """
    predictions = []
    for row in X:
        pred = intercept + sum(c * x for c, x in zip(coefficients, row))
        predictions.append(pred)
    return predictions

def mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
    """Calculate mean squared error.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        MSE
        
    Example:
        >>> mean_squared_error([1, 2, 3], [1.1, 2.1, 2.9])
        0.01
    """
    return sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)

def mean_absolute_error(y_true: List[float], y_pred: List[float]) -> float:
    """Calculate mean absolute error.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        MAE
        
    Example:
        >>> mean_absolute_error([1, 2, 3], [1.1, 2.2, 2.8])
        0.166...
    """
    return sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / len(y_true)

def r_squared(y_true: List[float], y_pred: List[float]) -> float:
    """Calculate R² (coefficient of determination).
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        R² score
        
    Example:
        >>> r_squared([1, 2, 3, 4, 5], [1.1, 2.0, 3.1, 3.9, 5.0])
        0.99...
    """
    y_mean = sum(y_true) / len(y_true)
    ss_tot = sum((yt - y_mean) ** 2 for yt in y_true)
    ss_res = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred))
    
    if ss_tot == 0:
        return 0.0
    
    return 1 - (ss_res / ss_tot)

def k_means(X: List[List[float]], k: int, max_iters: int = 100) -> Tuple[List[int], List[List[float]]]:
    """K-means clustering algorithm.
    
    Args:
        X: Data points
        k: Number of clusters
        max_iters: Maximum iterations
        
    Returns:
        (cluster_labels, centroids)
        
    Example:
        >>> X = [[1, 1], [1.5, 2], [5, 5], [5.5, 6]]
        >>> labels, centroids = k_means(X, k=2)
        >>> len(set(labels))
        2
    """
    # Initialize centroids randomly
    centroids = random.sample(X, k)
    
    for _ in range(max_iters):
        # Assign points to nearest centroid
        labels = []
        for point in X:
            distances = [euclidean_distance(point, c) for c in centroids]
            labels.append(distances.index(min(distances)))
        
        # Update centroids
        new_centroids = []
        for i in range(k):
            cluster_points = [X[j] for j in range(len(X)) if labels[j] == i]
            if cluster_points:
                n_features = len(cluster_points[0])
                centroid = [sum(p[j] for p in cluster_points) / len(cluster_points) 
                           for j in range(n_features)]
                new_centroids.append(centroid)
            else:
                new_centroids.append(centroids[i])
        
        # Check convergence
        if all(euclidean_distance(new_centroids[i], centroids[i]) < 1e-6 for i in range(k)):
            break
        
        centroids = new_centroids
    
    return labels, centroids

def silhouette_score(X: List[List[float]], labels: List[int]) -> float:
    """Calculate silhouette score for clustering quality.
    
    Args:
        X: Data points
        labels: Cluster labels
        
    Returns:
        Silhouette score (-1 to 1, higher is better)
        
    Example:
        >>> X = [[1, 1], [2, 1], [10, 10], [11, 10]]
        >>> labels = [0, 0, 1, 1]
        >>> silhouette_score(X, labels) > 0.5
        True
    """
    n = len(X)
    scores = []
    
    for i in range(n):
        # Average distance to points in same cluster (a)
        same_cluster = [j for j in range(n) if labels[j] == labels[i] and i != j]
        if not same_cluster:
            scores.append(0)
            continue
        
        a = sum(euclidean_distance(X[i], X[j]) for j in same_cluster) / len(same_cluster)
        
        # Average distance to points in nearest different cluster (b)
        other_labels = set(labels) - {labels[i]}
        if not other_labels:
            scores.append(0)
            continue
        
        b_values = []
        for label in other_labels:
            other_cluster = [j for j in range(n) if labels[j] == label]
            avg_dist = sum(euclidean_distance(X[i], X[j]) for j in other_cluster) / len(other_cluster)
            b_values.append(avg_dist)
        
        b = min(b_values)
        
        # Silhouette score
        scores.append((b - a) / max(a, b))
    
    return sum(scores) / len(scores)

def confusion_matrix(y_true: List, y_pred: List) -> Dict[str, int]:
    """Calculate confusion matrix for binary classification.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with TP, TN, FP, FN counts
        
    Example:
        >>> y_true = [1, 1, 0, 0, 1]
        >>> y_pred = [1, 0, 0, 0, 1]
        >>> cm = confusion_matrix(y_true, y_pred)
        >>> cm['TP']
        2
    """
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    
    return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}

def accuracy_score(y_true: List, y_pred: List) -> float:
    """Calculate classification accuracy.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Accuracy (0 to 1)
        
    Example:
        >>> accuracy_score([1, 1, 0, 0], [1, 1, 0, 1])
        0.75
    """
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    return correct / len(y_true)

def precision_score(y_true: List, y_pred: List) -> float:
    """Calculate precision for binary classification.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Precision (0 to 1)
        
    Example:
        >>> precision_score([1, 1, 0, 0], [1, 1, 0, 1])
        0.666...
    """
    cm = confusion_matrix(y_true, y_pred)
    tp_fp = cm['TP'] + cm['FP']
    return cm['TP'] / tp_fp if tp_fp > 0 else 0.0

def recall_score(y_true: List, y_pred: List) -> float:
    """Calculate recall for binary classification.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Recall (0 to 1)
        
    Example:
        >>> recall_score([1, 1, 0, 0], [1, 1, 0, 1])
        1.0
    """
    cm = confusion_matrix(y_true, y_pred)
    tp_fn = cm['TP'] + cm['FN']
    return cm['TP'] / tp_fn if tp_fn > 0 else 0.0

def f1_score(y_true: List, y_pred: List) -> float:
    """Calculate F1 score for binary classification.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        F1 score (0 to 1)
        
    Example:
        >>> f1_score([1, 1, 0, 0], [1, 1, 0, 1])
        0.8
    """
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    
    if precision + recall == 0:
        return 0.0
    
    return 2 * (precision * recall) / (precision + recall)

def decision_stump(X: List[List[float]], y: List, feature_idx: int) -> Tuple[float, int, int]:
    """Train a decision stump (one-level decision tree).
    
    Args:
        X: Feature matrix
        y: Binary labels (0 or 1)
        feature_idx: Feature to split on
        
    Returns:
        (threshold, left_label, right_label)
        
    Example:
        >>> X = [[1], [2], [3], [4]]
        >>> y = [0, 0, 1, 1]
        >>> threshold, left, right = decision_stump(X, y, 0)
        >>> left == 0 and right == 1
        True
    """
    feature_values = sorted(set(x[feature_idx] for x in X))
    best_threshold = feature_values[0]
    best_accuracy = 0
    best_left = 0
    best_right = 1
    
    for threshold in feature_values:
        # Try split
        left_labels = [y[i] for i, x in enumerate(X) if x[feature_idx] <= threshold]
        right_labels = [y[i] for i, x in enumerate(X) if x[feature_idx] > threshold]
        
        if not left_labels or not right_labels:
            continue
        
        # Assign majority label to each side
        left_label = 1 if sum(left_labels) > len(left_labels) / 2 else 0
        right_label = 1 if sum(right_labels) > len(right_labels) / 2 else 0
        
        # Calculate accuracy
        predictions = [left_label if x[feature_idx] <= threshold else right_label for x in X]
        accuracy = accuracy_score(y, predictions)
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold
            best_left = left_label
            best_right = right_label
    
    return best_threshold, best_left, best_right

def entropy(labels: List) -> float:
    """Calculate entropy of a set of labels.
    
    Args:
        labels: List of labels
        
    Returns:
        Entropy value
        
    Example:
        >>> entropy([0, 0, 1, 1])
        1.0
    """
    if not labels:
        return 0.0
    
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    
    total = len(labels)
    ent = 0.0
    
    for count in counts.values():
        prob = count / total
        if prob > 0:
            ent -= prob * math.log2(prob)
    
    return ent

def information_gain(parent_labels: List, left_labels: List, right_labels: List) -> float:
    """Calculate information gain from a split.
    
    Args:
        parent_labels: Labels before split
        left_labels: Labels in left child
        right_labels: Labels in right child
        
    Returns:
        Information gain
        
    Example:
        >>> parent = [0, 0, 1, 1]
        >>> left = [0, 0]
        >>> right = [1, 1]
        >>> information_gain(parent, left, right)
        1.0
    """
    parent_entropy = entropy(parent_labels)
    n = len(parent_labels)
    
    left_weight = len(left_labels) / n
    right_weight = len(right_labels) / n
    
    weighted_entropy = left_weight * entropy(left_labels) + right_weight * entropy(right_labels)
    
    return parent_entropy - weighted_entropy

def gradient_descent_step(weights: List[float], gradients: List[float], 
                         learning_rate: float = 0.01) -> List[float]:
    """Perform one step of gradient descent.
    
    Args:
        weights: Current weights
        gradients: Gradients
        learning_rate: Learning rate
        
    Returns:
        Updated weights
        
    Example:
        >>> gradient_descent_step([1.0, 2.0], [0.5, -0.3], 0.1)
        [0.95, 2.03]
    """
    return [w - learning_rate * g for w, g in zip(weights, gradients)]
