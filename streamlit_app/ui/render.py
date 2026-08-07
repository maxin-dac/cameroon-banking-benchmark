from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).resolve().parents[1] / "assets"

DISCLAIMER_TEXT = (
    "Outil d'aide à la décision basé sur des données publiques collectées manuellement. "
    "Ne remplace pas une étude approfondie ni les conditions officielles des banques. "
    "Montants HT, observés au 2026-06-22."
)


@st.cache_data
def _read(rel: str) -> str:
    return (ASSETS / rel).read_text(encoding="utf-8")


def init(page_title: str) -> None:
    st.set_page_config(
        page_title=f"{page_title} - CB Benchmark",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{_read('css/theme.css')}</style>", unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(_read("html/brand.html"), unsafe_allow_html=True)
        st.caption("Données publiques - observation 2026-06-22")


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        _read("html/header.html").format(eyebrow=eyebrow, title=title, subtitle=subtitle),
        unsafe_allow_html=True,
    )


def callout(tone: str, title: str, body: str) -> None:
    st.markdown(
        _read("html/callout.html").format(tone=tone, title=title, body=body),
        unsafe_allow_html=True,
    )


def empty_state(title: str, body: str) -> None:
    st.markdown(
        _read("html/empty_state.html").format(title=title, body=body),
        unsafe_allow_html=True,
    )


def disclaimer() -> None:
    st.markdown(
        _read("html/disclaimer.html").format(text=DISCLAIMER_TEXT),
        unsafe_allow_html=True,
    )


def kpi(label: str, value: str, hint: str = "", tone: str = "accent", icon: str = "") -> None:
    st.markdown(
        _read("html/kpi.html").format(label=label, value=value, hint=hint, tone=tone, icon=icon),
        unsafe_allow_html=True,
    )


def section(title: str) -> None:
    st.markdown(f'<p class="cb-section">{title}</p>', unsafe_allow_html=True)


def style_fig(fig):
    fig.update_layout(
        font_family="Inter, Segoe UI, sans-serif",
        font_color="#0f172a",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=32, b=8),
        height=440,
    )
    fig.update_xaxes(showgrid=False, linecolor="#e5e9f2")
    fig.update_yaxes(showgrid=True, gridcolor="#edf1f7", linecolor="#e5e9f2")
    return fig