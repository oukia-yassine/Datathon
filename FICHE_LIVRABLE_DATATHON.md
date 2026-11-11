# Fiche livrable — Datathon Normandie 2026

> Document prêt à copier/coller pour le formulaire de remise du livrable (12 novembre 2026) et support de préparation du pitch (23 novembre 2026).

---

## 1. Nom de la solution et des membres qui portent le projet

- **Nom de la solution :** **ÉquiVigie Normandie** *(provisoire — modifiable avant remise finale)*
- **Membres de l'équipe :**
  - **Youssef CHEDLY** — Développeur
  - **Yassir DOURAID** — Développeur
  - **Yassine OUKIA** — Data Analyst
  - *Pitch & présentation orale : portés collectivement par les 3 membres.*

---

## 2. Quelques mots-clés pour décrire la solution

`Filière équine` · `Natura 2000` · `Aide à la décision territoriale` · `Cartographie interactive` · `Vigilance écologique` · `Coexistence humain-nature` · `Sobriété numérique` · `Open Data Normandie`

---

## 3. Le problème auquel la solution répond

La Normandie concentre une filière équine majeure (centres équestres, poney-clubs, haras, équipements de compétition et de randonnée), souvent implantée dans des territoires à forte valeur écologique (vallées alluviales, marais, bocages, littoral, Perche).

Aujourd'hui, les collectivités et gestionnaires d'espaces naturels manquent d'un outil simple et objectif pour répondre à quatre questions concrètes :
1. **Où** sont localisées les installations équestres en Normandie ?
2. **Lesquelles** se trouvent à proximité directe ou à l'intérieur de périmètres sensibles (Natura 2000) ?
3. **Quels territoires** examiner en priorité sur le terrain ?
4. **Quelles actions** privilégier pour concilier activités équestres et préservation de la biodiversité (sans stigmatiser une filière dont les prairies entretiennent aussi les paysages ouverts) ?

---

## 4. Les cibles identifiées

- **Cible principale :** Collectivités territoriales (communes, EPCI, départements, Région), Parcs Naturels Régionaux (PNR) et animateurs / gestionnaires de sites Natura 2000.
- **Cible secondaire :** Acteurs de la filière équine normande (centres équestres, haras, Conseil des Chevaux de Normandie) souhaitant situer leurs installations dans leur contexte écologique et valoriser leurs bonnes pratiques.

---

## 5. Les bénéfices et impacts attendus

- **Priorisation rapide des diagnostics de terrain :** sur **421 installations équestres** normandes (**1 175 équipements**), ÉquiVigie identifie immédiatement les **97 installations situées à ≤ 1 km** d'un site Natura 2000 (dont **5 à l'intérieur** et **56 à 0–500 m**).
- **Dialogue territorial constructif (interactions positives & négatives) :** les pistes d'action contextualisées distinguent les atouts à valoriser (ex. maintien des prairies bocagères dans le Pays d'Auge ou le Perche, pâturage extensif des marais) des points de vigilance spécifiques au milieu (berges, zones humides, avifaune ZPS, éclairage près des gîtes à chiroptères, sentiers dunaires).
- **Outil exploitable immédiatement :** filtrage multicritère, fiche établissement au clic et export CSV prêt pour les équipes techniques des collectivités.
- **Sobriété numérique démontrée :** pré-calcul métrique hors ligne (`EPSG:2154`) et allègement des géométries cartographiques de **15,79 Mio à 1,03 Mio (-93,5 %)**.

---

## 6. Les données mobilisées (producteur et lien)

| Jeu de données | Producteur | Lien officiel | Licence |
|---|---|---|---|
| **Data ES** — Recensement des équipements sportifs, espaces et sites de pratiques | Ministère chargé des Sports | https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques | Licence Ouverte Etalab 2.0 |
| **Natura 2000 Directive « Habitats »** — ZSC, SIC, pSIC — Normandie | DREAL Normandie / INPN | https://www.data.gouv.fr/datasets/natura-2000-directive-habitats-zsc-sic-psic-normandie | Licence Ouverte Etalab 2.0 |
| **Natura 2000 Directives « Oiseaux »** — ZPS — Normandie | DREAL Normandie / INPN | https://www.data.gouv.fr/datasets/natura-2000-directives-oiseaux-zps-normandie | Licence Ouverte Etalab 2.0 |

---

## 7. Lien vers la solution / captures d'écran

- **Déploiement :** Application locale Streamlit (`py -m streamlit run app.py` / `streamlit run app.py`).
- **Captures d'écran :** *(À ajouter après lancement local de `app.py` : vue carte interactive + fiche Haras National du Pin, vue Tableau de bord & Priorisation, vue Méthodologie & Sobriété numérique)*.

---

## Bonus : Trame des 5 questions obligatoires du pitch (5 minutes)

1. **Quel est le problème ?** Les collectivités et animateurs Natura 2000 ne disposent pas d'outil unifié pour repérer où les activités équestres normandes interagissent avec les milieux sensibles, ni comment adapter le dialogue de terrain sans confondre proximité et impact négatif.
2. **Quelle est la solution ?** **ÉquiVigie Normandie**, une application cartographique d'aide à la décision qui croise 421 installations Data ES (1 175 équipements) et 96 sites Natura 2000 (82 ZSC + 14 ZPS), et propose des pistes d'action contextualisées (positives et préventives) selon la distance, la typologie écologique réelle du site et les équipements.
3. **Quels impacts ?** Cibler rapidement les 97 sites à ≤ 1 km (dont 30 dans l'Orne et 5 à l'intérieur des périmètres), orienter les diagnostics DOCOB / MAEC, valoriser les pratiques herbagères vertueuses et réduire de 93,5 % l'empreinte des couches cartographiques (sobriété numérique).
4. **Qui compose l'équipe ?** Youssef CHEDLY (Développeur), Yassir DOURAID (Développeur) et Yassine OUKIA (Data Analyst) — 3 compétences complémentaires data & développement.
5. **Quels sont les besoins pour changer d'échelle ?** Enrichir avec la Trame Verte et Bleue (SRCE Normandie), les données bocagères/haies (`DataNormandie`), le Registre Parcellaire Graphique (prairies) et co-valider les fiches d'action avec les PNR, animateurs Natura 2000 et représentants de la filière équine.
