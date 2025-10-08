"""
Application Streamlit - Prédiction des Délais d'Opportunités TDF
Avec intervalle de confiance
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Délais TDF",
    page_icon="🚀",
    layout="wide"
)

# Fonction de chargement des modèles (mise en cache)
@st.cache_resource
def charger_modeles():
    """Charge le modèle, l'encodeur et les métadonnées"""
    try:
        model = joblib.load('modeles/xgboost_model.joblib')
        encoder = joblib.load('modeles/onehot_encoder.joblib')
        with open('modeles/metadata.json', 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return model, encoder, metadata
    except FileNotFoundError as e:
        st.error(f"⚠️ Fichiers modèles non trouvés : {e}")
        st.info("💡 Veuillez d'abord exécuter le script 'script_sauvegarde_modele.py'")
        st.stop()

# Chargement des modèles
model, encoder, metadata = charger_modeles()

# En-tête de l'application
st.title("🚀 Prédiction des Délais d'Opportunités")
st.markdown("### Combien de jours avant de gagner cette opportunité ?")

st.divider()

# Affichage des informations du modèle
with st.expander("ℹ️ Informations sur le modèle"):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("MAE (Erreur Moyenne)", f"{metadata['mae']:.1f} jours")
    with col2:
        st.metric("R² (Performance)", f"{metadata['r2']:.2%}")
    
    st.caption(f"Modèle entraîné le : {metadata['date_entrainement']}")

st.divider()

# Formulaire de prédiction
st.subheader("📝 Renseignez les Caractéristiques de l'Opportunité")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        phase = st.selectbox(
            "Phase du Projet",
            options=["Etude", "Réalisation"],
            help="Phase actuelle du projet"
        )
        
        client = st.selectbox(
            "Client",
            options=["Client_1", "Client_2", "Client_3", "Client_4"],
            help="Identifiant du client"
        )
        
        macro_produit = st.selectbox(
            "Macro Produit",
            options=["Evolution PoP", "Nouveau PoP"],
            help="Type de produit global"
        )
    
    with col2:
        # Liste des produits
        liste_produits = [
            "Evol PoP Pyl FH/BLO",
            "Evol PoP Pyl Radio",
            "Evol PoP Pyl Radio 5G",
            "Evol PoP TT FH/BLO",
            "Nouv PoP PAC Rg 1",
            "Nouv PoP PAC Rg 1 ZB",
            "Nouv PoP PAC Rg suivant",
            "Nouv PoP Pyl FH",
            "Nouv PoP Pyl Radio"
        ]
        
        produit = st.selectbox(
            "Produit Spécifique",
            options=liste_produits,
            help="Produit détaillé"
        )
        
        mois_creation = st.slider(
            "Mois de Création",
            min_value=1,
            max_value=12,
            value=datetime.now().month,
            help="Mois de création de l'opportunité (1=Janvier, 12=Décembre)"
        )
    
    # Bouton de soumission
    submitted = st.form_submit_button("🔮 Prédire le Délai", use_container_width=True)

# Traitement de la prédiction
if submitted:
    st.divider()
    
    with st.spinner("Calcul de la prédiction en cours..."):
        # Préparation des données
        data_input = pd.DataFrame({
            'phase': [phase],
            'client': [client],
            'macro_produit': [macro_produit],
            'produit': [produit]
        })
        
        # Encodage des variables catégorielles
        encoded_features = encoder.transform(data_input)
        encoded_df = pd.DataFrame(
            encoded_features,
            columns=encoder.get_feature_names_out(['phase', 'client', 'macro_produit', 'produit'])
        )
        
        # Ajout du mois de création
        encoded_df['mois_creation'] = mois_creation
        
        # Réorganiser les colonnes pour correspondre à l'ordre attendu par le modèle
        # (Le modèle XGBoost est sensible à l'ordre des colonnes)
        expected_columns = model.get_booster().feature_names
        
        # Créer un DataFrame avec toutes les colonnes attendues, initialisées à 0
        final_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        # Remplir avec les valeurs encodées disponibles
        for col in encoded_df.columns:
            if col in final_df.columns:
                final_df[col] = encoded_df[col].values[0]
        
        # Prédiction ponctuelle
        prediction = model.predict(final_df)[0]
        prediction = max(0, prediction)  # Éviter les valeurs négatives
        
        # Calcul de l'intervalle de confiance
        # On utilise la MAE comme estimation de l'incertitude (±1 écart-type)
        incertitude = metadata['mae']
        borne_inf = max(0, prediction - incertitude)
        borne_sup = prediction + incertitude
    
    # Affichage du résultat
    st.success("✅ Prédiction terminée !")
    
    # Métrique principale avec intervalle de confiance
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    
    with col_metric1:
        st.metric(
            label="⏱️ Délai Prédit",
            value=f"{prediction:.0f} jours"
        )
    
    with col_metric2:
        st.metric(
            label="📉 Borne Inférieure",
            value=f"{borne_inf:.0f} jours",
            delta=f"-{incertitude:.0f}j",
            delta_color="inverse"
        )
    
    with col_metric3:
        st.metric(
            label="📈 Borne Supérieure",
            value=f"{borne_sup:.0f} jours",
            delta=f"+{incertitude:.0f}j"
        )
    
    # Intervalle de confiance en texte
    st.info(f"📊 **Intervalle de confiance (±1σ)** : entre **{borne_inf:.0f}** et **{borne_sup:.0f}** jours")
    
    # Code couleur et recommandation
    col1, col2 = st.columns(2)
    
    with col1:
        if prediction < 30:
            st.success("🟢 **Opportunité RAPIDE**")
            st.write("Cette opportunité devrait se conclure rapidement.")
        elif prediction < 60:
            st.warning("🟠 **Opportunité MOYENNE**")
            st.write("Délai standard, maintenir le suivi régulier.")
        else:
            st.error("🔴 **Opportunité LENTE**")
            st.write("Attention : Cette opportunité nécessite un suivi renforcé.")
    
    with col2:
        # Informations sur la fiabilité
        st.write("**🎯 Fiabilité de la Prédiction**")
        st.write(f"• Erreur moyenne du modèle : ±{metadata['mae']:.0f} jours")
        st.write(f"• Précision du modèle : R² = {metadata['r2']:.1%}")
        
        if metadata['r2'] > 0.6:
            st.write("✅ Confiance élevée")
        elif metadata['r2'] > 0.5:
            st.write("⚠️ Confiance moyenne")
        else:
            st.write("⚠️ Confiance faible")
    
    # Détails de la prédiction
    with st.expander("📊 Détails de la Prédiction"):
        st.write("**Caractéristiques saisies :**")
        details = {
            "Phase": phase,
            "Client": client,
            "Macro Produit": macro_produit,
            "Produit": produit,
            "Mois de Création": f"{mois_creation} ({['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'][mois_creation-1]})"
        }
        st.json(details)
        
        st.write("**Méthode de calcul de l'intervalle :**")
        st.write(f"• Prédiction centrale : {prediction:.1f} jours")
        st.write(f"• Incertitude (MAE) : ±{incertitude:.1f} jours")
        st.write(f"• Intervalle : [{borne_inf:.1f}, {borne_sup:.1f}] jours")

# Pied de page
st.divider()
st.caption("🤖 Application développée avec Streamlit | Modèle : XGBoost Regressor")

