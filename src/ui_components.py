"""Composants HTML/CSS réutilisables pour l'interface ÉquiVigie Normandie."""

from __future__ import annotations

import html
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.data_loader import IVT_COLORS, IVT_ORDER
from src.recommendations import ActionItem, DiagnosticResult


CUSTOM_CSS = """
<style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
        max-width: 1460px;
    }
    /* Masque l'indice "Press Enter to apply" des champs texte */
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    /* Barre d'outils Plotly toujours claire et encadrée au-dessus de chaque graphique */
    .js-plotly-plot .plotly .modebar {
        top: 0px !important;
        right: 4px !important;
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 7px !important;
        padding: 2px 6px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
        opacity: 1 !important;
    }
    .js-plotly-plot .plotly .modebar-btn path {
        fill: #334155 !important;
    }
    .js-plotly-plot .plotly .modebar-btn:hover path {
        fill: #15803d !important;
    }
    /* Rapproche l'icône d'aide (?) juste à côté du libellé sur tous les widgets */
    [data-testid="stWidgetLabel"] {
        width: fit-content !important;
        max-width: 100% !important;
        justify-content: flex-start !important;
        gap: 0.42rem !important;
    }
    [data-testid="stWidgetLabel"] > div:first-child {
        flex: 0 0 auto !important;
        width: fit-content !important;
    }
    [data-testid="stTooltipIcon"] {
        margin-left: 0 !important;
    }
    .hero-banner {
        background: linear-gradient(120deg, #0f3d32 0%, #14532d 55%, #0e7490 100%);
        color: #ffffff;
        padding: 1.05rem 1.4rem;
        border-radius: 14px;
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
        overflow: visible;
    }
    .hero-title {
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 0.25rem 0;
    }
    .hero-subtitle {
        font-size: 0.94rem;
        opacity: 0.95;
        margin: 0 0 0.6rem 0;
    }
    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.45rem;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.38rem;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 999px;
        padding: 0.22rem 0.74rem;
        font-size: 0.77rem;
        white-space: nowrap;
    }
    .hero-tip-wrap {
        position: relative;
        display: inline-flex;
        align-items: center;
    }
    .hero-tip-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 17px;
        height: 17px;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.7);
        background: rgba(255, 255, 255, 0.18);
        color: #ffffff;
        font-size: 0.7rem;
        font-weight: 700;
        cursor: help;
        line-height: 1;
    }
    .hero-tip-box {
        display: none;
        position: absolute;
        top: 135%;
        left: 0;
        width: 340px;
        max-width: 82vw;
        background: #0f172a;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 9px;
        padding: 0.7rem 0.85rem;
        font-size: 0.78rem;
        line-height: 1.48;
        white-space: normal;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.32);
        z-index: 9999;
    }
    .hero-tip-wrap:hover .hero-tip-box,
    .hero-tip-wrap:focus-within .hero-tip-box {
        display: block;
    }
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #15803d;
        border-radius: 10px;
        padding: 0.75rem 0.95rem;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.05);
        min-height: 112px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-label {
        font-size: 0.74rem;
        color: #475569;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .kpi-value {
        font-size: 1.46rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
        margin: 0.2rem 0;
    }
    .kpi-sub {
        font-size: 0.77rem;
        color: #64748b;
        line-height: 1.3;
    }
    .detail-header {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
    }
    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }
    .badge-pill {
        display: inline-block;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.74rem;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        white-space: nowrap;
    }
    .code-chip {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.8rem;
        color: #0f766e;
        background: #f1f5f9;
        padding: 0.04rem 0.25rem;
        border-radius: 4px;
    }
    .mini-metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .mini-metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.55rem 0.65rem;
    }
    .mini-metric-label {
        font-size: 0.71rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    .mini-metric-val {
        font-size: 1.12rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.16rem;
        white-space: nowrap;
    }
    .idea-block {
        font-size: 0.86rem;
        color: #1e293b;
        line-height: 1.5;
        margin-bottom: 0.9rem;
    }
    .idea-block:last-child {
        margin-bottom: 0.25rem;
    }
    .idea-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 9px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.85rem;
        font-size: 0.86rem;
        color: #1e293b;
        line-height: 1.5;
    }
    .ivt-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.85rem 0.95rem;
        margin-top: 0.65rem;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
    }
    .ivt-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .ivt-score-num {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
    }
    .ivt-track {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 0.7rem;
    }
    .ivt-fill {
        height: 100%;
        border-radius: 999px;
    }
    .ivt-pillar-row {
        margin-bottom: 0.48rem;
    }
    .ivt-pillar-row:last-child {
        margin-bottom: 0;
    }
    .ivt-pillar-top {
        display: flex;
        justify-content: space-between;
        font-size: 0.77rem;
        color: #334155;
        margin-bottom: 0.16rem;
    }
    .ivt-pillar-track {
        width: 100%;
        height: 6px;
        background: #f1f5f9;
        border-radius: 999px;
        overflow: hidden;
    }
    .map-legend-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.65rem 1.05rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem 0.85rem;
        margin-top: 0.4rem;
        font-size: 0.78rem;
        color: #1e293b;
    }
    .legend-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.32rem;
        vertical-align: middle;
    }
    .legend-poly {
        display: inline-block;
        width: 12px;
        height: 9px;
        margin-right: 0.32rem;
        vertical-align: middle;
        border-radius: 2px;
    }
    .empty-sel-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.05rem 1.15rem;
        margin-bottom: 0.75rem;
    }
    .disclaimer-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 0.75rem 0.95rem;
        font-size: 0.83rem;
        color: #1e3a8a;
        margin-top: 0.75rem;
        line-height: 1.5;
    }
</style>
"""


def fmt_int(value: int | float) -> str:
    """Formate un entier avec espace pour les milliers."""
    return f"{int(round(value)):,}".replace(",", " ")


def render_idea_blocks(items: list[tuple[str, str]], *, as_cards: bool = False) -> None:
    """Affiche une liste d'idées sans puces, chacune débutant par un titre en gras et espacée."""
    cls = "idea-card" if as_cards else "idea-block"
    blocks = "".join(
        f'<div class="{cls}"><strong>{html.escape(lead)}</strong> {html.escape(body)}</div>'
        for lead, body in items
    )
    st.markdown(blocks, unsafe_allow_html=True)


def render_kpi_row(
    *,
    nb_inst: int,
    total_inst: int,
    nb_eq: int,
    nb_1km: int,
    pct_1km: float,
    nb_inside: int,
    med_dist: float | None,
    mean_ivt: float | None,
    nb_ivt_high: int,
    nb_communes: int,
) -> None:
    """Affiche les 5 cartes KPI alignées et uniformes en haut de l'application."""
    med_txt = f"{med_dist:,.0f} m".replace(",", " ") if med_dist is not None else "—"
    med_sub = "Au site Natura 2000 le plus proche" if med_dist is not None else "Aucune installation dans le filtre"
    ivt_txt = f"{mean_ivt:.1f} %" if mean_ivt is not None else "—"
    ivt_sub = f"{nb_ivt_high} prioritaire(s) (IVT ≥ 70 %)" if mean_ivt is not None else "Aucune installation dans le filtre"

    k1, k2, k3, k4, k5 = st.columns(5)
    cards = [
        (
            k1,
            "#15803d",
            "Installations filtrées",
            f"{nb_inst} <span style='font-size:0.9rem;color:#64748b;'>/ {total_inst}</span>",
            f"{fmt_int(nb_eq)} équipements équestres",
        ),
        (
            k2,
            "#ea580c",
            "À 1 km ou moins",
            f"{nb_1km} <span style='font-size:0.9rem;color:#64748b;'>({pct_1km:.1f}%)</span>",
            f"Dont {nb_inside} à l'intérieur (0 m)",
        ),
        (
            k3,
            "#0284c7",
            "Distance médiane",
            med_txt,
            med_sub,
        ),
        (
            k4,
            "#b91c1c",
            "Vigilance moyenne (IVT)",
            ivt_txt,
            ivt_sub,
        ),
        (
            k5,
            "#0d9488",
            "Communes couvertes",
            f"{nb_communes}",
            "Sur 352 communes normandes",
        ),
    ]
    for col, top_color, label, value_html, sub in cards:
        col.markdown(
            f"""<div class="kpi-card" style="border-top-color:{top_color};">
                <div class="kpi-label">{html.escape(label)}</div>
                <div class="kpi-value">{value_html}</div>
                <div class="kpi-sub">{html.escape(sub)}</div>
            </div>""",
            unsafe_allow_html=True,
        )


def render_map_legend() -> None:
    """Affiche la légende horizontale sous la carte sans recouvrir l'échelle Leaflet."""
    st.markdown(
        """
        <div class="map-legend-bar">
            <span><strong>Proximité :</strong></span>
            <span><span class="legend-dot" style="background:#b91c1c;"></span>À l’intérieur (0 m)</span>
            <span><span class="legend-dot" style="background:#ea580c;"></span>0 – 500 m</span>
            <span><span class="legend-dot" style="background:#ca8a04;"></span>500 – 1 000 m</span>
            <span><span class="legend-dot" style="background:#15803d;"></span>&gt; 1 000 m</span>
            <span><span class="legend-poly" style="background:rgba(13,148,136,0.35);border:1px solid #0f766e;"></span>ZSC (Habitats)</span>
            <span><span class="legend-poly" style="background:rgba(37,99,235,0.22);border:1px dashed #1d4ed8;"></span>ZPS (Oiseaux)</span>
            <span><span class="legend-dot" style="background:transparent;border:2px dashed #d97706;"></span>Rayon 500 m / 1 km</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_selection_panel(df_filtered: pd.DataFrame) -> None:
    """Affiche un panneau synthétique lorsqu'aucune installation n'est sélectionnée."""
    total = len(df_filtered)
    counts = df_filtered["ivt_niveau"].value_counts().to_dict()

    bars_html = ""
    for lvl in IVT_ORDER:
        cnt = int(counts.get(lvl, 0))
        pct = (cnt / total * 100.0) if total else 0.0
        col = IVT_COLORS[lvl]
        bars_html += f"""
        <div class="ivt-pillar-row">
            <div class="ivt-pillar-top">
                <span><strong>{html.escape(lvl)}</strong></span>
                <span><b>{cnt}</b> ({pct:.1f}%)</span>
            </div>
            <div class="ivt-pillar-track">
                <div class="ivt-fill" style="width:{pct:.1f}%;background:{col};"></div>
            </div>
        </div>
        """

    st.markdown(
        f"""
        <div class="empty-sel-card">
            <div style="font-size:1.05rem;font-weight:800;color:#0f172a;margin-bottom:0.35rem;">
                Aucune installation sélectionnée
            </div>
            <div style="font-size:0.86rem;color:#475569;line-height:1.45;">
                Veuillez sélectionner une installation pour afficher sa fiche détaillée.
            </div>
        </div>
        <div class="ivt-card" style="margin-top:0;">
            <div style="font-size:0.76rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.03em;margin-bottom:0.65rem;">
                Répartition de la sélection ({total} installations) par niveau IVT
            </div>
            {bars_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_installation_identity_and_ivt(sel_row, selected_id: str, diag: DiagnosticResult) -> None:
    """Affiche l'en-tête synthétique, les métriques non tronquées et l'IVT détaillé."""
    addr_parts = [p for p in [sel_row["inst_adresse"], sel_row["inst_cp"], sel_row["commune"]] if str(p).strip()]
    addr_line = ", ".join(addr_parts)

    st.markdown(
        f"""
        <div class="detail-header">
            <div style="font-size:1.1rem;font-weight:800;color:#0f172a;margin-bottom:0.25rem;">
                {html.escape(str(sel_row['nom_installation']))}
            </div>
            <div style="font-size:0.83rem;color:#475569;margin-bottom:0.55rem;line-height:1.45;">
                <strong>Adresse :</strong> {html.escape(addr_line)} — <b>{html.escape(str(sel_row['departement']))} ({html.escape(str(sel_row['departement_code']))})</b>
            </div>
            <div style="font-size:0.8rem;color:#475569;margin-bottom:0.55rem;">
                <strong>Identifiant établissement :</strong> <span class="code-chip">{html.escape(selected_id)}</span>
            </div>
            <div class="badge-row">
                <span class="badge-pill" style="background:{diag.priority_color};">
                    {html.escape(diag.vigilance_label)} — {html.escape(diag.priority_tier)}
                </span>
                <span class="badge-pill" style="background:{diag.primary_typology.badge_color};">
                    {html.escape(diag.primary_typology.short_label)}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dist_fmt = f"{float(sel_row['distance_natura_m']):,.1f} m".replace(",", " ")
    st.markdown(
        f"""
        <div class="mini-metric-grid">
            <div class="mini-metric-box">
                <div class="mini-metric-label">Site le plus proche</div>
                <div class="mini-metric-val">{dist_fmt}</div>
            </div>
            <div class="mini-metric-box">
                <div class="mini-metric-label">Sites à ≤ 1 km</div>
                <div class="mini-metric-val">{diag.effective_sites_1km}</div>
            </div>
            <div class="mini-metric-box">
                <div class="mini-metric-label">Équipements</div>
                <div class="mini-metric-val">{int(sel_row['nombre_equipements'])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    zsc_dist = f"{float(sel_row['distance_zsc_m']):,.1f} m".replace(",", " ")
    zps_dist = f"{float(sel_row['distance_zps_m']):,.1f} m".replace(",", " ")
    st.markdown(
        f"""
        <div class="idea-block">
            <strong>ZSC (Habitats) la plus proche :</strong>
            {html.escape(str(sel_row['zsc_plus_proche_nom']))} (<span class="code-chip">{html.escape(str(sel_row['zsc_plus_proche_code']))}</span>) — <b>{zsc_dist}</b>
        </div>
        <div class="idea-block">
            <strong>ZPS (Oiseaux) la plus proche :</strong>
            {html.escape(str(sel_row['zps_plus_proche_nom']))} (<span class="code-chip">{html.escape(str(sel_row['zps_plus_proche_code']))}</span>) — <b>{zps_dist}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ivt = diag.vigilance_index
    pillars = [
        ("Distance géographique", ivt.dim_distance, 40.0, "#dc2626"),
        ("Proximité habitats ZSC/ZPS et cumul", ivt.dim_habitats, 25.0, "#2563eb"),
        ("Contexte écologique du milieu", ivt.dim_ecologie, 20.0, "#0d9488"),
        ("Contexte territorial et équipements", ivt.dim_territoire, 15.0, "#d97706"),
    ]
    pillars_html = "".join(
        f"""
        <div class="ivt-pillar-row">
            <div class="ivt-pillar-top">
                <span><strong>{html.escape(lbl)}</strong></span>
                <span><b>{val:.1f} %</b> / {mx:.0f} %</span>
            </div>
            <div class="ivt-pillar-track">
                <div class="ivt-fill" style="width:{min(100.0, val / mx * 100.0):.1f}%;background:{col};"></div>
            </div>
        </div>
        """
        for lbl, val, mx, col in pillars
    )

    st.markdown(
        f"""
        <div class="ivt-card">
            <div class="ivt-header">
                <div>
                    <div style="font-size:0.74rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.03em;">
                        Indice de Vigilance Territoriale (IVT)
                    </div>
                    <div class="ivt-score-num">
                        {ivt.score_total:.1f} %
                    </div>
                </div>
                <span class="badge-pill" style="background:{ivt.level_color};">
                    {html.escape(ivt.level_label)}
                </span>
            </div>
            <div class="ivt-track">
                <div class="ivt-fill" style="width:{ivt.score_total:.1f}%;background:{ivt.level_color};"></div>
            </div>
            {pillars_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_collapsible_action_cards(items: list[ActionItem], *, positive: bool) -> None:
    """Affiche les pistes d'action en grille équilibrée : titre en gras replié par défaut avec flèche."""
    if not items:
        return

    bg = "#f0fdf4" if positive else "#fffbeb"
    border = "#bbf7d0" if positive else "#fde68a"
    accent = "#15803d" if positive else "#d97706"
    variant_cls = "ev-grid-pos" if positive else "ev-grid-vig"
    cols_css = "1fr" if len(items) == 1 else "repeat(2, minmax(0, 1fr))"

    cards_html = "".join(
        f"""
        <details class="ev-action-card">
            <summary class="ev-action-summary">
                <span class="ev-action-title">{html.escape(item.title)}</span>
                <span class="ev-chevron" aria-hidden="true"></span>
            </summary>
            <div class="ev-action-body">
                <div class="ev-action-detail">{html.escape(item.detail)}</div>
                <div class="ev-action-why"><strong>Critère :</strong> {html.escape(item.rationale)}</div>
            </div>
        </details>
        """
        for item in items
    )

    st.html(
        f"""
        <style>
            .{variant_cls} {{
                display: grid;
                grid-template-columns: {cols_css};
                gap: 0.75rem;
                align-items: start;
                margin-bottom: 0.5rem;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            @media (max-width: 820px) {{
                .{variant_cls} {{
                    grid-template-columns: 1fr;
                }}
            }}
            .{variant_cls} .ev-action-card {{
                background: {bg};
                border: 1px solid {border};
                border-left: 5px solid {accent};
                border-radius: 8px;
                padding: 0.75rem 0.95rem;
                box-sizing: border-box;
            }}
            .{variant_cls} .ev-action-summary {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.75rem;
                cursor: pointer;
                list-style: none;
                font-weight: 700;
                font-size: 0.91rem;
                color: #0f172a;
                line-height: 1.38;
                user-select: none;
            }}
            .{variant_cls} .ev-action-summary::-webkit-details-marker {{
                display: none;
            }}
            .{variant_cls} .ev-chevron {{
                flex-shrink: 0;
                width: 8px;
                height: 8px;
                border-right: 2px solid {accent};
                border-bottom: 2px solid {accent};
                transform: rotate(-45deg);
                transition: transform 0.18s ease;
                margin-right: 2px;
            }}
            .{variant_cls} details[open] .ev-chevron {{
                transform: rotate(45deg);
            }}
            .{variant_cls} .ev-action-body {{
                margin-top: 0.65rem;
                padding-top: 0.55rem;
                border-top: 1px solid {border};
            }}
            .{variant_cls} .ev-action-detail {{
                font-size: 0.85rem;
                color: #334155;
                line-height: 1.5;
            }}
            .{variant_cls} .ev-action-why {{
                font-size: 0.76rem;
                color: #64748b;
                margin-top: 0.45rem;
            }}
        </style>
        <div class="{variant_cls}">{cards_html}</div>
        """
    )


def render_french_table(
    df: pd.DataFrame,
    *,
    table_id: str,
    height: int = 360,
    wide_cols: set[str] | None = None,
    numeric_suffixes: dict[str, str] | None = None,
) -> None:
    """Affiche un tableau interactif 100 % en français avec menu ⋮ toujours visible et statistiques."""
    wide_cols = wide_cols or set()
    numeric_suffixes = numeric_suffixes or {}

    if df.empty:
        st.info("Aucune ligne à afficher.")
        return

    cols = list(df.columns)
    col_stats: list[dict] = []
    for col in cols:
        series = df[col]
        total_cnt = int(len(series))
        is_num = pd.api.types.is_numeric_dtype(series)
        non_empty = series.dropna()
        if not is_num:
            non_empty = non_empty[non_empty.astype(str).str.strip() != ""]
        empty_cnt = total_cnt - int(len(non_empty))
        distinct_cnt = int(non_empty.nunique())

        top_counts = non_empty.astype(str).value_counts().head(5)
        dist_items = [
            {
                "label": str(k),
                "count": int(v),
                "pct": round(float(v) / total_cnt * 100.0, 1) if total_cnt else 0.0,
            }
            for k, v in top_counts.items()
        ]
        stat_obj: dict = {
            "is_num": bool(is_num),
            "total": total_cnt,
            "empty": empty_cnt,
            "distinct": distinct_cnt,
            "dist": dist_items,
        }
        if is_num and len(non_empty) > 0:
            stat_obj["min"] = round(float(non_empty.min()), 1)
            stat_obj["max"] = round(float(non_empty.max()), 1)
            stat_obj["mean"] = round(float(non_empty.mean()), 1)
        col_stats.append(stat_obj)

    records: list[list[dict]] = []
    for _, row in df.iterrows():
        row_cells = []
        for col in cols:
            val = row[col]
            is_num = pd.api.types.is_numeric_dtype(df[col])
            if pd.isna(val):
                disp = ""
                sort_val: str | float = ""
            elif is_num:
                fval = float(val)
                if fval.is_integer():
                    disp = f"{int(fval)}"
                else:
                    disp = f"{fval:.1f}"
                suffix = numeric_suffixes.get(col, "")
                if suffix:
                    disp = f"{disp}{suffix}"
                sort_val = fval
            else:
                disp = str(val)
                sort_val = disp.lower()
            row_cells.append({"d": disp, "s": sort_val})
        records.append(row_cells)

    payload = {
        "cols": cols,
        "wide": [c in wide_cols for c in cols],
        "stats": col_stats,
        "rows": records,
    }
    payload_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    root_id = f"ftbl_{table_id}"
    dots_svg = (
        '<svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<circle cx="8" cy="3" r="1.5"/><circle cx="8" cy="8" r="1.5"/><circle cx="8" cy="13" r="1.5"/>'
        "</svg>"
    )
    scroll_h = int(height)
    iframe_h = max(scroll_h + 52, 345)
    popup_max_h = iframe_h - 56

    doc_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<style>
    * {{ box-sizing: border-box; }}
    html, body {{
        margin: 0;
        padding: 2px 0 0 0;
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 13.5px;
        color: #0f172a;
    }}
    #{root_id} {{
        position: relative;
        width: 100%;
    }}
    #{root_id} .ft-topbar {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 6px;
        min-height: 0;
    }}
    #{root_id} .ft-reset-btn {{
        display: none;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #0f172a;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 12.5px;
        font-weight: 600;
        cursor: pointer;
    }}
    #{root_id} .ft-reset-btn:hover {{
        background: #e2e8f0;
    }}
    #{root_id} .ft-scroll {{
        max-height: {scroll_h}px;
        overflow: auto;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        background: #ffffff;
    }}
    #{root_id} table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
    }}
    #{root_id} thead th {{
        position: sticky;
        top: 0;
        z-index: 5;
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        border-right: 1px solid #f1f5f9;
        padding: 9px 10px;
        text-align: left;
        font-weight: 700;
        font-size: 12.8px;
        color: #334155;
        white-space: nowrap;
        vertical-align: middle;
    }}
    #{root_id} thead th:last-child {{
        border-right: none;
    }}
    #{root_id} .ft-th-inner {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
    }}
    #{root_id} .ft-menu-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 5px;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: #334155;
        cursor: pointer;
        flex-shrink: 0;
        padding: 0;
    }}
    #{root_id} .ft-menu-btn:hover {{
        background: #e2e8f0;
        color: #0f172a;
    }}
    #{root_id} tbody td {{
        padding: 8px 10px;
        border-bottom: 1px solid #f1f5f9;
        border-right: 1px solid #f8fafc;
        color: #0f172a;
        vertical-align: top;
        line-height: 1.4;
        font-size: 13.2px;
    }}
    #{root_id} tbody tr:hover td {{
        background: #f8fafc;
    }}
    #{root_id} .ft-wide {{
        min-width: 220px;
        white-space: normal;
    }}
    #{root_id} .ft-num {{
        text-align: right;
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
    }}
    #{root_id} .ft-popup {{
        display: none;
        position: fixed;
        z-index: 999;
        width: 270px;
        max-height: {popup_max_h}px;
        overflow-y: auto;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.18);
        padding: 7px;
    }}
    #{root_id} .ft-popup-head {{
        font-weight: 700;
        font-size: 12.8px;
        color: #0f172a;
        background: #f1f5f9;
        border-radius: 6px;
        padding: 6px 9px;
        margin-bottom: 5px;
        word-break: break-word;
    }}
    #{root_id} .ft-popup-item {{
        display: block;
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        border-radius: 6px;
        padding: 7px 9px;
        font-size: 13px;
        color: #1e293b;
        cursor: pointer;
    }}
    #{root_id} .ft-popup-item:hover {{
        background: #f1f5f9;
        color: #15803d;
    }}
    #{root_id} .ft-stats-box {{
        display: none;
        margin-top: 6px;
        padding: 8px;
        border-top: 1px solid #e2e8f0;
        font-size: 12.5px;
        color: #334155;
    }}
    #{root_id} .ft-stat-kv {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }}
    #{root_id} .ft-bar-row {{
        margin-top: 6px;
    }}
    #{root_id} .ft-bar-lbl {{
        display: flex;
        justify-content: space-between;
        gap: 6px;
        font-size: 11.8px;
        margin-bottom: 2px;
    }}
    #{root_id} .ft-bar-lbl span:first-child {{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 175px;
    }}
    #{root_id} .ft-bar-track {{
        height: 6px;
        background: #e2e8f0;
        border-radius: 999px;
        overflow: hidden;
    }}
    #{root_id} .ft-bar-fill {{
        height: 100%;
        background: #0284c7;
        border-radius: 999px;
    }}
</style>
</head>
<body>
<div id="{root_id}">
    <div class="ft-topbar">
        <button type="button" class="ft-reset-btn">Réafficher les colonnes masquées</button>
    </div>
    <div class="ft-scroll">
        <table>
            <thead><tr></tr></thead>
            <tbody></tbody>
        </table>
    </div>
    <div class="ft-popup">
        <div class="ft-popup-head"></div>
        <button type="button" class="ft-popup-item" data-act="asc">Trier par ordre croissant</button>
        <button type="button" class="ft-popup-item" data-act="desc">Trier par ordre décroissant</button>
        <button type="button" class="ft-popup-item" data-act="stats">Statistiques de la colonne</button>
        <button type="button" class="ft-popup-item" data-act="hide">Masquer cette colonne</button>
        <div class="ft-stats-box"></div>
    </div>
</div>
<script>
(() => {{
    const root = document.getElementById({json.dumps(root_id)});
    if (!root) return;
    const data = {payload_json};
    const theadRow = root.querySelector("thead tr");
    const tbody = root.querySelector("tbody");
    const popup = root.querySelector(".ft-popup");
    const popupHead = popup.querySelector(".ft-popup-head");
    const statsBox = popup.querySelector(".ft-stats-box");
    const resetBtn = root.querySelector(".ft-reset-btn");

    let hiddenCols = new Set();
    let sortCol = -1;
    let sortAsc = true;
    let activeCol = -1;
    let rowOrder = data.rows.map((_, i) => i);

    const esc = (s) => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

    function renderHeader() {{
        theadRow.innerHTML = "";
        data.cols.forEach((c, idx) => {{
            if (hiddenCols.has(idx)) return;
            const th = document.createElement("th");
            if (data.wide[idx]) th.className = "ft-wide";
            const mark = sortCol === idx ? (sortAsc ? " (croiss.)" : " (décr.)") : "";
            th.innerHTML =
                '<div class="ft-th-inner">' +
                '<span>' + esc(c + mark) + '</span>' +
                '<button type="button" class="ft-menu-btn" title="Options de colonne">' + {json.dumps(dots_svg)} + '</button>' +
                '</div>';
            const btn = th.querySelector(".ft-menu-btn");
            btn.setAttribute("data-col", c);
            btn.addEventListener("click", (ev) => {{
                ev.stopPropagation();
                openMenu(idx, ev.currentTarget);
            }});
            theadRow.appendChild(th);
        }});
        if (hiddenCols.size > 0) {{
            resetBtn.style.display = "inline-block";
            resetBtn.textContent = "Réafficher les colonnes masquées (" + hiddenCols.size + ")";
        }} else {{
            resetBtn.style.display = "none";
        }}
    }}

    function renderBody() {{
        const frag = document.createDocumentFragment();
        rowOrder.forEach((rIdx) => {{
            const tr = document.createElement("tr");
            const row = data.rows[rIdx];
            data.cols.forEach((_, cIdx) => {{
                if (hiddenCols.has(cIdx)) return;
                const td = document.createElement("td");
                const cls = [];
                if (data.wide[cIdx]) cls.push("ft-wide");
                if (data.stats[cIdx].is_num) cls.push("ft-num");
                if (cls.length) td.className = cls.join(" ");
                td.textContent = row[cIdx].d;
                tr.appendChild(td);
            }});
            frag.appendChild(tr);
        }});
        tbody.innerHTML = "";
        tbody.appendChild(frag);
    }}

    function buildStatsHtml(idx) {{
        const st = data.stats[idx];
        let h = '<div class="ft-stat-kv"><span>Valeurs totales</span><b>' + st.total + '</b></div>';
        h += '<div class="ft-stat-kv"><span>Vides</span><b>' + st.empty + '</b></div>';
        h += '<div class="ft-stat-kv"><span>Valeurs distinctes</span><b>' + st.distinct + '</b></div>';
        if (st.is_num && st.min !== undefined) {{
            h += '<div class="ft-stat-kv"><span>Minimum</span><b>' + st.min + '</b></div>';
            h += '<div class="ft-stat-kv"><span>Maximum</span><b>' + st.max + '</b></div>';
            h += '<div class="ft-stat-kv"><span>Moyenne</span><b>' + st.mean + '</b></div>';
        }}
        if (st.dist && st.dist.length) {{
            h += '<div style="margin-top:6px;font-weight:700;color:#0f172a;">Valeurs les plus fréquentes</div>';
            st.dist.forEach((item) => {{
                h += '<div class="ft-bar-row">' +
                    '<div class="ft-bar-lbl"><span title="' + esc(item.label) + '">' + esc(item.label) + '</span><b>' + item.pct + ' %</b></div>' +
                    '<div class="ft-bar-track"><div class="ft-bar-fill" style="width:' + Math.min(100, item.pct) + '%;"></div></div>' +
                    '</div>';
            }});
        }}
        return h;
    }}

    function openMenu(idx, btn) {{
        if (activeCol === idx && popup.style.display === "block") {{
            popup.style.display = "none";
            return;
        }}
        activeCol = idx;
        popupHead.textContent = data.cols[idx];
        statsBox.style.display = "none";
        statsBox.innerHTML = buildStatsHtml(idx);
        popup.style.display = "block";
        const btnRect = btn.getBoundingClientRect();
        const topPos = Math.min(btnRect.bottom + 4, window.innerHeight - 160);
        let leftPos = btnRect.left;
        if (leftPos + 275 > window.innerWidth) {{
            leftPos = Math.max(4, btnRect.right - 270);
        }}
        popup.style.top = topPos + "px";
        popup.style.left = leftPos + "px";
    }}

    popup.addEventListener("click", (ev) => {{
        ev.stopPropagation();
        const btn = ev.target.closest("[data-act]");
        if (!btn || activeCol < 0) return;
        const act = btn.getAttribute("data-act");
        if (act === "asc" || act === "desc") {{
            sortCol = activeCol;
            sortAsc = act === "asc";
            const isNum = data.stats[sortCol].is_num;
            rowOrder.sort((a, b) => {{
                const va = data.rows[a][sortCol].s;
                const vb = data.rows[b][sortCol].s;
                if (isNum) {{
                    const na = va === "" ? -Infinity : Number(va);
                    const nb = vb === "" ? -Infinity : Number(vb);
                    return sortAsc ? na - nb : nb - na;
                }}
                return sortAsc
                    ? String(va).localeCompare(String(vb), "fr")
                    : String(vb).localeCompare(String(va), "fr");
            }});
            renderHeader();
            renderBody();
            popup.style.display = "none";
        }} else if (act === "stats") {{
            statsBox.style.display = statsBox.style.display === "block" ? "none" : "block";
        }} else if (act === "hide") {{
            hiddenCols.add(activeCol);
            renderHeader();
            renderBody();
            popup.style.display = "none";
        }}
    }});

    resetBtn.addEventListener("click", () => {{
        hiddenCols.clear();
        renderHeader();
        renderBody();
    }});

    document.addEventListener("click", () => {{
        popup.style.display = "none";
    }});

    renderHeader();
    renderBody();
}})();
</script>
</body>
</html>"""

    components.html(doc_html, height=iframe_h, scrolling=False)
