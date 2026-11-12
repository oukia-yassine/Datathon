"""Moteur déterministe de pistes d'action territoriales — ÉquiVigie Normandie.

Croise trois axes objectifs issus des données réelles (zéro boîte noire) :
1. Exposition spatiale : classe de distance (EPSG:2154), présence à l'intérieur,
   cumul de sites à <= 1 km et double exposition ZSC + ZPS.
2. Typologie écologique réelle du ou des sites Natura 2000 concernés.
3. Profil réel des équipements et activités déclarés dans Data ES.

Chaque recommandation comporte systématiquement :
- Un volet « Coexistence & atouts à valoriser » (interactions positives) ;
- Un volet « Points de vigilance & actions de terrain » (prévention ciblée) ;
- Une justification traçable (« Pourquoi cette piste s'affiche ? »).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.natura_taxonomy import TypologyInfo, classify_natura_site


@dataclass(frozen=True)
class ActionItem:
    """Piste d'action unitaire avec sa justification traçable."""

    title: str
    detail: str
    rationale: str


@dataclass(frozen=True)
class VigilanceIndex:
    """Indicateur de Vigilance Territoriale (IVT / 100) décomposé en 4 piliers explicables."""

    score_total: float
    level_label: str
    level_color: str
    dim_distance: float
    dim_habitats: float
    dim_ecologie: float
    dim_territoire: float
    distance_detail: str
    habitats_detail: str
    ecologie_detail: str
    territoire_detail: str


@dataclass(frozen=True)
class DiagnosticResult:
    """Résultat complet de l'aide à la décision pour une installation équestre."""

    vigilance_label: str
    priority_tier: str
    priority_rank: int
    priority_color: str
    sort_index: float
    vigilance_index: VigilanceIndex
    effective_sites_1km: int
    dual_zsc_zps_1km: bool
    primary_typology: TypologyInfo
    secondary_typology: TypologyInfo | None
    equipment_tags: list[str]
    triggers_summary: list[str]
    positive_levers: list[ActionItem]
    vigilance_actions: list[ActionItem]


_TYPOLOGY_SENSITIVITY_WEIGHTS: dict[str, float] = {
    "marais_estuaires": 20.0,
    "littoral_dunes": 18.0,
    "vallees_cours_eau": 16.0,
    "cavites_chiropteres": 15.0,
    "bocages_forets_coteaux": 13.0,
}


_TYPOLOGY_RULES: dict[str, dict[str, ActionItem]] = {
    "vallees_cours_eau": {
        "positive": ActionItem(
            title="Rôle tampon des prairies permanentes en fond de vallée",
            detail=(
                "Valoriser le maintien des surfaces en herbe en bordure de cours d'eau : "
                "elles freinent l'érosion et filtrent naturellement les ruissellements par rapport à des terres labourées."
            ),
            rationale="Typologie « Vallées alluviales & cours d'eau »",
        ),
        "vigilance": ActionItem(
            title="Protection des berges et gestion des ruissellements vers le cours d'eau",
            detail=(
                "Vérifier l'éloignement des aires de fumier, le maintien d'une bande enherbée rivulaire "
                "et l'usage d'abreuvoirs aménagés hors berge afin d'éviter le piétinement des rives."
            ),
            rationale="Typologie « Vallées alluviales & cours d'eau »",
        ),
    },
    "marais_estuaires": {
        "positive": ActionItem(
            title="Entretien écologique des prairies humides par pâturage extensif",
            detail=(
                "Encourager le pâturage raisonné (faible chargement saisonnier), souvent indispensable "
                "en Normandie pour limiter l'enfrichement et conserver les habitats ouverts des marais."
            ),
            rationale="Typologie « Marais, tourbières & estuaires »",
        ),
        "vigilance": ActionItem(
            title="Portance des sols hydromorphes et sobriété sur les antiparasitaires",
            detail=(
                "Adapter l'accès aux parcelles humides en période hivernale (tassement des sols) et "
                "raisonner les traitements vermifuges afin de préserver la faune coprophage et aquatique."
            ),
            rationale="Typologie « Marais, tourbières & estuaires »",
        ),
    },
    "bocages_forets_coteaux": {
        "positive": ActionItem(
            title="Soutien actif au maillage bocager, haies et vergers traditionnels",
            detail=(
                "Valoriser les prairies pâturées comme pilier du bocage normand ; étudier les synergies "
                "avec les dispositifs MAEC ou programmes régionaux de plantation et d'entretien de haies."
            ),
            rationale="Typologie « Bocages, vergers, forêts & coteaux »",
        ),
        "vigilance": ActionItem(
            title="Préservation des lisières, vieux arbres et perméabilité des clôtures",
            detail=(
                "Veiller à préserver les arbres têtards, bandes ourlets et lisières forestières lors "
                "des travaux d'entretien, et privilégier des clôtures permettant le passage de la petite faune."
            ),
            rationale="Typologie « Bocages, vergers, forêts & coteaux »",
        ),
    },
    "littoral_dunes": {
        "positive": ActionItem(
            title="Vitrine d'un tourisme équestre côtier durable",
            detail=(
                "Associer le centre équestre à la sensibilisation des cavaliers sur la fragilité "
                "des écosystèmes littoraux et des estrans normands."
            ),
            rationale="Typologie « Littoral, baies, dunes & falaises »",
        ),
        "vigilance": ActionItem(
            title="Canalisation des cheminements hors cordons dunaires et zones de quiétude",
            detail=(
                "Vérifier que les itinéraires de sortie respectent strictement les sentiers balisés, "
                "à l'écart des dunes mobiles, falaises et zones d'estran sensibles."
            ),
            rationale="Typologie « Littoral, baies, dunes & falaises »",
        ),
    },
    "cavites_chiropteres": {
        "positive": ActionItem(
            title="Maintien de terrains de chasse nocturne pour les chiroptères",
            detail=(
                "Les prairies pâturées bordées de haies offrent des insectes et corridors de vol "
                "précieux aux chauves-souris gîtant dans les cavités et combles voisins."
            ),
            rationale="Typologie « Cavités & chiroptères »",
        ),
        "vigilance": ActionItem(
            title="Sobriété de l'éclairage nocturne et continuité des haies de vol",
            detail=(
                "Limiter et orienter vers le sol l'éclairage des carrières extérieures à la tombée de la nuit, "
                "conserver les haies reliées au gîte et raisonner les antiparasitaires (proies insectes)."
            ),
            rationale="Typologie « Cavités & chiroptères »",
        ),
    },
}


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in {"true", "1", "oui", "yes"}


def _to_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _to_int(val: Any, default: int = 0) -> int:
    try:
        return int(float(val))
    except (TypeError, ValueError):
        return default


def _detect_equipment_tags(types_equipements: str, activites: str, nb_equipements: int) -> list[str]:
    """Identifie les profils d'équipements/pratiques présents dans Data ES."""
    eq_l = (types_equipements or "").lower()
    act_l = (activites or "").lower()
    tags: list[str] = []

    if any(k in eq_l for k in ("parcours de cross", "structure de tourisme")) or any(
        k in act_l for k in ("randonnée équestre", "raid équestre", "concours complet")
    ):
        tags.append("Itinérance & plein air étendu")

    if any(k in eq_l for k in ("carrière", "piste de course", "parcours d'obstacles", "terrain de")):
        tags.append("Infrastructures extérieures fixes")

    if "manège" in eq_l and "Infrastructures extérieures fixes" not in tags:
        tags.append("Équipement couvert (manège)")

    if nb_equipements >= 4:
        tags.append(f"Pôle multi-équipements ({nb_equipements} équipements)")

    return tags or ["Équipement équestre recensé"]


def compute_vigilance_index(
    *,
    dist_m: float,
    dist_zsc_m: float,
    dist_zps_m: float,
    dans_natura: bool,
    natura_1km: bool,
    zsc_1km: bool,
    zps_1km: bool,
    effective_sites_1km: int,
    primary_typology: TypologyInfo,
    eq_tags: list[str],
    nb_eq: int,
    site_1km_count: int = 1,
    commune_inst_count: int = 1,
) -> VigilanceIndex:
    """Calcule l'Indicateur de Vigilance Territoriale (IVT / 100) selon 4 piliers explicables.

    Note : L'IVT mesure une priorité d'examen et de dialogue territorial (zéro preuve d'impact).
    """
    if dans_natura or dist_m == 0.0:
        dim_distance = 40.0
        distance_detail = "40,0 / 40 — Recouvrement direct du périmètre (0 m)"
    elif dist_m <= 500.0:
        dim_distance = round(36.0 - (dist_m / 500.0) * 10.0, 1)
        distance_detail = f"{dim_distance:.1f} / 40 — Interface rapprochée ({dist_m:.0f} m ≤ 500 m)"
    elif dist_m <= 1000.0:
        dim_distance = round(25.0 - ((dist_m - 500.0) / 500.0) * 10.0, 1)
        distance_detail = f"{dim_distance:.1f} / 40 — Proximité modérée ({dist_m:.0f} m ≤ 1 km)"
    elif dist_m <= 5000.0:
        dim_distance = round(12.0 - ((dist_m - 1000.0) / 4000.0) * 10.0, 1)
        distance_detail = f"{dim_distance:.1f} / 40 — Hors proximité immédiate ({dist_m:.0f} m)"
    else:
        dim_distance = round(max(0.0, 2.0 - ((dist_m - 5000.0) / 5000.0) * 2.0), 1)
        distance_detail = f"{dim_distance:.1f} / 40 — Éloignement important ({dist_m:.0f} m > 5 km)"

    dual_1km = zsc_1km and zps_1km
    zsc_pts = 8.0 if zsc_1km else (4.0 if dist_zsc_m <= 2000.0 else 0.0)
    zps_pts = 8.0 if zps_1km else (4.0 if dist_zps_m <= 2000.0 else 0.0)
    dual_pts = 4.0 if dual_1km else 0.0
    multi_pts = min(5.0, max(0, effective_sites_1km - 1) * 2.5)
    dim_habitats = round(min(25.0, zsc_pts + zps_pts + dual_pts + multi_pts), 1)

    hab_parts: list[str] = []
    if zsc_1km:
        hab_parts.append("ZSC ≤ 1 km (+8)")
    elif dist_zsc_m <= 2000.0:
        hab_parts.append("ZSC 1–2 km (+4)")
    if zps_1km:
        hab_parts.append("ZPS ≤ 1 km (+8)")
    elif dist_zps_m <= 2000.0:
        hab_parts.append("ZPS 1–2 km (+4)")
    if dual_1km:
        hab_parts.append("double exposition ZSC+ZPS (+4)")
    if multi_pts > 0:
        hab_parts.append(f"{effective_sites_1km} sites ≤ 1 km (+{multi_pts:.1f})")
    habitats_detail = f"{dim_habitats:.1f} / 25 — " + (", ".join(hab_parts) if hab_parts else "Aucun site ZSC/ZPS à ≤ 2 km")

    base_typ_w = _TYPOLOGY_SENSITIVITY_WEIGHTS.get(primary_typology.key, 13.0)
    expo_factor = 1.0 if dist_m <= 1000.0 else (0.6 if dist_m <= 3000.0 else 0.3)
    dim_ecologie = round(min(20.0, base_typ_w * expo_factor), 1)
    ecologie_detail = (
        f"{dim_ecologie:.1f} / 20 — {primary_typology.short_label} "
        f"(base {base_typ_w:.0f} × facteur d'exposition {expo_factor:.1f})"
    )

    equip_base = min(5.0, float(max(1, nb_eq)))
    if "Itinérance & plein air étendu" in eq_tags:
        practice_pts = 3.0
        practice_lbl = "itinérance/plein air (+3)"
    elif "Infrastructures extérieures fixes" in eq_tags:
        practice_pts = 1.5
        practice_lbl = "infrastructures extérieures (+1,5)"
    else:
        practice_pts = 0.5
        practice_lbl = "couvert/autre (+0,5)"
    equip_pts = min(8.0, equip_base + practice_pts)

    site_pressure_pts = min(4.0, max(0, site_1km_count - 1) * 0.5) if natura_1km else 0.0
    commune_density_pts = min(3.0, max(0, commune_inst_count - 1) * 1.5)
    dim_territoire = round(min(15.0, equip_pts + site_pressure_pts + commune_density_pts), 1)

    ter_parts = [f"{nb_eq} éq. & {practice_lbl}"]
    if site_pressure_pts > 0:
        ter_parts.append(f"{site_1km_count} inst. autour du site (+{site_pressure_pts:.1f})")
    if commune_density_pts > 0:
        ter_parts.append(f"{commune_inst_count} inst. dans la commune (+{commune_density_pts:.1f})")
    territoire_detail = f"{dim_territoire:.1f} / 15 — " + ", ".join(ter_parts)

    score_total = round(min(100.0, dim_distance + dim_habitats + dim_ecologie + dim_territoire), 1)

    if score_total >= 70.0:
        level_label, level_color = "Vigilance prioritaire", "#b91c1c"
    elif score_total >= 55.0:
        level_label, level_color = "Vigilance élevée", "#ea580c"
    elif score_total >= 40.0:
        level_label, level_color = "Vigilance modérée", "#ca8a04"
    else:
        level_label, level_color = "Veille courante", "#15803d"

    return VigilanceIndex(
        score_total=score_total,
        level_label=level_label,
        level_color=level_color,
        dim_distance=dim_distance,
        dim_habitats=dim_habitats,
        dim_ecologie=dim_ecologie,
        dim_territoire=dim_territoire,
        distance_detail=distance_detail,
        habitats_detail=habitats_detail,
        ecologie_detail=ecologie_detail,
        territoire_detail=territoire_detail,
    )


def build_recommendations(
    row: dict[str, Any],
    *,
    site_1km_count: int = 1,
    commune_inst_count: int = 1,
) -> DiagnosticResult:
    """Produit le diagnostic territorial complet et traçable pour une installation."""
    dist_m = _to_float(row.get("distance_natura_m"), 99999.0)
    dist_zsc_m = _to_float(row.get("distance_zsc_m"), 99999.0)
    dist_zps_m = _to_float(row.get("distance_zps_m"), 99999.0)

    dans_natura = _to_bool(row.get("dans_natura")) or dist_m == 0.0
    natura_1km = _to_bool(row.get("natura_a_1km")) or dist_m <= 1000.0
    zsc_1km = _to_bool(row.get("zsc_a_1km")) or dist_zsc_m <= 1000.0
    zps_1km = _to_bool(row.get("zps_a_1km")) or dist_zps_m <= 1000.0
    dual_1km = zsc_1km and zps_1km

    raw_sites_1km = _to_int(row.get("nombre_natura_dans_1km"), 0)
    effective_sites_1km = max(raw_sites_1km, 1 if natura_1km else 0)

    vigilance_label = str(row.get("niveau_vigilance_descriptif") or "").strip()
    if not vigilance_label:
        if dans_natura:
            vigilance_label = "À l’intérieur"
        elif dist_m <= 500:
            vigilance_label = "0–500 m"
        elif dist_m <= 1000:
            vigilance_label = "500–1000 m"
        else:
            vigilance_label = "> 1000 m"

    if dans_natura:
        priority_tier = "Priorité 1 — Interaction directe (dans le périmètre)"
        priority_rank = 1
        priority_color = "#b91c1c"
    elif dist_m <= 500:
        priority_tier = "Priorité 2 — Interface rapprochée (0–500 m)"
        priority_rank = 2
        priority_color = "#d97706"
    elif dist_m <= 1000:
        priority_tier = "Priorité 3 — Veille de proximité (500–1000 m)"
        priority_rank = 3
        priority_color = "#ca8a04"
    else:
        priority_tier = "Hors proximité immédiate (> 1000 m)"
        priority_rank = 4
        priority_color = "#15803d"

    natura_code = str(row.get("natura_plus_proche_code") or "")
    natura_nom = str(row.get("natura_plus_proche_nom") or "")
    primary_typology = classify_natura_site(natura_code, natura_nom)

    zsc_code = str(row.get("zsc_plus_proche_code") or "")
    zsc_nom = str(row.get("zsc_plus_proche_nom") or "")
    zps_code = str(row.get("zps_plus_proche_code") or "")
    zps_nom = str(row.get("zps_plus_proche_nom") or "")

    secondary_typology: TypologyInfo | None = None
    if zsc_1km and zps_1km:
        cand_code = zps_code if natura_code == zsc_code else zsc_code
        cand_nom = zps_nom if natura_code == zsc_code else zsc_nom
        cand_typ = classify_natura_site(cand_code, cand_nom)
        if cand_typ.key != primary_typology.key:
            secondary_typology = cand_typ

    types_eq = str(row.get("types_equipements") or "")
    activites = str(row.get("activites") or "")
    nb_eq = _to_int(row.get("nombre_equipements"), 1)
    eq_tags = _detect_equipment_tags(types_eq, activites, nb_eq)

    vigilance_index = compute_vigilance_index(
        dist_m=dist_m,
        dist_zsc_m=dist_zsc_m,
        dist_zps_m=dist_zps_m,
        dans_natura=dans_natura,
        natura_1km=natura_1km,
        zsc_1km=zsc_1km,
        zps_1km=zps_1km,
        effective_sites_1km=effective_sites_1km,
        primary_typology=primary_typology,
        eq_tags=eq_tags,
        nb_eq=nb_eq,
        site_1km_count=site_1km_count,
        commune_inst_count=commune_inst_count,
    )
    sort_index = vigilance_index.score_total

    triggers: list[str] = [
        f"Distance au site Natura 2000 le plus proche : {dist_m:.1f} m ({natura_code} — {natura_nom})",
        (
            f"Indicateur de Vigilance Territoriale (IVT) : {vigilance_index.score_total:.1f} % "
            f"({vigilance_index.level_label})"
        ),
    ]
    if dans_natura:
        triggers.append("Point représentatif situé à l'intérieur du périmètre Natura 2000")
    elif natura_1km:
        triggers.append(
            f"Exposition à ≤ 1 km : {effective_sites_1km} site(s) recensé(s)"
            + (" (cumul ZSC Habitats + ZPS Oiseaux)" if dual_1km else "")
        )
    triggers.append(f"Typologie du site le plus proche : {primary_typology.label}")
    if secondary_typology is not None:
        triggers.append(f"Typologie complémentaire dans 1 km : {secondary_typology.label}")
    triggers.append(f"Profil d'équipements : {', '.join(eq_tags)}")

    positive_levers: list[ActionItem] = []
    vigilance_actions: list[ActionItem] = []

    if dans_natura:
        positive_levers.append(
            ActionItem(
                title="Co-construire une convention de gestion locale (site vitrine)",
                detail=(
                    "Avec le point situé dans le périmètre Natura 2000, engager un dialogue positif "
                    "avec l'animateur du site pour valoriser les pratiques herbagères existantes (charte ou MAEC)."
                ),
                rationale="Point représentatif à l'intérieur d'un périmètre Natura 2000 (0 m)",
            )
        )
        vigilance_actions.append(
            ActionItem(
                title="Diagnostic de terrain prioritaire avec l'animateur Natura 2000",
                detail=(
                    "Vérifier sur site l'emprise réelle des parcelles, le plan d'épandage/stockage "
                    "des fumiers et la cohérence avec le Document d'Objectifs (DOCOB) du site."
                ),
                rationale="Point représentatif à l'intérieur d'un périmètre Natura 2000 (0 m)",
            )
        )
    elif dual_1km or effective_sites_1km >= 2:
        vigilance_actions.append(
            ActionItem(
                title="Coordination inter-enjeux (cumul de sites à ≤ 1 km)",
                detail=(
                    f"L'installation se situe à moins d'1 km de {effective_sites_1km} sites Natura 2000 "
                    + ("incluant ZSC et ZPS. " if dual_1km else ". ")
                    + "Privilégier une visite conjointe afin d'aligner enjeux habitats et avifaune."
                ),
                rationale=f"Cumul multi-sites dans 1 km ({effective_sites_1km} site(s))",
            )
        )

    rule_primary = _TYPOLOGY_RULES[primary_typology.key]
    if natura_1km:
        positive_levers.append(rule_primary["positive"])
        vigilance_actions.append(rule_primary["vigilance"])
        if secondary_typology is not None:
            rule_sec = _TYPOLOGY_RULES[secondary_typology.key]
            vigilance_actions.append(rule_sec["vigilance"])
    else:
        positive_levers.append(
            ActionItem(
                title="Valorisation territoriale des prairies et du maillage bocager",
                detail=(
                    f"Bien que situé à {dist_m:.0f} m de « {natura_nom} », l'établissement participe "
                    "aux continuités agro-écologiques locales (prairies, haies) hors périmètre Natura 2000."
                ),
                rationale=f"Distance > 1 000 m ({dist_m:.0f} m)",
            )
        )
        vigilance_actions.append(
            ActionItem(
                title="Veille environnementale courante (hors proximité immédiate)",
                detail=(
                    "Pas de priorité Natura 2000 immédiate identifiée à ≤ 1 km. Poursuivre les bonnes pratiques "
                    "courantes (gestion des fumiers, économie d'eau, maintien des haies locales)."
                ),
                rationale=f"Distance > 1 000 m ({dist_m:.0f} m)",
            )
        )

    if zps_1km:
        vigilance_actions.append(
            ActionItem(
                title=f"Calendrier adapté à l'avifaune (ZPS {zps_nom})",
                detail=(
                    "Prendre en compte les périodes sensibles de nidification et d'hivernage des oiseaux "
                    "(fauche tardive des bordures, taille des haies hors printemps, limitation du dérangement)."
                ),
                rationale=f"Site ZPS Directive Oiseaux à {dist_zps_m:.1f} m",
            )
        )

    if natura_1km:
        if "Itinérance & plein air étendu" in eq_tags:
            vigilance_actions.append(
                ActionItem(
                    title="Balisage et concertation sur les itinéraires de randonnée / cross",
                    detail=(
                        "Vérifier le tracé des sorties équestres (randonnée, endurance, cross) par rapport aux "
                        "sentiers autorisés et traversées sensibles du site Natura 2000."
                    ),
                    rationale=f"Présence d'équipements/activités d'itinérance ({types_eq})",
                )
            )
        if "Infrastructures extérieures fixes" in eq_tags and primary_typology.key != "cavites_chiropteres":
            vigilance_actions.append(
                ActionItem(
                    title="Gestion des eaux pluviales sur carrières et pistes extérieures",
                    detail=(
                        "Contrôler le drainage des surfaces travaillées (sable/sol stabilisé) et l'absence "
                        "d'entraînement de sédiments vers les fossés et milieux humides voisins."
                    ),
                    rationale=f"Présence d'infrastructures extérieures fixes ({types_eq})",
                )
            )
        if nb_eq >= 4:
            positive_levers.append(
                ActionItem(
                    title="Potentiel d'établissement pilote à l'échelle de l'EPCI",
                    detail=(
                        f"Avec {nb_eq} équipements recensés, cette structure dispose d'une forte visibilité "
                        "pour expérimenter une démarche type label environnemental équin (ex. EquuRES)."
                    ),
                    rationale=f"Structure multi-équipements ({nb_eq} équipements recensés)",
                )
            )

    return DiagnosticResult(
        vigilance_label=vigilance_label,
        priority_tier=priority_tier,
        priority_rank=priority_rank,
        priority_color=priority_color,
        sort_index=sort_index,
        vigilance_index=vigilance_index,
        effective_sites_1km=effective_sites_1km,
        dual_zsc_zps_1km=dual_1km,
        primary_typology=primary_typology,
        secondary_typology=secondary_typology,
        equipment_tags=eq_tags,
        triggers_summary=triggers,
        positive_levers=positive_levers,
        vigilance_actions=vigilance_actions,
    )
