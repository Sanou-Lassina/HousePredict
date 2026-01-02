# Guide.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Guide Utilisateur",
    page_icon="📚",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .guide-header {
        background: linear-gradient(45deg, #9C27B0, #E91E63);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .section-card {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 6px solid #9C27B0;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-5px);
    }
    .step-number {
        background: #E91E63;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    .code-block {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
        border-left: 4px solid #9C27B0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .tip-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
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
            <h1 style="margin-bottom:10px;">📚 Guide Complet Utilisateur</h1>
            <h4 style="font-weight:normal;">
                HousePredict - Plateforme de Prédiction Immobilière
            </h4>
            <p>Découvrez comment exploiter toute la puissance de notre application HousePredict</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Table des matières
    st.sidebar.markdown("## 📖 Table des Matières")
    sections = [
        "🎯 Introduction et Vue d'Ensemble",
        "🏠 Page d'Accueil - Tableau de Bord",
        "📊 Page Données - Exploration des Données",
        "📈 Page Analyse - Analyse Exploratoire",
        "🤖 Page Modélisation - Prédictions",
        "🚀 Bonnes Pratiques et Conseils",
        "🔧 Dépannage et Support"
    ]
    
    selected_section = st.sidebar.radio("Navigation du Guide", sections)
    
    # Sections du guide
    if selected_section == "🎯 Introduction et Vue d'Ensemble":
        show_introduction()
    elif selected_section == "🏠 Page d'Accueil - Tableau de Bord":
        show_homepage_guide()
    elif selected_section == "📊 Page Données - Exploration des Données":
        show_data_guide()
    elif selected_section == "📈 Page Analyse - Analyse Exploratoire":
        show_analysis_guide()
    elif selected_section == "🤖 Page Modélisation - Prédictions":
        show_modeling_guide()
    elif selected_section == "🚀 Bonnes Pratiques et Conseils":
        show_best_practices()
    elif selected_section == "🔧 Dépannage et Support":
        show_troubleshooting()

def show_introduction():
    st.markdown("""
    <div class='section-card'>
        <h2>🎯 Introduction à HousePredict</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 Qu'est-ce que HousePredict ?
        
        **HousePredict** est une plateforme complète d'analyse et de prédiction immobilière 
        utilisant l'intelligence artificielle pour estimer avec précision les prix des maisons.
        
        Notre application combine :
        - **L'analyse exploratoire avancée** des données immobilières
        - **La modélisation prédictive** avec l'algorithme XGBoost
        - **La visualisation interactive** des résultats
        - **L'interface utilisateur intuitive** adaptée aux professionnels
        """)
    
    with col2:
        st.image(
        "architecture.png",
        caption="Architecture de l'Application",
        use_container_width=True
    )
    
    
    st.markdown("""
    ### 🎯 Objectifs de l'Application
    
    L'application a été conçue pour répondre à quatre objectifs principaux :
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='feature-box'>
            <h4>📊 Exploration</h4>
            <p>Comprendre et explorer le dataset immobilier</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-box'>
            <h4>🔍 Analyse</h4>
            <p>Découvrir les patterns et corrélations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-box'>
            <h4>🤖 Prédiction</h4>
            <p>Estimer les prix avec le Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='feature-box'>
            <h4>📈 Visualisation</h4>
            <p>Présenter les résultats clairement</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🏗️ Architecture de l'Application
    
    L'application est structurée en 4 modules principaux :
    """)
    
    # Diagramme d'architecture simplifié
    architecture_data = {
        'Module': ['Accueil', 'Donnees', 'Annalyse', 'Modelisation'],
        'Fonction': ['Navigation & Dashboard', 'Exploration des données', 'Analyse statistique', 'Prédictions'],
        'Technologies': ['Streamlit, Plotly', 'Pandas, NumPy', 'Plotly, Scipy', 'Scikit-learn, XGBoost, Gradient Boosting, Régression Linéaire, Ridge, Lasso']
    }
    
    df_arch = pd.DataFrame(architecture_data)
    st.dataframe(df_arch, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 👥 Public Cible
    
    Cette application est conçue pour :
    - **🏢 Agents immobiliers** voulant estimer des propriétés
    - **📊 Analystes de données** explorant le marché immobilier
    - **🎓 Étudiants** apprenant le machine learning appliqué
    - **💼 Investisseurs** cherchant des opportunités
    """)

def show_homepage_guide():
    st.markdown("""
    <div class='section-card'>
        <h2>🏠 Page d'Accueil - Tableau de Bord Principal</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎪 Présentation Générale
    
    La page d'accueil sert de **tableau de bord principal** et de **point d'entrée** 
    vers toutes les fonctionnalités de l'application.
    """)
    
    # Structure de la page d'accueil
    st.subheader("🎯 Structure de la Page")
    
    steps = [
        {
            "step": 1,
            "title": "Barre Latérale de Navigation",
            "description": "Menu principal permettant de naviguer entre les 4 pages de l'application",
            "details": "Contient les onglets : Accueil, Données, Analyse Exploratoire, Modélisation"
        },
        {
            "step": 2,
            "title": "Header Animé avec Métriques",
            "description": "Section d'introduction avec animations et indicateurs clés",
            "details": "Affiche les métriques principales : Précision, Nombre de maisons, Prix moyen, Algorithme"
        },
        {
            "step": 3,
            "title": "Cartes de Fonctionnalités",
            "description": "Présentation visuelle des principales fonctionnalités",
            "details": "4 cartes interactives décrivant chaque module de l'application"
        },
        {
            "step": 4,
            "title": "Démonstration Interactive",
            "description": "Simulateur de prédiction en temps réel",
            "details": "Permet de tester l'application avec des valeurs personnalisées"
        }
    ]
    
    for step in steps:
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"<div class='step-number'>{step['step']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{step['title']}**")
            st.markdown(f"*{step['description']}*")
            st.markdown(f"🔹 {step['details']}")
        st.markdown("---")
    
    st.markdown("""
    ### 🎮 Utilisation de la Démonstration Interactive
    
    La section de démonstration permet de :
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Ajuster les paramètres :**
        - Surface habitable (50-400 m²)
        - Nombre de chambres (1-6)
        - Qualité générale (1-10)
        - Année de construction
        - Salles de bain
        - Places de garage
        """)
    
    with col2:
        st.markdown("""
        **🎯 Obtenir des résultats :**
        - Prix estimé en dollars
        - Répartition du prix par composante
        - Graphique circulaire interactif
        - Calcul en temps réel
        """)
    
    st.markdown("""
    <div class='tip-box'>
        💡 <strong>Astuce :</strong> Utilisez la démonstration pour comprendre quels facteurs 
        influencent le plus le prix des maisons avant de passer aux analyses avancées.
    </div>
    """, unsafe_allow_html=True)

def show_data_guide():
    st.markdown("""
    <div class='section-card'>
        <h2>📊 Page Données - Exploration des Données</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🔍 Objectif de la Page
    
    La page **Données** permet d'explorer et de comprendre la structure du dataset immobilier 
    avant de procéder aux analyses avancées.
    """)
    
    st.subheader("📋 Fonctionnalités Principales")
    
    features = [
        {
            "icon": "👀",
            "title": "Aperçu du Dataset",
            "description": "Visualisation rapide des données avec métriques clés",
            "usage": "Comprendre la taille et la structure des données"
        },
        {
            "icon": "🎛️",
            "title": "Filtres Interactifs",
            "description": "Filtrage des données par colonnes et fourchettes de prix",
            "usage": "Isoler des sous-ensembles de données spécifiques"
        },
        {
            "icon": "📈",
            "title": "Statistiques Descriptives",
            "description": "Métriques statistiques complètes pour chaque variable",
            "usage": "Analyser la distribution et les tendances générales"
        },
        {
            "icon": "🔧",
            "title": "Structure des Données",
            "description": "Analyse des types de données et valeurs manquantes",
            "usage": "Préparer le prétraitement des données"
        },
        {
            "icon": "📊",
            "title": "Distribution des Variables",
            "description": "Histogrammes et graphiques de distribution",
            "usage": "Visualiser la répartition des valeurs"
        },
        {
            "icon": "💾",
            "title": "Export des Données",
            "description": "Téléchargement dans différents formats",
            "usage": "Utiliser les données dans d'autres outils"
        }
    ]
    
    # Affichage des fonctionnalités en grille
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='padding: 1rem; border: 1px solid #e0e0e0; border-radius: 10px; margin: 0.5rem 0;'>
                <h4>{feature['icon']} {feature['title']}</h4>
                <p><small>{feature['description']}</small></p>
                <p style='color: #666; font-size: 0.8rem;'><strong>Usage:</strong> {feature['usage']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Guide d'Utilisation Pas-à-Pas
    
    1. **Commencez par l'aperçu** : Vérifiez le nombre de maisons et variables
    2. **Utilisez les filtres** : Sélectionnez les colonnes à analyser
    3. **Explorez les statistiques** : Identifiez les variables importantes
    4. **Vérifiez la qualité** : Contrôlez les valeurs manquantes
    5. **Visualisez les distributions** : Comprenez la forme des données
    6. **Exportez si nécessaire** : Téléchargez pour analyses complémentaires
    """)
    
    st.markdown("""
    <div class='warning-box'>
        ⚠️ <strong>Attention :</strong> Les filtres appliqués sur cette page n'affectent pas 
        les autres pages. Chaque page fonctionne de manière indépendante.
    </div>
    """, unsafe_allow_html=True)

def show_analysis_guide():
    st.markdown("""
    <div class='section-card'>
        <h2>📈 Page Analyse - Analyse Exploratoire des Données (EDA)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🧠 Objectif de l'Analyse Exploratoire
    
    L'**Analyse Exploratoire des Données (EDA)** vise à découvrir des patterns, 
    des anomalies, des relations et des hypothèses dans le dataset immobilier.
    """)
    
    st.subheader("🔬 Techniques d'Analyse Disponibles")
    
    # Graphiques disponibles
    analysis_methods = {
        "Distribution des Prix": "Comprendre la répartition des prix de vente",
        "Matrice de Corrélation": "Identifier les relations entre variables",
        "Relations Linéaires": "Analyser les liens entre variables numériques",
        "Impact des Catégories": "Étudier l'influence des variables catégorielles",
        "Analyse Temporelle": "Observer les tendances dans le temps",
        "Analyse Multivariée": "Combiner plusieurs variables dans une visualisation"
    }
    
    for method, description in analysis_methods.items():
        col1, col2 = st.columns([2, 8])
        with col1:
            st.markdown(f"**{method}**")
        with col2:
            st.markdown(description)
    
    st.markdown("""
    ### 📊 Interprétation des Graphiques
    
    #### 🎯 Matrice de Corrélation
    - **Couleur bleue** : Corrélation positive forte
    - **Couleur rouge** : Corrélation négative forte  
    - **Couleur blanche** : Pas de corrélation
    - **Valeurs** : Coefficient de corrélation de -1 à +1
    
    #### 📈 Scatter Plots
    - **Points alignés** : Relation linéaire forte
    - **Nuage diffus** : Relation faible ou non-linéaire
    - **Ligne de tendance** : Direction générale de la relation
    
    #### 🏘️ Box Plots Catégoriels
    - **Médiane** : Valeur centrale du prix
    - **Boîte** : 50% des données (Q1 à Q3)
    - **Moustaches** : Étendue normale des données
    - **Points** : Valeurs extrêmes (outliers)
    """)
    
    st.markdown("""
    <div class='tip-box'>
        💡 <strong>Astuce d'analyse :</strong> Concentrez-vous d'abord sur les variables 
        les plus corrélées avec le prix (OverallQual, GrLivArea, etc.) pour identifier 
        les facteurs les plus influents.
    </div>
    """, unsafe_allow_html=True)

def show_modeling_guide():
    st.markdown("""
    <div class='section-card'>
        <h2>🤖 Page Modélisation - Prédictions par Machine Learning</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🧠 Algorithme XGBoost
    
    Notre application utilise **XGBoost (Extreme Gradient Boosting)**, un algorithme 
    de machine learning avancé particulièrement efficace pour les problèmes de régression.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 Avantages de XGBoost
        
        - **Haute précision** : Meilleures performances que nombreux autres algorithmes
        - **Rapidité** : Optimisé pour les grandes quantités de données
        - **Robustesse** : Gère bien les valeurs manquantes et le bruit
        - **Interprétabilité** : Permet d'analyser l'importance des variables
        """)
    
    with col2:
        st.markdown("""
        #### 📊 Métriques d'Évaluation
        
        - **RMSE** : Racine de l'erreur quadratique moyenne (en dollars)
        - **MAE** : Erreur absolue moyenne (en dollars)
        - **R²** : Coefficient de détermination (0 à 1)
        - **MAPE** : Erreur percentage moyenne
        """)
    
    st.subheader("🔍 Analyse des Résidus")
    
    st.markdown("""
    L'analyse des résidus est cruciale pour valider la qualité du modèle :
    """)
    
    residual_analysis = [
        ("Distribution des Résidus", "Doit suivre une distribution normale centrée sur 0"),
        ("Résidus vs Prédictions", "Doit montrer une dispersion homogène (homoscédasticité)"),
        ("Prédictions vs Réelles", "Les points doivent suivre la ligne de parfaite prédiction"),
        ("QQ-Plot", "Les points doivent suivre la ligne normale")
    ]
    
    for analysis, interpretation in residual_analysis:
        st.markdown(f"**{analysis}** : {interpretation}")
    
    st.markdown("""
    ### 🎮 Prédictions en Temps Réel
    
    La section de prédiction individuelle permet de :
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📝 Saisir les caractéristiques :**
        - Surface habitable
        - Qualité générale
        - Surface du sous-sol
        - Année de construction
        - Places de garage
        """)
    
    with col2:
        st.markdown("""
        **💰 Obtenir la prédiction :**
        - Prix estimé en temps réel
        - Intervalle de confiance à 95%
        - Affichage visuel attractif
        - Métriques de confiance
        """)
    
    st.markdown("""
    <div class='warning-box'>
        ⚠️ <strong>Limitations :</strong> Le modèle a été entraîné sur des données spécifiques. 
        Les prédictions peuvent être moins précises pour des propriétés très atypiques 
        ou en dehors des plages d'entraînement.
    </div>
    """, unsafe_allow_html=True)

def show_best_practices():
    st.markdown("""
    <div class='section-card'>
        <h2>🚀 Bonnes Pratiques et Conseils d'Utilisation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    #### 🎯 Workflow Recommandé
    
    Pour une utilisation optimale de l'application, suivez cette séquence :
    """)
    
    workflow_steps = [
        ("1. Exploration", "Page Données - Comprenez la structure de vos données"),
        ("2. Analyse", "Page Analyse - Identifiez les patterns et relations"),
        ("3. Modélisation", "Page Modélisation - Utilisez les prédictions ML"),
        ("4. Validation", "Analysez les résidus et métriques de performance")
    ]
    
    for step, description in workflow_steps:
        st.markdown(f"**{step}** : {description}")
    
    st.subheader("💡 Conseils pour l'Analyse")
    
    tips = [
        "🎯 **Commencez simple** : Analysez d'abord les variables les plus corrélées avec le prix",
        "📊 **Utilisez les filtres** : Isolez des segments spécifiques du marché",
        "🔍 **Vérifiez les outliers** : Identifiez les valeurs extrêmes qui pourraient biaiser l'analyse",
        "📈 **Comparez les visualisations** : Utilisez différents types de graphiques pour la même variable",
        "🤖 **Validez le modèle** : Toujours vérifier l'analyse des résidus avant de faire confiance aux prédictions"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")
    
    st.subheader("🚫 Pièces à Éviter")
    
    warnings = [
        "Ne pas ignorer l'analyse des résidus",
        "Éviter de surinterpréter les corrélations faibles",
        "Ne pas utiliser le modèle en dehors de ses plages d'entraînement",
        "Éviter de prendre des décisions basées uniquement sur les prédictions ML"
    ]
    
    for warning in warnings:
        st.markdown(f"⚠️ {warning}")

def show_troubleshooting():
    st.markdown("""
    <div class='section-card'>
        <h2>🔧 Dépannage et Support Technique</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    En cas de problème persistant :
    
    - **📧 Email** : slassina92@gmail.com
    - **📚 Documentation** : https://www.kaggle.com/code/michaelfumery/exercice-pr-diction-de-prix-de-maison
    - **🐛 GitHub** : https://github.com/Sanou-Lassina
    
    **Informations à fournir :**
    - Message d'erreur complet
    - Steps pour reproduire le problème
    - Version de Python et des packages
    - Configuration système
    """)
    
    st.markdown("""
    <div class='tip-box'>
        🔧 <strong>Pour les développeurs :</strong> L'application est open-source et 
        peut être étendue. Consultez le code source sur GitHub pour contribuer 
        ou personnaliser les fonctionnalités.
    </div>
    """, unsafe_allow_html=True)
    
    # Footer du guide
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>🎉 Merci d'utiliser HousePredict !</h3>
        <p>Nous espérons que ce guide vous aidera à tirer le meilleur parti de notre application.</p>
        <p>Bonne analyse ! 🏠✨</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()