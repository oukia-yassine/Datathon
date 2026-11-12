"""Application principale Streamlit — ÉquiVigie Normandie."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

from src.data_loader import (
    IVT_ORDER,
    VIGILANCE_COLORS,
    VIGILANCE_ORDER,
    compute_department_summary,
    compute_natura_hotspots,
    load_equipments,
    load_installations,
    load_natura_geojson,
    split_activity_values,
    split_semicolon_values,
)
from src.map_builder import BASEMAP_CHOICES, build_interactive_map
from src.natura_taxonomy import TYPOLOGIES, classify_natura_site
from src.ui_components import (
    get_theme_css,
    render_collapsible_action_cards,
    render_empty_selection_panel,
    render_french_table,
    render_idea_blocks,
    render_installation_identity_and_ivt,
    render_kpi_row,
    render_map_legend,
)

ROOT_DIR = Path(__file__).resolve().parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

TYPOLOGY_COLOR_MAP: dict[str, str] = {
    t.short_label: t.badge_color for t in TYPOLOGIES.values()
}


st.set_page_config(
    page_title="ÉquiVigie Normandie",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

dark_mode = bool(st.session_state["dark_mode"])
st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)

if st.button(
    "",
    icon=":material/light_mode:" if dark_mode else ":material/dark_mode:",
    key="theme_toggle_btn",
    help="Passer en mode clair" if dark_mode else "Passer en mode sombre",
):
    st.session_state["dark_mode"] = not dark_mode
    st.rerun()


@st.cache_data(show_spinner="Chargement des données territoriales...")
def get_loaded_data():
    """Charge une seule fois les données normalisées et les garde en cache."""
    eq_df = load_equipments(RAW_DIR / "equipements_equestres_normandie.csv")
    inst_df, diagnostics = load_installations(
        RAW_DIR / "installations_proximite_natura2000.csv",
        equipments_df=eq_df,
    )
    opt_geojson_path = PROCESSED_DIR / "natura2000_simplifie.geojson"
    raw_geojson_path = RAW_DIR / "natura2000_zsc_zps_normandie.geojson"
    natura_path = opt_geojson_path if opt_geojson_path.exists() else raw_geojson_path
    natura_geojson = load_natura_geojson(natura_path, inst_df)
    return eq_df, inst_df, diagnostics, natura_geojson


eq_df, inst_df, diagnostics, natura_geojson = get_loaded_data()


def _reset_filters() -> None:
    for key in (
        "f_depts",
        "f_vig",
        "f_ivt_levels",
        "f_use_dist",
        "f_max_dist",
        "f_typologies",
        "f_natura_site",
        "f_equip_types",
        "f_activites",
        "f_search",
    ):
        if key in st.session_state:
            del st.session_state[key]


with st.sidebar:
    st.markdown("### Filtres territoriaux")
    st.button(
        "Réinitialiser les filtres",
        on_click=_reset_filters,
        key="reset_filters_btn",
        width="stretch",
    )

    search_txt = st.text_input(
        "Recherche rapide",
        value="",
        key="f_search",
        placeholder="Installation, commune, CP, site Natura...",
        help=(
            "Filtre instantanément les établissements affichés à partir du nom d'installation, "
            "de la commune, du code postal (ex. 14, 50480) ou du nom d'une zone Natura 2000."
        ),
    )

    all_depts = sorted(inst_df["departement"].unique().tolist())
    sel_depts = st.pills(
        "Départements",
        options=all_depts,
        selection_mode="multi",
        default=all_depts,
        key="f_depts",
    )

    sel_vig = st.pills(
        "Proximité Natura 2000",
        options=VIGILANCE_ORDER,
        selection_mode="multi",
        default=VIGILANCE_ORDER,
        key="f_vig",
    )

    sel_ivt_levels = st.pills(
        "Niveau de vigilance IVT",
        options=IVT_ORDER,
        selection_mode="multi",
        default=IVT_ORDER,
        key="f_ivt_levels",
    )

    all_typs = [t.short_label for t in TYPOLOGIES.values()]
    sel_typs = st.pills(
        "Typologie écologique du site le plus proche",
        options=all_typs,
        selection_mode="multi",
        default=all_typs,
        key="f_typologies",
    )

    with st.expander("Filtres avancés (seuil m, site, équipements)", expanded=False):
        use_dist_slider = st.checkbox(
            "Filtrer par seuil de distance maximal",
            value=False,
            key="f_use_dist",
            help="Permet de tester différents rayons exploratoires (ex. 500 m, 1 000 m, 2 000 m).",
        )
        max_dist_m = None
        if use_dist_slider:
            max_dist_m = st.slider(
                "Distance maximale au site Natura 2000 (m)",
                min_value=0,
                max_value=5000,
                value=1000,
                step=100,
                key="f_max_dist",
            )

        natura_sites = sorted(
            set(inst_df["natura_plus_proche_nom"].dropna().astype(str))
            | set(inst_df["zsc_plus_proche_nom"].dropna().astype(str))
            | set(inst_df["zps_plus_proche_nom"].dropna().astype(str))
        )
        sel_natura_site = st.selectbox(
            "Cibler un site Natura 2000",
            options=["Tous les sites"] + natura_sites,
            index=0,
            key="f_natura_site",
        )

        all_eq_types = split_semicolon_values(inst_df["types_equipements"])
        sel_eq_types = st.multiselect(
            "Type d'équipement",
            options=all_eq_types,
            default=[],
            key="f_equip_types",
            placeholder="Tous les équipements",
        )

        all_acts = split_activity_values(inst_df["activites"])
        sel_acts = st.multiselect(
            "Activité équestre pratiquée",
            options=all_acts,
            default=[],
            key="f_activites",
            placeholder="Toutes les activités",
        )


mask = (
    inst_df["departement"].isin(sel_depts)
    & inst_df["niveau_vigilance_descriptif"].isin(sel_vig)
    & inst_df["ivt_niveau"].isin(sel_ivt_levels)
    & inst_df["typologie_short"].isin(sel_typs)
)

if max_dist_m is not None:
    mask &= inst_df["distance_natura_m"] <= float(max_dist_m)

if sel_natura_site != "Tous les sites":
    mask &= (
        (inst_df["natura_plus_proche_nom"] == sel_natura_site)
        | (inst_df["zsc_plus_proche_nom"] == sel_natura_site)
        | (inst_df["zps_plus_proche_nom"] == sel_natura_site)
    )

if sel_eq_types:
    mask &= inst_df["types_equipements"].apply(
        lambda val: any(t in [x.strip() for x in str(val).split(";")] for t in sel_eq_types)
    )

if sel_acts:
    mask &= inst_df["activites"].apply(
        lambda val: any(
            a in [x.strip() for chunk in str(val).split(";") for x in chunk.split(",")]
            for a in sel_acts
        )
    )

if search_txt.strip():
    q = search_txt.strip().lower()
    mask &= (
        inst_df["nom_installation"].str.lower().str.contains(q, na=False)
        | inst_df["commune"].str.lower().str.contains(q, na=False)
        | inst_df["inst_cp"].str.lower().str.contains(q, na=False)
        | inst_df["natura_plus_proche_nom"].str.lower().str.contains(q, na=False)
    )

df_filtered = inst_df[mask].sort_values(
    ["ivt_score", "priorite_rang", "distance_natura_m", "nom_installation"],
    ascending=[False, True, True, True],
).copy()

with st.sidebar:
    st.caption(f"Sélection active : **{len(df_filtered)} / {len(inst_df)}** installations normandes")


st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">ÉquiVigie Normandie</div>
        <div class="hero-subtitle">
            Plateforme d'aide à la décision territoriale : interactions entre activités équestres et zones naturelles protégées (Natura 2000)
        </div>
        <div class="hero-pills">
            <span class="hero-pill">
                421 installations et 1 175 équipements équestres
                <span class="hero-tip-wrap">
                    <span class="hero-tip-btn" tabindex="0">?</span>
                    <span class="hero-tip-box">
                        <strong>Installation vs équipement : quelle différence ?</strong><br/><br/>
                        <strong>Équipement équestre (1 175) :</strong> unité pratique ou infrastructure recensée sur le terrain (carrière, manège, piste de galop, écurie, parcours de cross…).<br/><br/>
                        <strong>Installation (421) :</strong> site géographique regroupant un ou plusieurs équipements (ex. un centre équestre avec 2 carrières et 1 manège = 1 installation pour 3 équipements).<br/><br/>
                        Ce regroupement évite de compter plusieurs fois un même établissement dans les distances et le calcul de l'IVT.
                    </span>
                </span>
            </span>
            <span class="hero-pill">
                96 zones naturelles (82 ZSC et 14 ZPS)
                <span class="hero-tip-wrap">
                    <span class="hero-tip-btn" tabindex="0">?</span>
                    <span class="hero-tip-box">
                        <strong>Que signifient ZSC et ZPS ?</strong><br/><br/>
                        <strong>ZSC (Zone Spéciale de Conservation) :</strong> site Natura 2000 désigné au titre de la directive <em>Habitats</em> pour protéger des milieux naturels, la flore et la faune (hors oiseaux).<br/><br/>
                        <strong>ZPS (Zone de Protection Spéciale) :</strong> site Natura 2000 désigné au titre de la directive <em>Oiseaux</em> pour préserver les espèces d'oiseaux sauvages menacées et leurs habitats.
                    </span>
                </span>
            </span>
            <span class="hero-pill">
                IVT (Indicateur de Vigilance Territoriale)
                <span class="hero-tip-wrap">
                    <span class="hero-tip-btn" tabindex="0">?</span>
                    <span class="hero-tip-box">
                        <strong>À quoi sert l'IVT ?</strong><br/>
                        Calculé en pourcentage, il classe les installations à examiner en priorité en combinant :
                        la distance aux zones Natura 2000, la proximité d'habitats et d'oiseaux protégés (ZSC/ZPS),
                        la sensibilité écologique du milieu et la densité d'équipements.<br/><br/>
                        <strong>Proximité ≠ impact causal :</strong> un pourcentage élevé signale une proximité géographique
                        méritant un échange ou un diagnostic sur place, jamais une preuve de dégradation écologique.
                    </span>
                </span>
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

nb_inst = len(df_filtered)
nb_eq = int(df_filtered["nombre_equipements"].sum()) if nb_inst else 0
nb_1km = int(df_filtered["natura_a_1km"].sum()) if nb_inst else 0
pct_1km = round(nb_1km / nb_inst * 100.0, 1) if nb_inst else 0.0
nb_inside = int(df_filtered["dans_natura"].sum()) if nb_inst else 0
med_dist = float(df_filtered["distance_natura_m"].median()) if nb_inst else None
mean_ivt = float(df_filtered["ivt_score"].mean()) if nb_inst else None
nb_ivt_high = int((df_filtered["ivt_score"] >= 70.0).sum()) if nb_inst else 0
nb_communes = int(df_filtered["commune"].nunique()) if nb_inst else 0

render_kpi_row(
    nb_inst=nb_inst,
    total_inst=len(inst_df),
    nb_eq=nb_eq,
    nb_1km=nb_1km,
    pct_1km=pct_1km,
    nb_inside=nb_inside,
    med_dist=med_dist,
    mean_ivt=mean_ivt,
    nb_ivt_high=nb_ivt_high,
    nb_communes=nb_communes,
)

tab_map, tab_dash, tab_method = st.tabs(
    [
        "Carte interactive & Fiche territoriale",
        "Tableau de bord & Priorisation",
        "Méthodologie",
    ]
)


with tab_map:
    if df_filtered.empty:
        st.warning(
            "Aucune installation ne correspond aux filtres sélectionnés. "
            "Ajustez ou réinitialisez les filtres dans la barre latérale."
        )
    else:
        available_ids = df_filtered["inst_numero"].tolist()

        if "pending_inst_id" in st.session_state:
            cand_id = st.session_state.pop("pending_inst_id")
            if cand_id in available_ids:
                st.session_state["selected_inst_id"] = cand_id

        if (
            "selected_inst_id" in st.session_state
            and st.session_state["selected_inst_id"] is not None
            and st.session_state["selected_inst_id"] not in available_ids
        ):
            st.session_state["selected_inst_id"] = None

        if "last_map_click" not in st.session_state:
            st.session_state["last_map_click"] = None

        label_map = {
            r["inst_numero"]: (
                f"{r['nom_installation']} — {r['commune']} ({r['departement_code']}) "
                f"— {r['distance_natura_m']:.1f} m — IVT {r['ivt_score']:.1f} %"
            )
            for _, r in df_filtered.iterrows()
        }

        st.selectbox(
            "Installation sélectionnée",
            options=available_ids,
            index=None,
            placeholder="Cliquez sur un point de la carte ou sélectionnez une installation...",
            format_func=lambda x: label_map.get(x, x),
            help="Cliquez directement sur un point de la carte ou choisissez une installation dans cette liste.",
            key="selected_inst_id",
        )

        selected_id = st.session_state.get("selected_inst_id")
        if selected_id != st.session_state.get("_prev_selected_id"):
            st.session_state["_prev_selected_id"] = selected_id
            if selected_id is not None:
                st.session_state["focus_selected_chk"] = True

        col_map, col_card = st.columns([7, 5], gap="large")

        with col_map:
            tb1, tb2, tb3 = st.columns([1.45, 1.55, 1.45], gap="small", vertical_alignment="bottom")
            with tb1:
                with st.popover("Afficher sur la carte", width="stretch"):
                    show_zsc = st.checkbox(
                        "Natura 2000 — ZSC Habitats (82)",
                        value=True,
                        key="layer_zsc",
                        help="ZSC (Zone Spéciale de Conservation — Directive Habitats) : protège les milieux naturels et espèces hors oiseaux.",
                    )
                    show_zps = st.checkbox(
                        "Natura 2000 — ZPS Oiseaux (14)",
                        value=True,
                        key="layer_zps",
                        help="ZPS (Zone de Protection Spéciale — Directive Oiseaux) : protège les sites de reproduction, halte et hivernage des oiseaux sauvages.",
                    )
                    show_installations = st.checkbox("Installations équestres", value=True, key="layer_pts")
                    show_buffers = st.checkbox(
                        "Rayons d'analyse (500 m / 1 km)",
                        value=True,
                        key="layer_buf",
                        help=(
                            "Trace deux cercles concentriques (à 500 m et 1 km) autour de l'installation sélectionnée "
                            "pour visualiser immédiatement les zones naturelles situées à proximité."
                        ),
                    )
            with tb2:
                focus_selected = st.checkbox(
                    "Zoomer sur la sélection",
                    value=True,
                    disabled=(selected_id is None),
                    help=(
                        "Sélectionnez d'abord une installation sur la carte ou dans la liste ci-dessus pour pouvoir zoomer dessus."
                        if selected_id is None
                        else "Centre et zoome la carte sur l'installation sélectionnée."
                    ),
                    key="focus_selected_chk",
                )
            with tb3:
                basemap_choice = st.selectbox(
                    "Fond de carte",
                    options=BASEMAP_CHOICES,
                    index=0,
                    help=(
                        "Épuré : fond neutre sans numéros de route mettant en valeur les zones naturelles. "
                        "Classique : carte routière et communale. "
                        "Détaillé : carte enrichie avec chemins ruraux et sentiers."
                    ),
                    key="map_basemap",
                )

            fmap = build_interactive_map(
                df=df_filtered,
                natura_geojson=natura_geojson,
                selected_inst_id=selected_id,
                show_zsc=show_zsc,
                show_zps=show_zps,
                show_installations=show_installations,
                show_buffers=show_buffers,
                basemap=basemap_choice,
                focus_selected=focus_selected,
            )
            map_state = st_folium(
                fmap,
                height=520,
                use_container_width=True,
                returned_objects=["last_object_clicked"],
                key="equivigie_main_map",
            )
            render_map_legend()

            clicked = (map_state or {}).get("last_object_clicked")
            if clicked and clicked != st.session_state["last_map_click"]:
                st.session_state["last_map_click"] = clicked
                clat = clicked.get("lat")
                clon = clicked.get("lng")
                if clat is not None and clon is not None:
                    d2 = (df_filtered["latitude"] - float(clat)) ** 2 + (
                        df_filtered["longitude"] - float(clon)
                    ) ** 2
                    min_idx = d2.idxmin()
                    if float(d2.loc[min_idx]) <= 0.002 ** 2:
                        matched_id = str(df_filtered.loc[min_idx, "inst_numero"])
                        if matched_id != st.session_state.get("selected_inst_id"):
                            st.session_state["pending_inst_id"] = matched_id
                            st.rerun()

        with col_card:
            if selected_id is None:
                render_empty_selection_panel(df_filtered)
            else:
                sel_row = df_filtered[df_filtered["inst_numero"] == selected_id].iloc[0]
                diag = diagnostics[selected_id]
                render_installation_identity_and_ivt(sel_row, selected_id, diag)

        if selected_id is not None:
            sel_row = df_filtered[df_filtered["inst_numero"] == selected_id].iloc[0]
            diag = diagnostics[selected_id]

            st.markdown("---")
            st.markdown(f"#### Diagnostic et pistes d'action territoriales — {sel_row['nom_installation']}")

            st.markdown("##### Interactions positives et atouts à valoriser")
            render_collapsible_action_cards(diag.positive_levers, positive=True, dark_mode=dark_mode)

            st.markdown("##### Points de vigilance et actions de terrain à étudier")
            render_collapsible_action_cards(diag.vigilance_actions, positive=False, dark_mode=dark_mode)

            with st.expander("Traçabilité : calcul de l'IVT et justification des pistes"):
                ivt = diag.vigilance_index
                st.markdown(
                    f"<div class='idea-block'><strong>Score IVT global :</strong> "
                    f"{ivt.score_total:.1f} % ({html.escape(ivt.level_label)})</div>",
                    unsafe_allow_html=True,
                )
                ivt_items = [
                    ("Distance métrique :", ivt.distance_detail),
                    ("Habitats ZSC/ZPS et cumul :", ivt.habitats_detail),
                    ("Contexte écologique :", ivt.ecologie_detail),
                    ("Contexte territorial :", ivt.territoire_detail),
                ]
                render_idea_blocks(ivt_items)
                st.markdown(
                    "<div style='font-weight:700;font-size:0.86rem;margin:0.75rem 0 0.45rem 0;'>"
                    "Règles métiers déclenchées</div>",
                    unsafe_allow_html=True,
                )
                rule_items: list[tuple[str, str]] = []
                for trig in diag.triggers_summary:
                    if ":" in trig:
                        head, rest = trig.split(":", 1)
                        rule_items.append((f"{head.strip()} :", rest.strip()))
                    else:
                        rule_items.append((trig, ""))
                render_idea_blocks(rule_items)

            with st.expander(f"Détail des {int(sel_row['nombre_equipements'])} équipement(s)"):
                sub_eq = eq_df[eq_df["inst_numero"] == selected_id][
                    ["nom_equipement", "type_equipement", "activites", "equip_maj_date"]
                ].rename(
                    columns={
                        "nom_equipement": "Équipement",
                        "type_equipement": "Type",
                        "activites": "Activités",
                        "equip_maj_date": "Mise à jour",
                    }
                )
                render_french_table(
                    sub_eq,
                    table_id="equipments",
                    height=260,
                    wide_cols={"Équipement", "Activités"},
                    dark_mode=dark_mode,
                )

            st.markdown(
                """<div class="disclaimer-box">
                    <strong>Interprétation :</strong> l'Indicateur de Vigilance Territoriale (IVT) et la distance mesurée
                    évaluent une priorité d'examen géographique entre un établissement équestre et des périmètres Natura 2000.
                    Ils ne prouvent aucune dégradation écologique et servent à orienter les diagnostics et le dialogue territorial.
                </div>""",
                unsafe_allow_html=True,
            )


_PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "showTips": False,
    "modeBarButtonsToRemove": ["select2d", "lasso2d"],
}


def _render_chart(fig, title: str, *, height: int = 410, bottom_margin: int = 115) -> None:
    """Affiche un graphique Plotly avec titre externe, barre d'outils visible, axes espacés et infobulles lisibles."""
    axis_title_col = "#f8fafc" if dark_mode else "#0f172a"
    axis_tick_col = "#cbd5e1" if dark_mode else "#334155"
    grid_col = "rgba(148, 163, 184, 0.18)" if dark_mode else "rgba(15, 23, 42, 0.08)"
    plot_bg = "rgba(17, 24, 39, 0.55)" if dark_mode else "#ffffff"
    hover_bg = "#1e293b" if dark_mode else "#ffffff"
    hover_border = "#475569" if dark_mode else "#94a3b8"

    st.markdown(
        f"<div class='chart-title-bar'>{html.escape(title)}</div>",
        unsafe_allow_html=True,
    )
    fig.update_xaxes(
        automargin=True,
        title_font=dict(size=12.5, color=axis_title_col),
        tickfont=dict(size=11.5, color=axis_tick_col),
        title_standoff=24,
        gridcolor=grid_col,
        zerolinecolor=grid_col,
    )
    fig.update_yaxes(
        automargin=True,
        title_font=dict(size=12.5, color=axis_title_col),
        tickfont=dict(size=11.5, color=axis_tick_col),
        title_standoff=16,
        gridcolor=grid_col,
        zerolinecolor=grid_col,
    )
    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=plot_bg,
        font=dict(color=axis_title_col),
        legend=dict(font=dict(color=axis_tick_col)),
        modebar=dict(
            bgcolor="#e2e8f0",
            color="#0f172a",
            activecolor="#000000",
        ),
        title=None,
        height=height,
        margin=dict(t=48, b=bottom_margin, l=15, r=15),
        hoverlabel=dict(
            bgcolor=hover_bg,
            bordercolor=hover_border,
            font=dict(size=13.5, family="Inter, Segoe UI, Arial, sans-serif", color=axis_title_col),
            align="left",
            namelength=-1,
        ),
    )
    st.plotly_chart(fig, width="stretch", config=_PLOTLY_CONFIG)


with tab_dash:
    if df_filtered.empty:
        st.info("Aucune donnée à afficher avec les filtres actuels.")
    else:
        st.markdown("### Analyse territoriale et priorisation des diagnostics")

        c_left, c_right = st.columns(2, gap="large")

        with c_left:
            dep_dist = (
                df_filtered.groupby(["departement", "niveau_vigilance_descriptif"], as_index=False)
                .agg(installations=("inst_numero", "nunique"))
            )
            fig_dep = px.bar(
                dep_dist,
                x="departement",
                y="installations",
                color="niveau_vigilance_descriptif",
                category_orders={
                    "departement": sorted(df_filtered["departement"].unique().tolist()),
                    "niveau_vigilance_descriptif": VIGILANCE_ORDER,
                },
                color_discrete_map=VIGILANCE_COLORS,
                labels={
                    "departement": "<b>Département</b>",
                    "installations": "<b>Nombre d'installations</b>",
                    "niveau_vigilance_descriptif": "Distance",
                },
                barmode="stack",
            )
            fig_dep.update_traces(
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Tranche de distance : %{fullData.name}<br>"
                    "Installations : <b>%{y}</b><extra></extra>"
                )
            )
            fig_dep.update_layout(
                legend=dict(
                    orientation="h",
                    xref="container",
                    yref="container",
                    yanchor="bottom",
                    y=0.01,
                    xanchor="left",
                    x=0.02,
                    entrywidth=0.45,
                    entrywidthmode="fraction",
                    title_text="",
                    font=dict(size=11.5),
                )
            )
            _render_chart(fig_dep, "Installations par département et proximité Natura 2000", height=430, bottom_margin=118)

        with c_right:
            hotspots = compute_natura_hotspots(df_filtered, top_n=12)
            if hotspots.empty:
                st.info("Aucune installation à ≤ 1 km d'un site Natura 2000 dans la sélection actuelle.")
            else:
                short_dir = hotspots["directive"].str.replace(" (Habitats)", "", regex=False).str.replace(" (Oiseaux)", "", regex=False)
                hotspots["label"] = hotspots["site"] + " (" + short_dir + ")"
                fig_hot_df = hotspots.sort_values("nb_installations", ascending=True).copy()
                fig_hot_df["short_label"] = fig_hot_df["label"].apply(
                    lambda s: s[:34] + "…" if len(s) > 35 else s
                )
                fig_hot = px.bar(
                    fig_hot_df,
                    x="nb_installations",
                    y="short_label",
                    color="typologie",
                    color_discrete_map=TYPOLOGY_COLOR_MAP,
                    orientation="h",
                    custom_data=["site", "directive", "typologie"],
                    labels={
                        "nb_installations": "<b>Installations à ≤ 1 km</b>",
                        "short_label": "",
                        "typologie": "Typologie",
                    },
                )
                fig_hot.update_traces(
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "Directive : %{customdata[1]}<br>"
                        "Typologie : %{customdata[2]}<br>"
                        "Installations à ≤ 1 km : <b>%{x}</b><extra></extra>"
                    )
                )
                fig_hot.update_yaxes(
                    categoryorder="array",
                    categoryarray=fig_hot_df["short_label"].tolist(),
                )
                fig_hot.update_layout(
                    yaxis_title="<b>Sites Natura 2000</b>",
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.24,
                        xanchor="center",
                        x=0.42,
                        title_text="",
                        font=dict(size=11.5),
                    ),
                )
                _render_chart(fig_hot, "Top sites Natura 2000 avec le plus d'installations à ≤ 1 km", height=430, bottom_margin=122)

        c_ivt1, c_ivt2 = st.columns(2, gap="large")
        with c_ivt1:
            top_ivt = df_filtered.sort_values(
                ["ivt_score", "distance_natura_m"], ascending=[False, True]
            ).head(12).iloc[::-1]
            fig_ivt_stack = go.Figure()
            pillar_specs = [
                ("ivt_distance", "Distance (40 %)", "#dc2626"),
                ("ivt_habitats", "Habitats ZSC/ZPS (25 %)", "#2563eb"),
                ("ivt_ecologie", "Contexte écologique (20 %)", "#0d9488"),
                ("ivt_territoire", "Contexte territorial (15 %)", "#d97706"),
            ]
            y_labels = [
                f"{(n[:29] + '…' if len(n) > 30 else n)} ({c})"
                for n, c in zip(top_ivt["nom_installation"], top_ivt["departement_code"])
            ]
            custom_ivt = list(
                zip(
                    top_ivt["nom_installation"],
                    top_ivt["commune"],
                    top_ivt["ivt_score"],
                    top_ivt["distance_natura_m"],
                )
            )
            for col_name, lbl, col_hex in pillar_specs:
                fig_ivt_stack.add_trace(
                    go.Bar(
                        y=y_labels,
                        x=top_ivt[col_name],
                        name=lbl,
                        orientation="h",
                        marker_color=col_hex,
                        customdata=custom_ivt,
                        hovertemplate=(
                            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
                            f"Pilier : {lbl} -> <b>%{{x:.1f}} %</b><br>"
                            "IVT total : <b>%{customdata[2]:.1f} %</b> | Distance : %{customdata[3]:.0f} m"
                            "<extra></extra>"
                        ),
                    )
                )
            fig_ivt_stack.update_layout(
                barmode="stack",
                xaxis_title="<b>Indice IVT (%)</b>",
                yaxis_title="",
                xaxis=dict(range=[0, 102]),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.22,
                    xanchor="center",
                    x=0.42,
                    font=dict(size=11.5),
                ),
            )
            _render_chart(fig_ivt_stack, "Top 12 des installations par IVT — Décomposition des 4 piliers", height=485, bottom_margin=138)

        with c_ivt2:
            fig_scatter = px.scatter(
                df_filtered,
                x="distance_natura_m",
                y="ivt_score",
                color="typologie_short",
                color_discrete_map=TYPOLOGY_COLOR_MAP,
                size="nombre_equipements",
                custom_data=[
                    "nom_installation",
                    "commune",
                    "departement",
                    "typologie_short",
                    "ivt_niveau",
                    "distance_natura_m",
                    "ivt_score",
                    "nombre_equipements",
                ],
                labels={
                    "distance_natura_m": "<b>Distance au site Natura 2000 (m)</b>",
                    "ivt_score": "<b>Indice IVT (%)</b>",
                    "typologie_short": "Typologie",
                    "nombre_equipements": "Équipements",
                },
            )
            fig_scatter.update_traces(
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br><br>"
                    "Commune : %{customdata[1]} (%{customdata[2]})<br>"
                    "Typologie : %{customdata[3]}<br>"
                    "Niveau : %{customdata[4]}<br>"
                    "Indice IVT : <b>%{customdata[6]:.1f} %</b><br>"
                    "Distance Natura 2000 : <b>%{customdata[5]:.1f} m</b><br>"
                    "Équipements : %{customdata[7]}"
                    "<extra></extra>"
                )
            )
            ann_bg = "rgba(15,23,42,0.88)" if dark_mode else "rgba(255,255,255,0.88)"
            vline_col = "#cbd5e1" if dark_mode else "#1e293b"
            h_high_col = "#f87171" if dark_mode else "#b91c1c"
            h_mod_col = "#fbbf24" if dark_mode else "#b45309"
            max_scatter_x = max(float(df_filtered["distance_natura_m"].max()) * 1.05, 1500.0)
            fig_scatter.add_vline(
                x=1000,
                line_dash="dash",
                line_color=vline_col,
                annotation_text="Rayon 1 km (1 000 m)",
                annotation_position="top left",
                annotation_font=dict(size=11.5, color=vline_col),
                annotation_bgcolor=ann_bg,
            )
            fig_scatter.add_hline(
                y=70,
                line_dash="dot",
                line_color=h_high_col,
                annotation_text="Seuil prioritaire (IVT ≥ 70 %)",
                annotation_position="top right",
                annotation_font=dict(size=11.5, color=h_high_col),
                annotation_bgcolor=ann_bg,
            )
            fig_scatter.add_hline(
                y=40,
                line_dash="dot",
                line_color=h_mod_col,
                annotation_text="Seuil vigilance modérée (IVT ≥ 40 %)",
                annotation_position="top right",
                annotation_font=dict(size=11.5, color=h_mod_col),
                annotation_bgcolor=ann_bg,
            )
            fig_scatter.update_layout(
                xaxis=dict(range=[-350, max_scatter_x]),
                yaxis=dict(range=[0, 102]),
                legend=dict(
                    orientation="h",
                    xref="container",
                    yref="container",
                    yanchor="bottom",
                    y=0.01,
                    xanchor="left",
                    x=0.02,
                    entrywidth=0.46,
                    entrywidthmode="fraction",
                    title_text="",
                    font=dict(size=11.5),
                ),
            )
            _render_chart(fig_scatter, "Relation Distance métrique et Indice de Vigilance (IVT)", height=485, bottom_margin=138)

        c2_left, c2_right = st.columns(2, gap="large")

        with c2_left:
            close_only = df_filtered[df_filtered["natura_a_1km"]]
            typ_source = close_only if not close_only.empty else df_filtered
            typ_title = (
                "Typologies écologiques concernées (installations à ≤ 1 km)"
                if not close_only.empty
                else "Typologies écologiques des sites les plus proches"
            )
            typ_counts = (
                typ_source.groupby("typologie_short", as_index=False)
                .agg(installations=("inst_numero", "nunique"))
                .sort_values("installations", ascending=False)
            )
            fig_typ = px.pie(
                typ_counts,
                names="typologie_short",
                values="installations",
                color="typologie_short",
                color_discrete_map=TYPOLOGY_COLOR_MAP,
                hole=0.45,
            )
            fig_typ.update_traces(
                textposition="inside",
                insidetextorientation="horizontal",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Installations : <b>%{value}</b> (%{percent})<extra></extra>"
                ),
            )
            fig_typ.update_layout(
                legend=dict(
                    orientation="h",
                    xref="container",
                    yref="container",
                    yanchor="bottom",
                    y=0.01,
                    xanchor="left",
                    x=0.02,
                    entrywidth=0.46,
                    entrywidthmode="fraction",
                    font=dict(size=11.5),
                )
            )
            _render_chart(fig_typ, typ_title, height=430, bottom_margin=115)

        with c2_right:
            sel_ids = set(df_filtered["inst_numero"])
            eq_sub = eq_df[eq_df["inst_numero"].isin(sel_ids)]
            eq_counts = (
                eq_sub.groupby("type_equipement", as_index=False)
                .agg(equipements=("equip_numero", "nunique"))
                .sort_values("equipements", ascending=True)
            )
            fig_eq = px.bar(
                eq_counts,
                x="equipements",
                y="type_equipement",
                orientation="h",
                labels={
                    "equipements": "<b>Nombre d'équipements</b>",
                    "type_equipement": "",
                },
                color_discrete_sequence=["#0f766e"],
            )
            fig_eq.update_traces(
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Équipements : <b>%{x}</b><extra></extra>"
                )
            )
            fig_eq.update_layout(yaxis_title="")
            _render_chart(fig_eq, f"Répartition des {len(eq_sub)} équipements équestres de la sélection", height=430, bottom_margin=85)

        st.markdown("#### Synthèse départementale")
        dep_summary = compute_department_summary(df_filtered).rename(
            columns={
                "departement": "Département",
                "departement_code": "Code",
                "installations": "Installations",
                "equipements": "Équipements",
                "dans_natura": "À l'intérieur (0 m)",
                "a_1km_ou_moins": "À ≤ 1 km",
                "part_1km_pct": "Part ≤ 1 km (%)",
                "distance_mediane_m": "Distance médiane (m)",
                "ivt_moyen": "IVT moyen (%)",
            }
        )[
            [
                "Département",
                "Code",
                "Installations",
                "Équipements",
                "À l'intérieur (0 m)",
                "À ≤ 1 km",
                "Part ≤ 1 km (%)",
                "Distance médiane (m)",
                "IVT moyen (%)",
            ]
        ]
        render_french_table(
            dep_summary,
            table_id="dep_summary",
            height=240,
            numeric_suffixes={"Part ≤ 1 km (%)": " %", "IVT moyen (%)": " %"},
            dark_mode=dark_mode,
        )

        st.markdown("#### Liste de priorisation des diagnostics territoriaux")
        with st.container(border=True):
            st.markdown(
                "<div class='dash-sort-title'>"
                "Paramètres de tri et de sélection du tableau (choisissez votre critère)</div>",
                unsafe_allow_html=True,
            )
            sc1, sc2, sc3 = st.columns([2.2, 1.8, 1.6], gap="medium")
            with sc1:
                sort_col_choice = st.selectbox(
                    "Critère de classement",
                    options=[
                        "Indice IVT (%)",
                        "Distance Natura (m)",
                        "Nombre d'équipements",
                        "Nom d'installation",
                    ],
                    index=0,
                    key="dash_sort_col",
                )
            with sc2:
                sort_dir = st.segmented_control(
                    "Ordre de tri",
                    options=["Décroissant", "Croissant"],
                    default="Décroissant",
                    key="dash_sort_dir",
                )
                if not sort_dir:
                    sort_dir = "Décroissant"
            with sc3:
                top_limit = st.selectbox(
                    "Nombre d'installations à garder",
                    options=[10, 20, 50, 100, "Toutes"],
                    index=1,
                    key="dash_top_limit",
                )

        sort_col_map = {
            "Indice IVT (%)": ("ivt_score", "distance_natura_m"),
            "Distance Natura (m)": ("distance_natura_m", "ivt_score"),
            "Nombre d'équipements": ("nombre_equipements", "ivt_score"),
            "Nom d'installation": ("nom_installation", "ivt_score"),
        }
        primary_col, secondary_col = sort_col_map[sort_col_choice]
        is_asc = sort_dir == "Croissant"
        sorted_export_df = df_filtered.sort_values(
            [primary_col, secondary_col],
            ascending=[is_asc, True if primary_col != "distance_natura_m" else False],
        )
        if top_limit != "Toutes":
            sorted_export_df = sorted_export_df.head(int(top_limit))

        display_cols = [
            "nom_installation",
            "commune",
            "departement",
            "ivt_score",
            "ivt_niveau",
            "distance_natura_m",
            "natura_plus_proche_nom",
            "typologie_short",
        ]
        table_df = sorted_export_df[display_cols].rename(
            columns={
                "nom_installation": "Installation",
                "commune": "Commune",
                "departement": "Département",
                "ivt_score": "IVT (%)",
                "ivt_niveau": "Niveau IVT",
                "distance_natura_m": "Distance (m)",
                "natura_plus_proche_nom": "Site Natura le plus proche",
                "typologie_short": "Typologie écologique",
            }
        )
        st.markdown(
            f"<div class='dash-filter-summary'>"
            f"Affichage de <strong>{len(table_df)}</strong> installation(s) sur <strong>{len(df_filtered)}</strong> filtrées "
            f"— triées par <strong>{html.escape(sort_col_choice)}</strong> ({html.escape(sort_dir.lower())})."
            f"</div>",
            unsafe_allow_html=True,
        )
        render_french_table(
            table_df,
            table_id="priorisation",
            height=380,
            wide_cols={"Installation", "Site Natura le plus proche", "Typologie écologique"},
            numeric_suffixes={"IVT (%)": " %"},
            dark_mode=dark_mode,
        )

        dl1, dl2 = st.columns(2)
        dl1.download_button(
            "Télécharger le tableau affiché (CSV Excel UTF-8)",
            data=table_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="equivigie_priorisation_normandie.csv",
            mime="text/csv",
            icon=":material/download:",
            width="stretch",
        )
        dl2.download_button(
            "Télécharger la synthèse départementale (CSV)",
            data=dep_summary.to_csv(index=False).encode("utf-8-sig"),
            file_name="equivigie_synthese_departements.csv",
            mime="text/csv",
            icon=":material/download:",
            width="stretch",
        )


with tab_method:
    st.markdown("### Méthodologie")

    col_m1, col_m2 = st.columns(2, gap="large")
    with col_m1:
        st.markdown("#### 1. Pipeline de traitement spatial")
        render_idea_blocks(
            [
                (
                    "Recensement des équipements équestres :",
                    "sélection des 5 départements normands (14, 27, 50, 61, 76) et de la famille officielle Équipement équestre regroupant 1 175 équipements.",
                ),
                (
                    "Regroupement par installation :",
                    "agrégation par identifiant d'installation (421 installations distinctes) avec centroïde représentatif afin d'éviter le double comptage d'un centre multi-équipements.",
                ),
                (
                    "Calcul exact des distances :",
                    "mesure de la distance euclidienne entre chaque installation et les 96 sites Natura 2000 normands (82 ZSC et 14 ZPS), sans double comptage en cas de superposition ZSC/ZPS.",
                ),
                (
                    "Moteur de pistes d'action à 3 axes :",
                    "règles déterministes et explicables croisant exposition spatiale, typologie écologique réelle du site Natura 2000 et profil d'équipements.",
                ),
            ]
        )
    with col_m2:
        st.markdown("#### 2. Limites méthodologiques assumées")
        render_idea_blocks(
            [
                (
                    "Proximité différente d'impact écologique :",
                    "une distance faible ou un IVT élevé signale une coïncidence spatiale méritant une visite ou un dialogue territorial, jamais une preuve de dégradation.",
                ),
                (
                    "Périmètre du recensement sportif :",
                    "couvre les équipements sportifs déclarés, et non l'exhaustivité des élevages privés sans équipement sportif ni les effectifs d'équidés.",
                ),
                (
                    "Position ponctuelle :",
                    "la coordonnée d'une installation correspond au centre de ses équipements, et non aux limites cadastrales de toutes ses prairies.",
                ),
                (
                    "Zonage Natura 2000 :",
                    "constitue un socle officiel robuste mais ne couvre pas d'autres inventaires (ZNIEFF, corridors SRCE, zones humides hors Natura 2000).",
                ),
            ]
        )

    st.markdown("---")
    st.markdown("### Indicateur de Vigilance Territoriale (IVT en %)")
    st.markdown(
        "<div class='idea-block' style='font-size:1.02rem;line-height:1.65;margin-bottom:1.35rem;'>"
        "<strong>Principe général :</strong> "
        "l'IVT est un indice composite <span class='nw'>(0 à 100 %)</span>, <span class='nw'>100 %</span> déterministe, "
        "auditable et non culpabilisant, destiné aux collectivités, EPCI, PNR et animateurs Natura 2000 "
        "pour hiérarchiser les diagnostics de terrain à partir de 4 piliers complémentaires."
        "</div>",
        unsafe_allow_html=True,
    )

    p_col1, p_col2 = st.columns(2, gap="large")
    with p_col1:
        st.markdown(
            """
            <div class="idea-card">
                <div class="ivt-card-title">1. Distance écologique (0 à 40 %)</div>
                <div class="ivt-pill-line"><strong>À l'intérieur du site (0 m) :</strong> <span class="nw">40 %</span></div>
                <div class="ivt-pill-line"><strong>Entre 0 et 500 m :</strong> <span class="nw">26 à 36 %</span></div>
                <div class="ivt-pill-line"><strong>Entre 500 et 1 000 m :</strong> <span class="nw">15 à 25 %</span></div>
                <div class="ivt-pill-line"><strong>Entre 1 km et 5 km :</strong> <span class="nw">2 à 12 %</span></div>
                <div class="ivt-pill-line"><strong>Au-delà de 5 km :</strong> <span class="nw">0 à 2 %</span></div>
            </div>
            <div class="idea-card">
                <div class="ivt-card-title">2. Proximité des habitats ZSC/ZPS et cumul (0 à 25 %)</div>
                <div class="ivt-pill-line"><strong>Exposition ZSC (Habitats) :</strong> <span class="nw">+8 % à 1 km ou moins,</span> <span class="nw">+4 % entre 1 et 2 km</span></div>
                <div class="ivt-pill-line"><strong>Exposition ZPS (Oiseaux) :</strong> <span class="nw">+8 % à 1 km ou moins,</span> <span class="nw">+4 % entre 1 et 2 km</span></div>
                <div class="ivt-pill-line"><strong>Double exposition ZSC et ZPS :</strong> <span class="nw">+4 %</span></div>
                <div class="ivt-pill-line"><strong>Cumul multi-sites (à 1 km ou moins) :</strong> <span class="nw">+2,5 % par site supplémentaire,</span> <span class="nw">plafonné à +5 %</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p_col2:
        st.markdown(
            """
            <div class="idea-card">
                <div class="ivt-card-title">3. Contexte écologique du milieu (0 à 20 %)</div>
                <div class="ivt-pill-line"><strong>Sensibilité par typologie :</strong> <span class="nw">Marais et estuaires (20 %),</span> <span class="nw">Littoral et dunes (18 %),</span> <span class="nw">Vallées et cours d'eau (16 %),</span> <span class="nw">Cavités et chiroptères (15 %),</span> <span class="nw">Bocages et forêts (13 %)</span></div>
                <div class="ivt-pill-line"><strong>Pondération selon la distance :</strong> <span class="nw">coefficient 1,0 jusqu'à 1 km,</span> <span class="nw">coefficient 0,6 entre 1 et 3 km,</span> <span class="nw">coefficient 0,3 au-delà</span></div>
            </div>
            <div class="idea-card">
                <div class="ivt-card-title">4. Contexte territorial et équipements (0 à 15 %)</div>
                <div class="ivt-pill-line"><strong>Nombre d'équipements recensés :</strong> <span class="nw">de 1 à 5 %</span></div>
                <div class="ivt-pill-line"><strong>Emprise des pratiques :</strong> <span class="nw">itinérance ou cross (+3 %),</span> <span class="nw">infrastructures extérieures (+1,5 %),</span> <span class="nw">équipement couvert (+0,5 %),</span> <span class="nw">plafonné à 8 %</span></div>
                <div class="ivt-pill-line"><strong>Co-présence locale :</strong> <span class="nw">jusqu'à 4 % sur le même site,</span> <span class="nw">jusqu'à 3 % dans la même commune</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='idea-block' style='font-size:1.02rem;line-height:1.68;margin-top:0.95rem;'>"
        "<strong>Seuils de lecture :</strong> "
        "<span class='nw'><strong>≥ 70 %</strong> Vigilance prioritaire</span>, "
        "<span class='nw'><strong>55 à 69,9 %</strong> Vigilance élevée</span>, "
        "<span class='nw'><strong>40 à 54,9 %</strong> Vigilance modérée</span>, "
        "<span class='nw'><strong>&lt; 40 %</strong> Veille courante</span> "
        "(toutes les installations au-delà d'un kilomètre restent strictement inférieures à <span class='nw'>40 %</span>)."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Référentiel des 96 sites Natura 2000 normands et de leur typologie")
    nat_rows = []
    for ft in natura_geojson.get("features", []):
        p = ft.get("properties", {})
        typ = classify_natura_site(p.get("SITECODE", ""), p.get("SITENAME", ""))
        nat_rows.append(
            {
                "Nom du site": p.get("SITENAME", ""),
                "Code": p.get("SITECODE", ""),
                "Directive": p.get("type_zone", ""),
                "Typologie écologique": typ.label,
                "Installations à ≤ 1 km": p.get("installations_proches_1km", 0),
            }
        )
    nat_table = pd.DataFrame(nat_rows).sort_values(
        ["Installations à ≤ 1 km", "Directive", "Nom du site"], ascending=[False, True, True]
    )
    render_french_table(
        nat_table,
        table_id="natura_ref",
        height=340,
        wide_cols={"Nom du site", "Typologie écologique"},
        dark_mode=dark_mode,
    )
