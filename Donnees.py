import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ------------------------------
# 🔧 Fonction pour corriger ObjectDType pour Plotly
# ------------------------------
def sanitize_df_for_plotly(df):
    """Convertit les ObjectDType en string pour la compatibilité Plotly."""
    df = df.copy()
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        if "ObjectDType" in dtype_str or "object" in dtype_str:
            df[col] = df[col].astype(str)
    return df

# ------------------------------
# 🚀 Chargement optimisé des données (cache)
# ------------------------------
@st.cache_data(show_spinner=False)
def load_dataset():
    """Charge et prépare le dataset immobilier."""
    train = pd.read_csv("train.csv",
                        sep=';', encoding='utf-8', on_bad_lines='warn')
    test = pd.read_csv("test.csv",
                    sep=';', encoding='utf-8', on_bad_lines='warn')
    
    # Fusion des données train et test
    df = pd.concat([train, test], axis=0, ignore_index=True)
    df = df.drop(columns=['Id'])
    
    # Conversion des colonnes texte en string
    for col in df.columns:
        if "object" in str(df[col].dtype) or "ObjectDType" in str(df[col].dtype):
            df[col] = df[col].astype(str)
    
    return df

# ------------------------------
# 🎨 Configuration de la page
# ------------------------------
st.set_page_config(
    page_title="Exploration des Données | RealEstate Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# 🎨 CSS personnalisé pour design professionnel
# ------------------------------
st.markdown("""
<style>
    /* Design du header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 30px 30px;
        opacity: 0.3;
        z-index: 0;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Cartes de contenu */
    .content-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .content-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }
    
    .content-card h3 {
        color: #2d3748;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Métriques */
    .metric-card {
        background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Selectbox et autres inputs */
    .stSelectbox, .stMultiselect, .stSlider {
        background: white;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Titres des sections */
    .section-title {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Badges pour les statistiques */
    .stat-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4fd1c7 0%, #319795 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    /* Animation pour le chargement */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 🎯 Fonction principale
# ------------------------------
def main():
    # Header principal avec design dynamique
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
            <h1 style="margin-bottom:10px;">📊 Exploration des Données</h1>
            <h4 style="font-weight:normal;">
                Analyse approfondie du dataset immobilier - Visualisez, comprenez et exploitez les caractéristiques des maisons
            </h4>
        </div>
    """, unsafe_allow_html=True)

    
    # Chargement des données avec spinner personnalisé
    with st.spinner("🔄 Chargement et préparation des données en cours..."):
        df = load_dataset()
    
    # ------------------------------
    # 🎯 Section 1: Aperçu du Dataset
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>👀</span> Aperçu Global du Dataset</h3>", unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">📈 Nombre de Maisons</div>
            <div style="font-size: 2rem; font-weight: 700; color: #2d3748;">{:,}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">🔢 Variables Total</div>
            <div style="font-size: 2rem; font-weight: 700; color: #2d3748;">{}</div>
        </div>
        """.format(len(df.columns)), unsafe_allow_html=True)
    
    with col3:
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">🔢 Variables Numériques</div>
            <div style="font-size: 2rem; font-weight: 700; color: #2d3748;">{}</div>
        </div>
        """.format(numeric_cols), unsafe_allow_html=True)
    
    with col4:
        cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">🏷️ Variables Catégorielles</div>
            <div style="font-size: 2rem; font-weight: 700; color: #2d3748;">{}</div>
        </div>
        """.format(cat_cols), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Métriques de prix
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = df['SalePrice'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">💰 Prix Moyen</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #2d3748;">${avg_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        median_price = df['SalePrice'].median()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">📊 Prix Médian</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #2d3748;">${median_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        min_price = df['SalePrice'].min()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">📉 Prix Minimum</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #2d3748;">${min_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_price = df['SalePrice'].max()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #718096; margin-bottom: 0.5rem;">📈 Prix Maximum</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #2d3748;">${max_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ------------------------------
    # 📋 Section 2: Tableau interactif des données
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>📋</span> Exploration Interactive des Données</h3>", unsafe_allow_html=True)
    
    # Filtres interactifs
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        show_rows = st.slider(
            "**Lignes à afficher**",
            min_value=5,
            max_value=100,
            value=20,
            step=5,
            help="Sélectionnez le nombre de lignes à afficher dans le tableau"
        )
    
    with col2:
        # Sélection des colonnes par défaut incluant SalePrice
        default_cols = ['SalePrice'] + df.columns.tolist()[:4]
        default_cols = [col for col in default_cols if col in df.columns][:5]
        
        selected_columns = st.multiselect(
            "**Sélection des Colonnes**",
            options=df.columns.tolist(),
            default=default_cols,
            help="Choisissez les colonnes à afficher (SalePrice est obligatoire)"
        )
        
        # Validation: SalePrice doit être présent
        if "SalePrice" not in selected_columns:
            st.error("⚠️ **Attention:** La variable 'SalePrice' doit être sélectionnée pour l'analyse.")
            selected_columns.insert(0, "SalePrice")
    
    with col3:
        price_min = int(df['SalePrice'].min())
        price_max = int(df['SalePrice'].max())
        price_range = st.slider(
            "**Plage de Prix**",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=10000,
            help="Filtrez les données par fourchette de prix"
        )
    
    # Application des filtres
    filtered_df = df[selected_columns]
    filtered_df = filtered_df[
        (filtered_df['SalePrice'] >= price_range[0]) & 
        (filtered_df['SalePrice'] <= price_range[1])
    ]
    
    # Affichage du dataframe avec style
    st.dataframe(
        filtered_df.head(show_rows),
        use_container_width=True,
        height=400
    )
    
    # Informations sur le filtrage
    st.info(f"✅ **{len(filtered_df)}** maisons affichées sur **{len(df)}** totales | Prix: **${price_range[0]:,}** - **${price_range[1]:,}**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------------------
    # 📊 Section 3: Statistiques descriptives
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>📈</span> Analyse Statistique Avancée</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Statistiques Numériques")
        numeric_df = df.select_dtypes(include=[np.number])
        stats_df = numeric_df.describe().T
        stats_df['cv'] = (stats_df['std'] / stats_df['mean'] * 100).round(2)  # Coefficient de variation
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.subheader("🏷️ Statistiques Catégorielles")
        
        # Sélection des principales variables catégorielles
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()[:5]
        categorical_stats = []
        
        for col in cat_cols:
            stats = {
                'Variable': col,
                'Catégories': df[col].nunique(),
                'Mode': df[col].mode()[0] if not df[col].mode().empty else 'N/A',
                'Fréq. Mode': df[col].value_counts().iloc[0],
                '% Mode': f"{(df[col].value_counts().iloc[0] / len(df) * 100):.1f}%"
            }
            categorical_stats.append(stats)
        
        cat_stats_df = pd.DataFrame(categorical_stats)
        st.dataframe(cat_stats_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------------------
    # 🔧 Section 4: Structure des données
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>🔧</span> Structure et Qualité des Données</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition des Types de Données")
        
        # Analyse des types de données
        dtype_info = pd.DataFrame(df.dtypes.value_counts()).reset_index()
        dtype_info.columns = ['Type', 'Count']
        dtype_info['Pourcentage'] = (dtype_info['Count'] / len(df.columns) * 100).round(1)
        dtype_info = sanitize_df_for_plotly(dtype_info)
        
        fig = px.pie(
            dtype_info, 
            values='Count', 
            names='Type', 
            title="Distribution des Types de Variables",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Analyse des Valeurs Manquantes")
        
        # Calcul des valeurs manquantes
        missing_percent = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
        missing_df = pd.DataFrame({
            'Variable': missing_percent.index,
            'Pourcentage': missing_percent.values.round(2)
        })
        
        # Top 10 des variables avec valeurs manquantes
        missing_top10 = missing_df[missing_df['Pourcentage'] > 0].head(10)
        
        if not missing_top10.empty:
            fig = go.Figure(data=[
                go.Bar(
                    x=missing_top10['Pourcentage'],
                    y=missing_top10['Variable'],
                    orientation='h',
                    marker=dict(
                        color=missing_top10['Pourcentage'],
                        colorscale='RdYlGn_r',
                        showscale=True
                    ),
                    text=[f"{v}%" for v in missing_top10['Pourcentage']],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                title='Top 10 des Variables avec Valeurs Manquantes',
                xaxis_title='Pourcentage de valeurs manquantes',
                yaxis_title='Variables',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis=dict(autorange="reversed")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Aucune valeur manquante détectée dans le dataset !")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------------------
    # 📈 Section 5: Distribution des variables
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>📈</span> Visualisation des Distributions</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔢 Variables Numériques")
        
        # Filtrage des variables numériques (exclure SalePrice et binaires)
        numeric_features = [col for col in df.select_dtypes(include=[np.number]).columns 
                        if col != 'SalePrice']
        
        # Détection des variables binaires (0/1)
        binary_features = []
        for feature in numeric_features:
            unique_vals = df[feature].dropna().unique()
            if len(unique_vals) == 2 and set(unique_vals) == {0, 1}:
                binary_features.append(feature)
        
        # Variables numériques continues
        continuous_features = [f for f in numeric_features if f not in binary_features]
        
        selected_numeric = st.selectbox(
            "Choisissez une variable numérique continue :",
            continuous_features[:15],  # Limiter pour lisibilité
            key="numeric_select"
        )
        
        if selected_numeric:
            df_clean = sanitize_df_for_plotly(df)
            fig = px.histogram(
                df_clean, 
                x=selected_numeric,
                nbins=50,
                title=f"Distribution de {selected_numeric}",
                color_discrete_sequence=['#667eea'],
                opacity=0.8
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title=selected_numeric,
                yaxis_title="Fréquence"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏷️ Variables Catégorielles")
        
        # Variables catégorielles
        categorical_features = df.select_dtypes(include=['object']).columns.tolist()
        
        selected_categorical = st.selectbox(
            "Choisissez une variable catégorielle :",
            categorical_features[:15],  # Limiter pour lisibilité
            key="cat_select"
        )
        
        if selected_categorical:
            df_clean = sanitize_df_for_plotly(df)
            
            # Top 20 catégories pour lisibilité
            value_counts = df_clean[selected_categorical].value_counts().head(20)
            
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Distribution de {selected_categorical} (Top 20)",
                color=value_counts.values,
                color_continuous_scale='viridis',
                labels={'x': selected_categorical, 'y': 'Nombre'}
            )
            
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_tickangle=-45,
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------------------
    # 💾 Section 6: Export des données
    # ------------------------------
    st.markdown("<div class='content-card fade-in'>", unsafe_allow_html=True)
    st.markdown("<h3><span style='color:#667eea'>💾</span> Export et Partage des Données</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Télécharger CSV Complet", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Cliquez pour télécharger",
                data=csv,
                file_name="dataset_immobilier_complet.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("📊 Télécharger Données Filtrées", use_container_width=True):
            csv_filtered = filtered_df.to_csv(index=False)
            st.download_button(
                label="Cliquez pour télécharger",
                data=csv_filtered,
                file_name="dataset_immobilier_filtre.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if st.button("📈 Télécharger Statistiques", use_container_width=True):
            # Création d'un fichier Excel avec plusieurs feuilles
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Données Brutes', index=False)
                filtered_df.to_excel(writer, sheet_name='Données Filtrees', index=False)
                stats_df.to_excel(writer, sheet_name='Statistiques')
            
            excel_buffer.seek(0)
            st.download_button(
                label="Cliquez pour télécharger",
                data=excel_buffer,
                file_name="rapport_analyse_immobiliere.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ------------------------------
    # 📝 Footer avec informations
    # ------------------------------
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>📊 Qualité des Données</h4>
            <p>Dataset: {:,} observations<br>{:,} variables</p>
        </div>
        """.format(len(df), len(df.columns)), unsafe_allow_html=True)
    
    with col2:
        missing_total = df.isnull().sum().sum()
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>⚠️ Données Manquantes</h4>
            <p>Total: {:,} cellules<br>{:.2f}% du dataset</p>
        </div>
        """.format(missing_total, (missing_total / (len(df) * len(df.columns)) * 100)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>🔄 Dernière Mise à Jour</h4>
            <p>{}<br>Version: 2.0</p>
        </div>
        """.format(pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

# ------------------------------
# 🚀 Point d'entrée de l'application
# ------------------------------
if __name__ == "__main__":
    main()