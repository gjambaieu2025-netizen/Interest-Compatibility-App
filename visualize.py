import matplotlib.pyplot as plt
import numpy as np
# Functions for creating similarity matrix and plotting heatmap.
def create_similarity_matrix(users, similarities):
    n = len(users)
    matrix = np.zeros((n, n))
    # diagonal = 1.0 because each user is fully similar to themselves
    for i in range(n):
        matrix[i][i] = 1.0

    for user_a, user_b, score in similarities:
        i = users.index(user_a)
        j = users.index(user_b)
        matrix[i][j] = score
        matrix[j][i] = score

    return matrix

#Plotting Heatmap for Similarity Matrix.
def plot_similarity_heatmap(users, matrix):
    fig, ax = plt.subplots()
    cax = ax.imshow(matrix)

    ax.set_xticks(range(len(users)))
    ax.set_yticks(range(len(users)))
    ax.set_xticklabels(users)
    ax.set_yticklabels(users)

    plt.title("User Compatibility Heatmap")
    plt.colorbar(cax)
    plt.tight_layout()
    plt.show()
    return fig

#Plotting User Theme Distribution.
def plot_user_theme_distribution(counts):
    themes = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots()
    ax.bar(themes, values)

    ax.set_xlabel("Themes")
    ax.set_ylabel("Count")
    ax.set_title("User Interest Distribution")

    return fig