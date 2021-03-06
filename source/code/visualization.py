from sklearn.metrics import silhouette_samples, silhouette_score

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def choose_n_clusters(range_n_clusters, data, random_state):
    avg_values = []
    std_values = []
    min_values = []
    max_values = []
    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, ax1 = plt.subplots(1, 1)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.5, 0.5])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(data) + (n_clusters + 1) * 10])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters=n_clusters, random_state=random_state)
        cluster_labels = clusterer.fit_predict(data)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(data, cluster_labels)
        avg_values.append(silhouette_avg)

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(data, cluster_labels)
        std_values.append(np.std(sample_silhouette_values))
        min_values.append(min(sample_silhouette_values))
        max_values.append(max(sample_silhouette_values))
        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.spectral(float(i) / n_clusters)
            ax1.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7
            )

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.suptitle(
            ("Silhouette analysis for KMeans clustering on sample data with n_clusters = %d" % n_clusters),
            fontsize=14,
            fontweight='bold'
        )

        plt.show()
    return pd.DataFrame(data={'avg': avg_values, 'std': std_values, 'min': min_values, 'max': max_values})


def plot_word_clouds(documents, labels, label_names=None, top_features=20):
    unique_labels = np.array(sorted(list(set(labels))))
    # print(Counter(labels))
    f, axs = plt.subplots(len(unique_labels), 1, figsize=(150, 150))
    for label, ax in zip(unique_labels, axs):
        labelled_texts = [doc for doc, lab in zip(documents, labels) if lab == label]
        # print(sum(list(map(len, labelled_texts))))
        if sum(list(map(len, labelled_texts))) > 0:
            wordcloud = WordCloud(collocations=False, max_words=top_features).generate(' '.join(labelled_texts))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            ax.set_title(
                'Top-{} words for cluster: {}'.format(top_features, label_names[label] if label_names is not None else label + 1),
                fontsize=45
            )
    plt.tight_layout()
    plt.show()


def plot_confusion_matrixes(matrixes, titles):
    f, axs = plt.subplots(1, len(matrixes), figsize=(45, 15))
    for mat, title, ax in zip(matrixes, titles, axs):
        sns.heatmap(mat.T, square=True, fmt='d', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('true label')
        ax.set_ylabel('predicted label')
    plt.show()
