from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score, silhouette_score


EPS = 0.7
MIN_SAMPLES_VALUES = [5, 10, 19, 20, 25]
OUTPUT_DIR = Path("output")


def count_clusters(labels):
    unique_labels = set(labels)
    return len(unique_labels - {-1})


def count_noise(labels):
    return int(np.sum(labels == -1))


def safe_silhouette_score(x, labels):
    valid = labels != -1
    valid_labels = labels[valid]

    if len(set(valid_labels)) < 2:
        return np.nan

    return silhouette_score(x[valid], valid_labels)


def run_dbscan_experiment(x, y_true):
    results = []

    for min_samples in MIN_SAMPLES_VALUES:
        model = DBSCAN(
            eps=EPS,
            min_samples=min_samples,
            metric="euclidean",
        )
        labels = model.fit_predict(x)

        results.append(
            {
                "min_samples": min_samples,
                "labels": labels,
                "n_clusters": count_clusters(labels),
                "n_noise": count_noise(labels),
                "noise_pct": 100 * count_noise(labels) / len(labels),
                "silhouette": safe_silhouette_score(x, labels),
                "ari": adjusted_rand_score(y_true, labels),
            }
        )

    return results


def plot_original_data(x, output_dir):
    plt.figure(figsize=(7, 5))
    plt.scatter(x[:, 0], x[:, 1], s=18)
    plt.title("Base de dados original")
    plt.xlabel("Atributo 1")
    plt.ylabel("Atributo 2")
    plt.tight_layout()
    plt.savefig(output_dir / "lab04_tarefa04_base_original.png", dpi=180)
    plt.close()


def plot_dbscan_results(x, results, output_dir):
    fig, axes = plt.subplots(
        2,
        3,
        figsize=(15, 9),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )
    axes = axes.ravel()

    for ax, result in zip(axes, results):
        labels = result["labels"]
        scatter = ax.scatter(
            x[:, 0],
            x[:, 1],
            c=labels,
            cmap="tab20",
            s=16,
            alpha=0.85,
        )
        ax.scatter(
            x[labels == -1, 0],
            x[labels == -1, 1],
            c="lightgray",
            edgecolor="black",
            linewidth=0.2,
            s=18,
            label="ruido",
        )
        ax.set_title(
            "min_samples={}\nclusters={} | ruido={:.1f}%".format(
                result["min_samples"],
                result["n_clusters"],
                result["noise_pct"],
            )
        )
        ax.set_xlabel("Atributo 1")
        ax.set_ylabel("Atributo 2")

    axes[-1].axis("off")
    fig.colorbar(scatter, ax=axes[:-1], shrink=0.75, label="Rotulo DBSCAN")
    fig.suptitle("DBSCAN com eps=0.7 e diferentes valores de min_samples", fontsize=14)
    plt.savefig(output_dir / "lab04_tarefa04_dbscan_min_samples.png", dpi=180)
    plt.close()


def print_results_table(results):
    header = (
        "min_samples | clusters | ruido | ruido(%) | silhouette | ARI"
    )
    print(header)
    print("-" * len(header))

    for result in results:
        silhouette = result["silhouette"]
        silhouette_text = "nan" if np.isnan(silhouette) else f"{silhouette:.4f}"

        print(
            "{:11d} | {:8d} | {:5d} | {:8.2f} | {:10s} | {:.4f}".format(
                result["min_samples"],
                result["n_clusters"],
                result["n_noise"],
                result["noise_pct"],
                silhouette_text,
                result["ari"],
            )
        )


def choose_best_result(results, expected_clusters):
    return max(
        results,
        key=lambda item: (
            -abs(item["n_clusters"] - expected_clusters),
            item["ari"],
            item["silhouette"] if not np.isnan(item["silhouette"]) else -1,
            -item["noise_pct"],
        ),
    )


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    x, y = make_blobs(
        n_samples=1000,
        centers=8,
        n_features=2,
        random_state=800,
    )

    results = run_dbscan_experiment(x, y)
    plot_original_data(x, OUTPUT_DIR)
    plot_dbscan_results(x, results, OUTPUT_DIR)
    print_results_table(results)

    best = choose_best_result(results, expected_clusters=8)
    print()
    print(
        "Conclusao: com eps=0.7, o valor mais adequado foi min_samples={}.".format(
            best["min_samples"]
        )
    )
    print(
        "Esse valor recuperou {} clusters, marcou {:.2f}% dos pontos como ruido "
        "e obteve ARI={:.4f}.".format(
            best["n_clusters"],
            best["noise_pct"],
            best["ari"],
        )
    )


if __name__ == "__main__":
    main()
