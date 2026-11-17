import streamlit as st
import pandas as pd

# 1. Configuration de la page (DOIT être la première instruction Streamlit)
st.set_page_config(
    page_title="Explorateur de catalogue",
    page_icon="📚",
    layout="wide"
)

# Constante pour le chemin du fichier (modifiable si besoin)
FICHIER = "data/livres_poetry.csv"

# 2. Chargement des données avec le cache (Étape 1)
@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)

df = charger_donnees(FICHIER)

# Titre et légende de l'application
st.title("Explorateur de catalogue")
st.caption("Données collectées sur books.toscrape.com")

# 3. Filtres dans la barre latérale (Étape 2)
with st.sidebar:
    st.header("Filtres")
    
    # Note minimale (curseur simple)
    note_mini = st.slider("Note minimale", 1, 5, 1)
    
    # Fourchette de prix (curseur à deux poignées)
    prix_min, prix_max = st.slider(
        "Fourchette de prix (GBP)", 
        float(df["prix_gbp"].min()), 
        float(df["prix_gbp"].max()), 
        (float(df["prix_gbp"].min()), float(df["prix_gbp"].max()))
    )
    
    # Recherche textuelle dans les titres
    recherche = st.text_input("Le titre contient")

# Application des filtres sur une copie du DataFrame
selection = df.copy()
selection = selection[selection["note"] >= note_mini]
selection = selection[(selection["prix_gbp"] >= prix_min) & (selection["prix_gbp"] <= prix_max)]

if recherche:
    selection = selection[selection["titre"].str.contains(recherche, case=False, na=False)]

# 4. Traitement du cas vide (Étape 5)
if len(selection) == 0:
    st.warning("Aucun livre ne correspond à ces critères.")
else:
    # 5. Quatre indicateurs côte à côte sur la sélection (Étape 3)
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Livres retenus", f"{len(selection)} / {len(df)}")
    col2.metric("Prix moyen", f"{selection['prix_gbp'].mean():.2f} GBP")
    col3.metric("Note moyenne", f"{selection['note'].mean():.2f} / 5")
    col4.metric("Stock total", int(selection['stock'].sum()))

    st.markdown("---")

    # 6. Tableau de la sélection et palmarès (Étape 4)
    st.subheader("Sélection")
    st.dataframe(selection, use_container_width=True)

    # Deux colonnes pour les palmarès
    gauche, droite = st.columns(2)
    
    with gauche:
        st.subheader("Les mieux notés")
        st.dataframe(
            selection.nlargest(5, "note")[["titre", "note", "prix_gbp"]],
            use_container_width=True
        )
        
    with droite:
        st.subheader("Les moins chers")
        st.dataframe(
            selection.nsmallest(5, "prix_gbp")[["titre", "prix_gbp", "note"]],
            use_container_width=True
        )

# 7. Données brutes dans un expander (Étape 6)
with st.expander("Voir les données brutes"):
    st.dataframe(df, use_container_width=True)