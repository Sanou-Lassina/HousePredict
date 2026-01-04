# Annalyse.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
from scipy.stats import norm, probplot
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO, BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Analyse Exploratoire Avancée - HousePredict", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avancé
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }
    
    /* Navigation horizontale */
    .horizontal-nav {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .nav-button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 25px;
        border: none;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        min-width: 110px;
        text-align: center;
        white-space: nowrap;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
    }
    
    .section-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .section-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.3rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #e17055;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #667eea !important;
    }
    
    .variable-group {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Ajustements pour démarrer plus haut */
    .block-container {
        padding-top: 1rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dataset():
    train = pd.read_csv("train.csv",
                        sep=';', encoding='utf-8', on_bad_lines='warn')
    test  = pd.read_csv("test.csv",
                        sep=';', encoding='utf-8', on_bad_lines='warn')
    
    df = pd.concat([train, test], axis=0, ignore_index=True)
    df = df.drop(columns=['Id'])

    # Conversion ObjectDType → str
    for col in df.columns:
        if "object" in str(df[col].dtype) or "ObjectDType" in str(df[col].dtype):
            df[col] = df[col].astype(str)

    return df

def create_horizontal_navigation():
    """Crée la navigation horizontale unique"""
    
    # Initialiser l'état de la section
    if 'analysis_section' not in st.session_state:
        st.session_state.analysis_section = "target"
    
    # Créer les boutons de navigation dans une seule ligne
    st.markdown("### 📊 Navigation Analyse")
    
    # Utiliser des colonnes pour aligner les boutons horizontalement
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🎯 Variable Cible", 
                    use_container_width=True, 
                    type="primary" if st.session_state.analysis_section == "target" else "secondary",
                    key="nav_target"):
            st.session_state.analysis_section = "target"
            st.rerun()
    
    with col2:
        if st.button("🔄 Corrélation", 
                    use_container_width=True,
                    type="primary" if st.session_state.analysis_section == "correlation" else "secondary",
                    key="nav_correlation"):
            st.session_state.analysis_section = "correlation"
            st.rerun()
    
    with col3:
        if st.button("📊 Relations", 
                    use_container_width=True,
                    type="primary" if st.session_state.analysis_section == "relations" else "secondary",
                    key="nav_relations"):
            st.session_state.analysis_section = "relations"
            st.rerun()
    
    with col4:
        if st.button("🏘️ Catégorielles", 
                    use_container_width=True,
                    type="primary" if st.session_state.analysis_section == "categorical" else "secondary",
                    key="nav_categorical"):
            st.session_state.analysis_section = "categorical"
            st.rerun()
    
    with col5:
        if st.button("🎭 Multivariée", 
                    use_container_width=True,
                    type="primary" if st.session_state.analysis_section == "multivariate" else "secondary",
                    key="nav_multivariate"):
            st.session_state.analysis_section = "multivariate"
            st.rerun()
    
    with col6:
        if st.button("📅 Temporelle", 
                    use_container_width=True,
                    type="primary" if st.session_state.analysis_section == "temporal" else "secondary",
                    key="nav_temporal"):
            st.session_state.analysis_section = "temporal"
            st.rerun()
    
    # Séparateur
    st.markdown("---")
    
    return st.session_state.analysis_section

def analyze_target_variable(df):
    """Analyse de la variable cible SalePrice"""
    st.markdown("<div class='section-card'><h3>🎯 Analyse de la Variable Cible</h3></div>", unsafe_allow_html=True)
    
    # Métriques statistiques avancées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Moyenne</h4>
            <h3>${df['SalePrice'].mean():,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Médiane</h4>
            <h3>${df['SalePrice'].median():,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Écart-type</h4>
            <h3>${df['SalePrice'].std():,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Skewness</h4>
            <h3>{df['SalePrice'].skew():.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques avancés de distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogramme avec courbe de densité et distribution normale
        fig = go.Figure()
        
        # Histogramme
        fig.add_trace(go.Histogram(
            x=df['SalePrice'], 
            nbinsx=50,
            name='Distribution',
            marker_color='#667eea',
            opacity=0.7,
            histnorm='probability density'
        ))
        
        # Courbe de densité KDE
        density = stats.gaussian_kde(df['SalePrice'].dropna())
        x_range = np.linspace(df['SalePrice'].min(), df['SalePrice'].max(), 100)
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=density(x_range),
            mode='lines',
            name='Densité KDE',
            line=dict(color='#ff6b6b', width=3)
        ))
        
        # Distribution normale théorique
        mu, sigma = df['SalePrice'].mean(), df['SalePrice'].std()
        normal_curve = norm.pdf(x_range, mu, sigma)
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=normal_curve,
            mode='lines',
            name='Distribution Normale',
            line=dict(color='#4ecdc4', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Distribution de SalePrice avec Analyse de Normalité',
            xaxis_title='Prix de Vente ($)',
            yaxis_title='Densité de Probabilité',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot avancé avec outliers
        fig = px.box(df, y='SalePrice', 
                    title="Analyse des Outliers - SalePrice",
                    color_discrete_sequence=['#ffa726'])
        
        # Ajouter des annotations pour les outliers
        Q1 = df['SalePrice'].quantile(0.25)
        Q3 = df['SalePrice'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[df['SalePrice'] > upper_bound]
        
        fig.add_annotation(
            x=0, y=upper_bound,
            text=f"Seuil Outliers: ${upper_bound:,.0f}",
            showarrow=True,
            arrowhead=2,
            ax=-50,
            ay=-40
        )
        
        fig.update_layout(
            yaxis_title="Prix de Vente ($)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # QQ-Plot et transformation
    col1, col2 = st.columns(2)
    
    with col1:
        # QQ-Plot
        fig = go.Figure()
        
        # Calcul des quantiles
        sorted_data = np.sort(df['SalePrice'].dropna())
        theoretical_quantiles = stats.norm.ppf(
            np.linspace(0.01, 0.99, len(sorted_data))
        )
        
        fig.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=sorted_data,
            mode='markers',
            marker=dict(color='#667eea', size=6),
            name='Quantiles Observés'
        ))
        
        # Ligne de référence
        min_val = min(theoretical_quantiles.min(), sorted_data.min())
        max_val = max(theoretical_quantiles.max(), sorted_data.max())
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(color='#ff6b6b', dash='dash'),
            name='Ligne de Normalité'
        ))
        
        fig.update_layout(
            title='QQ-Plot - Test de Normalité',
            xaxis_title='Quantiles Théoriques',
            yaxis_title='Quantiles Observés'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Analyse des transformations
        st.subheader("🔧 Transformation des Données")
        
        original_skew = df['SalePrice'].skew()
        log_skew = np.log1p(df['SalePrice']).skew()
        sqrt_skew = np.sqrt(df['SalePrice']).skew()
        
        transform_data = {
            'Transformation': ['Original', 'Log(x+1)', 'Racine Carrée'],
            'Skewness': [original_skew, log_skew, sqrt_skew],
            'Recommandation': ['Non recommandé', '✅ Optimal', 'Amélioration']
        }
        
        transform_df = pd.DataFrame(transform_data)
        st.dataframe(transform_df, use_container_width=True, hide_index=True)
        
        # Graphique de comparaison des transformations
        fig = make_subplots(rows=1, cols=3, 
                    subplot_titles=['Original', 'Log Transformation', 'Racine Carrée'])
        
        # Original
        fig.add_trace(go.Histogram(x=df['SalePrice'], nbinsx=30, name='Original'), 1, 1)
        # Log
        fig.add_trace(go.Histogram(x=np.log1p(df['SalePrice']), nbinsx=30, name='Log'), 1, 2)
        # Sqrt
        fig.add_trace(go.Histogram(x=np.sqrt(df['SalePrice']), nbinsx=30, name='Sqrt'), 1, 3)
        
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

def advanced_correlation_analysis(df):
    """Analyse de corrélation avancée"""
    st.markdown("<div class='section-card'><h2>🔄 Analyse de Corrélation</h2></div>", unsafe_allow_html=True)
    
    # Sélection des variables numériques
    numeric_cols = df.select_dtypes(include=['number']).columns
    seuil = 10  # Seuil plus élevé pour plus de précision
    numeric_cols_filtered = [col for col in numeric_cols if df[col].nunique() > seuil]
    
    # Matrice de corrélation
    corr_matrix = df[numeric_cols_filtered].corr()
    
    # Heatmap interactive avancée
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        hoverongaps=False,
        text=corr_matrix.round(3),
        texttemplate="%{text}",
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Corrélation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="🔄 Matrice de Corrélation - Analyse des Relations Linéaires",
        width=1000,
        height=800,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Analyse détaillée des corrélations avec SalePrice
    st.subheader("🎯 Analyse des Corrélations avec SalePrice")
    
    sale_price_corr = corr_matrix['SalePrice'].sort_values(ascending=False)
    
    # Top 10 des corrélations positives et négatives
    col1, col2 = st.columns(2)
    
    with col1:
        top_positive = sale_price_corr[1:11]  # Exclure SalePrice lui-même
        fig = px.bar(x=top_positive.values, y=top_positive.index,
                    orientation='h',
                    title="Top 10 - Corrélations Positives",
                    color=top_positive.values,
                    color_continuous_scale='viridis')
        fig.update_layout(xaxis_title="Coefficient de Corrélation", yaxis_title="Variables")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        top_negative = sale_price_corr.tail(10)
        fig = px.bar(x=top_negative.values, y=top_negative.index,
                    orientation='h',
                    title="Top 10 - Corrélations Négatives",
                    color=top_negative.values,
                    color_continuous_scale='viridis_r')
        fig.update_layout(xaxis_title="Coefficient de Corrélation", yaxis_title="Variables")
        st.plotly_chart(fig, use_container_width=True)







def variable_relationship_analysis(df):
    """Analyse des relations entre variables"""
    st.markdown("<div class='section-card'><h3>📊 Analyse des relations entre les variables</h3></div>", unsafe_allow_html=True)
    
    # Créer une copie du DataFrame pour éviter les modifications
    df_clean = df.copy()
    
    # Sélection des variables
    numeric_cols = df_clean.select_dtypes(include=['number']).columns
    seuil = 10
    numeric_cols_filtered = [col for col in numeric_cols if df_clean[col].nunique() > seuil]
    
    # S'assurer que SalePrice est dans la liste s'il existe
    target_var = 'SalePrice'
    if target_var in numeric_cols and target_var not in numeric_cols_filtered:
        numeric_cols_filtered.append(target_var)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='variable-group'><h5>🔍 Variables Numériques</h5></div>", unsafe_allow_html=True)
        x_var = st.selectbox("Variable X (Numérique):", numeric_cols_filtered, index=1, key="rel_x")
    
    with col2:
        st.markdown("<div class='variable-group'><h5>🎯 Variable Cible</h5></div>", unsafe_allow_html=True)
        # Exclure la variable X déjà sélectionnée
        y_options = [target_var] + [col for col in numeric_cols_filtered 
                                  if col != target_var and col != x_var]
        y_var = st.selectbox("Variable Y:", y_options, index=0, key="rel_y")
    
    with col3:
        st.markdown("<div class='variable-group'><h5>🎨 Variables Catégorielles</h5></div>", unsafe_allow_html=True)
        categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
        color_var = st.selectbox("Variable de couleur (Catégorielle):", 
                               ['Aucune'] + list(categorical_cols), key="rel_color")
    
    # VÉRIFICATION : X et Y ne doivent pas être identiques
    if x_var == y_var:
        st.error("❌ **Erreur :** Les variables X et Y ne peuvent pas être identiques.")
        st.info("Veuillez sélectionner des variables différentes pour l'analyse.")
        
        # Afficher des suggestions
        st.markdown("**Suggestions :**")
        alternative_vars = [col for col in numeric_cols_filtered 
                          if col != x_var and col != target_var][:5]
        if alternative_vars:
            st.write("**Variables suggérées pour Y :**")
            for var in alternative_vars:
                st.write(f"  • {var}")
        return
    
    # Préparer les données pour le graphique
    plot_data = df_clean.copy()
    
    # Colonnes à inclure dans le graphique
    cols_needed = [x_var, y_var]
    if color_var != 'Aucune':
        cols_needed.append(color_var)
    
    # Supprimer les valeurs manquantes
    plot_data = plot_data[cols_needed].dropna()
    
    # Vérifier qu'il reste des données
    if len(plot_data) == 0:
        st.warning("⚠️ **Aucune donnée disponible** après suppression des valeurs manquantes.")
        st.info("Veuillez sélectionner d'autres variables.")
        return
    
    # Création du scatter plot
    try:
        # Préparer les données de survol sans doublons
        hover_cols = []
        # Ajouter jusqu'à 3 colonnes supplémentaires (en excluant celles déjà utilisées)
        additional_cols = [col for col in df_clean.columns 
                          if col not in cols_needed][:3]
        hover_cols = additional_cols
        
        if color_var != 'Aucune':
            fig = px.scatter(
                plot_data, 
                x=x_var, 
                y=y_var, 
                color=color_var,
                title=f"Relation {x_var} vs {y_var} par {color_var}",
                trendline="ols",
                opacity=0.6,
                hover_data=hover_cols if hover_cols else None,
                color_discrete_sequence=px.colors.qualitative.Set1
            )
        else:
            fig = px.scatter(
                plot_data, 
                x=x_var, 
                y=y_var,
                title=f"Relation {x_var} vs {y_var}",
                trendline="ols",
                color_discrete_sequence=['#667eea'],
                opacity=0.6,
                hover_data=hover_cols if hover_cols else None
            )
        
        # Calcul des métriques avancées
        correlation = plot_data[x_var].corr(plot_data[y_var])
        r_squared = correlation ** 2
        
        # Ajouter les métriques au graphique
        fig.add_annotation(
            x=0.02, y=0.98,
            xref="paper", yref="paper",
            text=f"Corrélation: {correlation:.3f}<br>R²: {r_squared:.3f}",
            showarrow=False,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=12, color="black")
        )
        
        # Améliorer le layout
        fig.update_layout(
            xaxis_title=f"{x_var}",
            yaxis_title=f"{y_var}",
            hovermode='closest',
            showlegend=True if color_var != 'Aucune' else False,
            legend_title_text=color_var if color_var != 'Aucune' else None
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Informations supplémentaires
        with st.expander("📈 Métriques détaillées"):
            col_metrics1, col_metrics2 = st.columns(2)
            
            with col_metrics1:
                st.metric("Corrélation", f"{correlation:.3f}")
                st.metric("Coefficient de détermination (R²)", f"{r_squared:.3f}")
                
                # Interprétation qualitative
                if abs(correlation) >= 0.8:
                    corr_strength = "Très forte"
                elif abs(correlation) >= 0.6:
                    corr_strength = "Forte"
                elif abs(correlation) >= 0.4:
                    corr_strength = "Modérée"
                elif abs(correlation) >= 0.2:
                    corr_strength = "Faible"
                else:
                    corr_strength = "Très faible"
                
                st.info(f"**Relation :** {corr_strength}")
            
            with col_metrics2:
                # Statistiques descriptives
                st.write("**Statistiques :**")
                stats_df = plot_data[[x_var, y_var]].describe().round(2)
                st.dataframe(stats_df, use_container_width=True)
        
        # Afficher les informations sur les données utilisées
        st.info(f"📊 **Données utilisées :** {len(plot_data)} observations (valeurs non-manquantes)")
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la création du graphique : {str(e)}")
        
        # Solution de secours simple
        try:
            st.info("Tentative de création d'un graphique simplifié...")
            fig_simple = px.scatter(
                plot_data, 
                x=x_var, 
                y=y_var,
                title=f"Relation {x_var} vs {y_var} (version simplifiée)",
                color_discrete_sequence=['#667eea'],
                opacity=0.6
            )
            
            # Calcul simple de corrélation
            correlation_simple = plot_data[x_var].corr(plot_data[y_var])
            fig_simple.add_annotation(
                x=0.02, y=0.98,
                xref="paper", yref="paper",
                text=f"Corrélation: {correlation_simple:.3f}",
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
            
            st.plotly_chart(fig_simple, use_container_width=True)
            
        except Exception as e2:
            st.error(f"Impossible d'afficher le graphique : {str(e2)}")
            st.write("Veuillez sélectionner d'autres variables ou vérifier vos données.")









def categorical_analysis(df):
    """Analyse approfondie des variables catégorielles"""
    st.markdown("<div class='section-card'><h3>🏘️ Analyse des Variables Catégorielles</h3></div>", unsafe_allow_html=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='variable-group'><h5>📋 Sélection Variable Catégorielle</h5></div>", unsafe_allow_html=True)
        cat_var = st.selectbox("Choisir une variable catégorielle:", categorical_cols)
    
    with col2:
        st.markdown("<div class='variable-group'><h5>🎛️ Options d'Analyse</h5></div>", unsafe_allow_html=True)
        analysis_type = st.selectbox("Type d'analyse:", 
                                ["Box Plot", "Violin Plot", "Prix Moyen", "Distribution"])
    
    if analysis_type == "Box Plot":
        fig = px.box(df, x=cat_var, y='SalePrice',
                    title=f"Distribution des Prix par {cat_var}",
                    color=cat_var)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Violin Plot":
        fig = px.violin(df, x=cat_var, y='SalePrice',
                    title=f"Distribution en Violon - {cat_var}",
                    color=cat_var,
                    box=True)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Prix Moyen":
        avg_price = df.groupby(cat_var)['SalePrice'].agg(['mean', 'std', 'count']).reset_index()
        avg_price = avg_price.sort_values('mean', ascending=True)
        
        fig = px.bar(avg_price, x='mean', y=cat_var,
                    orientation='h',
                    title=f"Prix Moyen par {cat_var}",
                    error_x='std',
                    color='mean',
                    color_continuous_scale='viridis')
        fig.update_layout(xaxis_title="Prix Moyen ($)", yaxis_title=cat_var)
        st.plotly_chart(fig, use_container_width=True)






def multivariate_analysis(df):
    """Analyse multivariée avancée"""
    st.markdown("<div class='section-card'><h3>🎭 Analyse Multivariée Avancée</h3></div>", unsafe_allow_html=True)
    
    # Créer une copie pour éviter les modifications accidentelles
    df_clean = df.copy()
    
    # Filtrer les colonnes numériques avec plus de valeurs uniques
    numeric_cols = df_clean.select_dtypes(include=['number']).columns
    categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
    
    seuil = 10
    numeric_cols_filtered = [col for col in numeric_cols if df_clean[col].nunique() > seuil]
    
    # S'assurer que SalePrice est inclus s'il existe
    target_var = 'SalePrice'
    if target_var in numeric_cols and target_var not in numeric_cols_filtered:
        numeric_cols_filtered.append(target_var)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        x_var = st.selectbox("Axe X:", numeric_cols_filtered, 
                           index=min(1, len(numeric_cols_filtered)-1), 
                           key="multivar_x")
    with col2:
        # Filtrer pour exclure la variable X déjà sélectionnée (sauf pour SalePrice)
        y_options = [target_var] + [col for col in numeric_cols_filtered 
                                   if col != target_var and col != x_var]
        if x_var != target_var:
            y_options = [target_var] + [col for col in numeric_cols_filtered 
                                       if col != target_var and col != x_var]
        
        y_var = st.selectbox("Axe Y:", y_options, 
                           index=0, key="multivar_y")
    
    with col3:
        # Exclure les variables déjà sélectionnées pour X et Y
        size_options = ['Aucune'] + [col for col in numeric_cols_filtered 
                                    if col not in [x_var, y_var]]
        size_var = st.selectbox("Variable taille:", size_options, 
                              index=0, key="multivar_size")
    
    with col4:
        color_options = ['Aucune'] + list(categorical_cols)
        color_cat_var = st.selectbox("Variable couleur:", color_options, 
                                   key="multivar_color")
    
    # VÉRIFICATION : X et Y ne doivent pas être identiques
    if x_var == y_var:
        st.error("❌ **Erreur :** Les variables X et Y ne peuvent pas être identiques.")
        st.info("Veuillez sélectionner des variables différentes pour l'axe X et l'axe Y.")
        
        # Afficher un graphique alternatif avec une suggestion
        st.markdown("**Suggestions :**")
        st.write(f"- Gardez **{x_var}** sur l'axe X")
        st.write(f"- Sélectionnez une autre variable pour l'axe Y")
        
        # Proposer des alternatives
        alternative_vars = [col for col in numeric_cols_filtered 
                          if col != x_var and col != target_var][:5]
        if alternative_vars:
            st.write("**Variables suggérées pour Y :**")
            for var in alternative_vars:
                st.write(f"  • {var}")
        
        return  # Arrêter l'exécution ici
    
    # Préparer les données pour le plot
    plot_data = df_clean.copy()
    
    # Gérer les valeurs manquantes pour les colonnes sélectionnées
    cols_to_clean = [x_var, y_var]
    if size_var != 'Aucune':
        cols_to_clean.append(size_var)
    if color_cat_var != 'Aucune':
        cols_to_clean.append(color_cat_var)
    
    # Supprimer les lignes avec NaN dans les colonnes utilisées
    plot_data = plot_data[cols_to_clean].dropna()
    
    # Vérifier si on a suffisamment de données après nettoyage
    if len(plot_data) == 0:
        st.warning("⚠️ **Données insuffisantes :** Toutes les lignes ont été supprimées à cause de valeurs manquantes.")
        st.info("Essayez de sélectionner d'autres variables ou vérifiez les données manquantes.")
        return
    
    # Scatter plot avec gestion des erreurs
    try:
        if size_var != 'Aucune' and color_cat_var != 'Aucune':
            # S'assurer que la variable size est numérique
            if pd.api.types.is_numeric_dtype(plot_data[size_var]):
                fig = px.scatter(plot_data, x=x_var, y=y_var, size=size_var, 
                               color=color_cat_var,
                               title=f"Relation {x_var} vs {y_var} - Multidimensionnelle",
                               hover_data=[col for col in plot_data.columns 
                                         if col not in [x_var, y_var, size_var, color_cat_var]][:3],
                               opacity=0.7,
                               color_discrete_sequence=px.colors.qualitative.Set1)
            else:
                st.warning(f"La variable '{size_var}' doit être numérique pour l'utiliser comme taille.")
                fig = px.scatter(plot_data, x=x_var, y=y_var, color=color_cat_var,
                               title=f"Relation {x_var} vs {y_var} par {color_cat_var}",
                               opacity=0.7,
                               color_discrete_sequence=px.colors.qualitative.Set1)
        
        elif size_var != 'Aucune':
            if pd.api.types.is_numeric_dtype(plot_data[size_var]):
                fig = px.scatter(plot_data, x=x_var, y=y_var, size=size_var,
                               title=f"Relation {x_var} vs {y_var} (taille: {size_var})",
                               color_discrete_sequence=['#667eea'],
                               opacity=0.7)
            else:
                st.warning(f"La variable '{size_var}' doit être numérique pour l'utiliser comme taille.")
                fig = px.scatter(plot_data, x=x_var, y=y_var,
                               title=f"Relation {x_var} vs {y_var}",
                               color_discrete_sequence=['#667eea'],
                               opacity=0.7)
        
        elif color_cat_var != 'Aucune':
            fig = px.scatter(plot_data, x=x_var, y=y_var, color=color_cat_var,
                           title=f"Relation {x_var} vs {y_var} par {color_cat_var}",
                           opacity=0.7,
                           color_discrete_sequence=px.colors.qualitative.Set1)
        else:
            fig = px.scatter(plot_data, x=x_var, y=y_var,
                           title=f"Relation {x_var} vs {y_var}",
                           color_discrete_sequence=['#667eea'],
                           opacity=0.7)
        
        # Personnaliser le layout
        fig.update_layout(
            xaxis_title=x_var,
            yaxis_title=y_var,
            hovermode='closest',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les informations sur les données utilisées
        with st.expander("ℹ️ Informations sur les données utilisées"):
            st.write(f"**Nombre de points affichés :** {len(plot_data)}")
            st.write(f"**Colonnes utilisées :** {', '.join(cols_to_clean)}")
            if size_var != 'Aucune':
                st.write(f"**Variable taille :** {size_var}")
            if color_cat_var != 'Aucune':
                st.write(f"**Variable couleur :** {color_cat_var} (catégories : {plot_data[color_cat_var].nunique()})")
            
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique : {str(e)}")
        st.info("Essayez de sélectionner d'autres variables ou vérifiez les types de données.")
        
        # Afficher un graphique simple de secours
        try:
            fig = px.scatter(plot_data, x=x_var, y=y_var,
                           title=f"Relation {x_var} vs {y_var} (version simplifiée)",
                           color_discrete_sequence=['#667eea'],
                           opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.write("Impossible d'afficher le graphique avec les variables sélectionnées.")






def temporal_analysis(df):
    """Analyse temporelle avancée"""
    st.markdown("<div class='section-card'><h3>📅 Analyse Temporelle et Saisonnière</h3></div>", unsafe_allow_html=True)
    
    # Vérifier les colonnes temporelles disponibles
    time_cols = ['YearBuilt', 'YearRemodAdd', 'YrSold', 'MoSold']
    available_time_cols = [col for col in time_cols if col in df.columns]
    
    if available_time_cols:
        time_var = st.selectbox("Variable temporelle:", available_time_cols, key="temporal_var")
        
        # Analyse par période
        temporal_stats = df.groupby(time_var)['SalePrice'].agg([
            'count', 'mean', 'median', 'std'
        ]).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution du prix moyen
            fig = px.line(temporal_stats, x=time_var, y='mean',
                        title=f"Évolution du Prix Moyen par {time_var}",
                        markers=True)
            fig.update_traces(line=dict(color='#ff6b6b', width=3))
            fig.add_trace(go.Scatter(
                x=temporal_stats[time_var],
                y=temporal_stats['mean'] + temporal_stats['std'],
                fill=None,
                mode='lines',
                line=dict(color='lightgray'),
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=temporal_stats[time_var],
                y=temporal_stats['mean'] - temporal_stats['std'],
                fill='tonexty',
                mode='lines',
                line=dict(color='lightgray'),
                name='± Écart-type'
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Nombre de ventes par période
            fig = px.bar(temporal_stats, x=time_var, y='count',
                        title=f"Nombre de Ventes par {time_var}",
                        color='count',
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)

def main():
    # Démarrer plus haut en réduisant l'espace
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    
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
            <h1 style="margin-bottom:10px;">📈 Analyse Exploratoire des données</h1>
            <h4 style="font-weight:normal;">
                Analyse Exploratoire Avancée – Comprendre les Facteurs Clés et Dévoiler les Insights Stratégiques
            </h4>
        </div>
    """, unsafe_allow_html=True)
    
    # Chargement optimisé des données
    with st.spinner('🔄 Chargement et préparation des données...'):
        df = load_dataset()
    
    # Navigation horizontale UNIQUE
    current_section = create_horizontal_navigation()
    
    # Affichage des sections d'analyse
    if current_section == "target":
        analyze_target_variable(df)
    elif current_section == "correlation":
        advanced_correlation_analysis(df)
    elif current_section == "relations":
        variable_relationship_analysis(df)
    elif current_section == "categorical":
        categorical_analysis(df)
    elif current_section == "multivariate":
        multivariate_analysis(df)
    elif current_section == "temporal":
        temporal_analysis(df)
    
    # Section insights globaux
    st.markdown("<div class='section-card'><h4>💡 Insights et Recommandations Globales</h4></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='insight-box'>
            <h5>🎯 Insights Clés</h5>
            <ul>
                <li><strong>OverallQual</strong> est le prédicteur le plus puissant</li>
                <li>La surface habitable (<strong>GrLivArea</strong>) explique 50%+ de la variance</li>
                <li>L'année de construction impacte significativement le prix</li>
                <li>Présence de multicolinéarité entre certaines variables</li>
                <li>Distribution des prix nécessite une transformation log</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='warning-box'>
            <h5>⚠️ Recommandations Modélisation</h5>
            <ul>
                <li>Appliquer une transformation log sur SalePrice</li>
                <li>Gérer la multicolinéarité dans le feature engineering</li>
                <li>Encoder correctement les variables catégorielles</li>
                <li>Considérer l'importance des variables de localisation</li>
                <li>Valider les hypothèses de normalité des résidus</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()