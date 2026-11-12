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

SITE_TYPOLOGY_MAP: dict[str, str] = {
    "FR2200363": "vallees_cours_eau",
    "FR2300123": "vallees_cours_eau",
    "FR2300124": "vallees_cours_eau",
    "FR2300125": "vallees_cours_eau",
    "FR2300126": "vallees_cours_eau",
    "FR2300128": "vallees_cours_eau",
    "FR2300132": "vallees_cours_eau",
    "FR2300137": "vallees_cours_eau",
    "FR2300147": "vallees_cours_eau",
    "FR2300149": "vallees_cours_eau",
    "FR2300150": "vallees_cours_eau",
    "FR2300152": "vallees_cours_eau",
    "FR2302006": "vallees_cours_eau",
    "FR2302007": "vallees_cours_eau",
    "FR2302009": "vallees_cours_eau",
    "FR2302010": "vallees_cours_eau",
    "FR2500091": "vallees_cours_eau",
    "FR2500099": "vallees_cours_eau",
    "FR2500103": "vallees_cours_eau",
    "FR2500107": "vallees_cours_eau",
    "FR2500110": "vallees_cours_eau",
    "FR2500113": "vallees_cours_eau",
    "FR2500117": "vallees_cours_eau",
    "FR2500118": "vallees_cours_eau",
    "FR2500119": "vallees_cours_eau",
    "FR2502015": "vallees_cours_eau",
    "FR2312003": "vallees_cours_eau",
    "FR2300121": "marais_estuaires",
    "FR2300122": "marais_estuaires",
    "FR2300131": "marais_estuaires",
    "FR2302012": "marais_estuaires",
    "FR2500088": "marais_estuaires",
    "FR2500090": "marais_estuaires",
    "FR2500092": "marais_estuaires",
    "FR2500094": "marais_estuaires",
    "FR2310044": "marais_estuaires",
    "FR2510046": "marais_estuaires",
    "FR2510059": "marais_estuaires",
    "FR2300133": "bocages_forets_coteaux",
    "FR2300136": "bocages_forets_coteaux",
    "FR2300145": "bocages_forets_coteaux",
    "FR2300146": "bocages_forets_coteaux",
    "FR2302002": "bocages_forets_coteaux",
    "FR2500076": "bocages_forets_coteaux",
    "FR2500096": "bocages_forets_coteaux",
    "FR2500100": "bocages_forets_coteaux",
    "FR2500106": "bocages_forets_coteaux",
    "FR2500108": "bocages_forets_coteaux",
    "FR2500109": "bocages_forets_coteaux",
    "FR2502001": "bocages_forets_coteaux",
    "FR2502014": "bocages_forets_coteaux",
    "FR5200646": "bocages_forets_coteaux",
    "FR2512004": "bocages_forets_coteaux",
    "FR2300139": "littoral_dunes",
    "FR2500077": "littoral_dunes",
    "FR2500079": "littoral_dunes",
    "FR2500080": "littoral_dunes",
    "FR2500081": "littoral_dunes",
    "FR2500082": "littoral_dunes",
    "FR2500083": "littoral_dunes",
    "FR2500084": "littoral_dunes",
    "FR2500085": "littoral_dunes",
    "FR2500086": "littoral_dunes",
    "FR2502018": "littoral_dunes",
    "FR2502019": "littoral_dunes",
    "FR2502020": "littoral_dunes",
    "FR2502021": "littoral_dunes",
    "FR2502022": "littoral_dunes",
    "FR2310045": "littoral_dunes",
    "FR2510037": "littoral_dunes",
    "FR2510047": "littoral_dunes",
    "FR2510048": "littoral_dunes",
    "FR2510099": "littoral_dunes",
    "FR2512001": "littoral_dunes",
    "FR2512002": "littoral_dunes",
    "FR2512003": "littoral_dunes",
    "FR2512005": "littoral_dunes",
    "FR2302001": "cavites_chiropteres",
    "FR2302004": "cavites_chiropteres",
    "FR2302005": "cavites_chiropteres",
    "FR2302008": "cavites_chiropteres",
    "FR2302011": "cavites_chiropteres",
    "FR2502002": "cavites_chiropteres",
    "FR2502003": "cavites_chiropteres",
    "FR2502004": "cavites_chiropteres",
    "FR2502005": "cavites_chiropteres",
    "FR2502006": "cavites_chiropteres",
    "FR2502007": "cavites_chiropteres",
    "FR2502008": "cavites_chiropteres",
    "FR2502009": "cavites_chiropteres",
    "FR2502010": "cavites_chiropteres",
    "FR2502011": "cavites_chiropteres",
    "FR2502012": "cavites_chiropteres",
    "FR2502013": "cavites_chiropteres",
    "FR2502016": "cavites_chiropteres",
    "FR2502017": "cavites_chiropteres",
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
