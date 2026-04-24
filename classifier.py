import re

THEME_KEYWORDS = {
    "technology": ["python", "ai", "programming", "software", "coding", "computer"],
    "sports": ["football", "soccer", "basketball", "tennis", "baseball"],
    "music": ["music", "song", "concert", "playlist"],
    "education": ["tutorial", "lecture", "course", "study"],
    "movies": ["movie", "film", "trailer", "series", "cinema"]
}

HASHTAG_MAP = {
    "#coding": "technology",
    "#ai": "technology",
    "#soccer": "sports",
    "#football": "sports",
    "#music": "music"
}
#Defining classifying function.
import re

def classify_title(title: str):
    text = title.lower().strip()

    # Step 1: extract hashtags directly as themes
    hashtags = re.findall(r"#(\w+)", text)  # remove '#' automatically

    if hashtags:
        return list(set(hashtags))  # unique themes from hashtags

    # Step 2: fallback → keyword matching
    theme_scores = {}

    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for word in keywords:
            if re.search(rf"\b{re.escape(word)}\b", text):
                score += 1
        if score > 0:
            theme_scores[theme] = score

    # Step 3: choose best theme
    if not theme_scores:
        return ["other"]

    max_score = max(theme_scores.values())

    best_themes = [
        theme for theme, score in theme_scores.items()
        if score == max_score
    ]

    return best_themes
print(classify_title("Football match highlights"))
print(classify_title("Soccer training drills"))
print(classify_title("Basketball game highlights"))
print(classify_title("Python programming tutorial"))
