"""Chargement et enrichissement métier des données pré-traitées d'ÉquiVigie Normandie."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from src.recommendations import DiagnosticResult, build_recommendations


VIGILANCE_ORDER: list[str] = [
    "À l’intérieur",
    "0–500 m",
    "500–1000 m",
    "> 1000 m",
]

VIGILANCE_COLORS: dict[str, str] = {
    "À l’intérieur": "#b91c1c",
    "0–500 m": "#ea580c",
    "500–1000 m": "#ca8a04",
    "> 1000 m": "#15803d",
}

IVT_ORDER: list[str] = [
    "Vigilance prioritaire",
    "Vigilance élevée",
    "Vigilance modérée",
    "Veille courante",
]

IVT_COLORS: dict[str, str] = {
    "Vigilance prioritaire": "#b91c1c",
    "Vigilance élevée": "#ea580c",
    "Vigilance modérée": "#ca8a04",
    "Veille courante": "#15803d",
}


def _clean_bool_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().isin({"true", "1", "oui", "yes"})


def load_equipments(csv_path: Path) -> pd.DataFrame:
    """Charge la table des 1 175 équipements équestres Data ES en Normandie."""
    df = pd.read_csv(
        csv_path,
        dtype={
            "equip_numero": str,
            "inst_numero": str,
            "dep_code": str,
            "inst_cp": str,
        },
        encoding="utf-8-sig",
    )
    for col in ("inst_adresse", "inst_cp", "activites", "nom_equipement", "type_equipement", "equip_maj_date"):
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    return df


def load_installations(
    installations_csv: Path,
    equipments_df: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, dict[str, DiagnosticResult]]:
    """Charge les 421 installations analysées et calcule leurs diagnostics contextualisés."""
    df = pd.read_csv(
        installations_csv,
        dtype={
            "inst_numero": str,
            "departement_code": str,
            "zsc_plus_proche_code": str,
            "zps_plus_proche_code": str,
            "natura_plus_proche_code": str,
        },
        encoding="utf-8-sig",
    )

    for col in ("distance_zsc_m", "distance_zps_m", "distance_natura_m", "longitude", "latitude"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ("nombre_equipements", "nombre_zsc_dans_1km", "nombre_zps_dans_1km", "nombre_natura_dans_1km"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    for col in ("dans_zsc", "zsc_a_1km", "dans_zps", "zps_a_1km", "dans_natura", "natura_a_1km"):
        df[col] = _clean_bool_series(df[col])

    if equipments_df is not None and not equipments_df.empty:
        eq_meta = (
            equipments_df.groupby("inst_numero", as_index=False)
            .agg(
                inst_adresse=("inst_adresse", lambda s: next((v for v in s if v), "")),
                inst_cp=("inst_cp", lambda s: next((v for v in s if v), "")),
                equip_maj_max=("equip_maj_date", "max"),
            )
        )
        df = df.merge(eq_meta, on="inst_numero", how="left")
    else:
        df["inst_adresse"] = ""
        df["inst_cp"] = ""
        df["equip_maj_max"] = ""

    df["inst_adresse"] = df["inst_adresse"].fillna("")
    df["inst_cp"] = df["inst_cp"].fillna("")
    df["equip_maj_max"] = df["equip_maj_max"].fillna("")

    commune_counts: Counter[str] = Counter(df["commune"].fillna("").astype(str).str.strip())
    site_1km_counts: Counter[str] = Counter()
    for _, r in df[df["natura_a_1km"]].iterrows():
        zsc_c = str(r.get("zsc_plus_proche_code") or "").strip()
        zps_c = str(r.get("zps_plus_proche_code") or "").strip()
        if r["zsc_a_1km"] and zsc_c:
            site_1km_counts[zsc_c] += 1
        if r["zps_a_1km"] and zps_c:
            site_1km_counts[zps_c] += 1

    diagnostics: dict[str, DiagnosticResult] = {}
    records = df.to_dict(orient="records")
    typology_keys: list[str] = []
    typology_labels: list[str] = []
    typology_shorts: list[str] = []
    priority_ranks: list[int] = []
    priority_tiers: list[str] = []
    sort_indices: list[float] = []
    ivt_scores: list[float] = []
    ivt_niveaux: list[str] = []
    ivt_distances: list[float] = []
    ivt_habitats: list[float] = []
    ivt_ecologies: list[float] = []
    ivt_territoires: list[float] = []
    eff_sites_1km: list[int] = []
    dual_flags: list[bool] = []
    eq_profiles: list[str] = []
    comm_inst_counts: list[int] = []
    site_inst_counts: list[int] = []

    for rec in records:
        comm_name = str(rec.get("commune") or "").strip()
        nat_code = str(rec.get("natura_plus_proche_code") or "").strip()
        comm_cnt = max(1, int(commune_counts.get(comm_name, 1)))
        site_cnt = max(1 if rec.get("natura_a_1km") else 0, int(site_1km_counts.get(nat_code, 0)))

        diag = build_recommendations(
            rec,
            site_1km_count=max(1, site_cnt),
            commune_inst_count=comm_cnt,
        )
        diagnostics[rec["inst_numero"]] = diag
        typology_keys.append(diag.primary_typology.key)
        typology_labels.append(diag.primary_typology.label)
        typology_shorts.append(diag.primary_typology.short_label)
        priority_ranks.append(diag.priority_rank)
        priority_tiers.append(diag.priority_tier)
        sort_indices.append(diag.sort_index)
        ivt_scores.append(diag.vigilance_index.score_total)
        ivt_niveaux.append(diag.vigilance_index.level_label)
        ivt_distances.append(diag.vigilance_index.dim_distance)
        ivt_habitats.append(diag.vigilance_index.dim_habitats)
        ivt_ecologies.append(diag.vigilance_index.dim_ecologie)
        ivt_territoires.append(diag.vigilance_index.dim_territoire)
        eff_sites_1km.append(diag.effective_sites_1km)
        dual_flags.append(diag.dual_zsc_zps_1km)
        eq_profiles.append("; ".join(diag.equipment_tags))
        comm_inst_counts.append(comm_cnt)
        site_inst_counts.append(site_cnt)

    df["typologie_key"] = typology_keys
    df["typologie_label"] = typology_labels
    df["typologie_short"] = typology_shorts
    df["priorite_rang"] = priority_ranks
    df["priorite_label"] = priority_tiers
    df["indice_priorisation"] = sort_indices
    df["ivt_score"] = ivt_scores
    df["ivt_niveau"] = ivt_niveaux
    df["ivt_distance"] = ivt_distances
    df["ivt_habitats"] = ivt_habitats
    df["ivt_ecologie"] = ivt_ecologies
    df["ivt_territoire"] = ivt_territoires
    df["sites_1km_effectifs"] = eff_sites_1km
    df["double_expo_zsc_zps"] = dual_flags
    df["profil_equipements"] = eq_profiles
    df["commune_installations"] = comm_inst_counts
    df["site_proche_installations_1km"] = site_inst_counts

    return df, diagnostics


def load_natura_geojson(geojson_path: Path, installations_df: pd.DataFrame) -> dict[str, Any]:
    """Charge les polygones Natura 2000 allégés et y associe le comptage d'installations proches."""
    data = json.loads(geojson_path.read_text(encoding="utf-8"))

    from src.natura_taxonomy import classify_natura_site

    close_df = installations_df[installations_df["natura_a_1km"]]
    counts_by_code: Counter[str] = Counter()
    for _, row in close_df.iterrows():
        if row["zsc_a_1km"] and row["zsc_plus_proche_code"]:
            counts_by_code[str(row["zsc_plus_proche_code"])] += 1
        if row["zps_a_1km"] and row["zps_plus_proche_code"]:
            counts_by_code[str(row["zps_plus_proche_code"])] += 1

    for feat in data.get("features", []):
        props = feat.setdefault("properties", {})
        code = str(props.get("SITECODE", ""))
        name = str(props.get("SITENAME", ""))
        typ = classify_natura_site(code, name)
        props["typologie_label"] = typ.short_label
        props["directive_label"] = (
            "ZSC — Directive Habitats" if props.get("type_zone") == "ZSC" else "ZPS — Directive Oiseaux"
        )
        props["installations_proches_1km"] = int(counts_by_code.get(code, 0))

    return data


def load_sobriete_metrics(metrics_path: Path) -> dict[str, Any]:
    """Charge les métriques chiffrées d'allègement du GeoJSON."""
    if not metrics_path.exists():
        return {}
    return json.loads(metrics_path.read_text(encoding="utf-8"))


def split_semicolon_values(series: pd.Series) -> list[str]:
    """Extrait les valeurs uniques triées d'une colonne séparée par ';'."""
    vals: set[str] = set()
    for item in series.dropna().astype(str):
        for part in item.split(";"):
            cleaned = part.strip()
            if cleaned:
                vals.add(cleaned)
    return sorted(vals)


def split_activity_values(series: pd.Series) -> list[str]:
    """Extrait les activités uniques triées (séparateurs ';' et ',')."""
    vals: set[str] = set()
    for item in series.dropna().astype(str):
        for chunk in item.split(";"):
            for act in chunk.split(","):
                cleaned = act.strip()
                if cleaned:
                    vals.add(cleaned)
    return sorted(vals)


def compute_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Agrège les indicateurs clés par département normand."""
    if df.empty:
        return pd.DataFrame(
            columns=[
                "departement_code",
                "departement",
                "installations",
                "equipements",
                "dans_natura",
                "a_1km_ou_moins",
                "part_1km_pct",
                "distance_mediane_m",
                "ivt_moyen",
            ]
        )
    agg_dict: dict[str, tuple[str, str]] = {
        "installations": ("inst_numero", "nunique"),
        "equipements": ("nombre_equipements", "sum"),
        "dans_natura": ("dans_natura", "sum"),
        "a_1km_ou_moins": ("natura_a_1km", "sum"),
        "distance_mediane_m": ("distance_natura_m", "median"),
    }
    if "ivt_score" in df.columns:
        agg_dict["ivt_moyen"] = ("ivt_score", "mean")

    grp = (
        df.groupby(["departement_code", "departement"], as_index=False)
        .agg(**agg_dict)
        .sort_values("departement_code")
    )
    grp["part_1km_pct"] = (grp["a_1km_ou_moins"] / grp["installations"] * 100.0).round(1)
    grp["distance_mediane_m"] = grp["distance_mediane_m"].round(1)
    if "ivt_moyen" in grp.columns:
        grp["ivt_moyen"] = grp["ivt_moyen"].round(1)
    else:
        grp["ivt_moyen"] = 0.0
    return grp


def compute_natura_hotspots(df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    """Identifie les sites Natura 2000 comptant le plus d'installations à <= 1 km."""
    from src.natura_taxonomy import classify_natura_site

    rows: list[dict[str, Any]] = []
    for _, r in df.iterrows():
        if r["zsc_a_1km"]:
            rows.append(
                {
                    "code": r["zsc_plus_proche_code"],
                    "site": r["zsc_plus_proche_nom"],
                    "directive": "ZSC (Habitats)",
                    "inst_numero": r["inst_numero"],
                }
            )
        if r["zps_a_1km"]:
            rows.append(
                {
                    "code": r["zps_plus_proche_code"],
                    "site": r["zps_plus_proche_nom"],
                    "directive": "ZPS (Oiseaux)",
                    "inst_numero": r["inst_numero"],
                }
            )
    if not rows:
        return pd.DataFrame(columns=["code", "site", "directive", "typologie", "nb_installations"])

    hot = (
        pd.DataFrame(rows)
        .groupby(["code", "site", "directive"], as_index=False)
        .agg(nb_installations=("inst_numero", "nunique"))
        .sort_values(["nb_installations", "site"], ascending=[False, True])
        .head(top_n)
    )
    hot["typologie"] = [
        classify_natura_site(c, s).short_label for c, s in zip(hot["code"], hot["site"])
    ]
    return hot
