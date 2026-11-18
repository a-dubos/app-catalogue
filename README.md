# Explorateur de catalogue - Streamlit

Application interactive de visualisation et d'exploration de données de livres (catégorie *Poetry*), développée avec **Streamlit** et **Pandas**.

## Fonctionnalités
- **Barre latérale de filtres** : 
  - Filtrage par note minimale (curseur).
  - Filtrage par fourchette de prix en GBP (curseur à double poignée).
  - Recherche textuelle dynamique dans les titres.
- **Indicateurs clés (KPI)** : Affichage en temps réel du nombre de livres retenus, du prix moyen, de la note moyenne et du stock total de la sélection.
- **Palmarès** : Visualisation rapide des 5 livres les mieux notés et des 5 livres les moins chers.
- **Données brutes** : Possibilité d'afficher l'intégralité du catalogue brut via un panneau dépliable (*expander*).

# Tableau de bord visuel - Streamlit

Application interactive de visualisation de données de livres (catégorie *Poetry*), développée avec **Streamlit**, **Pandas** et **Plotly**.

## Fonctionnalités du Dashboard
- **Filtres dynamiques** dans la barre latérale (note minimale, fourchette de prix, recherche textuelle).
- **Indicateurs clés (KPI)** calculés en temps réel sur la sélection.
- **Visualisations graphiques** :
  - Un histogramme de répartition des prix.
  - Un diagramme en barres du nombre de livres par note.
  - Un nuage de points interactif (Prix vs Note) piloté par un widget de sélection de couleur.
- **Phrases de lecture** textuelles sous chaque graphique pour interpréter les tendances.
- **Panneau repliable** pour consulter les données brutes.
