app.py:import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Simulateur Énergie Pro", layout="wide")

st.title("🏡 Simulateur de Coût Énergétique Avancé")
st.markdown("---")

# --- PARAMÈTRES DANS LA BARRE LATÉRALE ---
st.sidebar.header("📋 Caractéristiques")

superficie = st.sidebar.slider("Superficie (m²)", 10, 300, 80)
dpe = st.sidebar.selectbox("Classe DPE", ["A", "B", "C", "D", "E", "F", "G"], index=3)
nb_personnes = st.sidebar.slider("Nombre d'occupants", 1, 8, 3)

st.sidebar.header("⚙️ Énergie & Tarifs")
type_energie = st.sidebar.selectbox("Source d'énergie principale", ["Électricité", "Gaz naturel", "Granulés Bois", "Fioul"])
zone_climat = st.sidebar.select_slider("Zone Climatique (Rigueur de l'hiver)", 
                                       options=["H3 (Sud)", "H2 (Ouest/Centre)", "H1 (Nord/Est)"], 
                                       value="H2 (Ouest/Centre)")

# Dictionnaires de données
valeurs_dpe = {'A': 50, 'B': 90, 'C': 150, 'D': 230, 'E': 310, 'F': 400, 'G': 500}

# Prix moyens actualisés (estimations 2024/2025)
tarifs = {
    "Électricité": {"kwh": 0.25, "abo": 200},
    "Gaz naturel": {"kwh": 0.12, "abo": 280},
    "Granulés Bois": {"kwh": 0.09, "abo": 50},
    "Fioul": {"kwh": 0.14, "abo": 0}
}

# Coefficients climatiques (H1 est plus froid que H3)
coeffs_climat = {"H3 (Sud)": 0.8, "H2 (Ouest/Centre)": 1.0, "H1 (Nord/Est)": 1.2}

# --- CALCULS ---
# 1. Consommation Chauffage ajustée par le climat
conso_base = superficie * valeurs_dpe[dpe]
conso_chauffage = conso_base * coeffs_climat[zone_climat]

# 2. Consommation Usages (Eau chaude + Électroménager)
conso_usage = nb_personnes * 600 

conso_totale = conso_chauffage + conso_usage

# 3. Calcul financier
prix_unitaire = tarifs[type_energie]["kwh"]
abonnement = tarifs[type_energie]["abo"]
facture_energie = conso_totale * prix_unitaire
facture_totale = facture_energie + abonnement

# --- AFFICHAGE ---
col1, col2, col3 = st.columns(3)
col1.metric("Conso. Annuelle", f"{conso_totale:,.0f} kWh")
col2.metric("Facture Annuelle", f"{facture_totale:,.0f} €")
col3.metric("Mensualité", f"{facture_totale / 12:,.0f} €/mois")

# --- GRAPHIQUES ---
st.markdown("---")
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 Répartition de la dépense")
    df_pie = pd.DataFrame({
        "Type": ["Énergie brute", "Abonnement fixe"],
        "Montant": [facture_energie, abonnement]
    })
    fig_pie = px.pie(df_pie, values='Montant', names='Type', hole=0.5, color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("💡 Analyse du DPE")
    st.write(f"En zone **{zone_climat}**, un logement **{dpe}** est estimé à **{valeurs_dpe[dpe] * coeffs_climat[zone_climat]:.0f} kWh/m²/an**.")
    # Barre de progression comparative
    st.progress(valeurs_dpe[dpe] / 500)
    st.caption("Positionnement sur l'échelle de consommation (A -> G)")

st.warning("⚠️ Ces chiffres sont des estimations. La température de consigne (ex: 19°C vs 22°C) peut faire varier la facture de 20% à 30%.")
