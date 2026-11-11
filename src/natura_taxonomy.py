"""Typologie écologique des 96 sites Natura 2000 normands (82 ZSC + 14 ZPS).

Chaque site officiel (SITECODE) présent dans ``natura2000_zsc_zps_normandie.geojson``
est rattaché à une typologie écologique explicite afin d'ancrer les pistes
d'action dans les caractéristiques réelles du milieu concerné (sans boîte noire).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TypologyInfo:
    """Description structurée d'une typologie écologique Natura 2000."""

    key: str
    label: str
    short_label: str
    badge_color: str
    description: str


TYPOLOGIES: dict[str, TypologyInfo] = {
    "vallees_cours_eau": TypologyInfo(
        key="vallees_cours_eau",
        label="Vallées alluviales, cours d'eau & bassins",
        short_label="Vallées & cours d'eau",
        badge_color="#0284c7",
        description=(
            "Milieux rivulaires et bassins versants sensibles au ruissellement, "
            "à l'érosion des berges et à la qualité hydrobiologique."
        ),
    ),
    "marais_estuaires": TypologyInfo(
        key="marais_estuaires",
        label="Marais, tourbières, étangs & estuaires",
        short_label="Marais & zones humides",
        badge_color="#0d9488",
        description=(
            "Zones humides et estuariennes où l'équilibre entre portance des sols, "
            "pâturage extensif et qualité de l'eau est déterminant."
        ),
    ),
    "bocages_forets_coteaux": TypologyInfo(
        key="bocages_forets_coteaux",
        label="Bocages, vergers, forêts & coteaux",
        short_label="Bocages, forêts & coteaux",
        badge_color="#15803d",
        description=(
            "Paysages agro-forestiers, prairies bocagères et pelouses calcaires dont "
            "l'ouverture et le maillage de haies dépendent d'une gestion adaptée."
        ),
    ),
    "littoral_dunes": TypologyInfo(
        key="littoral_dunes",
        label="Littoral, baies, dunes & falaises",
        short_label="Littoral & dunes",
        badge_color="#2563eb",
        description=(
            "Espaces côtiers, cordons dunaires et estrans vulnérables au piétinement, "
            "à l'érosion mécanique et au dérangement de la faune littorale."
        ),
    ),
    "cavites_chiropteres": TypologyInfo(
        key="cavites_chiropteres",
        label="Cavités, anciennes carrières & combles (Chiroptères)",
        short_label="Cavités & chiroptères",
        badge_color="#7c3aed",
        description=(
            "Gîtes souterrains ou bâtis de chauves-souris sensibles à l'éclairage "
            "nocturne, aux ruptures de haies (corridors de chasse) et aux antiparasitaires."
        ),
    ),
}

# Mapping explicite des 96 SITECODE officiels de DREAL Normandie (82 ZSC + 14 ZPS)
SITE_TYPOLOGY_MAP: dict[str, str] = {
    # --- Vallées alluviales, cours d'eau & bassins ---
    "FR2200363": "vallees_cours_eau",  # Vallée de la Bresle
    "FR2300123": "vallees_cours_eau",  # Boucles de la Seine Aval
    "FR2300124": "vallees_cours_eau",  # Boucles de la Seine Amont, Coteaux de Saint-Adrien
    "FR2300125": "vallees_cours_eau",  # Boucles de la Seine Amont, Coteaux d'Orival
    "FR2300126": "vallees_cours_eau",  # Boucles de la Seine Amont d'Amfreville à Gaillon
    "FR2300128": "vallees_cours_eau",  # Vallée de l'Eure
    "FR2300132": "vallees_cours_eau",  # Bassin de l'Arques
    "FR2300137": "vallees_cours_eau",  # L'Yères
    "FR2300147": "vallees_cours_eau",  # Val Eglantier
    "FR2300149": "vallees_cours_eau",  # Corbie
    "FR2300150": "vallees_cours_eau",  # Risle, Guiel, Charentonne
    "FR2300152": "vallees_cours_eau",  # Vallée de l'Epte
    "FR2302006": "vallees_cours_eau",  # Iles et berges de la Seine en Seine-Maritime
    "FR2302007": "vallees_cours_eau",  # Iles et berges de la Seine dans l'Eure
    "FR2302009": "vallees_cours_eau",  # Le Haut Bassin de la Calonne
    "FR2302010": "vallees_cours_eau",  # La Vallée de l'Iton au lieu-dit Le Hom
    "FR2500091": "vallees_cours_eau",  # Vallée de l'Orne et ses affluents
    "FR2500099": "vallees_cours_eau",  # Haute vallée de l'Orne et affluents
    "FR2500103": "vallees_cours_eau",  # Haute Vallée de la Touques et affluents
    "FR2500107": "vallees_cours_eau",  # Haute Vallée de la Sarthe
    "FR2500110": "vallees_cours_eau",  # Vallée de la Sée
    "FR2500113": "vallees_cours_eau",  # Bassin de l'Airou
    "FR2500117": "vallees_cours_eau",  # Bassin de la Souleuvre
    "FR2500118": "vallees_cours_eau",  # Bassin de la Druance
    "FR2500119": "vallees_cours_eau",  # Bassin de l'Andainette
    "FR2502015": "vallees_cours_eau",  # Vallée du Sarthon et affluents
    "FR2312003": "vallees_cours_eau",  # Terrasses alluviales de la Seine (ZPS)
    # --- Marais, tourbières, étangs & estuaires ---
    "FR2300121": "marais_estuaires",  # Estuaire de la Seine
    "FR2300122": "marais_estuaires",  # Marais Vernier, Risle Maritime
    "FR2300131": "marais_estuaires",  # Pays de Bray humide
    "FR2302012": "marais_estuaires",  # Les étangs et mares des forêts de Breteuil et Conches
    "FR2500088": "marais_estuaires",  # Marais du Cotentin et du Bessin - Baie des Veys
    "FR2500090": "marais_estuaires",  # Marais arrière-littoraux du Bessin
    "FR2500092": "marais_estuaires",  # Marais du Grand Hazé
    "FR2500094": "marais_estuaires",  # Marais alcalin de Chicheboville-Bellengreville
    "FR2310044": "marais_estuaires",  # Estuaire et marais de la Basse Seine (ZPS)
    "FR2510046": "marais_estuaires",  # Basses Vallées du Cotentin et Baie des Veys (ZPS)
    "FR2510059": "marais_estuaires",  # Estuaire de l'Orne (ZPS)
    # --- Bocages, vergers, forêts & coteaux ---
    "FR2300133": "bocages_forets_coteaux",  # Pays de Bray - Cuestas Nord et Sud
    "FR2300136": "bocages_forets_coteaux",  # La forêt d'Eu et les pelouses adjacentes
    "FR2300145": "bocages_forets_coteaux",  # Forêt de Lyons
    "FR2300146": "bocages_forets_coteaux",  # Bois de la Roquette
    "FR2302002": "bocages_forets_coteaux",  # Forêt d'Eawy
    "FR2500076": "bocages_forets_coteaux",  # Landes du Tertre Bizet et Fosse Arthour
    "FR2500096": "bocages_forets_coteaux",  # Monts d'Eraines
    "FR2500100": "bocages_forets_coteaux",  # Sites d'Ecouves
    "FR2500106": "bocages_forets_coteaux",  # Forêts, étangs et tourbières du Haut-Perche
    "FR2500108": "bocages_forets_coteaux",  # Bois et coteaux à l'ouest de Mortagne-au-Perche
    "FR2500109": "bocages_forets_coteaux",  # Bois et coteaux calcaires sous Bellême
    "FR2502001": "bocages_forets_coteaux",  # Hêtraie de Cerisy
    "FR2502014": "bocages_forets_coteaux",  # Bocages et vergers du sud Pays d'Auge
    "FR5200646": "bocages_forets_coteaux",  # Alpes Mancelles
    "FR2512004": "bocages_forets_coteaux",  # Forêts et étangs du Perche (ZPS)
    # --- Littoral, baies, dunes & falaises ---
    "FR2300139": "littoral_dunes",  # Littoral Cauchois
    "FR2500077": "littoral_dunes",  # Baie du mont Saint-Michel
    "FR2500079": "littoral_dunes",  # Chausey
    "FR2500080": "littoral_dunes",  # Littoral Ouest du Cotentin de Bréhal à Pirou
    "FR2500081": "littoral_dunes",  # Havre de Saint-Germain-sur-Ay et Landes de Lessay
    "FR2500082": "littoral_dunes",  # Littoral ouest du Cotentin de Saint-Germain-sur-Ay au Rozel
    "FR2500083": "littoral_dunes",  # Massif dunaire de Héauville à Vauville
    "FR2500084": "littoral_dunes",  # Récifs et landes de la Hague
    "FR2500085": "littoral_dunes",  # Récifs et marais arrière-littoraux du Cap Lévi à la Pointe de Saire
    "FR2500086": "littoral_dunes",  # Tatihou - Saint-Vaast-la-Hougue
    "FR2502018": "littoral_dunes",  # Banc et récifs de Surtainville
    "FR2502019": "littoral_dunes",  # Anse de Vauville
    "FR2502020": "littoral_dunes",  # Baie de Seine occidentale
    "FR2502021": "littoral_dunes",  # Baie de Seine orientale
    "FR2502022": "littoral_dunes",  # Nord Bretagne DH
    "FR2310045": "littoral_dunes",  # Littoral Seino-Marin (ZPS)
    "FR2510037": "littoral_dunes",  # Chausey (ZPS)
    "FR2510047": "littoral_dunes",  # Baie de Seine occidentale (ZPS)
    "FR2510048": "littoral_dunes",  # Baie du Mont Saint Michel (ZPS)
    "FR2510099": "littoral_dunes",  # Falaise du Bessin Occidental (ZPS)
    "FR2512001": "littoral_dunes",  # Littoral augeron (ZPS)
    "FR2512002": "littoral_dunes",  # Landes et dunes de la Hague (ZPS)
    "FR2512003": "littoral_dunes",  # Havre de la Sienne (ZPS)
    "FR2512005": "littoral_dunes",  # Nord Bretagne DO (ZPS)
    # --- Cavités, anciennes carrières & combles (Chiroptères) ---
    "FR2302001": "cavites_chiropteres",  # réseau de cavités du nord-ouest de la Seine-Maritime
    "FR2302004": "cavites_chiropteres",  # les cavités de Beaumont-le-Roger
    "FR2302005": "cavites_chiropteres",  # L'Abbaye de Jumièges
    "FR2302008": "cavites_chiropteres",  # Les grottes du Mont Roberge
    "FR2302011": "cavites_chiropteres",  # les cavités de Tillières-sur-Avre
    "FR2502002": "cavites_chiropteres",  # Carrière de Loisail
    "FR2502003": "cavites_chiropteres",  # Carrière de la Mansonnière
    "FR2502004": "cavites_chiropteres",  # Anciennes carrières de la vallée de la Mue
    "FR2502005": "cavites_chiropteres",  # Anciennes carrières de Beaufour-Druval
    "FR2502006": "cavites_chiropteres",  # Ancienne carrière de la Cressonnière
    "FR2502007": "cavites_chiropteres",  # Anciennes carrières d'Orbec
    "FR2502008": "cavites_chiropteres",  # Ancienne champignonnière des Petites Hayes
    "FR2502009": "cavites_chiropteres",  # Anciennes mines de Barenton et de Bion
    "FR2502010": "cavites_chiropteres",  # Anciennes carrières souterraines d'Habloville
    "FR2502011": "cavites_chiropteres",  # Combles de la chapelle de l'Oratoire de Passais
    "FR2502012": "cavites_chiropteres",  # Coteaux calcaires et anciennes carrières de La Meauffe, Cavigny et Airel
    "FR2502013": "cavites_chiropteres",  # Ancienne carrière souterraine de Saint-Pierre-Canivet
    "FR2502016": "cavites_chiropteres",  # Combles de l'église de Burcy
    "FR2502017": "cavites_chiropteres",  # Combles de l'église d'Amayé-sur-Orne
}


def classify_natura_site(site_code: str, site_name: str = "") -> TypologyInfo:
    """Retourne la typologie écologique d'un site Natura 2000 normand.

    Priorité au référentiel explicite par ``SITECODE`` ; repli lexical uniquement
    si un code inédit était rencontré.
    """
    code = (site_code or "").strip().upper()
    if code in SITE_TYPOLOGY_MAP:
        return TYPOLOGIES[SITE_TYPOLOGY_MAP[code]]

    name_l = (site_name or "").lower()
    if any(k in name_l for k in ("carrière", "cavité", "grotte", "mine", "comble", "champignonnière", "abbaye")):
        return TYPOLOGIES["cavites_chiropteres"]
    if any(k in name_l for k in ("marais", "estuaire", "tourbière", "étang", "humide")):
        return TYPOLOGIES["marais_estuaires"]
    if any(k in name_l for k in ("littoral", "baie", "dune", "falaise", "récif", "havre", "chausey", "tatihou")):
        return TYPOLOGIES["littoral_dunes"]
    if any(k in name_l for k in ("vallée", "bassin", "rivière", "risle", "orne", "eure", "seine", "sarthe", "touques", "arques")):
        return TYPOLOGIES["vallees_cours_eau"]
    return TYPOLOGIES["bocages_forets_coteaux"]
