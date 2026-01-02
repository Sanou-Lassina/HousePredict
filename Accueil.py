import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from PIL import Image
import os

# Configuration de la page
st.set_page_config(
    page_title="HousePredict - Plateforme Prédictive Immobilière",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé POUR LA PAGE D'ACCUEIL SEULEMENT
st.markdown("""
<style>
    /* Styles spécifiques pour la page d'accueil seulement */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f1f5f9 0%, #ffffff 100%);
    }
    
    /* Sidebar dynamique pour toutes les pages - COULEUR PROFESSIONNELLE MODIFIÉE */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7f7f7, #d4d4d4);
    }
    
    /* Header de la page d'accueil - avec un peu d'espace */
    .homepage-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
        padding: 3rem 0 2rem 0;
        margin: 0;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.2);
        position: relative;
    }
    
    .author-badge {
        position: absolute;
        top: 25px;
        left: 25px;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        z-index: 1000;
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FFFFFF, #dbeafe, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 300%;
        text-align: center;
        margin: 0 0 0.5rem 0;
        padding: 0 1rem;
        font-weight: 900;
        animation: gradientShift 4s ease infinite, fadeInUp 1.5s ease-out;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        text-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .page-subtitle {
        font-size: 1.4rem;
        color: #ffffff;
        text-align: center;
        margin: 0 0 0.5rem 0;
        padding: 0 10%;
        font-weight: 300;
        animation: fadeIn 2s ease-in;
        line-height: 1.6;
    }
    
    /* ONGLETS DYNAMIQUES MODIFIÉS - DESIGN PROFESSIONNEL */
    [data-testid="stSidebarNav"] ul {
        padding: 0.5rem 0.8rem !important;
        margin: 0 !important;
    }
    
    .sidebar-tab {
        padding: 0.85rem 1.2rem !important;
        margin: 0.25rem 0 !important;
        border-radius: 12px !important;
        border: 2px solid transparent !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: rgba(255, 255, 255, 0.07) !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .sidebar-tab::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 3px;
        background: #4299e1;
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .sidebar-tab:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: #4299e1 !important;
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
    }
    
    .sidebar-tab:hover::before {
        transform: scaleY(1);
    }
    
    .sidebar-tab-selected {
        background: linear-gradient(135deg, rgba(56, 178, 172, 0.25), rgba(49, 151, 149, 0.2)) !important;
        border-color: #38b2ac !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(56, 178, 172, 0.2);
    }
    
    .sidebar-tab-selected::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 3px;
        background: #38b2ac;
        transform: scaleY(1);
    }
    
    /* Indicateur d'état actif */
    .sidebar-tab-selected::after {
        content: '●';
        position: absolute;
        right: 15px;
        color: #38b2ac;
        font-size: 0.8rem;
        animation: pulse 2s infinite;
    }
    
    /* Cartes de fonctionnalités pour la homepage */
    .homepage-feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border-left: 4px solid #3b82f6;
        height: 100%;
        min-height: 280px;
    }
    
    .homepage-feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        border-left: 4px solid #1e40af;
    }
    
    /* Animations */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .page-subtitle {
            font-size: 1.1rem;
            padding: 0 5%;
        }
        .author-badge {
            position: relative;
            top: 0;
            left: 0;
            display: inline-block;
            margin: 0 auto 1rem auto;
        }
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Sidebar - Navigation professionnelle
    with st.sidebar:
        with st.sidebar:
            if os.path.exists("architecture.png"):
                st.image("architecture.png", width=600)
            else:
                st.error("❌ Image architecture.png introuvable")
        
        # En-tête de la sidebar
        st.markdown("# 🏢 HousePredict")
        
        st.markdown("<div class='styled-divider'></div>", unsafe_allow_html=True)
        
        page = st.radio(
            " ",
            [
                "🏠 Accueil", 
                "📊 Données", 
                "📈 Visualisation", 
                "🤖 Modélisation", 
                "📚 Documentation"
            ],
            key="navigation"
        )
        
        st.markdown("<div class='styled-divider'></div>", unsafe_allow_html=True)
        
        # Contact professionnel
        st.markdown("#### 📞 Support Professionnel")
        st.markdown("""
        <div style="color: #d4d4d4; font-size: 0.9rem; line-height: 1.6; padding: 1rem;">
        <a href="mailto:slassina92@gmail.com" style="color: #60a5fa; text-decoration: none;">✉️ Envoyer un message</a><br><br>
        <a href="tel:+22674544113" style="color: #60a5fa; text-decoration: none;">📞 Appelez-Moi</a><br><br>
        <a href="https://www.linkedin.com/in/slassina/" target="_blank" style="color: #60a5fa; text-decoration: none;">🔗 Voir le profil LinkedIn</a><br><br>
        <a href="https://sanou-lassina.github.io/Ma_Page/" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 500; display: inline-block;">🌐 Voir mon portfolio</a>
        </div>

        """, unsafe_allow_html=True)

    # Routing des pages
    if page == "🏠 Accueil":
        show_homepage()
    elif page == "📊 Données":
        import Donnees
        Donnees.main()
    elif page == "📈 Visualisation":
        import Annalyse
        Annalyse.main()
    elif page == "🤖 Modélisation":
        import Modelisation
        Modelisation.main()
    elif page == "📚 Documentation":
        import Guide
        Guide.main()

def show_homepage():
    # Conteneur principal
    st.markdown("<div class='main'>", unsafe_allow_html=True)
        
    # CSS personnalisé avec animations et design moderne
    st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            
            .professional-header {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                padding: 25px 30px;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
                margin-bottom: 30px;
                color: white;
                position: relative;
                overflow: hidden;
                animation: fadeIn 1s ease-out;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .professional-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #10B981, #3B82F6, #EF4444);
                animation: shimmer 3s infinite;
            }
            
            .professional-header h1 {
                margin-bottom: 8px;
                font-weight: 700;
                font-size: 2.8rem;
                letter-spacing: 1px;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                animation: slideUp 0.8s ease-out 0.2s both;
            }
            
            .professional-header h6 {
                font-weight: 400;
                font-size: 1.1rem;
                opacity: 0.9;
                margin-bottom: 0;
                letter-spacing: 0.5px;
                animation: slideUp 0.8s ease-out 0.4s both;
            }
            
            .badge {
                display: inline-block;
                background: rgba(255, 255, 255, 0.15);
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.85rem;
                margin-top: 12px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: fadeIn 1s ease-out 0.6s both;
            }
            
            .pulse-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                background-color: #10B981;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
                vertical-align: middle;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes shimmer {
                0% { background-position: -200px 0; }
                100% { background-position: 200px 0; }
            }
            
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }
            
            /* Effet au survol */
            .professional-header:hover {
                transform: translateY(-2px);
                transition: transform 0.3s ease;
                box-shadow: 0 12px 30px rgba(30, 58, 138, 0.4);
            }
            </style>
    """, unsafe_allow_html=True)

        # Header professionnel avec animations
    st.markdown("""
            <div class="professional-header">
                <h1>🏠 HOUSEPREDICT</h1>
                <h6>
                    <span class="pulse-dot"></span>
                    Application de Prédiction Immobilière
                </h6>
                <div class="badge">
                    Développé par : Lassina SANOU
                </div>
            </div>
    """, unsafe_allow_html=True)
        

    # Barre de séparation
    st.markdown("---")

    # Header professionnel
    st.markdown("""
        
        <style>
        /* Texte de l'auteur en bas à gauche */
        .author-bottom-left {
            position: absolute;
            bottom: 15px;
            left: 20px;
            color: white;
            font-size: 0.9em;
            background: rgba(0,0,0,0.25);
            padding: 6px 15px;
            border-radius: 20px;
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.2);
            z-index: 2;
        }

        /* Animations dynamiques */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            from {
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                transform: scale(1);
            }
            to {
                text-shadow: 0 0 20px rgba(255,255,255,0.8), 2px 2px 4px rgba(0,0,0,0.3);
                transform: scale(1.02);
            }
        }

        @keyframes shimmer {
            100% {
                left: 100%;
            }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2em;
                letter-spacing: 1px;
                padding: 12px 0;
            }
            
            .header-container {
                padding: 20px 15px 35px;
            }
            
            .author-bottom-left {
                position: relative;
                bottom: 0;
                left: 0;
                text-align: center;
                margin-top: 15px;
                display: inline-block;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Introduction - MODIFIE: padding réduit
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0; max-width: 900px; margin: 0 auto;' class='content-animation'>
        <h2 style='color: #1e293b; font-size: 1.8rem; margin-bottom: 1rem;'>
            Bienvenue sur la Plateforme de Prediction de Prix des Maisons Immobilière
        </h2>
        <p style='color: #475569; font-size: 1.1rem; line-height: 1.8;'>
            HousePredict combine l'expertise en intelligence artificielle avec une analyse immobilière sophistiquée 
            pour offrir des prédictions de prix précises et des insights actionnables. Notre système utilise des 
            algorithmes de machine learning de pointe pour analyser des milliers de propriétés et identifier 
            les tendances du marché en temps réel.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section fonctionnalités avec descriptions détaillées
    st.markdown("<h2 class='section-title'>✨ Fonctionnalités Premium</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card content-animation delay-1'>
            <div class='feature-icon'>🔍</div>
            <h3>Exploration des Données</h3>
            <div class='feature-description'>
                Plongez au cœur de vos données immobilières avec notre module d'exploration avancé. 
                Visualisez les tendances historiques, identifiez les corrélations cachées et découvrez 
                les facteurs influençant les prix.
            </div>
            <div class='feature-details'>
                <ul>
                    <li>Analyse multidimensionnelle des propriétés</li>
                    <li>Visualisations interactives en temps réel</li>
                    <li>Détection automatique des outliers</li>
                    <li>Filtres avancés par critères multiples</li>
                    <li>Export de données formaté pour reporting</li>
                    <li>Statistiques descriptives complètes</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card content-animation delay-3'>
            <div class='feature-icon'>🤖</div>
            <h3>Modélisation Prédictive</h3>
            <div class='feature-description'>
                Notre système utilise XGBoost optimisé pour des prédictions de prix extrêmement précises. 
                L'algorithme s'entraîne sur des milliers de points de données pour fournir des estimations 
                fiables avec des intervalles de confiance.
            </div>
            <div class='feature-details'>
                <ul>
                    <li>Algorithme XGBoost optimisé et calibré</li>
                    <li>Feature engineering automatique</li>
                    <li>Validation croisée intégrée</li>
                    <li>Hyperparamètres optimisés automatiquement</li>
                    <li>Intervalles de confiance des prédictions</li>
                    <li>Explicabilité des décisions du modèle</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card content-animation delay-2'>
            <div class='feature-icon'>📊</div>
            <h3>Analytique Visuelle</h3>
            <div class='feature-description'>
                Transformez des données complexes en visualisations intuitives. Notre module d'analytique 
                offre des dashboards personnalisables, des graphiques interactifs et des rapports automatiques 
                pour une prise de décision éclairée.
            </div>
            <div class='feature-details'>
                <ul>
                    <li>Dashboards temps réel personnalisables</li>
                    <li>Graphiques interactifs Plotly avancés</li>
                    <li>Analyse comparative de marchés</li>
                    <li>Visualisation géospatiale des propriétés</li>
                    <li>Rapports automatisés en PDF/Excel</li>
                    <li>Alertes sur tendances anormales</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card content-animation delay-4'>
            <div class='feature-icon'>📈</div>
            <h3>Diagnostics et Optimisation</h3>
            <div class='feature-description'>
                Analysez la performance de votre modèle avec des outils de diagnostic complets. 
                Identifiez les sources d'erreur, optimisez les paramètres et améliorez continuellement 
                la précision de vos prédictions.
            </div>
            <div class='feature-details'>
                <ul>
                    <li>Analyse approfondie des résidus</li>
                    <li>Métriques de performance détaillées</li>
                    <li>Courbes d'apprentissage du modèle</li>
                    <li>Analyse d'importance des caractéristiques</li>
                    <li>Tests de robustesse du modèle</li>
                    <li>Recommandations d'optimisation</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Section base de données avancée
    st.markdown("<div class='styled-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>🏗️ Architecture de la Base de Données</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); height: 100%;'>
            <h4 style='color: #1e40af; margin-bottom: 1rem;'>🏗️ Structure Architecturale</h4>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Surface habitable :</strong> Analyse précise en pieds carrés avec segmentation par type d'espace</li>
                <li><strong>Chambres & pièces :</strong> Distribution et configuration spatiale détaillée</li>
                <li><strong>Année construction :</strong> Historique complet avec facteur d'âge actualisé</li>
                <li><strong>Qualité matériaux :</strong> Classification multi-niveaux selon standards internationaux</li>
                <li><strong>État général :</strong> Évaluation structurée selon 10 critères techniques</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); height: 100%;'>
            <h4 style='color: #059669; margin-bottom: 1rem;'>📍 Écosystème Local</h4>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Géolocalisation :</strong> Coordonnées précises avec analyse de voisinage</li>
                <li><strong>Quartier & zonage :</strong> Classification selon 5 catégories socio-économiques</li>
                <li><strong>Commodités :</strong> Proximité aux services essentiels (écoles, hôpitaux, transports)</li>
                <li><strong>Type rue & accessibilité :</strong> Analyse du trafic et connectivité</li>
                <li><strong>Configuration terrain :</strong> Topographie et utilisation optimale</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); height: 100%;'>
            <h4 style='color: #dc2626; margin-bottom: 1rem;'>💰 Facteurs de Valorisation</h4>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Aménagements premium :</strong> Piscine, spa, installations sportives</li>
                <li><strong>Garage & parking :</strong> Capacité, qualité et fonctionnalités</li>
                <li><strong>Extérieurs :</strong> Jardin, terrasse, espaces verts qualifiés</li>
                <li><strong>Surface sous-sol :</strong> Aménagée et aménageable avec potentiel</li>
                <li><strong>Équipements :</strong> Cuisine, salle de bain, climatisation, etc.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Section workflow professionnel
    st.markdown("<div class='styled-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>🎯 Workflow Professionnel</h2>", unsafe_allow_html=True)
    
    steps = [
        {
            "icon": "📊",
            "title": "1. Exploration des Données",
            "desc": "Importez et explorez votre jeu de données immobilières. Utilisez nos outils de visualisation pour comprendre la distribution des propriétés, identifier les valeurs aberrantes et préparer vos données pour l'analyse.",
            "features": ["Visualisation interactive", "Nettoyage automatique", "Statistiques descriptives"]
        },
        {
            "icon": "📈",
            "title": "2. Analyse Avancée",
            "desc": "Plongez dans l'analyse approfondie des corrélations entre les variables. Identifiez les facteurs clés influençant les prix et générez des insights actionnables pour votre stratégie immobilière.",
            "features": ["Analyse de corrélation", "Tendances temporelles", "Segmentation de marché"]
        },
        {
            "icon": "🤖",
            "title": "3. Modélisation",
            "desc": "Entraînez notre algorithme XGBoost optimisé sur vos données. Obtenez des prédictions précises avec des intervalles de confiance et comprenez l'importance relative de chaque caractéristique.",
            "features": ["Prédictions en temps réel", "Explicabilité AI", "Optimisation automatique"]
        },
        {
            "icon": "📋",
            "title": "4. Reporting & Export",
            "desc": "Générez des rapports professionnels complets avec visualisations et analyses. Exportez vos résultats dans les formats de votre choix pour présentation ou intégration.",
            "features": ["Rapports automatisés", "Exports multiples", "Dashboards personnalisables"]
        }
    ]
    
    for i, step in enumerate(steps):
        if i % 2 == 0:
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #3b82f6, #1e40af); color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;'>
                    <div style='font-size: 2.5rem; margin-bottom: 1rem;'>{step['icon']}</div>
                    <h4 style='margin-bottom: 1rem; font-size: 1.3rem;'>{step['title']}</h4>
                    <p style='margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;'>{step['desc']}</p>
                    <div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>
                        {''.join([f"<span style='background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem;'>{feature}</span>" for feature in step['features']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 2rem; border-radius: 15px; margin: 1rem 0;'>
                    <div style='font-size: 2.5rem; margin-bottom: 1rem;'>{step['icon']}</div>
                    <h4 style='margin-bottom: 1rem; font-size: 1.3rem;'>{step['title']}</h4>
                    <p style='margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;'>{step['desc']}</p>
                    <div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>
                        {''.join([f"<span style='background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem;'>{feature}</span>" for feature in step['features']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer professionnel
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='footer'>
        <h4>🏢 HousePredict - Prédiction Immobilière</h4>
        <p>
            Plateforme d'analyse et de prédiction immobilière par modélisation. 
            Transformez vos données en avantage concurrentiel avec notre solution complète de machine learning.
        </p>
        <p style='font-size: 0.9rem; margin-top: 1.5rem; color: #94a3b8;'>
        © 2025 HousePredict | Technologies : Streamlit · Régression Linéaire . Ridge . Lasso . Random Forest . Gradient Boosting . XGBoost · Plotly · Pandas · NumPy<br>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()