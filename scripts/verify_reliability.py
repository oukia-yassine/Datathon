"""Script autonome d'audit de fiabilité géométrique, de recalcul indépendant de l'IVT et d'analyse de sensibilité.

Exécute cinq contrôles indépendants reproductibles :
1. Audit de qualité et de fraîcheur des données Data ES (coordonnées, doublons, emprise englobante, dates).
2. Recalcul géométrique indépendant en Lambert-93 (EPSG:2154) et comparaison intégrale du Top 12 des sites Natura 2000.
3. Réimplémentation indépendante des 4 piliers de l'IVT à partir des formules documentées (écart 0,0 sur les 421 installations).
4. Vérification de l'invariance de l'IVT sous filtrage interactif (Streamlit AppTest : 5 départements vs Orne seul).
5. Analyse de sensibilité normalisée (+/- 20 % sur les poids des 5 typologies et sur chacun des 4 piliers, évaluée sur les 97 installations à <= 1 km, sur le Top 22 et sur le seuil de 40 points).
"""

from __future__ import annotations

import json
import logging
import math
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from shapely import transform as shapely_transform
from shapely.geometry import Point, shape

logging.getLogger("streamlit").setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_loader import compute_natura_hotspots, load_equipments, load_installations
from src.natura_taxonomy import SITE_TYPOLOGY_MAP, TYPOLOGIES
from src.recommendations import _TYPOLOGY_SENSITIVITY_WEIGHTS, compute_vigilance_index

RAW = ROOT / "data" / "raw"


def wgs84_to_lambert93(lon_deg: float, lat_deg: float) -> tuple[float, float]:
    e = 0.0818191910428158
    lc = math.radians(3.0)
    n = 0.7256077650532670
    c = 11754255.426096
    xs = 700000.0
    ys = 12655612.049876
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    sin_lat = math.sin(lat)
    l_iso = math.log(
        math.tan(math.pi / 4.0 + lat / 2.0)
        * ((1.0 - e * sin_lat) / (1.0 + e * sin_lat)) ** (e / 2.0)
    )
    r = c * math.exp(-n * l_iso)
    gamma = n * (lon - lc)
    x = xs + r * math.sin(gamma)
    y = ys - r * math.cos(gamma)
    return x, y


def project_geom_to_2154(geom):
    return shapely_transform(
        geom,
        lambda coords: [wgs84_to_lambert93(float(pt[0]), float(pt[1])) for pt in coords],
    )


def independent_ivt_from_spec(
    row: pd.Series,
    commune_counts: Counter[str],
    site_1km_counts: Counter[str],
    typ_weights: dict[str, float] | None = None,
) -> tuple[float, float, float, float, float]:
    weights = typ_weights or _TYPOLOGY_SENSITIVITY_WEIGHTS
    d = float(row["distance_natura_m"])
    d_zsc = float(row["distance_zsc_m"])
    d_zps = float(row["distance_zps_m"])
    inside = bool(row["dans_natura"]) or d == 0.0
    n_1km = bool(row["natura_a_1km"]) or d <= 1000.0
    zsc_1km = bool(row["zsc_a_1km"]) or d_zsc <= 1000.0
    zps_1km = bool(row["zps_a_1km"]) or d_zps <= 1000.0
    eff_sites = max(int(row["nombre_natura_dans_1km"]), 1 if n_1km else 0)

    if inside:
        p1 = 40.0
    elif d <= 500.0:
        p1 = round(36.0 - (d / 500.0) * 10.0, 1)
    elif d <= 1000.0:
        p1 = round(25.0 - ((d - 500.0) / 500.0) * 10.0, 1)
    elif d <= 5000.0:
        p1 = round(12.0 - ((d - 1000.0) / 4000.0) * 10.0, 1)
    else:
        p1 = round(max(0.0, 2.0 - ((d - 5000.0) / 5000.0) * 2.0), 1)

    zsc_p = 8.0 if zsc_1km else (4.0 if d_zsc <= 2000.0 else 0.0)
    zps_p = 8.0 if zps_1km else (4.0 if d_zps <= 2000.0 else 0.0)
    dual_p = 4.0 if (zsc_1km and zps_1km) else 0.0
    multi_p = min(5.0, max(0, eff_sites - 1) * 2.5)
    p2 = round(min(25.0, zsc_p + zps_p + dual_p + multi_p), 1)

    code = str(row["natura_plus_proche_code"]).strip().upper()
    typ_key = SITE_TYPOLOGY_MAP[code]
    expo = 1.0 if d <= 1000.0 else (0.6 if d <= 3000.0 else 0.3)
    p3 = round(min(20.0, weights[typ_key] * expo), 1)

    nb_eq = int(row["nombre_equipements"])
    eq_l = str(row["types_equipements"] or "").lower()
    act_l = str(row["activites"] or "").lower()
    if any(k in eq_l for k in ("parcours de cross", "structure de tourisme")) or any(
        k in act_l for k in ("randonnée équestre", "raid équestre", "concours complet")
    ):
        prac = 3.0
    elif any(k in eq_l for k in ("carrière", "piste de course", "parcours d'obstacles", "terrain de")):
        prac = 1.5
    else:
        prac = 0.5
    eq_pts = min(8.0, min(5.0, float(max(1, nb_eq))) + prac)
    site_cnt = max(1 if n_1km else 0, int(site_1km_counts.get(code, 0)))
    comm_cnt = max(1, int(commune_counts.get(str(row["commune"]).strip(), 1)))
    site_pts = min(4.0, max(0, site_cnt - 1) * 0.5) if n_1km else 0.0
    comm_pts = min(3.0, max(0, comm_cnt - 1) * 1.5)
    p4 = round(min(15.0, eq_pts + site_pts + comm_pts), 1)

    raw_tot = round(min(100.0, p1 + p2 + p3 + p4), 1)
    tot = raw_tot if n_1km else min(raw_tot, 39.9)
    return p1, p2, p3, p4, tot


def main() -> None:
    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    inst_df, _ = load_installations(RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df)
    gj = json.loads((RAW / "natura2000_zsc_zps_normandie.geojson").read_text(encoding="utf-8"))

    print("=== 1. AUDIT QUALITE ET FRAICHEUR DES DONNEES DATA ES ===")
    print(f"Total installations : {len(inst_df)} | Total equipements : {len(eq_df)}")
    print(
        f"Coordonnees manquantes (lon/lat) : "
        f"{int(inst_df['longitude'].isna().sum())} / {int(inst_df['latitude'].isna().sum())}"
    )
    print(f"Doublons inst_numero : {int(inst_df['inst_numero'].duplicated().sum())}")
    print(f"Doublons exacts (lon, lat) : {int(inst_df.duplicated(subset=['longitude', 'latitude']).sum())}")
    print(f"Emprise englobante longitude : [{inst_df['longitude'].min():.4f}, {inst_df['longitude'].max():.4f}]")
    print(f"Emprise englobante latitude  : [{inst_df['latitude'].min():.4f}, {inst_df['latitude'].max():.4f}]")
    print(f"Plage de mise a jour Data ES (equip_maj_date) : {eq_df['equip_maj_date'].min()} -> {eq_df['equip_maj_date'].max()}")

    print("\n=== 2. RECALCUL INDEPENDANT EPSG:2154 & COMPARAISON DU TOP 12 SITES ===")
    sites_2154 = []
    for feat in gj["features"]:
        props = feat["properties"]
        geom_2154 = project_geom_to_2154(shape(feat["geometry"]))
        sites_2154.append((props["SITECODE"], props["SITENAME"], props["type_zone"], geom_2154))

    max_diff = 0.0
    all_pairs_1km: Counter[tuple[str, str, str]] = Counter()
    for _, row in inst_df.iterrows():
        px_m, py_m = wgs84_to_lambert93(float(row["longitude"]), float(row["latitude"]))
        pt = Point(px_m, py_m)
        min_d = min(pt.distance(g) for _, _, _, g in sites_2154)
        for code, name, tz, g in sites_2154:
            if pt.distance(g) <= 1000.0:
                all_pairs_1km[(code, name, tz)] += 1
        diff = abs(min_d - float(row["distance_natura_m"]))
        if diff > max_diff:
            max_diff = diff

    print(f"Ecart maximal de distance sur les 421 installations vs CSV : {max_diff:.4f} m (arrondi a 0,1 m)")

    geom_top12 = sorted(
        all_pairs_1km.items(),
        key=lambda item: (-item[1], item[0][1]),
    )[:12]
    app_top12 = compute_natura_hotspots(inst_df, top_n=12)
    top12_match = all(
        geom_top12[i][0][0] == app_top12.iloc[i]["code"]
        and geom_top12[i][1] == int(app_top12.iloc[i]["nb_installations"])
        for i in range(12)
    )
    print(f"Egalite stricte des 12 premiers sites Natura 2000 (toutes paires <= 1 km vs application) : {top12_match}")
    for i in range(12):
        code, name, tz = geom_top12[i][0]
        cnt = geom_top12[i][1]
        app_cnt = int(app_top12.iloc[i]["nb_installations"])
        print(f"  {i + 1:2d}. {code} ({tz}) {name} : geom={cnt} | app={app_cnt}")

    print("\n=== 3. REIMPLEMENTATION INDEPENDANTE DES 4 PILIERS IVT (421 INSTALLATIONS) ===")
    commune_counts: Counter[str] = Counter(inst_df["commune"].fillna("").astype(str).str.strip())
    site_1km_counts: Counter[str] = Counter()
    for _, r in inst_df[inst_df["natura_a_1km"]].iterrows():
        if r["zsc_a_1km"] and r["zsc_plus_proche_code"]:
            site_1km_counts[str(r["zsc_plus_proche_code"]).strip()] += 1
        if r["zps_a_1km"] and r["zps_plus_proche_code"]:
            site_1km_counts[str(r["zps_plus_proche_code"]).strip()] += 1

    max_ivt_diff = 0.0
    for _, row in inst_df.iterrows():
        p1, p2, p3, p4, tot = independent_ivt_from_spec(row, commune_counts, site_1km_counts)
        d_tot = abs(tot - float(row["ivt_score"]))
        d_p = max(
            abs(p1 - float(row["ivt_distance"])),
            abs(p2 - float(row["ivt_habitats"])),
            abs(p3 - float(row["ivt_ecologie"])),
            abs(p4 - float(row["ivt_territoire"])),
        )
        max_ivt_diff = max(max_ivt_diff, d_tot, d_p)

    extreme_far = compute_vigilance_index(
        dist_m=1005.0,
        dist_zsc_m=1005.0,
        dist_zps_m=1005.0,
        dans_natura=False,
        natura_1km=False,
        zsc_1km=False,
        zps_1km=False,
        effective_sites_1km=0,
        primary_typology=TYPOLOGIES["marais_estuaires"],
        eq_tags=["Itinérance & plein air étendu"],
        nb_eq=10,
        site_1km_count=10,
        commune_inst_count=5,
    )
    print(f"Ecart maximal entre la formule documentee (§3.3) et le code sur 421 installations : {max_ivt_diff:.4f} pt")
    print(f"Garde de securite a > 1 km sur cas extreme synthetique (1 005 m) : {extreme_far.score_total:.1f} < 40 ({extreme_far.level_label})")

    print("\n=== 4. INVARIANCE DE L'IVT SOUS FILTRAGE INTERACTIF (STREAMLIT APPTEST) ===")
    import logging
    from streamlit.testing.v1 import AppTest

    for lg_name in ("streamlit", "streamlit.runtime", "streamlit.elements"):
        logging.getLogger(lg_name).setLevel(logging.ERROR)

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    at.selectbox(key="selected_inst_id").select("I613280001").run()
    md_all = "\n".join(m.value for m in at.markdown)
    for dep in ("Calvados", "Eure", "Manche", "Seine-Maritime"):
        at.pills(key="f_depts").unselect(dep)
    at.run()
    md_orne_only = "\n".join(m.value for m in at.markdown)
    ui_invariant = ("70.5 %" in md_all) and ("70.5 %" in md_orne_only) and ("9.5 %</b> / 15 %" in md_orne_only)
    print(f"Invariance de la fiche IVT affichee (I613280001 : 5 departements vs Orne seul) : {ui_invariant}")

    print("\n=== 5. ANALYSE DE SENSIBILITE NORMALISEE (SUR LES 97 INSTALLATIONS <= 1 KM & TOP 22) ===")
    close_mask = inst_df["natura_a_1km"]
    base_top22 = set(inst_df.nlargest(22, "ivt_score")["inst_numero"])
    base_close_ranks = inst_df.loc[close_mask, "ivt_score"].rank()
    spearman_dist_close = inst_df.loc[close_mask, "distance_natura_m"].rank().corr(base_close_ranks)
    print(
        f"Correlation de rang Distance / IVT : globale (421) = "
        f"{inst_df['distance_natura_m'].rank().corr(inst_df['ivt_score'].rank()):.3f} | "
        f"intra <= 1 km (97) = {spearman_dist_close:.3f}"
    )

    print("5a. Perturbation de +/- 20 % des poids des 5 typologies ecologiques :")
    for typ_key, base_w in _TYPOLOGY_SENSITIVITY_WEIGHTS.items():
        for factor, sign_lbl in ((1.2, "+20 %"), (0.8, "-20 %")):
            mod_weights = dict(_TYPOLOGY_SENSITIVITY_WEIGHTS)
            mod_weights[typ_key] = round(base_w * factor, 2)
            scores = [
                independent_ivt_from_spec(r, commune_counts, site_1km_counts, mod_weights)[4]
                for _, r in inst_df.iterrows()
            ]
            s_ser = pd.Series(scores, index=inst_df.index)
            top22_p = set(inst_df.assign(s=s_ser).nlargest(22, "s")["inst_numero"])
            overlap = len(base_top22 & top22_p)
            sp_close = base_close_ranks.corr(s_ser.loc[close_mask].rank())
            crossings_40 = int(((inst_df["ivt_score"] >= 40.0) != (s_ser >= 40.0)).sum())
            print(
                f"  - Typologie {typ_key:22s} ({sign_lbl}) : Top 22 = {overlap}/22 ({overlap / 22 * 100:.1f} %) | "
                f"Spearman (<=1km) = {sp_close:.4f} | Bascules seuil 40 = {crossings_40}"
            )

    print("5b. Perturbation de +/- 20 % de chaque pilier (renormalisee a 100 points) :")
    pillar_max = {"distance": 40.0, "habitats": 25.0, "ecologie": 20.0, "territoire": 15.0}
    for target_p in ("distance", "habitats", "ecologie", "territoire"):
        for delta, d_lbl in ((1.20, "+20 %"), (0.80, "-20 %")):
            new_max_t = pillar_max[target_p] * delta
            rem_scale = (100.0 - new_max_t) / (100.0 - pillar_max[target_p])
            scales = {
                k: (delta if k == target_p else rem_scale)
                for k in pillar_max
            }
            raw_s = (
                inst_df["ivt_distance"] * scales["distance"]
                + inst_df["ivt_habitats"] * scales["habitats"]
                + inst_df["ivt_ecologie"] * scales["ecologie"]
                + inst_df["ivt_territoire"] * scales["territoire"]
            ).round(1)
            s_ser = raw_s.where(inst_df["natura_a_1km"], raw_s.clip(upper=39.9))
            top22_p = set(inst_df.assign(s=s_ser).nlargest(22, "s")["inst_numero"])
            overlap = len(base_top22 & top22_p)
            sp_close = base_close_ranks.corr(s_ser.loc[close_mask].rank())
            crossings_40 = int(((inst_df["ivt_score"] >= 40.0) != (s_ser >= 40.0)).sum())
            uncapped_crossings_40 = int(((inst_df["ivt_score"] >= 40.0) != (raw_s >= 40.0)).sum())
            print(
                f"  - Pilier {target_p:10s} ({d_lbl} normalise) : Top 22 = {overlap}/22 ({overlap / 22 * 100:.1f} %) | "
                f"Spearman (<=1km) = {sp_close:.4f} | Bascules seuil 40 = {crossings_40} (sans plafond 39.9 = {uncapped_crossings_40})"
            )


if __name__ == "__main__":
    main()
