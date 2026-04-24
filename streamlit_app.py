import streamlit as st
import pandas as pd
#Importing all the necessary functions from the other files
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
from visualize import create_similarity_matrix, plot_similarity_heatmap,plot_user_theme_distribution

#App formatting 
st.title("Interest Compatibility App")
#Three modes for the app.
mode= st.sidebar.selectbox("Select mode",["Overall Compatibility Analyzer","User-to-User Analyzer","Single User Analyzer"])

#Deining functions for overall pipeline.


#Overall Compatabilty Analyse mode.
if mode == "Overall Compatibility Analyzer":
    st.header("Overall Compatibility Analyzer")
    uploaded_file = st.file_uploader("Upload Users Data", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df)

        if st.button("Run Analysis"):
            df.to_csv("temp_uploaded.csv", index=False)
            results = run_pipeline(df)

            st.subheader("Ranked Compatibility Matches")
            for user_a, user_b, score, shared_themes in results["ranked"]:
                explanation = ", ".join(shared_themes[:3]) if shared_themes else "none"
                st.write(f"{user_a} ↔ {user_b}: {score:.3f} | Shared themes: {explanation}")

            users = list(results["normalized"].keys())
            matrix = create_similarity_matrix(users, results["similarities"])

            st.subheader("Compatibility Heatmap")
            fig = plot_similarity_heatmap(users, matrix)
            st.pyplot(fig)


#User-to-User Analyzer mode.
elif mode == "User-to-User Analyzer":
    st.header("Compare Two Users")

    file_a = st.file_uploader("Upload User A data", type=["csv"], key="a")
    file_b = st.file_uploader("Upload User B data", type=["csv"], key="b")

    if file_a and file_b:
        df_a = pd.read_csv(file_a)
        df_b = pd.read_csv(file_b)

        df_a["user"] = "User_A"
        df_b["user"] = "User_B"
        st.subheader("Data Preview_User A")
        st.dataframe(df_a)
        st.subheader("Data Preview_User B")
        st.dataframe(df_b)
        combined_df = pd.concat([df_a, df_b])
        if st.button("Results"):
            results = run_pipeline(combined_df)
            similarity_score = results["similarities"][0][2] if results["similarities"] else 0.0
            shared_themes = results["ranked"][0][3] if results["ranked"] else []
            st.write(
            f"{df_a['user'].iloc[0]} and {df_b['user'].iloc[0]} are {similarity_score*100:.2f}% compatible "
            f"because they share: {', '.join(shared_themes[:5]) if shared_themes else 'None'}"
            )
#Single User Analyzer mode.
elif mode == "Single User Analyzer":
    st.header("Single User Analysis")

    file = st.file_uploader("Upload user data", type=["csv"], key="single")

    if file:
        df = pd.read_csv(file)

        df["user"] = "User"
        if st.button("Results"):
            results = run_pipeline(df)
            #extracting theme counts
            user_theme_counts = results["theme_counts"]
            counts = list(user_theme_counts.values())[0]
            percentages = {theme: count / sum(counts.values()) * 100 for theme, count in counts.items()}
            #show theme distribution \
            st.subheader("Theme Distribution")
            import pandas as pd

            st.subheader("Theme Distribution")

            df_counts = pd.DataFrame({
                "Theme": list(counts.keys()),
                "Count": list(counts.values()),
                "Percentage": [
                    (count / sum(counts.values()))*100 for count in counts.values()
                ]
            })

            st.table(df_counts)
            #show total actvity or content items
            st.write(f"Total content items: {len(df)}")
            
            #show dominant theme
            dominant = max(results["theme_counts"][df["user"].iloc[0]], key=results["theme_counts"][df["user"].iloc[0]].get)
            st.write(f"Dominant Interest: {dominant}")
           #Plot.
            fig = plot_user_theme_distribution(counts)
            st.pyplot(fig)
