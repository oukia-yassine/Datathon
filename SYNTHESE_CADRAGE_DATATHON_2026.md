# Synthèse de cadrage — Projet Datathon Normandie 2026

> **Document de partage et d'alignement d'équipe** (généré le 11 novembre 2026)  
> **Thématique officielle :** « Biodiversité et activités humaines » (4ᵉ édition du Datathon Normandie)  
> **Nom provisoire de la solution :** **ÉquiVigie Normandie** *(à confirmer)*  
> **Périmètre géographique :** Normandie (Calvados `14`, Eure `27`, Manche `50`, Orne `61`, Seine-Maritime `76`)

---

## 1. Cadre officiel, échéances et exigences du jury

### Calendrier critique
- **Lancement :** 12 octobre 2026.
- **Remise du livrable technique :** **jeudi 12 novembre 2026 à 12h00** *(source : slide 14 du support officiel `Lancement_Datathon2026`)*.
- **Cérémonie de clôture & jury :** **lundi 23 novembre 2026 à partir de 17h00** à l'Hôtel de Région de Rouen.
- **Format de soutenance :** 5 minutes de pitch (1 à 2 présentateurs) + 5 minutes de questions/réponses (toute l'équipe), devant répondre à **5 questions obligatoires** :
  1. Quel est le problème ?
  2. Quelle est la solution ?
  3. Quels impacts ?
  4. Qui compose l'équipe ?
  5. Quels sont les besoins pour changer d'échelle ?

### Critères d'évaluation du jury
1. Pertinence du projet avec les thématiques du Datathon.
2. Originalité du projet (méthodes de traitement et de valorisation des données).
3. Caractère innovant de la solution.
4. **Prise en compte de la dimension de numérique responsable / sobriété numérique.**
5. Faisabilité du projet (MVP fonctionnel et démontrable).
6. Qualité de la présentation orale.

### Contraintes réglementaires clés
- **Données ouvertes exclusivement (Open Data)** issues de producteurs régionaux, nationaux ou européens.
- **Solutions libres de droit** (article 7 du règlement) : le code produit doit être accompagné d'une licence open source (voir section 6). Les participants conservent la propriété intellectuelle de leur projet (article 10).
- **Aucune donnée à caractère personnel** (article 9).
- **Déploiement choisi pour la remise :** déploiement local fonctionnel et reproductible + captures d'écran + documentation + fiche projet.

---

## 2. Positionnement retenu : de *ÉquiBiodiv* (Gemini) à *ÉquiVigie* (ChatGPT)

### Pourquoi nous avons écarté l'approche initiale (Gemini)
L'idée de départ (*ÉquiBiodiv Normandie*) proposait de croiser la base **SIRE (IFCE)** avec ODIN et la Trame Verte et Bleue pour attribuer un « score d'impact / compatibilité écologique » (vert / orange / rouge). Cette approche présentait deux faiblesses majeures devant des experts :
1. **Limite des données SIRE publiques :** le fichier public SIRE décrit des équidés individuels (race, sexe, robe, naissance), sans géolocalisation directe des établissements ni effectifs par parcelle.
2. **Raccourci scientifique attaquable :** la proximité géographique d'une activité équine avec un espace naturel ne prouve **aucune dégradation écologique**. Au contraire, les prairies pâturées de façon raisonnée contribuent souvent au maintien de paysages ouverts et du bocage normand.

### Le positionnement retenu (*ÉquiVigie Normandie*)
Nous développons une **plateforme cartographique d'aide à la décision et de vigilance territoriale** pour identifier les **proximités et interactions potentielles** entre les établissements équestres et les milieux naturels sensibles (Natura 2000) en Normandie.

- **Problème adressé :** les collectivités territoriales (EPCI, communes), les Parcs Naturels Régionaux (PNR) et les animateurs Natura 2000 manquent d'une vue consolidée pour savoir **où** les activités équestres se situent à proximité de sites sensibles, **quels territoires examiner en priorité** sur le terrain et **quelles bonnes pratiques valoriser ou recommander**.
- **Cibles identifiées :**
  - **Cible prioritaire :** collectivités territoriales, EPCI, animateurs de sites Natura 2000, PNR et acteurs publics de l'aménagement/biodiversité.
  - **Cible secondaire :** acteurs de la filière équine (centres équestres, haras, Conseil des Chevaux de Normandie) souhaitant situer leur contexte écologique et valoriser leurs pratiques durables.
- **Alignement avec les deux problématiques officielles du Datathon (slide 9) :**
  - *Priorisation territoriale :* repérer les secteurs de proximité/chevauchement pour orienter les diagnostics.
  - *Interactions humain-nature :* montrer les interactions **positives ET négatives** à travers des indicateurs transparents et des pistes d'action contextualisées.

---

## 3. Bilan des données déjà traitées et vérifiées

Le traitement géospatial amont a déjà été réalisé en **Lambert-93 (`EPSG:2154`)** (calculs métriques exacts) à partir de deux sources officielles et réexporté en `EPSG:4326` pour la cartographie.

### Sources mobilisées
1. **Data ES — Recensement des équipements sportifs, espaces et sites de pratiques**  
   - *Producteur :* Ministère chargé des Sports.  
   - *Lien :* https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques (et https://equipements.sports.gouv.fr/explore/dataset/data-es/).  
   - *Filtrage effectué :* départements `14, 27, 50, 61, 76` et famille officielle `Equipement équestre`.
2. **Natura 2000 Normandie (ZSC + ZPS)**  
   - *Producteur :* DREAL Normandie / réseau INPN.  
   - *Liens :*  
     - Directives « Habitats » (ZSC / SIC / pSIC) — Normandie : https://www.data.gouv.fr/datasets/natura-2000-directive-habitats-zsc-sic-psic-normandie  
     - Directives « Oiseaux » (ZPS) — Normandie : https://www.data.gouv.fr/datasets/natura-2000-directives-oiseaux-zps-normandie

### Chiffres clés vérifiés sur les fichiers traités
- **1 175 équipements équestres** individuels (carrières, manèges, parcours de cross, pistes de course, structures de tourisme équestre…) regroupés en **421 installations distinctes** (`inst_numero`), afin de ne pas compter plusieurs fois un même centre équestre.
- **96 sites Natura 2000 normands :** **82 ZSC** (Directive Habitats) + **14 ZPS** (Directive Oiseaux).
- **Répartition des 421 installations par département :**
  - Calvados (`14`) : **105** installations (dont **9** à ≤ 1 km d'un site Natura 2000)
  - Eure (`27`) : **86** installations (dont **20** à ≤ 1 km)
  - Manche (`50`) : **74** installations (dont **20** à ≤ 1 km)
  - Orne (`61`) : **67** installations (dont **30** à ≤ 1 km, soit ~45 % !)
  - Seine-Maritime (`76`) : **89** installations (dont **18** à ≤ 1 km)
- **Répartition par classe de distance au site Natura 2000 le plus proche (sans double comptage ZSC/ZPS) :**
  - **`À l’intérieur` (0 m) :** **5 installations** *(toutes situées dans l'Orne, dont le Haras National du Pin dans `FR2502014 Bocages et vergers du sud Pays d'Auge`, ainsi que des installations dans `FR2512004 Forêts et étangs du Perche`)*.
  - **`0–500 m` :** **56 installations**.
  - **`500–1000 m` :** **36 installations**.
  - **Total à ≤ 1 km :** **97 installations** (~23 % des installations normandes).
  - **`> 1000 m` :** **324 installations**.

### Choix de format : CSV vs GeoJSON
Les deux formats ont des rôles complémentaires dans l'application :
- **`GeoJSON`** pour la **carte interactive** :
  - `installations_proximite_natura2000.geojson` (`461 Ko`, 421 points avec attributs).
  - `natura2000_zsc_zps_normandie.geojson` (`16,56 Mo` actuellement, 96 polygones ZSC/ZPS — **à simplifier pour l'affichage cartographique**, voir section 5).
- **`CSV`** pour les **KPIs, filtres, classements, graphiques et fiches détaillées** :
  - `installations_proximite_natura2000.csv` (lecture rapide par `pandas`).
  - CSV détaillé des **1 175 équipements** (`equipements_equestres_normandie.csv`), indispensable pour afficher dans la fiche d'une installation son **adresse postale (`inst_adresse`, `inst_cp`)**, la **liste précise de ses équipements** et leur date de mise à jour (`equip_maj_date`).

### Limites méthodologiques assumées (à présenter en toute transparence)
1. **Proximité ≠ impact causal :** un niveau de vigilance signale une coïncidence spatiale nécessitant une visite ou un échange de terrain, jamais une preuve de dégradation.
2. **Périmètre Data ES :** recense les équipements sportifs déclarés ; ne couvre pas exhaustivement les élevages/haras privés sans équipement sportif et ne contient pas le nombre de chevaux.
3. **Centroïde d'installation :** la position d'une installation est la moyenne des coordonnées de ses équipements, et non le contour exact de ses parcelles ou pâtures.
4. **Périmètre écologique V1 :** Natura 2000 (ZSC + ZPS) est un socle officiel robuste mais ne couvre pas d'autres zonages (ZNIEFF, corridors SRCE, zones humides hors Natura 2000).

---

## 4. Cœur de la solution : le moteur de pistes d'action contextualisées

Pour éviter des conseils génériques et rendre chaque fiche **logique, spécifique et défendable devant le jury**, le moteur de recommandation est **100 % déterministe et transparent** (zéro boîte noire). Il croise **trois dimensions réelles** présentes dans nos fichiers :

### Axe A — Exposition spatiale (priorisation)
- `À l’intérieur` (`0 m`) → **Priorité 1 : Diagnostic / valorisation directe recommandée**
- `0–500 m` → **Priorité 2 : Vigilance d'interface directe**
- `500–1000 m` → **Priorité 3 : Veille territoriale & zone tampon**
- `> 1000 m` → **Hors proximité immédiate : Valorisation des bonnes pratiques générales**
- **Modulateurs issus des données :** cumul de sites à ≤ 1 km (`nombre_natura_dans_1km`, jusqu'à 4 sites pour certaines zones littorales/estuariennes) et double exposition simultanée **ZSC + ZPS** (`zsc_a_1km` et `zps_a_1km`).

### Axe B — Typologie écologique réelle des 96 sites Natura 2000 normands
Chaque site Natura 2000 concerné est rattaché à sa typologie réelle (identifiée sur les 96 sites normands) et à sa directive (`ZSC` Habitats / `ZPS` Oiseaux), avec systématiquement **un volet positif (coexistence à valoriser)** et **un volet vigilance (actions préventives à vérifier)** :

1. **Vallées alluviales, cours d'eau & bassins** *(ex. `Haute vallée de l'Orne et affluents`, `Risle, Guiel, Charentonne`, `Vallée de l'Eure`, `Bassin de l'Arques`)*
   - *Vigilance :* maîtrise des ruissellements depuis les carrières extérieures et aires de fumier vers le cours d'eau (bandes enherbées tampons), aménagement d'abreuvoirs hors berge pour éviter le piétinement et l'érosion des rives.
   - *Positif :* maintien de prairies permanentes en fond de vallée jouant un rôle de filtre naturel contre le ruissellement.
2. **Marais, tourbières & estuaires** *(ex. `Marais du Cotentin et du Bessin - Baie des Veys`, `Pays de Bray humide`, `Estuaire et marais de la Basse Seine`, `Marais Vernier`)*
   - *Vigilance :* respect de la portance des sols hydromorphes (adapter la charge en période hivernale), attention aux traitements antiparasitaires équestres (certains vermifuges impactent la faune coprophage et aquatique), maîtrise des apports azotés.
   - *Positif :* le pâturage extensif raisonné empêche l'enfrichement et maintient les prairies humides ouvertes nécessaires aux espèces patrimoniales.
3. **Bocages, vergers & forêts** *(ex. `Forêts et étangs du Perche` — 11 installations à ≤ 1 km ; `Bocages et vergers du sud Pays d'Auge` — incluant le Haras National du Pin)*
   - *Vigilance :* préservation des haies bocagères, lisières et vieux arbres (arbres têtards/vergers) lors de l'entretien des pistes et clôtures ; maintien de clôtures perméables à la petite faune.
   - *Positif :* rôle historique de la filière équine dans le maintien du bocage et des prairies permanentes (éligibilité / synergie possible avec des MAEC et des programmes de plantation de haies).
4. **Littoral, baies, dunes & landes** *(ex. `Baie du Mont Saint Michel`, `Littoral Cauchois`, `Landes et dunes de la Hague`, `Littoral augeron`)*
   - *Vigilance :* canalisation des itinéraires de promenade/randonnée hors cordons dunaires mobiles et zones d'estran sensibles, respect des zones de quiétude littorales.
   - *Positif :* valorisation d'un tourisme équestre encadré et sensibilisation des cavaliers à la préservation du trait de côte.
5. **Cavités, anciennes carrières & combles à chiroptères** *(ex. `Combles de la chapelle de l'Oratoire de Passais`, `Anciennes carrières de Beaufour-Druval`)*
   - *Vigilance :* les enjeux majeurs ne sont pas le piétinement mais l'éclairage nocturne des carrières extérieures près des lisières, la préservation des haies (corridors de vol) et la gestion raisonnée des vermifuges (maintien des insectes coprophages, proies des chauves-souris).
   - *Positif :* les prairies pâturées bordées de haies constituent des terrains de chasse favorables aux chiroptères.
6. **Directive Oiseaux — ZPS** *(ex. `Forêts et étangs du Perche`, `Basses Vallées du Cotentin`, `Estuaire de l'Orne`)*
   - *Vigilance :* adaptation du calendrier des interventions bruyantes ou mécaniques (fauche, entretien des pistes, broyage des haies) hors période sensible de nidification et d'hivernage.

### Axe C — Profil réel des équipements et activités (`Data ES`)
Les pistes sont affinées selon les équipements de l'installation :
- **Pratiques d'itinérance / plein air étendu** (`Randonnée équestre`, `Raid équestre d'endurance`, `Structure de tourisme équestre`, `Parcours de cross`) → focus sur le balisage des tracés, les traversées de cours d'eau et le dérangement hors sentiers.
- **Équipements extérieurs fixes** (`Carrière`, `Carrière de dressage/rond de longe`, `Piste de course sur le plat`) → focus sur le drainage/ruissellement des eaux pluviales, le stockage des fumiers et la sobriété d'éclairage nocturne.
- **Équipements couverts uniquement** (`Manège` seul) → enjeux principalement liés aux abords (gestion des fumiers, eaux de toiture, paddocks attenants si présents).
- **Grandes structures** (`nombre_equipements >= 4`) → potentiel d'action « vitrine » ou d'accompagnement structurant à l'échelle intercommunale (ex. démarches qualité environnementale de la filière équine).

### Argumentaire clé pour le jury
> *« Notre moteur de pistes d'action s'appuie uniquement sur trois réalités mesurables : la distance métrique calculée, la typologie écologique réelle du site Natura 2000 concerné (ZSC/ZPS) et les équipements déclarés dans Data ES. Nous ne jugeons pas la filière équine : nous donnons aux collectivités et animateurs Natura 2000 une grille objective pour savoir par où commencer le dialogue de terrain, prévenir les risques ciblés et valoriser les pratiques favorables au bocage et aux prairies. »*

---

## 5. Architecture de l'application MVP, les 4 fonctionnalités & sobriété numérique

### Les 4 fonctionnalités structurant l'application (alignées sur la proposition ChatGPT)
1. **Cartographie des activités équestres :** visualisation des 421 installations sur la carte de Normandie + consultation du détail des 1 175 équipements associés (types, activités, adresse).
2. **Cartographie écologique :** affichage des 96 périmètres Natura 2000 normands avec distinction visuelle et couches activables séparément (**82 ZSC Habitats** / **14 ZPS Oiseaux**).
3. **Analyse spatiale interactive :** filtres croisés par département (`14, 27, 50, 61, 76`), classe de proximité / seuil de distance, type d'équipement ou activité, recherche par commune/nom ou site Natura 2000, et affichage visuel des zones tampons (`500 m` / `1 km`) autour d'une installation sélectionnée.
4. **Tableau de bord, priorisation & recommandations :**
   - KPIs dynamiques (installations filtrées, part à ≤ 1 km, à l'intérieur, distance médiane).
   - Graphiques interactifs (répartition par département, par tranche de distance, top sites Natura 2000 les plus proches d'installations).
   - Classement des installations/communes prioritaires avec **export CSV**.
   - **Fiche détaillée au clic** sur une installation : indicateurs explicables + **pistes d'action contextualisées (volet positif + volet vigilance)**.
   - Onglet dédié **Méthodologie, Sources, Limites & Sobriété numérique**.

### Stack technique retenue (déploiement local)
- **Python 3.13** + **Streamlit** (interface web interactive)
- **Folium** + **streamlit-folium** (carte interactive à couches + sélection au clic)
- **Plotly** (graphiques interactifs)
- **Pandas** (filtrage et agrégation rapide sur CSV)
- **Shapely** (uniquement en pré-traitement hors-ligne pour alléger le GeoJSON d'affichage)

### Démarche concrète de « Sobriété numérique » (critère évalué par le jury)
1. **Pré-calcul géospatial hors-ligne (zéro recalcul dans l'app) :** toutes les distances et intersections `EPSG:2154` sont déjà pré-calculées en amont ; l'interface lit et met en cache (`@st.cache_data`) des données légères, sans base de données serveur permanente ni modèle d'IA lourd.
2. **Simplification géométrique dédiée à l'affichage web :** le fichier brut `natura2000_zsc_zps_normandie.geojson` pèse **`16,56 Mo`** en raison de la finesse des polygones d'origine. Nous conservons les distances exactes issues des géométries complètes, mais nous générons une version simplifiée topologiquement (`simplify`) uniquement pour l'affichage carte, réduisant son poids de **~85 à 90 %** (chargement fluide, faible empreinte mémoire et CPU).
3. **Règles métiers déterministes :** aucune requête API externe lourde ni inférence GPU à l'exécution (l'app fonctionne localement de façon sobre et autonome).

---

## 6. Licences & conformité règlement

- **Code source (article 7 du règlement — « solutions libres de droit ») :** ajout d'un fichier `LICENSE` open source standard (recommandé : **licence MIT**, simple et permissive, garantissant la réutilisation libre tout en conservant la paternité de l'équipe).
- **Données ouvertes utilisées :** Data ES (Ministère des Sports) et Natura 2000 (DREAL Normandie / INPN) sont diffusées sous **Licence Ouverte / Etalab 2.0**, réutilisables librement avec mention explicite des producteurs, titres et URLs dans l'application et la documentation.
- **Données personnelles (article 9) :** aucune donnée personnelle identifiante n'est exploitée (uniquement des équipements publics/sportifs et des zonages environnementaux officiels).

---

## 7. Points restant à valider avant de lancer le code

1. **Verrouillage du périmètre V1 :** on reste bien uniquement sur **Data ES + Natura 2000 (ZSC + ZPS)** déjà traités afin de sécuriser un MVP complet et testé avant **demain 12 novembre à 12h** ?
2. **Validation du moteur de pistes d'action (section 4) :** la logique à 3 axes (Exposition × Typologie écologique réelle × Équipements) avec double volet (Positif + Vigilance) est-elle validée ?
3. **Validation de la stack (section 5) :** accord pour **Streamlit + Folium + Plotly + simplification du GeoJSON de 16,56 Mo** en déploiement local ?
4. **Identité projet pour la fiche livrable et l'interface :**
   - Nom définitif de la solution (garder **`ÉquiVigie Normandie`** ou autre nom ?).
   - Noms/prénoms et rôles des **3 membres de l'équipe** à inscrire dans l'onglet *À propos*, le `README.md` et la fiche de remise.
