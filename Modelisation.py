import streamlit as st
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import os

# Configuration de la page
st.set_page_config(
    page_title="Prédiction du Prix des Maisons",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .card {
        background-color: #F9FAFB;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .prediction-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background-color: #10B981;
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #059669;
        transform: translateY(-2px);
    }
    .feature-input {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #D1D5DB;
    }
    .info-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        border-radius: 5px;
        padding: 15px;
        margin: 15px 0;
    }
    .debug-info {
        background-color: #F3F4F6;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger le modèle
@st.cache_resource
def load_model():
    try:
        # Essayer plusieurs chemins possibles
        possible_paths = [
            Path("D:/Projets/Projet_Maison/Application/xgboost_model.pkl"),
        ]
        
        model = None
        model_path = None
        
        for path in possible_paths:
            if path.exists():
                model_path = path
                break
        
        if model_path is None:
            # Essayer de trouver le fichier dans le répertoire courant
            files = os.listdir()
            pkl_files = [f for f in files if f.endswith('.pkl') or f.endswith('.joblib')]
            if pkl_files:
                model_path = Path(pkl_files[0])
            else:
                st.error("Aucun fichier de modèle trouvé")
                return None
        
        # Essayer différentes méthodes de chargement
        try:
            # Méthode 1: pickle standard
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
        except Exception as e1:
            try:
                # Méthode 2: joblib (si utilisé)
                import joblib
                model = joblib.load(model_path)
            except Exception as e2:
                st.error(f"Échec du chargement du modèle: {str(e2)}")
                return None
        return model
        
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle : {str(e)}")
        return None


# Fonction principale
def main():
    # En-tête principal
    # Header principal avec sous-titre
    st.markdown("""
        <div style="
            background-color:#1E3A8A;
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow:0px 4px 10px rgba(0,0,0,0.2);
            margin-bottom:20px;
            color:white;
        ">
            <h1 style="margin-bottom:10px;">Prédiction Immobilière - Estimateur de Prix</h1>
        </div>
    """, unsafe_allow_html=True)
    
    
    # Charger le modèle
    model = load_model()
    if model is None:
        st.stop()
    
    # Diviser en deux colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">📐 Caractéristiques du Terrain</div>', unsafe_allow_html=True)
        
        # Caractéristiques du terrain
        LotArea = st.number_input(
            "Superficie du terrain (pieds carrés)",
            min_value=200,
            max_value=5000,
            value=300,
            step=50,
            help="Surface totale du terrain"
        )
        
        st.markdown('<div class="feature-input">', unsafe_allow_html=True)
        OverallQual = st.slider(
            "Qualité générale de la construction",
            min_value=1,
            max_value=10,
            value=6,
            help="Note de 1 à 10 pour la qualité des matériaux et finitions"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        YearRemodAdd = st.number_input(
            "Année de rénovation",
            min_value=1950,
            max_value=2023,
            value=2000,
            step=1,
            help="Dernière année de rénovation majeure"
        )
        
    with col2:
        st.markdown('<div class="sub-header">🏠 Caractéristiques de la Maison</div>', unsafe_allow_html=True)
        
        TotalBsmtSF = st.number_input(
            "Superficie totale du sous-sol (pieds carrés)",
            min_value=0,
            max_value=500,
            value=100,
            step=50,
            help="Surface totale du sous-sol"
        )
        
        st.markdown('<div class="feature-input">', unsafe_allow_html=True)
        GrLivArea = st.number_input(
            "Surface habitable (pieds carrés)",
            min_value=500,
            max_value=5000,
            value=1500,
            step=50,
            help="Surface habitable hors sol"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        FullBath = st.slider(
            "Nombre de salles de bain complètes",
            min_value=0,
            max_value=4,
            value=1,
            help="Salles de bain complètes (baignoire + douche + WC)"
        )
        
        TotRmsAbvGrd = st.slider(
            "Nombre total de pièces hors sol",
            min_value=0,
            max_value=15,
            value=1,
            help="Toutes les pièces hors sol (sauf salles de bain)"
        )
    
    # Deuxième ligne de caractéristiques
    st.markdown('<div class="sub-header">🚗 Caractéristiques du Garage</div>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        GarageYrBlt = st.number_input(
            "Année de construction du garage",
            min_value=1990,
            max_value=2025,
            value=2000,
            step=1,
            help="Année de construction du garage (0 si pas de garage)"
        )
    
    with col4:
        GarageCars = st.slider(
            "Capacité du garage (nombre de voitures)",
            min_value=0,
            max_value=4,
            value=2,
            help="Nombre de voitures que peut contenir le garage"
        )
    
    with col5:
        GarageArea = st.number_input(
            "Superficie du garage (pieds carrés)",
            min_value=0,
            max_value=1500,
            value=500,
            step=25,
            help="Surface du garage"
        )
    
    # Caractéristiques supplémentaires
    st.markdown('<div class="sub-header">📊 Informations Supplémentaires</div>', unsafe_allow_html=True)
    
    col6, col7, col8 = st.columns(3)
    
    with col6:
        _1stFlrSF = st.number_input(
            "Surface du 1er étage (pieds carrés)",
            min_value=50,
            max_value=4000,
            value=1200,
            step=50,
            help="Surface du premier étage"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col7:
        YrSold = st.number_input(
            "Année de vente",
            min_value=2006,
            max_value=2025,
            value=2010,
            step=1,
            help="Année de la vente"
        )
    
    with col8:
        # Espace réservé pour d'autres features si nécessaire
        pass
    
    # Bouton de prédiction
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        predict_button = st.button(
            "🚀 Prédire le Prix", 
            use_container_width=True,
            type="primary"
        )
    
    # Prédiction
    if predict_button:
        try:
            # Création du dataframe d'entrée
            input_data = pd.DataFrame({
                'LotArea': [LotArea],
                'OverallQual': [OverallQual],
                'YearRemodAdd': [YearRemodAdd],
                'TotalBsmtSF': [TotalBsmtSF],
                '1stFlrSF': [_1stFlrSF],
                'GrLivArea': [GrLivArea],
                'FullBath': [FullBath],
                'TotRmsAbvGrd': [TotRmsAbvGrd],
                'GarageYrBlt': [GarageYrBlt],
                'GarageCars': [GarageCars],
                'GarageArea': [GarageArea],
                'YrSold': [YrSold]
            })
            
            with st.spinner("Calcul de l'estimation en cours..."):
                prediction_log = model.predict(input_data)[0]
                
                price_real = np.expm1(prediction_log)
            
            
            st.markdown("""
            <style>
                .simple-card {
                    background: #F8FAFC;
                    border-radius: 12px;
                    padding: 30px;
                    text-align: center;
                    margin: 20px 0;
                    border-left: 5px solid #3B82F6;
                }
                .simple-price {
                    font-size: 3rem;
                    font-weight: bold;
                    color: #1E3A8A;
                    margin: 10px 0;
                }
                .simple-label {
                    color: #4B5563;
                    font-size: 1.2rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
            </style>
            """, unsafe_allow_html=True)

            # Carte simple et épurée
            st.markdown(f"""
            <div class="simple-card">
                <div class="simple-label">Prix Estimé</div>
                <div class="simple-price">${price_real:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            
            # Détails de l'entrée
            st.markdown('<div class="sub-header">📋 Résumé des Caractéristiques</div>', unsafe_allow_html=True)
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.metric("Superficie du terrain", f"{LotArea:,} pi²")
                st.metric("Qualité générale", f"{OverallQual}/10")
                st.metric("Année rénovation", YearRemodAdd)
            
            with summary_col2:
                st.metric("Surface habitable", f"{GrLivArea:,} pi²")
                st.metric("Salles de bain", FullBath)
                st.metric("Nombre de pièces", TotRmsAbvGrd)
            
            with summary_col3:
                st.metric("Superficie sous-sol", f"{TotalBsmtSF:,} pi²")
                st.metric("Capacité garage", f"{GarageCars} voitures")
                st.metric("Surface garage", f"{GarageArea:,} pi²")
            
            # Téléchargement des résultats
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 💾 Export des Résultats")
            
            # Création du rapport
            report_data = {
                "Caractéristique": [
                    "Superficie du terrain", "Qualité générale", "Année de rénovation",
                    "Surface habitable", "Salles de bain complètes", "Nombre de pièces",
                    "Superficie sous-sol", "Capacité garage", "Surface garage",
                    "Année de vente", "Prix estimé (log)", "Prix estimé (réel)"
                ],
                "Valeur": [
                    f"{LotArea} pi²", f"{OverallQual}/10", YearRemodAdd,
                    f"{GrLivArea} pi²", FullBath, TotRmsAbvGrd,
                    f"{TotalBsmtSF} pi²", GarageCars, f"{GarageArea} pi²",
                    YrSold, f"{prediction_log:.4f}", f"${price_real:,.0f}"
                ]
            }
            
            report_df = pd.DataFrame(report_data)
            csv = report_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Télécharger le rapport (CSV)",
                data=csv,
                file_name="estimation_immobiliere.csv",
                mime="text/csv",
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {str(e)}")
            st.info("Vérifiez que toutes les valeurs sont correctement renseignées.")
    
    # Section d'information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ℹ️ À propos de ce modèle")
    st.markdown("""
    **Informations techniques:**
    - Algorithme: XGBoost (Extreme Gradient Boosting)
    
    **Précision du modèle** : Les prédictions sont basées sur des données historiques 
    et doivent être considérées comme des estimations indicatives. Des facteurs 
    supplémentaires non inclus dans ce modèle peuvent influencer le prix final.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()