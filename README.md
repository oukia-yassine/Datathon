# 🐎 ÉquiVigie Normandie

**Datathon Normandie 2026 — « Biodiversité et activités humaines »**  
*Plateforme cartographique d'aide à la décision territoriale pour analyser les proximités et interactions entre installations équestres et sites Natura 2000 en Normandie.*

- **Équipe :** Youssef CHEDLY (Développeur), Yassir DOURAID (Développeur), Yassine OUKIA (Data Analyst)
- **Licence du code :** MIT ([LICENSE](LICENSE)) — conforme à l'article 7 du règlement du Datathon Normandie 2026

---

## 1. Problématique & positionnement

La filière équine est un marqueur identitaire fort de la Normandie. Toutefois, la simple proximité géographique d'une activité équine avec un espace naturel protégé **ne prouve aucun impact négatif** : selon les pratiques et la nature des milieux, les prairies pâturées peuvent aussi contribuer au maintien des paysages ouverts et du bocage.

**ÉquiVigie Normandie** évite le piège d'un « score d'impact » non démontré et propose aux **collectivités, EPCI, Parcs Naturels Régionaux, animateurs Natura 2000 et acteurs de la filière** un outil transparent de **vigilance territoriale** pour :
1. Localiser les activités équestres normandes (`Data ES`) et les sites Natura 2000 (`ZSC` Habitats & `ZPS` Oiseaux).
2. Mesurer objectivement les proximités géographiques en projection métrique (`EPSG:2154`).
3. Prioriser les territoires et installations à examiner sur le terrain.
4. Générer des **pistes d'action contextualisées** (interactions **positives à valoriser** et **points de vigilance à vérifier**).

---

## 2. Les 4 fonctionnalités de l'application

1. **Cartographie des activités équestres :** visualisation des **421 installations distinctes** regroupant **1 175 équipements équestres** (`Manège`, `Carrière`, `Parcours de cross`, `Structure de tourisme équestre`, etc.) avec adresses et activités détaillées.
2. **Cartographie écologique :** superposition activable des **96 périmètres Natura 2000** normands (**82 ZSC** Directive Habitats + **14 ZPS** Directive Oiseaux).
3. **Analyse spatiale interactive :** filtres par département (`14, 27, 50, 61, 76`), tranche de distance, curseur de distance maximale en mètres, typologie écologique, site Natura 2000 ciblé, type d'équipement, activité et recherche textuelle, plus cercles visuels `500 m` / `1 000 m`.
4. **Tableau de bord, priorisation & pistes d'action :** KPIs réactifs, graphiques Plotly, tableau de priorisation exportable en CSV, fiche détaillée au clic sur la carte avec **moteur de recommandations déterministe à 3 axes** (Exposition spatiale × Typologie écologique réelle des 96 sites × Profil d'équipements Data ES).

---

## 3. Données mobilisées

- **Data ES — Recensement des équipements sportifs, espaces et sites de pratiques**  
  - Producteur : Ministère chargé des Sports (Licence Ouverte Etalab 2.0)  
  - Lien : https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques
- **Natura 2000 — Directives Habitats (`ZSC`) et Oiseaux (`ZPS`) — Normandie**  
  - Producteur : DREAL Normandie / INPN (Licence Ouverte Etalab 2.0)  
  - ZSC : https://www.data.gouv.fr/datasets/natura-2000-directive-habitats-zsc-sic-psic-normandie  
  - ZPS : https://www.data.gouv.fr/datasets/natura-2000-directives-oiseaux-zps-normandie

---

## 4. Installation et lancement en local

### Prérequis
- Python 3.10+ (testé sous Python 3.13)

### Installation des dépendances
```bash
pip install -r requirements.txt
```
*(Sous Windows si `pip` ou `streamlit` n'est pas dans le PATH, utiliser `py -m pip install -r requirements.txt`.)*

### (Optionnel) Régénérer le GeoJSON allégé pour la sobriété numérique
Le fichier optimisé `data/processed/natura2000_simplifie.geojson` est déjà fourni dans le dépôt. Pour le régénérer :
```bash
python scripts/optimize_geojson.py
```

### Lancer l'application
```bash
streamlit run app.py
# Ou sous Windows :
py -m streamlit run app.py
```

### Exécuter les tests automatisés
```bash
pytest -q
# Ou sous Windows :
py -m pytest -q
```

---

## 5. Sobriété numérique (Numérique responsable)

- **Pré-calcul spatial hors ligne (`EPSG:2154`) :** aucun calcul géométrique lourd lors de l'utilisation de l'interface.
- **Simplification topologique dédiée à l'affichage :** `natura2000_zsc_zps_normandie.geojson` (**15,79 Mio / 381 801 sommets**) a été simplifié pour la carte web en `natura2000_simplifie.geojson` (**1,03 Mio / 27 446 sommets**), soit **-93,5 % de poids fichier** et **-92,8 % de sommets** sans perte de précision sur les distances pré-calculées.
- **Moteur de règles déterministe et cache mémoire (`@st.cache_data`) :** aucune dépendance à un serveur distant ni à un modèle d'IA énergivore.

---

## 6. Structure du projet

```text
DATATHON/
├── app.py                              # Application Streamlit principale
├── requirements.txt                    # Dépendances Python
├── LICENSE                             # Licence libre MIT
├── README.md                           # Documentation projet
├── data/
│   ├── raw/                            # Fichiers pré-traités fournis par le Data Analyst
│   └── processed/                      # GeoJSON Natura 2000 allégé + métriques de sobriété
├── scripts/
│   └── optimize_geojson.py             # Script de simplification géométrique
├── src/
│   ├── data_loader.py                  # Chargement CSV/GeoJSON et agrégations
│   ├── natura_taxonomy.py              # Typologie écologique explicite des 96 sites normands
│   ├── recommendations.py              # Moteur déterministe de pistes d'action (3 axes)
│   └── map_builder.py                  # Carte interactive Folium multicouche
└── tests/
    └── test_equivigie.py               # Suite de tests Pytest
```
