"""Composants HTML/CSS réutilisables pour l'interface ÉquiVigie Normandie."""

from __future__ import annotations

import html
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.data_loader import IVT_COLORS, IVT_ORDER
from src.recommendations import ActionItem, DiagnosticResult


def get_theme_css(dark_mode: bool = False) -> str:
    """Retourne la feuille de style CSS adaptée au thème clair ou sombre."""
    if dark_mode:
        app_bg = "#0b1120"
        sidebar_bg = "#111827"
        header_bg = "rgba(11, 17, 32, 0.92)"
        text_primary = "#f8fafc"
        text_secondary = "#cbd5e1"
        text_muted = "#94a3b8"
        card_bg = "#111827"
        card_alt_bg = "#1e293b"
        border_col = "#334155"
        track_bg = "#1e293b"
        hero_bg = "linear-gradient(120deg, #0b2e24 0%, #0f3d32 55%, #0e4a5c 100%)"
        hero_border = "#166534"
        hero_title_col = "#f8fafc"
        hero_sub_col = "#e2e8f0"
        hero_pill_bg = "rgba(15, 23, 42, 0.52)"
        hero_pill_border = "rgba(134, 239, 172, 0.4)"
        hero_pill_col = "#f8fafc"
        hero_tip_btn_bg = "rgba(255, 255, 255, 0.16)"
        hero_tip_btn_border = "rgba(255, 255, 255, 0.7)"
        hero_tip_btn_col = "#ffffff"
        tip_box_bg = "#1e293b"
        tip_box_border = "#475569"
        sidebar_btn_bg = "#1e293b"
        sidebar_expand_bg = "#064e3b"
        sidebar_btn_border = "#34d399"
        sidebar_btn_col = "#ecfdf5"
        toggle_bg = "#1e293b"
        toggle_hover = "#334155"
        toggle_border = "#475569"
        toggle_col = "#fbbf24"
        tab_bar_bg = "#9ca3af"
        tab_bar_hover = "#cbd5e1"
        tab_bar_border = "#000000"
        tab_inactive_col = "#000000"
        tab_active_bg = "#374151"
        tab_active_col = "#ffffff"
        dl_bg = "#cbd5e1"
        dl_hover = "#e2e8f0"
        dl_border = "#64748b"
        modebar_bg = "#e2e8f0"
        modebar_border = "#94a3b8"
        modebar_icon = "#0f172a"
        modebar_hover = "#000000"
        disclaimer_bg = "#172554"
        disclaimer_border = "#1d4ed8"
        disclaimer_accent = "#60a5fa"
        disclaimer_col = "#dbeafe"
        code_bg = "#0f172a"
        code_col = "#5eead4"
    else:
        app_bg = "#ffffff"
        sidebar_bg = "#f8fafc"
        header_bg = "rgba(255, 255, 255, 0.92)"
        text_primary = "#0f172a"
        text_secondary = "#334155"
        text_muted = "#64748b"
        card_bg = "#ffffff"
        card_alt_bg = "#f8fafc"
        border_col = "#e2e8f0"
        track_bg = "#e2e8f0"
        hero_bg = "linear-gradient(120deg, #dcfce7 0%, #bfead2 55%, #c7e9e4 100%)"
        hero_border = "#86efac"
        hero_title_col = "#000000"
        hero_sub_col = "#1e293b"
        hero_pill_bg = "rgba(255, 255, 255, 0.78)"
        hero_pill_border = "#6ee7b7"
        hero_pill_col = "#0f172a"
        hero_tip_btn_bg = "#ffffff"
        hero_tip_btn_border = "#047857"
        hero_tip_btn_col = "#064e3b"
        tip_box_bg = "#0f172a"
        tip_box_border = "#334155"
        sidebar_btn_bg = "#ffffff"
        sidebar_expand_bg = "#ecfdf5"
        sidebar_btn_border = "#15803d"
        sidebar_btn_col = "#14532d"
        toggle_bg = "#f1f5f9"
        toggle_hover = "#e2e8f0"
        toggle_border = "#cbd5e1"
        toggle_col = "#0f172a"
        tab_bar_bg = "#e5e7eb"
        tab_bar_hover = "#d1d5db"
        tab_bar_border = "#000000"
        tab_inactive_col = "#0f172a"
        tab_active_bg = "#4b5563"
        tab_active_col = "#ffffff"
        dl_bg = "#dfe4ea"
        dl_hover = "#cbd5e1"
        dl_border = "#94a3b8"
        modebar_bg = "#e2e8f0"
        modebar_border = "#94a3b8"
        modebar_icon = "#0f172a"
        modebar_hover = "#000000"
        disclaimer_bg = "#eff6ff"
        disclaimer_border = "#bfdbfe"
        disclaimer_accent = "#2563eb"
        disclaimer_col = "#1e3a8a"
        code_bg = "#f1f5f9"
        code_col = "#0f766e"

    dark_overrides = (
        """
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #0b1120 !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarHeader"] {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border-color: #1e293b !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stCaptionContainer"] p,
    [data-testid="stCheckbox"] label p {
        color: #f8fafc !important;
    }
    [data-testid="stMarkdownContainer"] hr {
        border-color: #334155 !important;
    }
    [data-testid="stTextInputRootElement"],
    [data-testid="stTextInputRootElement"] > div,
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] [role="group"],
    [data-testid="stSelectbox"] input,
    [data-testid="stMultiSelect"] [role="group"],
    [data-testid="stMultiSelect"] input,
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="base-input"] > div {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #f8fafc !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stSelectbox"] input::placeholder,
    [data-testid="stMultiSelect"] input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="input"] input,
    [data-testid="stSelectbox"] button,
    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg {
        color: #e2e8f0 !important;
        fill: #e2e8f0 !important;
    }
    .react-aria-Popover,
    .react-aria-ListBox,
    [data-testid="stSelectboxVirtualDropdown"],
    [data-testid="stPopoverBody"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #f8fafc !important;
    }
    .react-aria-ListBox [role="option"],
    [role="option"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }
    .react-aria-ListBox [role="option"]:hover,
    .react-aria-ListBox [role="option"][aria-selected="true"],
    .react-aria-ListBox [role="option"][data-focused="true"],
    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #334155 !important;
        color: #ffffff !important;
    }
    [data-testid="stCheckbox"] label > div:first-of-type {
        background-color: #1e293b !important;
        border-color: #64748b !important;
    }
    [data-testid="stCheckbox"] input:checked + div,
    [data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type {
        background-color: #15803d !important;
        border-color: #4ade80 !important;
    }
    [data-testid="stPopoverBody"] label p {
        color: #f8fafc !important;
    }
    [data-testid="stExpander"] details {
        background-color: #111827 !important;
        border-color: #334155 !important;
        color: #f8fafc !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] summary:focus,
    [data-testid="stExpander"] details[open] > summary {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-radius: 7px !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary svg {
        color: #f8fafc !important;
        fill: #f8fafc !important;
    }
    [data-testid="stExpanderDetails"] {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border-top: 1px solid #334155 !important;
    }
    [data-baseweb="tooltip"],
    [data-baseweb="tooltip"] > div,
    [data-testid="stTooltipContent"],
    [role="tooltip"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.45) !important;
    }
    [data-baseweb="tooltip"] *,
    [data-testid="stTooltipContent"] *,
    [role="tooltip"] * {
        color: #f8fafc !important;
        background-color: transparent !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #334155 !important;
        background-color: #111827 !important;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button,
    [data-testid="stPopover"] button {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover,
    [data-testid="stPopover"] button:hover {
        background-color: #334155 !important;
    }
    [data-testid="stButtonGroup"] button,
    [data-testid="stPills"] button,
    [data-testid="stSegmentedControl"] button {
        background-color: #1e293b !important;
        border-color: #475569 !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stButtonGroup"] button [data-testid="stMarkdownContainer"] p,
    [data-testid="stPills"] button [data-testid="stMarkdownContainer"] p,
    [data-testid="stSegmentedControl"] button [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }
    [data-testid="stButtonGroup"] button[aria-checked="true"],
    [data-testid="stButtonGroup"] button[aria-pressed="true"],
    [data-testid="stButtonGroup"] button[data-selected="true"],
    [data-testid="stPills"] button[aria-checked="true"],
    [data-testid="stPills"] button[aria-pressed="true"],
    [data-testid="stSegmentedControl"] button[aria-checked="true"],
    [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background-color: #14532d !important;
        border-color: #4ade80 !important;
        color: #ffffff !important;
    }
    [data-testid="stButtonGroup"] button[aria-checked="true"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stButtonGroup"] button[aria-pressed="true"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stButtonGroup"] button[data-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    [data-testid="stCaptionContainer"] p {
        color: #cbd5e1 !important;
    }
    [data-testid="stTooltipIcon"] svg {
        color: #94a3b8 !important;
        stroke: #94a3b8 !important;
    }
    [data-testid="stAlert"] {
        background-color: #1e293b !important;
        border-color: #334155 !important;
        color: #f8fafc !important;
    }
        """
        if dark_mode
        else ""
    )

    return f"""
<style>
    [data-testid="stHeader"] {{
        background: {header_bg} !important;
        height: 3.75rem !important;
        min-height: 3.75rem !important;
        backdrop-filter: blur(6px);
        z-index: 9990 !important;
    }}
    [data-testid="stMainBlockContainer"],
    .block-container {{
        padding-top: 4.55rem !important;
        padding-bottom: 2.8rem !important;
        max-width: 1460px !important;
    }}
    [data-testid="InputInstructions"] {{
        display: none !important;
    }}
    [data-testid="stHeaderActionElements"] a {{
        display: none !important;
    }}
    [data-testid="stSidebarCollapseButton"] {{
        opacity: 1 !important;
        visibility: visible !important;
    }}
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stExpandSidebarButton"] {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.45rem !important;
        background: {sidebar_btn_bg} !important;
        border: 1.5px solid {sidebar_btn_border} !important;
        color: {sidebar_btn_col} !important;
        border-radius: 9px !important;
        padding: 0.42rem 0.9rem !important;
        min-height: 38px !important;
        width: auto !important;
        max-width: none !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.12) !important;
        opacity: 1 !important;
    }}
    [data-testid="stExpandSidebarButton"] {{
        background: {sidebar_expand_bg} !important;
        border-width: 2px !important;
    }}
    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="stExpandSidebarButton"] svg {{
        width: 22px !important;
        height: 22px !important;
        color: {sidebar_btn_col} !important;
        fill: {sidebar_btn_col} !important;
    }}
    [data-testid="stSidebarCollapseButton"] button::before {{
        content: "Masquer les filtres";
        font-size: 0.88rem;
        font-weight: 700;
        color: {sidebar_btn_col};
        white-space: nowrap;
    }}
    [data-testid="stExpandSidebarButton"]::after {{
        content: "Afficher les filtres";
        font-size: 0.9rem;
        font-weight: 700;
        color: {sidebar_btn_col};
        white-space: nowrap;
    }}
    .st-key-theme_toggle_btn {{
        position: fixed !important;
        top: 0.62rem !important;
        right: 4.5rem !important;
        z-index: 999995 !important;
        width: auto !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    .st-key-theme_toggle_btn button {{
        width: 38px !important;
        height: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        border-radius: 999px !important;
        background: {toggle_bg} !important;
        border: 1.5px solid {toggle_border} !important;
        color: {toggle_col} !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.14) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0 !important;
    }}
    .st-key-theme_toggle_btn button:hover {{
        background: {toggle_hover} !important;
    }}
    .st-key-theme_toggle_btn button [data-testid="stMarkdownContainer"] {{
        display: none !important;
    }}
    .st-key-theme_toggle_btn button span,
    .st-key-theme_toggle_btn button svg {{
        color: {toggle_col} !important;
        fill: {toggle_col} !important;
        margin: 0 !important;
    }}
    [data-testid="stTabs"] {{
        margin-top: 3.25rem !important;
    }}
    [data-testid="stTabs"] [role="tablist"] {{
        display: flex !important;
        width: 100% !important;
        gap: 0 !important;
        background: {tab_bar_bg} !important;
        border: 1.5px solid {tab_bar_border} !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin-bottom: 1.15rem !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08) !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"] {{
        flex: 1 1 0 !important;
        margin: 0 !important;
        padding: 0.9rem 1.15rem !important;
        background: {tab_bar_bg} !important;
        border: none !important;
        border-left: 1.5px solid {tab_bar_border} !important;
        border-radius: 0 !important;
        min-height: 56px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: none !important;
        transition: background-color 0.16s ease, color 0.16s ease !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"]:first-of-type {{
        border-left: none !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"]:not([aria-selected="true"]):hover {{
        background: {tab_bar_hover} !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"] p,
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"] span {{
        font-size: 1.24rem !important;
        font-weight: 700 !important;
        color: {tab_inactive_col} !important;
        letter-spacing: -0.01em !important;
        line-height: 1.25 !important;
        margin: 0 !important;
        text-align: center !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"][aria-selected="true"] {{
        background: {tab_active_bg} !important;
        border-bottom: none !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"][aria-selected="true"] p,
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"][aria-selected="true"] span {{
        color: {tab_active_col} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"]::before,
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"]::after,
    [data-testid="stTabs"] [role="tablist"] [data-testid="stTab"] .react-aria-SelectionIndicator,
    [data-testid="stTabs"] [role="tablist"]::after {{
        display: none !important;
        content: none !important;
        border: none !important;
    }}
    .js-plotly-plot .plotly .modebar {{
        top: 0px !important;
        right: 4px !important;
        background: {modebar_bg} !important;
        background-color: {modebar_bg} !important;
        border: 1.5px solid {modebar_border} !important;
        border-radius: 8px !important;
        padding: 2px 4px !important;
        margin: 0 !important;
        overflow: hidden !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0 !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.12) !important;
        opacity: 1 !important;
    }}
    .js-plotly-plot .plotly .modebar-group {{
        background: {modebar_bg} !important;
        background-color: {modebar_bg} !important;
        margin: 0 !important;
        padding: 2px 3px !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        display: inline-flex !important;
        align-items: center !important;
        float: none !important;
    }}
    .js-plotly-plot .plotly .modebar-btn {{
        background: transparent !important;
        padding: 3px 5px !important;
        margin: 0 !important;
        border-radius: 4px !important;
    }}
    .js-plotly-plot .plotly .modebar-btn:hover {{
        background: #cbd5e1 !important;
    }}
    .js-plotly-plot .plotly .modebar-btn path {{
        fill: {modebar_icon} !important;
    }}
    .js-plotly-plot .plotly .modebar-btn:hover path,
    .js-plotly-plot .plotly .modebar-btn.active path {{
        fill: {modebar_hover} !important;
    }}
    [data-testid="stWidgetLabel"] {{
        width: fit-content !important;
        max-width: 100% !important;
        justify-content: flex-start !important;
        gap: 0.42rem !important;
    }}
    [data-testid="stWidgetLabel"] > div:first-child {{
        flex: 0 0 auto !important;
        width: fit-content !important;
    }}
    [data-testid="stTooltipIcon"] {{
        margin-left: 0 !important;
    }}
    .hero-banner {{
        background: {hero_bg};
        border: 1.5px solid {hero_border};
        color: {hero_title_col};
        padding: 1.28rem 1.65rem;
        border-radius: 14px;
        margin-top: 0.35rem;
        margin-bottom: 1.05rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        overflow: visible;
    }}
    .hero-title {{
        font-size: 2.72rem;
        font-weight: 400;
        color: {hero_title_col};
        letter-spacing: -0.025em;
        line-height: 1.12;
        margin: 0 0 0.45rem 0;
    }}
    .hero-subtitle {{
        font-size: 1.12rem;
        color: {hero_sub_col};
        opacity: 1;
        margin: 0 0 0.85rem 0;
        line-height: 1.45;
    }}
    .hero-pills {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem;
    }}
    .hero-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.42rem;
        background: {hero_pill_bg};
        border: 1px solid {hero_pill_border};
        color: {hero_pill_col};
        border-radius: 999px;
        padding: 0.32rem 0.92rem;
        font-size: 0.94rem;
        font-weight: 500;
        white-space: nowrap;
    }}
    .hero-tip-wrap {{
        position: relative;
        display: inline-flex;
        align-items: center;
    }}
    .hero-tip-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 19px;
        height: 19px;
        border-radius: 50%;
        border: 1.5px solid {hero_tip_btn_border};
        background: {hero_tip_btn_bg};
        color: {hero_tip_btn_col};
        font-size: 0.76rem;
        font-weight: 700;
        cursor: help;
        line-height: 1;
    }}
    .hero-tip-box {{
        display: none;
        position: absolute;
        top: 135%;
        left: 0;
        width: 355px;
        max-width: 82vw;
        background: {tip_box_bg};
        color: #f8fafc;
        border: 1px solid {tip_box_border};
        border-radius: 9px;
        padding: 0.75rem 0.9rem;
        font-size: 0.82rem;
        line-height: 1.5;
        white-space: normal;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.35);
        z-index: 9999;
    }}
    .hero-pill:last-child .hero-tip-box {{
        left: auto;
        right: 0;
    }}
    .hero-pill:hover .hero-tip-box,
    .hero-tip-wrap:hover .hero-tip-box {{
        display: block;
    }}
    .kpi-card {{
        background: {card_bg};
        border: 1px solid {border_col};
        border-top: 4px solid #15803d;
        border-radius: 10px;
        padding: 0.78rem 0.95rem;
        margin-bottom: 1.35rem;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.06);
        min-height: 112px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .kpi-label {{
        font-size: 0.74rem;
        color: {text_muted};
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }}
    .kpi-value {{
        font-size: 1.46rem;
        font-weight: 800;
        color: {text_primary};
        line-height: 1.2;
        margin: 0.2rem 0;
    }}
    .kpi-sub {{
        font-size: 0.77rem;
        color: {text_muted};
        line-height: 1.3;
    }}
    .detail-header {{
        background: {card_alt_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
    }}
    .detail-title {{
        font-size: 1.1rem;
        font-weight: 800;
        color: {text_primary};
        margin-bottom: 0.25rem;
    }}
    .detail-meta {{
        font-size: 0.83rem;
        color: {text_secondary};
        margin-bottom: 0.55rem;
        line-height: 1.45;
    }}
    .badge-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }}
    .badge-pill {{
        display: inline-block;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.74rem;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        white-space: nowrap;
    }}
    .code-chip {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.8rem;
        color: {code_col};
        background: {code_bg};
        padding: 0.06rem 0.3rem;
        border-radius: 4px;
    }}
    .mini-metric-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }}
    .mini-metric-box {{
        background: {card_bg};
        border: 1px solid {border_col};
        border-radius: 8px;
        padding: 0.55rem 0.65rem;
    }}
    .mini-metric-label {{
        font-size: 0.71rem;
        color: {text_muted};
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }}
    .mini-metric-val {{
        font-size: 1.12rem;
        font-weight: 800;
        color: {text_primary};
        margin-top: 0.16rem;
        white-space: nowrap;
    }}
    .idea-block {{
        font-size: 0.98rem;
        color: {text_secondary};
        line-height: 1.62;
        margin-bottom: 1.05rem;
    }}
    .idea-block:last-child {{
        margin-bottom: 0.35rem;
    }}
    .idea-card {{
        background: {card_alt_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 0.95rem 1.15rem;
        margin-bottom: 1.05rem;
        font-size: 0.97rem;
        color: {text_secondary};
        line-height: 1.62;
    }}
    .ivt-card-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 0.5rem;
    }}
    .ivt-pill-line {{
        margin-top: 0.38rem;
        color: {text_secondary};
        line-height: 1.55;
    }}
    .nw {{
        white-space: nowrap;
    }}
    .ivt-card {{
        background: {card_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 0.85rem 0.95rem;
        margin-top: 0.65rem;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.05);
    }}
    .card-kicker {{
        font-size: 0.76rem;
        font-weight: 700;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.65rem;
    }}
    .ivt-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    .ivt-score-num {{
        font-size: 1.45rem;
        font-weight: 800;
        color: {text_primary};
    }}
    .ivt-track {{
        width: 100%;
        height: 8px;
        background: {track_bg};
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 0.7rem;
    }}
    .ivt-fill {{
        height: 100%;
        border-radius: 999px;
    }}
    .ivt-pillar-row {{
        margin-bottom: 0.48rem;
    }}
    .ivt-pillar-row:last-child {{
        margin-bottom: 0;
    }}
    .ivt-pillar-top {{
        display: flex;
        justify-content: space-between;
        font-size: 0.77rem;
        color: {text_secondary};
        margin-bottom: 0.16rem;
    }}
    .ivt-pillar-track {{
        width: 100%;
        height: 6px;
        background: {track_bg};
        border-radius: 999px;
        overflow: hidden;
    }}
    .map-legend-bar {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.7rem 1.2rem;
        background: {card_alt_bg};
        border: 1px solid {border_col};
        border-radius: 9px;
        padding: 0.65rem 1.05rem;
        margin-top: 0.45rem;
        font-size: 0.96rem;
        color: {text_primary};
        line-height: 1.5;
    }}
    .legend-dot {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.38rem;
        vertical-align: middle;
    }}
    .legend-poly {{
        display: inline-block;
        width: 14px;
        height: 11px;
        margin-right: 0.38rem;
        vertical-align: middle;
        border-radius: 2px;
    }}
    .empty-sel-card {{
        background: {card_alt_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 1.05rem 1.15rem;
        margin-bottom: 0.75rem;
    }}
    .empty-sel-title {{
        font-size: 1.05rem;
        font-weight: 800;
        color: {text_primary};
        margin-bottom: 0.35rem;
    }}
    .empty-sel-sub {{
        font-size: 0.86rem;
        color: {text_secondary};
        line-height: 1.45;
    }}
    .dash-sort-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 0.45rem;
    }}
    .dash-filter-summary {{
        font-size: 1.0rem;
        color: {text_primary};
        font-weight: 500;
        margin: 0.55rem 0 0.55rem 0;
    }}
    .chart-title-bar {{
        font-size: 0.97rem;
        font-weight: 700;
        color: {text_primary};
        margin: 0.35rem 0 0.25rem 0;
    }}
    .disclaimer-box {{
        background: {disclaimer_bg};
        border: 1px solid {disclaimer_border};
        border-left: 4px solid {disclaimer_accent};
        border-radius: 8px;
        padding: 0.75rem 0.95rem;
        font-size: 0.83rem;
        color: {disclaimer_col};
        margin-top: 0.75rem;
        line-height: 1.5;
    }}
    {dark_overrides}
    [data-testid="stDownloadButton"] button {{
        background: {dl_bg} !important;
        border: 1.5px solid {dl_border} !important;
        color: #000000 !important;
        border-radius: 10px !important;
        min-height: 44px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: {dl_hover} !important;
        border-color: #475569 !important;
        color: #000000 !important;
    }}
    [data-testid="stDownloadButton"] button *,
    [data-testid="stDownloadButton"] button [data-testid="stMarkdownContainer"] p,
    [data-testid="stDownloadButton"] button svg {{
        color: #000000 !important;
        fill: #000000 !important;
    }}
</style>
"""


CUSTOM_CSS = get_theme_css(False)


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
            f"{nb_inst} <span style='font-size:0.9rem;opacity:0.72;'>/ {total_inst}</span>",
            f"{fmt_int(nb_eq)} équipements équestres",
        ),
        (
            k2,
            "#ea580c",
            "À 1 km ou moins",
            f"{nb_1km} <span style='font-size:0.9rem;opacity:0.72;'>({pct_1km:.1f}%)</span>",
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
            "Sur 352 communes équipées",
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
            <span><strong>Couleur des points (distance) :</strong></span>
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
            <div class="empty-sel-title">
                Aucune installation sélectionnée
            </div>
            <div class="empty-sel-sub">
                Veuillez sélectionner une installation pour afficher sa fiche détaillée.
            </div>
        </div>
        <div class="ivt-card" style="margin-top:0;">
            <div class="card-kicker">
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
            <div class="detail-title">
                {html.escape(str(sel_row['nom_installation']))}
            </div>
            <div class="detail-meta">
                <strong>Adresse :</strong> {html.escape(addr_line)} — <b>{html.escape(str(sel_row['departement']))} ({html.escape(str(sel_row['departement_code']))})</b>
            </div>
            <div class="detail-meta" style="font-size:0.8rem;">
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


def render_collapsible_action_cards(
    items: list[ActionItem],
    *,
    positive: bool,
    dark_mode: bool = False,
) -> None:
    """Affiche les pistes d'action en grille équilibrée : titre en gras replié par défaut avec flèche."""
    if not items:
        return

    if dark_mode:
        bg = "#062c1c" if positive else "#3b2307"
        border = "#166534" if positive else "#92400e"
        accent = "#4ade80" if positive else "#fbbf24"
        title_col = "#f8fafc"
        detail_col = "#e2e8f0"
        why_col = "#cbd5e1"
    else:
        bg = "#f0fdf4" if positive else "#fffbeb"
        border = "#bbf7d0" if positive else "#fde68a"
        accent = "#15803d" if positive else "#d97706"
        title_col = "#0f172a"
        detail_col = "#334155"
        why_col = "#64748b"
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
                color: {title_col};
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
                color: {detail_col};
                line-height: 1.5;
            }}
            .{variant_cls} .ev-action-why {{
                font-size: 0.76rem;
                color: {why_col};
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
    dark_mode: bool = False,
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
    est_table_h = 46 + len(df) * 38
    iframe_h = min(scroll_h + 18, max(92, est_table_h + 12))
    popup_max_h = 345

    if dark_mode:
        t_text = "#f8fafc"
        t_head_text = "#e2e8f0"
        t_muted = "#cbd5e1"
        t_bg = "#111827"
        t_head_bg = "#1e293b"
        t_border = "#334155"
        t_cell_border = "#1e293b"
        t_hover_bg = "#1e293b"
        t_btn_bg = "#1e293b"
        t_btn_hover = "#334155"
        t_btn_border = "#475569"
        t_popup_bg = "#1e293b"
        t_popup_head_bg = "#0f172a"
        t_popup_hover_col = "#4ade80"
        t_track_bg = "#334155"
        t_bar_col = "#38bdf8"
        t_scroll_thumb = "#475569"
        t_scroll_track = "#111827"
    else:
        t_text = "#0f172a"
        t_head_text = "#334155"
        t_muted = "#334155"
        t_bg = "#ffffff"
        t_head_bg = "#f8fafc"
        t_border = "#e2e8f0"
        t_cell_border = "#f1f5f9"
        t_hover_bg = "#f8fafc"
        t_btn_bg = "#ffffff"
        t_btn_hover = "#e2e8f0"
        t_btn_border = "#cbd5e1"
        t_popup_bg = "#ffffff"
        t_popup_head_bg = "#f1f5f9"
        t_popup_hover_col = "#15803d"
        t_track_bg = "#e2e8f0"
        t_bar_col = "#0284c7"
        t_scroll_thumb = "#cbd5e1"
        t_scroll_track = "#f8fafc"

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
        font-size: 13px;
        color: {t_text};
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
        background: {t_head_bg};
        border: 1px solid {t_btn_border};
        color: {t_text};
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 12.5px;
        font-weight: 600;
        cursor: pointer;
    }}
    #{root_id} .ft-reset-btn:hover {{
        background: {t_btn_hover};
    }}
    #{root_id} .ft-scroll {{
        max-height: {scroll_h}px;
        overflow: auto;
        border: 1px solid {t_border};
        border-radius: 10px;
        background: {t_bg};
        scrollbar-width: thin;
        scrollbar-color: {t_scroll_thumb} {t_scroll_track};
    }}
    #{root_id} .ft-scroll::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    #{root_id} .ft-scroll::-webkit-scrollbar-track {{
        background: {t_scroll_track};
        border-radius: 8px;
    }}
    #{root_id} .ft-scroll::-webkit-scrollbar-thumb {{
        background: {t_scroll_thumb};
        border-radius: 8px;
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
        background: {t_head_bg};
        border-bottom: 1px solid {t_border};
        border-right: 1px solid {t_cell_border};
        padding: 8px 7px;
        text-align: left;
        font-weight: 700;
        font-size: 12.2px;
        color: {t_head_text};
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
        gap: 4px;
    }}
    #{root_id} .ft-menu-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 5px;
        border: 1px solid {t_btn_border};
        background: {t_btn_bg};
        color: {t_head_text};
        cursor: pointer;
        flex-shrink: 0;
        padding: 0;
    }}
    #{root_id} .ft-menu-btn:hover {{
        background: {t_btn_hover};
        color: {t_text};
    }}
    #{root_id} tbody td {{
        padding: 7px 7px;
        border-bottom: 1px solid {t_cell_border};
        border-right: 1px solid {t_cell_border};
        color: {t_text};
        vertical-align: top;
        line-height: 1.35;
        font-size: 12.6px;
    }}
    #{root_id} tbody tr:hover td {{
        background: {t_hover_bg};
    }}
    #{root_id} .ft-wide {{
        min-width: 135px;
        white-space: normal;
    }}
    #{root_id} .ft-num {{
        text-align: right;
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
    }}
    #{root_id} .ft-popup {{
        display: none;
        position: absolute;
        z-index: 999;
        width: 276px;
        max-height: {popup_max_h}px;
        overflow-y: auto;
        background: {t_popup_bg};
        border: 1px solid {t_btn_border};
        border-radius: 10px;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.28);
        padding: 6px;
        scrollbar-width: thin;
        scrollbar-color: {t_scroll_thumb} {t_popup_bg};
    }}
    #{root_id} .ft-popup-head {{
        font-weight: 700;
        font-size: 12.4px;
        color: {t_text};
        background: {t_popup_head_bg};
        border-radius: 6px;
        padding: 5px 8px;
        margin-bottom: 4px;
        word-break: break-word;
    }}
    #{root_id} .ft-popup-item {{
        display: block;
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        border-radius: 6px;
        padding: 5px 8px;
        font-size: 12.5px;
        color: {t_text};
        cursor: pointer;
    }}
    #{root_id} .ft-popup-item:hover {{
        background: {t_popup_head_bg};
        color: {t_popup_hover_col};
    }}
    #{root_id} .ft-stats-box {{
        display: none;
        margin-top: 4px;
        padding: 6px 8px;
        border-top: 1px solid {t_border};
        font-size: 12px;
        color: {t_muted};
    }}
    #{root_id} .ft-stats-title {{
        margin-top: 4px;
        font-weight: 700;
        color: {t_text};
    }}
    #{root_id} .ft-stat-kv {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px;
    }}
    #{root_id} .ft-bar-row {{
        margin-top: 4px;
    }}
    #{root_id} .ft-bar-lbl {{
        display: flex;
        justify-content: space-between;
        gap: 6px;
        font-size: 11.4px;
        margin-bottom: 2px;
    }}
    #{root_id} .ft-bar-lbl span:first-child {{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 175px;
    }}
    #{root_id} .ft-bar-track {{
        height: 5px;
        background: {t_track_bg};
        border-radius: 999px;
        overflow: hidden;
    }}
    #{root_id} .ft-bar-fill {{
        height: 100%;
        background: {t_bar_col};
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
    const scrollBox = root.querySelector(".ft-scroll");

    function syncHeight() {{
        try {{
            const baseH = scrollBox.offsetTop + scrollBox.offsetHeight + 8;
            let targetH = baseH;
            if (popup.style.display === "block") {{
                const popBottom = popup.offsetTop + popup.offsetHeight + 12;
                if (popBottom > targetH) targetH = popBottom;
            }}
            if (window.frameElement) {{
                window.frameElement.style.height = targetH + "px";
                if (window.frameElement.parentElement) {{
                    window.frameElement.parentElement.style.height = targetH + "px";
                }}
            }}
        }} catch (_) {{}}
    }}

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
            h += '<div class="ft-stats-title">Valeurs les plus fréquentes</div>';
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
            syncHeight();
            return;
        }}
        activeCol = idx;
        popupHead.textContent = data.cols[idx];
        statsBox.style.display = "none";
        statsBox.innerHTML = buildStatsHtml(idx);
        popup.style.display = "block";
        const rootRect = root.getBoundingClientRect();
        const btnRect = btn.getBoundingClientRect();
        const topPos = Math.max(2, btnRect.bottom - rootRect.top + 4);
        let leftPos = btnRect.left - rootRect.left;
        if (leftPos + 285 > rootRect.width) {{
            leftPos = Math.max(4, btnRect.right - rootRect.left - 280);
        }}
        popup.style.top = topPos + "px";
        popup.style.left = leftPos + "px";
        syncHeight();
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
            syncHeight();
        }} else if (act === "stats") {{
            statsBox.style.display = statsBox.style.display === "block" ? "none" : "block";
            syncHeight();
        }} else if (act === "hide") {{
            hiddenCols.add(activeCol);
            renderHeader();
            renderBody();
            popup.style.display = "none";
            syncHeight();
        }}
    }});

    resetBtn.addEventListener("click", () => {{
        hiddenCols.clear();
        renderHeader();
        renderBody();
        syncHeight();
    }});

    document.addEventListener("click", () => {{
        if (popup.style.display === "block") {{
            popup.style.display = "none";
            syncHeight();
        }}
    }});

    renderHeader();
    renderBody();
    syncHeight();
    window.addEventListener("resize", syncHeight);
}})();
</script>
</body>
</html>"""

    components.html(doc_html, height=iframe_h, scrolling=False)
