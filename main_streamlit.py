import streamlit as st
import requests

# URL de ton backend FastAPI
API_URL = "http://localhost:8000"

# Titre de l'application
st.title("🎬 Movie Explorer")

# Initialiser l'état de session
if "movie" not in st.session_state:
    st.session_state.movie = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# Bouton pour récupérer un film aléatoire
if st.button("🎲 Show Random Movie"):
    try:
        response = requests.get(f"{API_URL}/movies/random/")
        response.raise_for_status()
        movie_data = response.json()

        # Stocker le film dans la session
        st.session_state.movie = movie_data
        st.session_state.summary = None  # Réinitialiser le résumé

    except requests.RequestException as e:
        st.error(f"❌ Erreur lors de la récupération du film : {e}")
        st.session_state.movie = None

# Affichage des détails du film
if st.session_state.movie:
    movie = st.session_state.movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"🎬 Directed by: {movie['director']}")
    st.markdown("**🎭 Cast:**")
    for actor in movie["actors"]:
        st.write(f"- {actor['actor_name']}")

# Bouton pour générer un résumé (activé uniquement si un film est chargé)
if st.session_state.movie:
    if st.button("🧠 Get Summary"):
        try:
            movie_id = st.session_state.movie["id"]
            payload = {"movie_id": movie_id}
            response = requests.post(f"{API_URL}/generate_summary/", json=payload)
            response.raise_for_status()
            summary_data = response.json()

            # Stocker le résumé dans session_state
            st.session_state.summary = summary_data["summary_text"]

        except requests.RequestException as e:
            st.error(f"❌ Erreur lors de la génération du résumé : {e}")
            st.session_state.summary = None

# Affichage du résumé si présent
if st.session_state.summary:
    st.markdown("### 📝 Summary:")
    st.info(st.session_state.summary)
