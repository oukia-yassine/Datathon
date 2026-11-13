# ÉquiVigie Normandie

**Datathon Normandie 2026 — « Biodiversité et activités humaines »**  
*Plateforme cartographique d'aide à la décision territoriale pour analyser les proximités et interactions entre installations équestres et sites Natura 2000 en Normandie.*

- **Équipe :** Youssef CHEDLY (Développeur), Yassir DOURAID (Développeur), Yassine OUKIA (Data Analyst)
- **Dépôt GitHub :** https://github.com/oukia-yassine/Datathon.git
- **Licence du code :** MIT ([LICENSE](LICENSE)) — conforme à l'article 7 du règlement du Datathon Normandie 2026

---

## 1. Problématique & positionnement

La filière équine est un marqueur identitaire fort de la Normandie. Toutefois, la simple proximité géographique d'une activité équine avec un espace naturel protégé **ne prouve aucun impact négatif** : selon les pratiques et la nature des milieux, les prairies pâturées peuvent au contraire contribuer au maintien des paysages ouverts, des prairies humides et du bocage.

**ÉquiVigie Normandie** écarte le piège d'un « score d'impact » non démontré et propose aux **collectivités, EPCI, Parcs Naturels Régionaux, animateurs Natura 2000 et acteurs de la filière** un outil transparent de **vigilance territoriale** pour :
1. Localiser les activités équestres normandes (`Data ES`) et les sites Natura 2000 (`ZSC` Habitats & `ZPS` Oiseaux).
2. Mesurer objectivement les distances réelles en mètres (`EPSG:2154`) entre chaque établissement et les périmètres protégés.
3. Hiérarchiser les visites et diagnostics de terrain grâce à l'**Indicateur de Vigilance Territoriale (IVT sur 100)** décomposé en 4 piliers explicables.
4. Générer des **pistes d'action contextualisées** (**interactions positives à valoriser** et **points de vigilance à vérifier**).

---

## 2. Les 4 fonctionnalités de l'application et chiffres clés

1. **Cartographie des activités équestres :** visualisation des **421 installations distinctes** regroupant **1 175 équipements équestres** (`Carrière` : 543, `Manège` : 386, `Carrière de dressage/rond de longe` : 110, `Parcours de cross` : 45, `Parcours d'obstacles` : 34, `Piste de course sur le plat` : 32, `Structure de tourisme équestre` : 20, etc.) répartis sur **352 communes équipées** en Normandie.
2. **Cartographie écologique :** superposition activable des **96 périmètres Natura 2000** normands (**82 ZSC** Directive Habitats + **14 ZPS** Directive Oiseaux), classés en **5 typologies écologiques de milieux** (*Vallées & cours d'eau*, *Marais & zones humides*, *Bocages, forêts & coteaux*, *Littoral & dunes*, *Cavités & chiroptères*).
3. **Analyse spatiale interactive :**
   - **97 installations situées à ≤ 1 km** d'un site Natura 2000 (**23,0 %**), dont **5 à l'intérieur (`0 m`)** toutes situées dans l'Orne, **56 entre 0 et 500 m** et **36 entre 500 et 1 000 m** ; **324 installations à > 1 km** (**77,0 %**). Distance médiane régionale : **3 434 m**.
   - Filtres réactifs par département (`14, 27, 50, 61, 76`), tranche de proximité, niveau IVT, typologie écologique, seuil de distance en mètres, site Natura 2000 le plus proche, type d'équipement, activité et recherche textuelle, avec rayons visuels de `500 m` et `1 km`.
4. **Indicateur de Vigilance Territoriale (IVT), tableau de bord & pistes d'action :**
   - **Formule IVT (0 à 100, moyenne régionale 27,4 %) :** somme de 4 piliers transparents :
     - **Distance écologique (sur 40)**
     - **Proximité des habitats ZSC/ZPS et cumul (sur 25)**
     - **Contexte écologique du milieu (sur 20)**
     - **Contexte territorial et équipements (sur 15)**
   - **Répartition régionale par niveau IVT :** **22** installations en *Vigilance prioritaire* (`≥ 70 %`, max `84,6 %`), **51** en *Vigilance élevée* (`55–69,9 %`), **24** en *Vigilance modérée* (`40–54,9 %`) et **324** en *Veille courante* (`< 40 %`, regroupant 100 % des installations situées au-delà de 1 km, sécurisé par plafonnement à `39,9` hors rayon de 1 km).
   - **6 graphiques Plotly**, synthèse départementale, liste de priorisation exportable en CSV et fiche diagnostic au clic avec traçabilité complète des règles déclenchées.

---

## 3. Données mobilisées (Open Data — Licence Etalab 2.0)

- **Data ES — Recensement des équipements sportifs, espaces et sites de pratiques**  
  - Producteur : Ministère chargé des Sports (mises à jour d'équipements jusqu'au `2026-10-16`)  
  - Lien : https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques
- **Natura 2000 — Directives Habitats (`ZSC`) et Oiseaux (`ZPS`) — Normandie**  
  - Producteur : DREAL Normandie / INPN  
  - ZSC : https://www.data.gouv.fr/datasets/natura-2000-directive-habitats-zsc-sic-psic-normandie  
  - ZPS : https://www.data.gouv.fr/datasets/natura-2000-directives-oiseaux-zps-normandie

---

## 4. Installation, lancement et tests en local

### Prérequis
- **Python 3.10 ou plus récent** (projet testé sous Python 3.13).
- Une connexion Internet pour installer les dépendances la première fois.
- Les fichiers de données inclus dans `data/` (déjà présents dans cette archive).

### Linux (Ubuntu / Debian)

**1. Installer Python et les outils nécessaires** (si besoin) :

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
python3 --version
```

**2. Récupérer le projet** (choisir une seule méthode) :

```bash
# Méthode A : cloner le dépôt GitHub
git clone https://github.com/oukia-yassine/Datathon.git
cd Datathon
```

Ou extraire le fichier ZIP téléchargé et ouvrir un terminal dans le dossier `DATATHON` contenant `app.py` :

```bash
# Méthode B : après extraction de l'archive, adapter le chemin si nécessaire
cd ~/Téléchargements/DATATHON
# Sur un système configuré en anglais : cd ~/Downloads/DATATHON
```

**3. Créer et activer un environnement virtuel** :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**4. Installer les dépendances** :

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**5. Lancer ÉquiVigie** :

```bash
python -m streamlit run app.py
```

Ouvrir **http://localhost:8501** si le navigateur ne s'ouvre pas automatiquement. Pour arrêter le serveur : `Ctrl+C` dans le terminal.

**6. Exécuter les tests et l'audit de fiabilité** (facultatif) :

```bash
python -m pytest -v
python scripts/verify_reliability.py
```

Pour quitter l'environnement virtuel : `deactivate`. Lors des lancements suivants, il suffit de revenir dans le dossier du projet, d'exécuter `source .venv/bin/activate`, puis `python -m streamlit run app.py`.

> **Dépannage :** si `python3 -m venv .venv` indique que `ensurepip` est absent, installer le paquet `python3-venv` correspondant à la version de Python. Si le port `8501` est occupé, utiliser `python -m streamlit run app.py --server.port 8502` puis ouvrir http://localhost:8502.

### Windows (PowerShell)

Dans le dossier du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Tests et audit :

```powershell
python -m pytest -v
python scripts/verify_reliability.py
```

Si PowerShell bloque l'activation de l'environnement virtuel, il est aussi possible de lancer directement `.\.venv\Scripts\python.exe -m streamlit run app.py` après installation des dépendances avec cet interpréteur.

---

## 5. Structure du projet

```text
DATATHON/
├── app.py                              # Application Streamlit principale (3 onglets, thèmes clair/sombre)
├── requirements.txt                    # Dépendances Python
├── LICENSE                             # Licence libre MIT
├── README.md                           # Documentation générale du projet
├── data/
│   ├── raw/                            # Données brutes et pré-traitées (CSV + GeoJSON exact)
│   └── processed/                      # GeoJSON Natura 2000 allégé et métriques de sobriété
├── scripts/
│   ├── optimize_geojson.py             # Script de simplification géométrique reproductible
│   └── verify_reliability.py           # Audit indépendant EPSG:2154, 4 piliers IVT, invariance et sensibilité
├── src/
│   ├── data_loader.py                  # Chargement CSV/GeoJSON, calcul IVT et agrégations
│   ├── natura_taxonomy.py              # Classification explicite des 96 sites en 5 typologies
│   ├── recommendations.py              # Calcul IVT (4 piliers) et moteur déterministe de pistes d'action
│   ├── map_builder.py                  # Carte interactive Folium multicouche
│   └── ui_components.py                # Composants HTML/CSS et visualisations
└── tests/
    └── test_equivigie.py               # Suite de 7 tests automatisés Pytest (données, IVT, carte, UI)
```
