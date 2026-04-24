from data_loader import load_history_data
from classifier import classify_title
from similarity import (
    build_user_theme_counts,
    get_all_themes,
    build_user_vectors,
    normalize_user_vectors,
    compute_all_similarities,
    rank_matches,
    run_pipeline,
)
from visualize import create_similarity_matrix, plot_similarity_heatmap


def main():
    df = load_history_data("data.csv")  # fix path if needed
    results=run_pipeline(df)

    print("Ranked compatibility matches:\n")
    for user_a, user_b, score, shared_themes in results["ranked"]:
        explanation = ", ".join(shared_themes[:3]) if shared_themes else "none"
        print(f"{user_a} <-> {user_b}: {score:.3f} | Shared themes: {explanation}")

    #  visualization
    users = list(results["normalized"].keys())
    matrix = create_similarity_matrix(users, results["similarities"])
    plot_similarity_heatmap(users, matrix)


if __name__ == "__main__":
    main()