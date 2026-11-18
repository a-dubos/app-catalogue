import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (DOIT être la première instruction Streamlit)
st.set_page_config(
    page_title="Tableau de bord visuel",
    page_icon="📊",
    layout="wide"
)

# Constante pour le chemin du fichier
FICHIER = "data/livres_poetry.csv"

# 2. Chargement des données avec le cache
@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)

df = charger_donnees(FICHIER)

# Titre et légende de la page
st.title("Tableau de bord visuel du catalogue")
st.caption("Analyse graphique des données de books.toscrape.com")

# 3. Les filtres dans la barre latérale
with st.sidebar:
    st.header("Filtres")
    
    # Note minimale
    note_mini = st.slider("Note minimale", 1, 5, 1)
    
    # Fourchette de prix
    prix_min, prix_max = st.slider(
        "Fourchette de prix (GBP)", 
        float(df["prix_gbp"].min()), 
        float(df["prix_gbp"].max()), 
        (float(df["prix_gbp"].min()), float(df["prix_gbp"].max()))
    )
    
    # Recherche textuelle
    recherche = st.text_input("Le titre contient")

# Application des filtres sur une copie du DataFrame
selection = df.copy()
selection = selection[selection["note"] >= note_mini]
selection = selection[(selection["prix_gbp"] >= prix_min) & (selection["prix_gbp"] <= prix_max)]

if recherche:
    selection = selection[selection["titre"].str.contains(recherche, case=False, na=False)]

# 4. Traitement du cas vide (obligatoire avant les graphiques)
if len(selection) == 0:
    st.warning("Aucun livre ne correspond à ces critères.")
else:
    # --- Affichage des indicateurs chiffrés en haut ---
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Livres retenus", f"{len(selection)} / {len(df)}")
    col_kpi2.metric("Prix moyen", f"{selection['prix_gbp'].mean():.2f} GBP")
    col_kpi3.metric("Note moyenne", f"{selection['note'].mean():.2f} / 5")
    
    st.markdown("---")

    # --- ÉTAPE 3 : Deux graphiques côte à côte ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Répartition des prix")
        # Graphique 1 : Histogramme des prix
        fig_prix = px.histogram(
            selection,
            x="prix_gbp",
            nbins=10,
            labels={"prix_gbp": "Prix (GBP)"},
            title="Distribution des prix"
        )
        st.plotly_chart(fig_prix, use_container_width=True)
        st.caption("Ce graphique montre que la majorité des prix se concentrent sur certaines tranches tarifaires de la sélection.")

    with col2:
        st.subheader("Nombre de livres par note")
        # Graphique 2 : Nombre de livres par note
        par_note = selection["note"].value_counts().sort_index()
        st.bar_chart(par_note)
        st.caption("Ce diagramme en barres permet d'identifier rapidement les notes les plus attribuées au sein des livres filtrés.")

    # --- Troisième graphique en dessous, sur toute la largeur ---
    st.subheader("Relation Prix / Note")
    
    # --- ÉTAPE 4 : Graphique piloté par un widget ---
    # Un sélecteur pour choisir quelle variable colorer ou afficher
    mode_couleur = st.radio(
        "Colorer les points du nuage selon :",
        ["note", "stock"],
        horizontal=True
    )

    # Graphique 3 : Nuage de points interactif Plotly
    fig_scatter = px.scatter(
        selection,
        x="prix_gbp",
        y="note",
        size="stock",
        color=mode_couleur,
        hover_name="titre",
        labels={"prix_gbp": "Prix (GBP)", "note": "Note sur 5", "stock": "Stock"},
        title="Chaque point est un livre (survolez pour voir le titre)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption(f"Ce nuage de points met en relation le prix et la note des livres, avec une coloration dynamique basée sur le critère : {mode_couleur}.")