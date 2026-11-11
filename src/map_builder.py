"""Construction de la carte interactive Folium — ÉquiVigie Normandie."""

from __future__ import annotations

import html
from typing import Any

import folium
import pandas as pd

from src.data_loader import VIGILANCE_COLORS

BASEMAP_CHOICES: list[str] = [
    "Épuré",
    "Classique",
    "Détaillé",
]

_IGN_PLAN_URL = (
    "https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0"
    "&LAYER=GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2&STYLE=normal&FORMAT=image/png"
    "&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}"
)
_ESRI_LIGHT_URL = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/"
    "World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
)


def build_interactive_map(
    df: pd.DataFrame,
    natura_geojson: dict[str, Any],
    selected_inst_id: str | None = None,
    show_zsc: bool = True,
    show_zps: bool = True,
    show_installations: bool = True,
    show_buffers: bool = True,
    basemap: str = "Épuré",
    focus_selected: bool = False,
) -> folium.Map:
    """Construit la carte Folium multicouche (installations + ZSC + ZPS + tampons)."""
    center_lat, center_lon, zoom_start = 49.15, -0.15, 8

    selected_row = None
    if selected_inst_id and not df.empty:
        match = df[df["inst_numero"] == selected_inst_id]
        if not match.empty:
            selected_row = match.iloc[0]
            if focus_selected:
                center_lat = float(selected_row["latitude"])
                center_lon = float(selected_row["longitude"])
                zoom_start = 13

    if basemap == "Détaillé":
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles="OpenStreetMap",
            control_scale=False,
            attribution_control=False,
            prefer_canvas=True,
        )
    elif basemap == "Classique":
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles=None,
            control_scale=False,
            attribution_control=False,
            prefer_canvas=True,
        )
        folium.TileLayer(
            tiles=_IGN_PLAN_URL,
            attr="IGN",
            name="Classique",
            max_zoom=18,
            control=False,
        ).add_to(m)
    else:
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles=None,
            control_scale=False,
            attribution_control=False,
            prefer_canvas=True,
        )
        folium.TileLayer(
            tiles=_ESRI_LIGHT_URL,
            attr="Esri",
            name="Épuré",
            max_zoom=16,
            control=False,
        ).add_to(m)

    m.get_root().header.add_child(
        folium.Element("<style>.leaflet-control-attribution{display:none !important;}</style>")
    )

    # 1. Couche écologique ZSC (Habitats)
    if show_zsc and natura_geojson:
        zsc_features = [
            ft for ft in natura_geojson.get("features", [])
            if (ft.get("properties") or {}).get("type_zone") == "ZSC"
        ]
        if zsc_features:
            zsc_layer = folium.FeatureGroup(name="Natura 2000 — ZSC (Habitats)", show=True)
            folium.GeoJson(
                {"type": "FeatureCollection", "features": zsc_features},
                style_function=lambda _: {
                    "fillColor": "#0d9488",
                    "color": "#0f766e",
                    "weight": 1.4,
                    "fillOpacity": 0.22,
                },
                highlight_function=lambda _: {
                    "fillOpacity": 0.42,
                    "weight": 2.5,
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=["SITENAME", "typologie_label", "installations_proches_1km"],
                    aliases=["Zone ZSC (Habitats) :", "Milieu naturel :", "Installations à moins d'1 km :"],
                    localize=True,
                ),
            ).add_to(zsc_layer)
            zsc_layer.add_to(m)

    # 2. Couche écologique ZPS (Oiseaux)
    if show_zps and natura_geojson:
        zps_features = [
            ft for ft in natura_geojson.get("features", [])
            if (ft.get("properties") or {}).get("type_zone") == "ZPS"
        ]
        if zps_features:
            zps_layer = folium.FeatureGroup(name="Natura 2000 — ZPS (Oiseaux)", show=True)
            folium.GeoJson(
                {"type": "FeatureCollection", "features": zps_features},
                style_function=lambda _: {
                    "fillColor": "#2563eb",
                    "color": "#1d4ed8",
                    "weight": 1.6,
                    "dashArray": "4 3",
                    "fillOpacity": 0.16,
                },
                highlight_function=lambda _: {
                    "fillOpacity": 0.36,
                    "weight": 2.6,
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=["SITENAME", "typologie_label", "installations_proches_1km"],
                    aliases=["Zone ZPS (Oiseaux) :", "Milieu naturel :", "Installations à moins d'1 km :"],
                    localize=True,
                ),
            ).add_to(zps_layer)
            zps_layer.add_to(m)

    # 3. Cercles d'analyse spatiale (500 m et 1 000 m) autour de l'installation sélectionnée
    if show_buffers and selected_row is not None:
        buf_layer = folium.FeatureGroup(name="Rayons d'analyse (500 m / 1 km)", show=True)
        sel_lat = float(selected_row["latitude"])
        sel_lon = float(selected_row["longitude"])
        folium.Circle(
            location=[sel_lat, sel_lon],
            radius=1000,
            color="#d97706",
            weight=2.0,
            dash_array="6 4",
            fill=True,
            fill_color="#f59e0b",
            fill_opacity=0.08,
            tooltip="Rayon d'analyse exploratoire : 1 000 m",
        ).add_to(buf_layer)
        folium.Circle(
            location=[sel_lat, sel_lon],
            radius=500,
            color="#dc2626",
            weight=2.0,
            dash_array="4 3",
            fill=True,
            fill_color="#ef4444",
            fill_opacity=0.11,
            tooltip="Rayon de proximité rapprochée : 500 m",
        ).add_to(buf_layer)
        buf_layer.add_to(m)

    # 4. Couche activités équestres (points)
    if show_installations and not df.empty:
        pts_layer = folium.FeatureGroup(name="Installations équestres", show=True)
        # Dessiner d'abord les plus éloignés pour garder les prioritaires et la sélection visibles au-dessus
        ordered = df.copy()
        ordered["_is_sel"] = ordered["inst_numero"] == (selected_inst_id or "")
        ordered = ordered.sort_values(["_is_sel", "priorite_rang"], ascending=[True, False])

        for _, row in ordered.iterrows():
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            inst_id = str(row["inst_numero"])
            nom = str(row["nom_installation"])
            commune = str(row["commune"])
            dep = str(row["departement"])
            vig = str(row["niveau_vigilance_descriptif"])
            dist_m = float(row["distance_natura_m"])
            nb_eq = int(row["nombre_equipements"])
            nat_nom = str(row["natura_plus_proche_nom"])
            typ_short = str(row["typologie_short"])
            ivt_score = float(row["ivt_score"]) if "ivt_score" in row else 0.0
            ivt_niveau = str(row["ivt_niveau"]) if "ivt_niveau" in row else ""

            color = VIGILANCE_COLORS.get(vig, "#475569")
            is_selected = selected_inst_id == inst_id
            radius = 9.5 if is_selected else (6.5 if vig == "À l’intérieur" else (5.5 if dist_m <= 1000 else 4.2))
            border_color = "#0f172a" if is_selected else "#ffffff"
            weight = 2.8 if is_selected else 1.2

            if is_selected:
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=15,
                    color="#0f172a",
                    weight=1.6,
                    dash_array="3 3",
                    fill=False,
                ).add_to(pts_layer)

            ivt_line = f"<b>Indice vigilance (IVT) :</b> {ivt_score:.1f} % ({html.escape(ivt_niveau)})<br/>" if ivt_niveau else ""
            popup_html = (
                f"<div style='font-family:sans-serif;font-size:12px;min-width:230px;line-height:1.45;'>"
                f"<strong>{html.escape(nom)}</strong><br/>"
                f"<span style='color:#475569;'>{html.escape(commune)} ({html.escape(dep)})</span><br/>"
                f"<hr style='margin:5px 0;border:none;border-top:1px solid #e2e8f0;'/>"
                f"{ivt_line}"
                f"<b>Proximité Natura 2000 :</b> {dist_m:.0f} m ({html.escape(vig)})<br/>"
                f"<b>Site le plus proche :</b> {html.escape(nat_nom)}<br/>"
                f"<b>Typologie :</b> {html.escape(typ_short)}<br/>"
                f"<b>Équipements recensés :</b> {nb_eq}"
                f"</div>"
            )
            ivt_tip = f", IVT {ivt_score:.0f} %" if ivt_niveau else ""
            tooltip_txt = f"{nom} — {commune} ({vig}, {dist_m:.0f} m{ivt_tip})"

            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color=border_color,
                weight=weight,
                fill=True,
                fill_color=color,
                fill_opacity=0.94,
                tooltip=tooltip_txt,
                popup=folium.Popup(popup_html, max_width=320),
            ).add_to(pts_layer)

        pts_layer.add_to(m)

    # Recadrage modéré si filtrage actif (sans zoom excessif sur quelques points isolés)
    if not df.empty and not focus_selected and len(df) < 421:
        min_lat, max_lat = float(df["latitude"].min()), float(df["latitude"].max())
        min_lon, max_lon = float(df["longitude"].min()), float(df["longitude"].max())
        mid_lat = (min_lat + max_lat) / 2.0
        mid_lon = (min_lon + max_lon) / 2.0
        half_lat = max((max_lat - min_lat) / 2.0 + 0.06, 0.18)
        half_lon = max((max_lon - min_lon) / 2.0 + 0.10, 0.28)
        m.fit_bounds([[mid_lat - half_lat, mid_lon - half_lon], [mid_lat + half_lat, mid_lon + half_lon]])

    return m
