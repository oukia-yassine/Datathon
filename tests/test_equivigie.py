"""Tests automatisés pour ÉquiVigie Normandie — Datathon Normandie 2026."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_loader import (
    compute_department_summary,
    compute_natura_hotspots,
    load_equipments,
    load_installations,
    load_natura_geojson,
)
from src.map_builder import BASEMAP_CHOICES, build_interactive_map
from src.natura_taxonomy import SITE_TYPOLOGY_MAP
from src.recommendations import build_recommendations


RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def test_all_96_natura_sites_have_explicit_typology():
    raw_gj = json.loads((RAW / "natura2000_zsc_zps_normandie.geojson").read_text(encoding="utf-8"))
    features = raw_gj["features"]
    assert len(features) == 96
    missing = [
        f["properties"]["SITECODE"]
        for f in features
        if f["properties"]["SITECODE"] not in SITE_TYPOLOGY_MAP
    ]
    assert missing == [], f"Codes Natura 2000 non typés explicitement : {missing}"


def test_dataset_counts_and_consistency():
    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    inst_df, diagnostics = load_installations(
        RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df
    )
    assert len(eq_df) == 1175
    assert len(inst_df) == 421
    assert len(diagnostics) == 421
    assert int(inst_df["dans_natura"].sum()) == 5
    assert int(inst_df["natura_a_1km"].sum()) == 97
    assert (inst_df["inst_adresse"] != "").sum() > 350

    dep_sum = compute_department_summary(inst_df)
    assert list(dep_sum["departement_code"]) == ["14", "27", "50", "61", "76"]
    assert int(dep_sum["installations"].sum()) == 421
    assert int(dep_sum["a_1km_ou_moins"].sum()) == 97
    assert "ivt_moyen" in dep_sum.columns
    assert (dep_sum["ivt_moyen"] > 0).all()

    hotspots = compute_natura_hotspots(inst_df, top_n=10)
    assert not hotspots.empty
    assert hotspots.iloc[0]["site"] == "Forêts et étangs du Perche"
    assert int(hotspots.iloc[0]["nb_installations"]) == 11


def test_vigilance_index_four_pillars_and_separation():
    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    inst_df, diagnostics = load_installations(
        RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df
    )
    assert ((inst_df["ivt_score"] >= 0.0) & (inst_df["ivt_score"] <= 100.0)).all()
    assert ((inst_df["ivt_distance"] >= 0.0) & (inst_df["ivt_distance"] <= 40.0)).all()
    assert ((inst_df["ivt_habitats"] >= 0.0) & (inst_df["ivt_habitats"] <= 25.0)).all()
    assert ((inst_df["ivt_ecologie"] >= 0.0) & (inst_df["ivt_ecologie"] <= 20.0)).all()
    assert ((inst_df["ivt_territoire"] >= 0.0) & (inst_df["ivt_territoire"] <= 15.0)).all()

    pillar_sum = (
        inst_df["ivt_distance"]
        + inst_df["ivt_habitats"]
        + inst_df["ivt_ecologie"]
        + inst_df["ivt_territoire"]
    ).round(1)
    assert (inst_df["ivt_score"] - pillar_sum).abs().max() <= 0.2

    far_df = inst_df[~inst_df["natura_a_1km"]]
    close_df = inst_df[inst_df["natura_a_1km"]]
    assert (far_df["ivt_score"] < 40.0).all()
    assert (far_df["ivt_niveau"] == "Veille courante").all()
    assert (close_df["ivt_score"] >= 40.0).all()

    assert diagnostics["I613280001"].vigilance_index.score_total >= 65.0
    assert diagnostics["I501990004"].vigilance_index.score_total >= 70.0


def test_effective_sites_guard_at_999m():
    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    _, diagnostics = load_installations(
        RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df
    )
    assert "I764010004" in diagnostics
    diag = diagnostics["I764010004"]
    assert diag.effective_sites_1km >= 1
    assert diag.priority_rank == 3
    assert diag.vigilance_index.score_total >= 40.0


def test_recommendations_contextualized_for_real_cases():
    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    _, diagnostics = load_installations(
        RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df
    )

    pin = diagnostics["I613280001"]
    assert pin.priority_rank == 1
    assert pin.primary_typology.key == "bocages_forets_coteaux"
    assert any("bocage" in a.title.lower() or "convention" in a.title.lower() for a in pin.positive_levers)

    perchers = diagnostics["I613240001"]
    assert perchers.primary_typology.key == "cavites_chiropteres"
    assert any("éclairage" in a.title.lower() for a in perchers.vigilance_actions)

    bec = diagnostics["I501990004"]
    assert bec.primary_typology.key == "littoral_dunes"
    assert bec.dual_zsc_zps_1km is True
    assert any("avifaune" in a.title.lower() for a in bec.vigilance_actions)

    angerville = diagnostics["I140120001"]
    assert angerville.priority_rank == 4
    assert any("hors proximité" in a.title.lower() for a in angerville.vigilance_actions)


def test_simplified_geojson_sobriety_and_map_render():
    raw_size = (RAW / "natura2000_zsc_zps_normandie.geojson").stat().st_size
    opt_path = PROCESSED / "natura2000_simplifie.geojson"
    assert opt_path.exists()
    opt_size = opt_path.stat().st_size
    assert opt_size < raw_size * 0.25

    eq_df = load_equipments(RAW / "equipements_equestres_normandie.csv")
    inst_df, _ = load_installations(
        RAW / "installations_proximite_natura2000.csv", equipments_df=eq_df
    )
    nat_gj = load_natura_geojson(opt_path, inst_df)
    assert len(nat_gj["features"]) == 96

    for bm in BASEMAP_CHOICES:
        fmap = build_interactive_map(inst_df, nat_gj, selected_inst_id="I613280001", basemap=bm)
        html_out = fmap._repr_html_()
        assert "Natura 2000" in html_out
        assert "basemaps.cartocdn.com" not in html_out
        assert "IVT" in html_out


def test_streamlit_app_end_to_end():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception
    assert not at.error

    assert at.session_state["selected_inst_id"] is None
    assert len(at.pills(key="f_depts").value) == 5

    at.selectbox(key="selected_inst_id").select("I501990004").run()
    assert not at.exception
    assert at.session_state["selected_inst_id"] == "I501990004"

    at.session_state["pending_inst_id"] = "I613280001"
    at.run()
    assert not at.exception
    assert at.session_state["selected_inst_id"] == "I613280001"

    at.pills(key="f_depts").unselect("Orne").run()
    assert not at.exception
    assert at.session_state["selected_inst_id"] is None

    at.pills(key="f_depts").select("Orne").run()
    assert not at.exception
    at.checkbox(key="f_use_dist").check().run()
    assert not at.exception
    at.slider(key="f_max_dist").set_value(500).run()
    assert not at.exception

    at.text_input(key="f_search").set_value("zzzz_aucune_installation_xyz").run()
    assert not at.exception
    assert len(at.warning) >= 1

    at.button(key="reset_filters_btn").click().run()
    assert not at.exception
    assert len(at.pills(key="f_depts").value) == 5

    at.selectbox(key="dash_sort_col").select("Distance Natura (m)").run()
    assert not at.exception
    at.segmented_control(key="dash_sort_dir").set_value("Croissant").run()
    assert not at.exception
    at.selectbox(key="dash_top_limit").select(10).run()
    assert not at.exception
