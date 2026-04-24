import math
from collections import defaultdict, Counter
from classifier import classify_title

#Function for theme counting.
def build_user_theme_counts(df, classify_title):
    user_theme_counts = defaultdict(Counter)

    for row in df.itertuples():
        themes = classify_title(row.title)
        for theme in themes:
            user_theme_counts[row.user][theme] += 1

    return user_theme_counts

#Funtion for theme frquency profiling.
def get_all_themes(user_theme_counts):
    themes = set()

    for counts in user_theme_counts.values():
        themes.update(counts.keys())

    return sorted(themes)

#Converting THeme Counts to Vectors.
def build_user_vectors(user_theme_counts, all_themes):
    user_vectors = {}

    for user, counts in user_theme_counts.items():
        vector = [counts.get(theme, 0) for theme in all_themes]
        user_vectors[user] = vector

    return user_vectors
#Normalizing Vectors(Caluclation)
def normalize_vector(vector):
    magnitude = math.sqrt(sum(x * x for x in vector))

    if magnitude == 0:
        return vector

    return [x / magnitude for x in vector]
#Normalizeing User Vectors.
def normalize_user_vectors(user_vectors):
    normalized = {}

    for user, vector in user_vectors.items():
        normalized[user] = normalize_vector(vector)

    return normalized

#Cosine Similarities Calculation.
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

#Pairwise Comparisons and Similarity Scoring.
def compute_all_similarities(normalized_user_vectors):
    users = list(normalized_user_vectors.keys())
    similarities = []

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            user_a = users[i]
            user_b = users[j]
            score = cosine_similarity(
                normalized_user_vectors[user_a],
                normalized_user_vectors[user_b]
            )
            similarities.append((user_a, user_b, score))

    return similarities

#Getting shared theme counts for matched users.
def get_shared_themes(user_a_counts, user_b_counts):
    shared = []

    for theme in user_a_counts:
        if theme in user_b_counts:
            shared_score = min(user_a_counts[theme], user_b_counts[theme])
            shared.append((theme, shared_score))

    shared.sort(key=lambda x: x[1], reverse=True)
    return [theme for theme, score in shared]

#Ranking Matches based on Similarity Scores and Shared Themes.
def rank_matches(similarities, user_theme_counts):
    ranked = []

    for user_a, user_b, score in similarities:
        shared_themes = get_shared_themes(
            user_theme_counts[user_a],
            user_theme_counts[user_b]
        )
        ranked.append((user_a, user_b, score, shared_themes))

    ranked.sort(key=lambda x: x[2], reverse=True)
    return ranked
#IDF Calculation for themes across users.

def compute_idf(user_theme_counts):
    total_users = len(user_theme_counts)
    theme_user_count = {}

    # count how many users have each theme
    for counts in user_theme_counts.values():
        for theme in counts:
            theme_user_count[theme] = theme_user_count.get(theme, 0) + 1

    # compute IDF
    idf = {}
    for theme, count in theme_user_count.items():
        idf[theme] = math.log((total_users + 1) / (count + 1)) + 1

    return idf


def apply_tfidf(user_theme_counts, idf):
    tfidf_counts = {}

    for user, counts in user_theme_counts.items():
        tfidf_counts[user] = {}
        for theme, tf in counts.items():
            tfidf_counts[user][theme] = tf * idf.get(theme, 0)

    return tfidf_counts

def run_pipeline(df):
    # Step 1: build counts
    user_theme_counts = build_user_theme_counts(df, classify_title)

    # Step 2: compute TF-IDF
    idf = compute_idf(user_theme_counts)
    tfidf_counts = apply_tfidf(user_theme_counts, idf)

    # Step 3: use TF-IDF instead of raw counts
    all_themes = get_all_themes(tfidf_counts)
    user_vectors = build_user_vectors(tfidf_counts, all_themes)

    # Step 4: continue as usual
    normalized_vectors = normalize_user_vectors(user_vectors)
    similarities = compute_all_similarities(normalized_vectors)
    ranked_matches = rank_matches(similarities, user_theme_counts)

    return {
        "theme_counts": user_theme_counts,
        "vectors": user_vectors,
        "normalized": normalized_vectors,
        "similarities": similarities,
        "ranked": ranked_matches
    }