"""Script reproductible d'allègement géométrique pour la sobriété numérique.

Les distances officielles entre installations équestres et sites Natura 2000
ont été calculées en amont sur les géométries exactes (EPSG:2154). Ce script
génère uniquement une version simplifiée des polygones pour l'affichage web
(réduction de 93,5 % du poids fichier et de 92,8 % des sommets) et mesure les
gains dans ``data/processed/sobriete_metrics.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

from shapely.geometry import mapping, shape


def count_vertices(geom_dict: dict) -> int:
    """Compte le nombre total de sommets d'une géométrie GeoJSON."""
    gtype = geom_dict.get("type")
    coords = geom_dict.get("coordinates", [])
    if gtype == "Polygon":
        return sum(len(ring) for ring in coords)
    if gtype == "MultiPolygon":
        return sum(len(ring) for poly in coords for ring in poly)
    return 0


def round_coords(obj, precision: int = 4):
    """Arrondit les coordonnées WGS84 à 4 décimales (~10 m) pour alléger le JSON."""
    if isinstance(obj, list):
        return [round_coords(item, precision) for item in obj]
    if isinstance(obj, float):
        return round(obj, precision)
    return obj


def optimize_natura_geojson(
    src_path: Path,
    dst_path: Path,
    metrics_path: Path,
    tolerance_deg: float = 0.001,
) -> dict:
    """Simplifie topologiquement les polygones Natura 2000 et journalise le gain."""
    raw_bytes = src_path.stat().st_size
    data = json.loads(src_path.read_text(encoding="utf-8"))

    vertices_before = 0
    vertices_after = 0
    new_features = []

    for feat in data.get("features", []):
        geom_raw = feat.get("geometry")
        if not geom_raw:
            continue
        vertices_before += count_vertices(geom_raw)
        geom = shape(geom_raw)
        simplified = geom.simplify(tolerance_deg, preserve_topology=True)
        if simplified.is_empty:
            simplified = geom
        geom_out = mapping(simplified)
        geom_out["coordinates"] = round_coords(geom_out["coordinates"], precision=4)
        vertices_after += count_vertices(geom_out)
        new_features.append(
            {
                "type": "Feature",
                "properties": feat.get("properties", {}),
                "geometry": geom_out,
            }
        )

    out_collection = {
        "type": "FeatureCollection",
        "features": new_features,
    }
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_text = json.dumps(out_collection, ensure_ascii=False, separators=(",", ":"))
    dst_path.write_text(dst_text, encoding="utf-8")

    opt_bytes = dst_path.stat().st_size
    reduction_pct = round((1.0 - opt_bytes / raw_bytes) * 100.0, 1) if raw_bytes else 0.0
    vertices_reduction_pct = (
        round((1.0 - vertices_after / vertices_before) * 100.0, 1) if vertices_before else 0.0
    )

    metrics = {
        "source_file": src_path.name,
        "optimized_file": dst_path.name,
        "features_count": len(new_features),
        "tolerance_deg": tolerance_deg,
        "coord_precision_decimals": 4,
        "raw_size_bytes": raw_bytes,
        "raw_size_mb": round(raw_bytes / (1024 * 1024), 2),
        "optimized_size_bytes": opt_bytes,
        "optimized_size_mb": round(opt_bytes / (1024 * 1024), 2),
        "size_reduction_pct": reduction_pct,
        "vertices_before": vertices_before,
        "vertices_after": vertices_after,
        "vertices_reduction_pct": vertices_reduction_pct,
    }
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = optimize_natura_geojson(
        src_path=root / "data" / "raw" / "natura2000_zsc_zps_normandie.geojson",
        dst_path=root / "data" / "processed" / "natura2000_simplifie.geojson",
        metrics_path=root / "data" / "processed" / "sobriete_metrics.json",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
