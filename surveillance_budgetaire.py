import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import date, datetime, timedelta
import warnings
import base64
import bcrypt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ONCF - Surveillance Budgétaire",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded"
)

#excel_file = pd.ExcelFile("C:/Users/pc/Desktop/Projet/BD_ONCF.xlsx")
excel_file = pd.ExcelFile("BD_ONCF.xlsx")

st.markdown("""
<style>
    :root {
        --oncf-red: #E31E24;
        --oncf-dark-red: #B71C1C;
        --oncf-light-red: #FFEBEE;
        --oncf-gold: #FFB300;
        --oncf-dark-gold: #FF8F00;
        --oncf-green: #2E7D32;
        --oncf-blue: #1565C0;
        --oncf-gray: #424242;
        --oncf-light-gray: #F5F5F5;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F5F5F5 0%, #FAFAFA 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--oncf-red) 0%, var(--oncf-dark-red) 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(227, 30, 36, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--oncf-red);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border: 1px solid var(--oncf-red);
        color: var(--oncf-dark-red);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--oncf-red);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        border: 1px solid var(--oncf-gold);
        color: #E65100;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--oncf-gold);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        border: 1px solid var(--oncf-green);
        color: var(--oncf-green);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--oncf-green);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--oncf-light-gray) 0%, white 100%);
    }
    
    .oncf-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .login-container {
        max-width: 400px;
        margin: 5rem auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border-top: 4px solid var(--oncf-red);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-header h2 {
        color: var(--oncf-red);
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .login-header p {
        color: var(--oncf-gray);
        font-size: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--oncf-red) 0%, var(--oncf-dark-red) 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--oncf-dark-red) 0%, var(--oncf-red) 100%);
        box-shadow: 0 5px 15px rgba(227, 30, 36, 0.4);
        transform: translateY(-2px);
    }
    
    .stSelectbox > div > div {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--oncf-red);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
        border-radius: 8px 8px 0 0;
        padding: 1rem 1.5rem;
        color: var(--oncf-gray);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--oncf-red) 0%, var(--oncf-dark-red) 100%);
        color: white;
        border-color: var(--oncf-red);
    }
    
    .footer {
        background: linear-gradient(135deg, var(--oncf-gray) 0%, #616161 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .risk-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .risk-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .risk-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .recommendation {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #2196f3;
    }

</style>
""", unsafe_allow_html=True)

# Fonctions de chargement des données
#@st.cache_data

def load_sample_data():
    services_data = pd.read_excel("BD_ONCF.xlsx", sheet_name="services")
    projets_data = pd.read_excel("BD_ONCF.xlsx", sheet_name="projets")
    engagements_data = pd.read_excel("BD_ONCF.xlsx", sheet_name="engagements")
    depenses_data = pd.read_excel("BD_ONCF.xlsx", sheet_name="dépenses")
    alertes_data = pd.read_excel("BD_ONCF.xlsx", sheet_name="alertes")
    users_data =  pd.read_excel("BD_ONCF.xlsx", sheet_name="utilisateurs")
    return (
        pd.DataFrame(services_data),
        pd.DataFrame(projets_data),
        pd.DataFrame(engagements_data),
        pd.DataFrame(depenses_data),
        pd.DataFrame(alertes_data),
        pd.DataFrame(users_data)
    )

# Chargement des données
df_services, df_projets, df_engagements, df_depenses, df_alertes, df_users = load_sample_data()

# 🔐 Vérification mot de passe
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"
    
img_base64 = get_image_base64("Logo-oncf.png")

background_image = get_base64_image("oncf1.jpg") 

# Interface de connexion
def show_login():

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{background_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}


        .login-box  {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 3rem;
            border-radius: 16px;
            max-width: 400px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            color: white;
            border: none !important; 
        }}

        input {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: black !important;
            font-family: 'Trebuchet MS', sans-serif;
        }}

        input::placeholder {{
            color: #ccc !important;
            font-family: 'Trebuchet MS', sans-serif;
        }}

        label, .stTextInput label {{
            color: white !important;
        }}

        button[kind="primary"] {{
            background-color: #942813 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 6px;
        }}

        .stTitle {{
            color: #bf1e2e;
            text-align: center;
        }}

        div[data-testid="stForm"] {{
            border: none !important;
        }}

        </style>
    """, unsafe_allow_html=True)
    #st.title("🔐 Connexion à la plateforme")
    #st.markdown("""<h1 style="color:white; font-family: 'Trebuchet MS', sans-serif;">🔐 Connexion à la plateforme</h1>""", unsafe_allow_html=True)

    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""<h1 style="color:white; font-family: 'Trebuchet MS', sans-serif;">🔐 Connexion à la plateforme</h1>""", unsafe_allow_html=True)
            #st.markdown("### 🔐 Connexion à la plateforme")
            username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
            password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                login_button = st.form_submit_button("Se connecter")
    
    if login_button:
        # Vérification simple (dans un vrai système, utilisez une base de données sécurisée)
            user_row = df_users[df_users["username"] == username]
            if not user_row.empty:
                stored_hash = user_row.iloc[0]["password"]
                if check_password(password, stored_hash):
                    #st.success(f"Bienvenue {user_row.iloc[0]['name']} !")
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.session_state.role = user_row.iloc[0]["role"]
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect.")
            else:
                st.error("❌ Utilisateur non trouvé.")

def reset_form():
    st.session_state["nom_projet"] = ""
    st.session_state["service"] = df_services['nom_service'][0] if not df_services.empty else ""
    st.session_state["budget"] = 100000
    st.session_state["date_debut"] = datetime.date.today()
    st.session_state["date_fin"] = datetime.date.today()

# Logo ONCF dans la sidebar
def show_logo_sidebar():
    st.sidebar.markdown(f"""
    <div class="oncf-logo">
        <div style="text-align: center;">
           <div style="text-align: center;">
                <img src="data:image/png;base64,{img_base64}" style="width:80px; margin-bottom: 0.5rem;">
            </div>
            <p style="color: var(--oncf-gray); margin: 0; font-size: 0.8rem;">Office National des<br>Chemins de Fer</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def calculer_indicateurs(df_projets, df_engagements, df_depenses):
    """Calcule les indicateurs clés de performance"""
    
    # Fusion des données
    df_proj_eng = df_projets.merge(df_engagements.groupby('id_projet')['montant'].sum().reset_index().rename(columns={'montant': 'total_engagements'}), 
                                   on='id_projet', how='left')
    df_complete = df_proj_eng.merge(df_depenses.groupby('id_projet')['montant'].sum().reset_index().rename(columns={'montant': 'total_depenses'}), 
                                   on='id_projet', how='left')
    
    # Remplacer les NaN par 0
    df_complete['total_engagements'] = df_complete['total_engagements'].fillna(0)
    df_complete['total_depenses'] = df_complete['total_depenses'].fillna(0)
    
    # Calculer les taux
    df_complete['taux_engagement'] = (df_complete['total_engagements'] / df_complete['budget_initial'] * 100).round(2)
    df_complete['taux_execution'] = (df_complete['total_depenses'] / df_complete['budget_initial'] * 100).round(2)
    df_complete['reste_budget'] = df_complete['budget_initial'] - df_complete['total_depenses']
    
    return df_complete

def generer_id_projet(df,date_debut):
    if date_debut is None:
        return "PJ-0000"  # ou lève une exception ou retourne une valeur temporaire
    annee_debut = date_debut.year
    prefix = f"PJ-{annee_debut}-"

    # Filtrer les IDs qui commencent par le prefix de cette année
    ids_annee = df['id_projet'].dropna().apply(str).loc[lambda s: s.str.startswith(prefix)]

    if ids_annee.empty:
        nouveau_num = 1
    else:
        # Extraire le numéro final des IDs et prendre le max
        numeros = ids_annee.str.extract(r'PJ-\d{4}-(\d{3})')[0].astype(int)
        nouveau_num = numeros.max() + 1

    # Formater en 3 chiffres avec des zéros devant
    return f"{prefix}{nouveau_num:03d}"

def generer_id_engagement(df,date_engagement):
    if date_engagement is None:
        return "BC-0000"  # ou lève une exception ou retourne une valeur temporaire
    annee_engagement = date_engagement.year
    prefix = f"BC-{annee_engagement}-"

    # S'assurer que la colonne 'id_engagement' existe
    if 'id_engagement' not in df.columns:
        return f"{prefix}100"  # Premier engagement de l'année

    # Filtrer les IDs qui commencent par le prefix de cette année
    ids_annee = df['id_engagement'].dropna().apply(str).loc[lambda s: s.str.startswith(prefix)]

    if ids_annee.empty:
        nouveau_num = 100
    else:
        # Extraire le numéro final des IDs et prendre le max
        numeros = ids_annee.str.extract(rf'{prefix}(\d{{3}})')[0].dropna().astype(int)
        if numeros.empty:
            nouveau_num = 100
        else:
            nouveau_num = numeros.max() + 1

    # Formater en 3 chiffres avec des zéros devant
    return f"{prefix}{nouveau_num:03d}"

def generer_id_depense(df,date_depense):
    if date_depense is None:
        return "FAC-0000-0000"  # ou lève une exception ou retourne une valeur temporaire
    annee_depense = date_depense.year
    prefix = f"FAC-{annee_depense}-"

    # S'assurer que la colonne 'id_depense' existe
    if 'id_depense' not in df.columns:
        return f"{prefix}1"  # Premier depense de l'année

    # Filtrer les IDs qui commencent par le prefix de cette année
    ids_annee = df['id_depense'].dropna().apply(str).loc[lambda s: s.str.startswith(prefix)]

    if ids_annee.empty:
        nouveau_num = 1
    else:
        # Extraire le numéro final des IDs et prendre le max
        numeros = ids_annee.str.extract(r'FAC-\d{4}-(\d{3})')[0].astype(int)
        if numeros.empty:
            nouveau_num = 1
        else:
            nouveau_num = numeros.max() + 1

    # Formater en 3 chiffres avec des zéros devant
    return f"{prefix}{nouveau_num:03d}"

def sauvegarder_alertes(nouvelles_alertes, excel_file):
    """
    Sauvegarde les nouvelles alertes dans le fichier Excel
    """
    try:
        # Charger toutes les feuilles
        with pd.ExcelFile(excel_file, engine='openpyxl') as xls:
            all_sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
        
        # Ajouter les nouvelles alertes
        df_nouvelles_alertes = pd.DataFrame(nouvelles_alertes)
        
        if "alertes" in all_sheets:
            df_alertes_existantes = all_sheets["alertes"]
            df_alertes_mise_a_jour = pd.concat([df_alertes_existantes, df_nouvelles_alertes], ignore_index=True)
        else:
            df_alertes_mise_a_jour = df_nouvelles_alertes
        
        # Remplacer la feuille alertes
        all_sheets["alertes"] = df_alertes_mise_a_jour
        
        # Réécrire le fichier complet
        with pd.ExcelWriter(excel_file, engine='xlsxwriter', datetime_format='dd/mm/yyyy') as writer:
            for sheet_name, df_sheet in all_sheets.items():
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
                
        print(f"✅ {len(nouvelles_alertes)} nouvelle(s) alerte(s) générée(s) et sauvegardée(s)")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde des alertes: {e}")

def generer_alertes_automatiques(df_projets, df_engagements, df_depenses, excel_file):
    
    nouvelles_alertes = []
    # Calculer les totaux par projet
    engagements_par_projet = df_engagements.groupby('id_projet')['montant'].sum().reset_index()
    engagements_par_projet.rename(columns={'montant': 'total_engagements'}, inplace=True)
    
    depenses_par_projet = df_depenses.groupby('id_projet')['montant'].sum().reset_index()
    depenses_par_projet.rename(columns={'montant': 'total_depenses'}, inplace=True)
    
    # Fusionner avec les projets
    df_analyse = df_projets.merge(engagements_par_projet, on='id_projet', how='left')
    df_analyse = df_analyse.merge(depenses_par_projet, on='id_projet', how='left')
    
    # Remplacer NaN par 0
    df_analyse['total_engagements'] = df_analyse['total_engagements'].fillna(0)
    df_analyse['total_depenses'] = df_analyse['total_depenses'].fillna(0)
    
    # Charger les alertes existantes pour éviter les doublons
    try:
        alertes_existantes = pd.read_excel(excel_file, sheet_name="alertes")
    except:
        alertes_existantes = pd.DataFrame()
    
    for _, projet in df_analyse.iterrows():
        id_projet = projet['id_projet']
        nom_projet = projet['nom_projet']
        budget_initial = projet['budget_initial']
        total_engagements = projet['total_engagements']
        total_depenses = projet['total_depenses']
        
        # ALERTE 2: Total dépenses > Budget initial
        if total_depenses > budget_initial:
            alerte_id = f"DEP_SUP_BUD_{id_projet}"
            
            # Vérifier si cette alerte existe déjà
            if alertes_existantes.empty or not any(
                (alertes_existantes['id_projet'] == id_projet) & 
                (alertes_existantes['type'] == 'Dépassement Budget')
            ):
                taux_depassement = (total_depenses / budget_initial) * 100
                nouvelle_alerte = {
                    'id_alerte': alerte_id,
                    'id_projet': id_projet,
                    'type': 'Dépassement Budget',
                    'seuil': 100,
                    'valeur_actuelle': round(taux_depassement, 2),
                    'date_detection': datetime.now().strftime('%Y-%m-%d'),
                    'message': f"CRITIQUE: Dépassement budgétaire de {taux_depassement-100:.1f}% pour le projet '{nom_projet}' (Budget: {budget_initial:,.0f} DH, Dépenses: {total_depenses:,.0f} DH)"
                }
                nouvelles_alertes.append(nouvelle_alerte)
        # ALERTE 1: Dépenses > Engagements
        elif total_depenses > total_engagements and total_engagements > 0:
            alerte_id = f"DEP_SUP_ENG_{id_projet}"
            
            # Vérifier si cette alerte existe déjà
            if alertes_existantes.empty or not any(
                (alertes_existantes['id_projet'] == id_projet) & 
                (alertes_existantes['type'] == 'Dépenses > Engagements')
            ):
                nouvelle_alerte = {
                    'id_alerte': alerte_id,
                    'id_projet': id_projet,
                    'type': 'Dépenses > Engagements',
                    'seuil': 100,
                    'valeur_actuelle': round((total_depenses / total_engagements) * 100, 2) if total_engagements > 0 else 0,
                    'date_detection': datetime.now().strftime('%Y-%m-%d'),
                    'message': f"ATTENTION: Les dépenses ({total_depenses:,.0f} DH) dépassent les engagements ({total_engagements:,.0f} DH) pour le projet '{nom_projet}'"
                }
                nouvelles_alertes.append(nouvelle_alerte)
        # ALERTE 3: Risque de dépassement (80% du budget atteint)
        elif total_depenses > (budget_initial * 0.8):
            alerte_id = f"RISQUE_DEP_{id_projet}"
            if alertes_existantes.empty or not any(
                (alertes_existantes['id_projet'] == id_projet) & 
                (alertes_existantes['type'] == 'Risque Dépassement')
            ):
                taux_utilisation = (total_depenses / budget_initial) * 100
                nouvelle_alerte = {
                    'id_alerte': alerte_id,
                    'id_projet': id_projet,
                    'type': 'Risque Dépassement',
                    'seuil': 80,
                    'valeur_actuelle': round(taux_utilisation, 2),
                    'date_detection': datetime.now().strftime('%Y-%m-%d'),
                    'message': f"ATTENTION: Risque de dépassement pour le projet '{nom_projet}' - {taux_utilisation:.1f}% du budget utilisé"
                }
                nouvelles_alertes.append(nouvelle_alerte)
    # Sauvegarder les nouvelles alertes dans Excel
    if nouvelles_alertes:
        sauvegarder_alertes(nouvelles_alertes, excel_file)
    return nouvelles_alertes

def afficher_alertes_streamlit(nouvelles_alertes):
    """
    Affiche les nouvelles alertes dans Streamlit avec des couleurs appropriées
    """
    import streamlit as st
    
    if nouvelles_alertes:
        st.warning(f"🚨 {len(nouvelles_alertes)} nouvelle(s) alerte(s) générée(s)!")
        
        for alerte in nouvelles_alertes:
            if alerte['type'] == 'Dépassement Budget':
                st.markdown(f"""
                <div class="alert-danger">
                    <strong>🔥 CRITIQUE - {alerte['type']}</strong><br>
                    Projet: {alerte['id_projet']}<br>
                    Taux: {alerte['valeur_actuelle']:.1f}%<br>
                    {alerte['message']}
                </div>
                """, unsafe_allow_html=True)
            
            elif alerte['type'] == 'Dépenses > Engagements':
                st.markdown(f"""
                <div class="alert-danger">
                    <strong>⚠️ ALERTE - {alerte['type']}</strong><br>
                    Projet: {alerte['id_projet']}<br>
                    Ratio: {alerte['valeur_actuelle']:.1f}%<br>
                    {alerte['message']}
                </div>
                """, unsafe_allow_html=True)
            
            else:  # Risque Dépassement
                st.markdown(f"""
                <div class="alert-warning">
                    <strong>⚡ ATTENTION - {alerte['type']}</strong><br>
                    Projet: {alerte['id_projet']}<br>
                    Utilisation: {alerte['valeur_actuelle']:.1f}%<br>
                    {alerte['message']}
                </div>
                """, unsafe_allow_html=True)

def calculer_tendance_depenses(df_depenses, id_projet):
    """
    Calcule la tendance des dépenses pour un projet donné
    """
    depenses_projet = df_depenses[df_depenses['id_projet'] == id_projet].copy()
    
    if len(depenses_projet) < 2:
        return 0, 0, 0  # pas assez de données
    
    # Trier par date
    depenses_projet = depenses_projet.sort_values('date_depense')
    depenses_projet['jours_depuis_debut'] = (depenses_projet['date_depense'] - depenses_projet['date_depense'].min()).dt.days
    depenses_projet['depenses_cumulees'] = depenses_projet['montant'].cumsum()
    
    # Régression linéaire simple
    X = depenses_projet['jours_depuis_debut'].values.reshape(-1, 1)
    y = depenses_projet['depenses_cumulees'].values
    
    if len(X) > 1:
        model = LinearRegression()
        model.fit(X, y)
        tendance_quotidienne = model.coef_[0]
        r2_score = model.score(X, y)
    else:
        tendance_quotidienne = 0
        r2_score = 0
    
    return tendance_quotidienne, r2_score, len(depenses_projet)

def predire_budget_final(df_projets, df_depenses, id_projet):
    """
    Prédit le budget final basé sur les tendances actuelles
    """
    projet = df_projets[df_projets['id_projet'] == id_projet].iloc[0]
    depenses_projet = df_depenses[df_depenses['id_projet'] == id_projet].copy()
    
    if depenses_projet.empty:
        return {
            'budget_predit': projet['budget_initial'],
            'probabilite_depassement': 0,
            'depassement_predit': 0,
            'confiance': 0,
            'methode': 'Aucune donnée'
        }
    
    # Calculer la tendance
    tendance, r2, nb_points = calculer_tendance_depenses(df_depenses, id_projet)
    
    # Dates du projet
    date_debut = pd.to_datetime(projet['date_debut'])
    date_fin = pd.to_datetime(projet['date_fin_prev'])
    jours_total = (date_fin - date_debut).days
    
    # Jours écoulés depuis le début
    jours_ecoules = (datetime.now() - date_debut).days
    jours_restants = max(0, jours_total - jours_ecoules)
    
    # Dépenses actuelles
    depenses_actuelles = depenses_projet['montant'].sum()
    
    # Méthode 1: Tendance linéaire
    if tendance > 0 and jours_restants > 0:
        depenses_predites_fin = depenses_actuelles + (tendance * jours_restants)
        methode = "Tendance linéaire"
    else:
        # Méthode 2: Ratio temporel
        if jours_ecoules > 0:
            ratio_temps = jours_ecoules / jours_total
            ratio_depenses = depenses_actuelles / projet['budget_initial']
            
            if ratio_depenses > ratio_temps:  # Dépenses plus rapides que prévu
                facteur_acceleration = ratio_depenses / ratio_temps
                depenses_predites_fin = depenses_actuelles / ratio_temps * facteur_acceleration
            else:
                depenses_predites_fin = depenses_actuelles / ratio_temps
            
            methode = "Projection temporelle"
        else:
            depenses_predites_fin = projet['budget_initial']
            methode = "Estimation par défaut"
    
    # Calcul des métriques de prédiction
    depassement_predit = max(0, depenses_predites_fin - projet['budget_initial'])
    probabilite_depassement = min(100, max(0, (depenses_predites_fin / projet['budget_initial'] - 1) * 100))
    
    # Niveau de confiance basé sur la qualité des données
    if nb_points >= 5:
        confiance = min(90, r2 * 100) if r2 > 0 else 60
    elif nb_points >= 3:
        confiance = 50
    else:
        confiance = 30
    
    return {
        'budget_predit': depenses_predites_fin,
        'probabilite_depassement': probabilite_depassement,
        'depassement_predit': depassement_predit,
        'confiance': confiance,
        'methode': methode,
        'tendance_quotidienne': tendance,
        'r2_score': r2,
        'jours_restants': jours_restants
    }

def analyser_facteurs_risque(df_projets, df_engagements, df_depenses, id_projet):
    """
    Analyse les facteurs de risque pour un projet
    """
    projet = df_projets[df_projets['id_projet'] == id_projet].iloc[0]
    engagements_projet = df_engagements[df_engagements['id_projet'] == id_projet]
    depenses_projet = df_depenses[df_depenses['id_projet'] == id_projet]
    
    facteurs_risque = []
    score_risque = 0
    
    # Facteur 1: Ratio dépenses/engagements
    if not engagements_projet.empty and not depenses_projet.empty:
        total_engagements = engagements_projet['montant'].sum()
        total_depenses = depenses_projet['montant'].sum()
        
        if total_depenses > total_engagements:
            facteurs_risque.append("🔴 Dépenses supérieures aux engagements")
            score_risque += 30
        elif total_depenses > total_engagements * 0.8:
            facteurs_risque.append("🟡 Dépenses proches des engagements (>80%)")
            score_risque += 15
    
    # Facteur 2: Vitesse de consommation du budget
    date_debut = pd.to_datetime(projet['date_debut'])
    date_fin = pd.to_datetime(projet['date_fin_prev'])
    jours_total = (date_fin - date_debut).days
    jours_ecoules = max(1, (datetime.now() - date_debut).days)
    
    if jours_ecoules > 0 and not depenses_projet.empty:
        ratio_temps = jours_ecoules / jours_total
        ratio_budget = depenses_projet['montant'].sum() / projet['budget_initial']
        
        if ratio_budget > ratio_temps * 1.5:
            facteurs_risque.append("🔴 Consommation budgétaire très rapide")
            score_risque += 25
        elif ratio_budget > ratio_temps * 1.2:
            facteurs_risque.append("🟡 Consommation budgétaire rapide")
            score_risque += 15
    
    # Facteur 3: Fréquence des dépenses
    if len(depenses_projet) > 0:
        depenses_recentes = depenses_projet[
            depenses_projet['date_depense'] >= (datetime.now() - timedelta(days=30))
        ]
        
        if len(depenses_recentes) > len(depenses_projet) * 0.5:
            facteurs_risque.append("🟡 Forte concentration de dépenses récentes")
            score_risque += 10
    
    # Facteur 4: Montant des engagements non réalisés
    if not engagements_projet.empty:
        total_engagements = engagements_projet['montant'].sum()
        total_depenses = depenses_projet['montant'].sum() if not depenses_projet.empty else 0
        engagements_restants = total_engagements - total_depenses
        
        if engagements_restants > projet['budget_initial'] * 0.3:
            facteurs_risque.append("🟡 Importants engagements non encore réalisés")
            score_risque += 20
    
    if not facteurs_risque:
        facteurs_risque.append("✅ Aucun facteur de risque majeur détecté")
    
    return facteurs_risque, min(100, score_risque)

def generer_recommandations(prediction, facteurs_risque, score_risque):
    """
    Génère des recommandations basées sur l'analyse prédictive
    """
    recommandations = []
    
    if prediction['probabilite_depassement'] > 80:
        recommandations.append("🚨 **URGENT**: Suspendre immédiatement les nouveaux engagements")
        recommandations.append("📋 Réaliser un audit complet des dépenses prévues")
        recommandations.append("💰 Négocier une augmentation de budget ou revoir le périmètre")
    
    elif prediction['probabilite_depassement'] > 50:
        recommandations.append("⚠️ **ATTENTION**: Réviser le planning des dépenses")
        recommandations.append("🔍 Analyser les postes de dépenses les plus importants")
        recommandations.append("📊 Mettre en place un suivi hebdomadaire renforcé")
    
    elif prediction['probabilite_depassement'] > 20:
        recommandations.append("📈 Surveiller l'évolution des dépenses mensuelles")
        recommandations.append("💡 Identifier les opportunités d'optimisation")
    
    # Recommandations spécifiques aux facteurs de risque
    if score_risque > 50:
        recommandations.append("🔄 Réajuster la planification financière du projet")
        recommandations.append("👥 Renforcer l'équipe de contrôle budgétaire")
    
    if not recommandations:
        recommandations.append("✅ Continuer le suivi standard du projet")
    
    return recommandations

def afficher_onglet_predictions_detaille(df_projets, df_engagements, df_depenses):
    """
    Affiche l'onglet de prédictions détaillées
    """
    st.header("Prédictions de dépassement budgétaire")
    
    # Sélection du projet
    projets_actifs = df_projets[df_projets['statut'] == 'En cours']
    
    if projets_actifs.empty:
        st.warning("Aucun projet actif trouvé pour l'analyse prédictive.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        projet_selectionne = st.selectbox(
            "Sélectionner un projet :",
            projets_actifs['nom_projet'].unique()
        )
    
   
    
    if projet_selectionne:
        # Récupérer les données du projet
        projet_data = projets_actifs[projets_actifs['nom_projet'] == projet_selectionne].iloc[0]
        id_projet = projet_data['id_projet']
        
        # Effectuer la prédiction
        prediction = predire_budget_final(df_projets, df_depenses, id_projet)
        facteurs_risque, score_risque = analyser_facteurs_risque(
            df_projets, df_engagements, df_depenses, id_projet
        )
        recommandations = generer_recommandations(prediction, facteurs_risque, score_risque)
        
        # Affichage des résultats
        st.subheader(f"📊 Analyse prédictive: {projet_selectionne}")
        
        # Métriques principales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💼 Budget initial", 
                f"{projet_data['budget_initial']:,.0f} DH"
            )
        
        with col2:
            st.metric(
                "🔮 Budget prédit", 
                f"{prediction['budget_predit']:,.0f} DH",
                delta=f"{prediction['depassement_predit']:,.0f} DH"
            )
        
        with col3:
            couleur_prob = "🔴" if prediction['probabilite_depassement'] > 70 else "🟡" if prediction['probabilite_depassement'] > 30 else "🟢"
            st.metric(
                "🚨 Risque de dépassement", 
                f"{couleur_prob} {prediction['probabilite_depassement']:.1f}%"
            )
        
        #with col4:
        #    couleur_conf = "🟢" if prediction['confiance'] > 70 else "🟡" if prediction['confiance'] > 50 else "🔴"
         #   st.metric(
          #      "🎯 Niveau de confiance", 
           #     f"{couleur_conf} {prediction['confiance']:.0f}%"
            #)
        
        # Graphique de prédiction
        st.subheader("📈 Projection budgétaire")
        
        # Créer les données pour le graphique
        depenses_projet = df_depenses[df_depenses['id_projet'] == id_projet].copy()
        
        if not depenses_projet.empty:
            depenses_projet = depenses_projet.sort_values('date_depense')
            depenses_projet['depenses_cumulees'] = depenses_projet['montant'].cumsum()
            
            # Créer le graphique
            fig = go.Figure()
            
            # Ligne des dépenses réelles
            fig.add_trace(go.Scatter(
                x=depenses_projet['date_depense'],
                y=depenses_projet['depenses_cumulees'],
                mode='lines+markers',
                name='Dépenses Réelles',
                line=dict(color='#E31E24', width=3)
            ))
            
            # Ligne de budget initial
            fig.add_hline(
                y=projet_data['budget_initial'],
                line_dash="dash",
                line_color="blue",
                annotation_text="Budget initial"
            )
            
            # Ligne de prédiction
            fig.add_hline(
                y=prediction['budget_predit'],
                line_dash="dot",
                line_color="red" if prediction['probabilite_depassement'] > 50 else "green",
                annotation_text=f"Budget prédit ({prediction['methode']})"
            )
            
            fig.update_layout(
                title=f"Évolution et prédiction budgétaire - {projet_selectionne}",
                xaxis_title="Date",
                yaxis_title="Montant cumulé (DH)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des facteurs de risque
        col1, col2 = st.columns(2)
        
def analyser_risques_portfolio(df_projets, df_engagements, df_depenses):
    """
    Analyse les risques au niveau du portfolio de projets
    """
    st.subheader("📊 Analyse des risques du portfolio")
    
    projets_actifs = df_projets[df_projets['statut'] == 'En cours']
    risques_projets = []
    
    for _, projet in projets_actifs.iterrows():
        prediction = predire_budget_final(df_projets, df_depenses, projet['id_projet'])
        _, score_risque = analyser_facteurs_risque(
            df_projets, df_engagements, df_depenses, projet['id_projet']
        )
        
        risques_projets.append({
            'nom_projet': projet['nom_projet'],
            'budget_initial': projet['budget_initial'],
            'probabilite_depassement': prediction['probabilite_depassement'],
            'score_risque': score_risque,
            'depassement_predit': prediction['depassement_predit']
        })
    
    df_risques = pd.DataFrame(risques_projets)
    
    if not df_risques.empty:
        # Matrice des risques
        fig_matrix = px.scatter(
            df_risques,
            x='probabilite_depassement',
            y='score_risque',
            size='budget_initial',
            hover_name='nom_projet',
            title="Matrice des risques - Portfolio de projets",
            labels={
                'probabilite_depassement': 'Probabilité de dépassement (%)',
                'score_risque': 'Score de risque'
            }
        )
        
        # Zones de risque
        fig_matrix.add_shape(
            type="rect", x0=0, y0=0, x1=30, y1=40,
            fillcolor="green", opacity=0.2, line_width=0
        )
        fig_matrix.add_shape(
            type="rect", x0=30, y0=40, x1=70, y1=70,
            fillcolor="orange", opacity=0.2, line_width=0
        )
        fig_matrix.add_shape(
            type="rect", x0=70, y0=70, x1=100, y1=100,
            fillcolor="red", opacity=0.2, line_width=0
        )
        
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Tableau de synthèse
        st.subheader("📋 Synthèse des risques par projet")
        df_risques_display = df_risques.copy()
        df_risques_display['budget_initial'] = df_risques_display['budget_initial'].apply(lambda x: f"{x:,.0f} DH")
        df_risques_display['depassement_predit'] = df_risques_display['depassement_predit'].apply(lambda x: f"{x:,.0f} DH")
        df_risques_display['probabilite_depassement'] = df_risques_display['probabilite_depassement'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_risques_display, use_container_width=True)

# Interface principale
def main():
    # Vérification de la connexion
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login()
        return
    
    # Logo dans la sidebar
    show_logo_sidebar()

    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>Système de Surveillance Budgétaire</h1>
        <p>Tableau de bord interactif pour le suivi des budgets, engagements et dépenses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    df_services, df_projets, df_engagements, df_depenses, df_alertes, df_users = load_sample_data()
    
    # Convertir les dates
    df_projets['date_debut'] = pd.to_datetime(df_projets['date_debut'])
    df_projets['date_fin_prev'] = pd.to_datetime(df_projets['date_fin_prev'])
    df_engagements['date_engagement'] = pd.to_datetime(df_engagements['date_engagement'])
    df_depenses['date_depense'] = pd.to_datetime(df_depenses['date_depense'])
    
    # Générer les alertes automatiquement au chargement de la page
    try:
        nouvelles_alertes = generer_alertes_automatiques(
            df_projets, df_engagements, df_depenses, 
            "BD_ONCF.xlsx"
        )
        
        # Afficher les nouvelles alertes s'il y en a
       # if nouvelles_alertes:
           # afficher_alertes_streamlit(nouvelles_alertes)
            # Recharger les données d'alertes après mise à jour
            #df_alertes = pd.read_excel("C:/Users/pc/Desktop/Projet/données.xlsx", sheet_name="alertes")
            
    except Exception as e:
        st.error(f"Erreur lors de la génération des alertes: {e}")

    # Calculer les indicateurs
    df_indicateurs = calculer_indicateurs(df_projets, df_engagements, df_depenses)
    
    # Sidebar pour les filtres
    st.sidebar.header("🔍 Filtres")
    
    # Filtre par service
    services_list = ['Tous'] + list(df_services['nom_service'].unique())
    service_selectionne = st.sidebar.selectbox('Service', services_list)
    
    # Filtre par statut
    statuts_list = ['Tous'] + list(df_projets['statut'].unique())
    statut_selectionne = st.sidebar.selectbox('Statut', statuts_list)
    
    # Filtre par période
    date_min = df_projets['date_debut'].min()
    date_max = df_projets['date_fin_prev'].max()
    #periode = st.sidebar.date_input('Période', [date_min.date(), date_max.date()])
    
    # Appliquer les filtres
    df_filtered = df_indicateurs.copy()
    
    if service_selectionne != 'Tous':
        service_id = df_services[df_services['nom_service'] == service_selectionne]['id_service'].iloc[0]
        df_filtered = df_filtered[df_filtered['id_service'] == service_id]
    
    if statut_selectionne != 'Tous':
        df_filtered = df_filtered[df_filtered['statut'] == statut_selectionne]
    
    if st.sidebar.button(" Déconnexion", key="logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Navigation par onglets
    tab1, tab2, tab3, tab4, tab6, tab5 = st.tabs(["📊 Tableau de bord", "💰 Analyse budgétaire", "📈 Suivi projets", "⚠️ Alertes", "🔮 Prédictions","📋 Saisie données"])
    
    with tab1:
        st.header("Tableau de bord")
        
        # KPIs principaux
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_budget = df_filtered['budget_initial'].sum()
            st.metric("💰 Budget total", f"{total_budget:,.0f} DH")
        
        with col2:
            total_engagements = df_filtered['total_engagements'].sum()
            taux_eng_global = (total_engagements / total_budget * 100) if total_budget > 0 else 0
            st.metric("📝 Total engagements", f"{total_engagements:,.0f} DH", delta=f"{taux_eng_global:.1f}%")
        
        with col3:
            total_depenses = df_filtered['total_depenses'].sum()
            taux_dep_global = (total_depenses / total_budget * 100) if total_budget > 0 else 0
            st.metric("💸 Total dépenses", f"{total_depenses:,.0f} DH", delta=f"{taux_dep_global:.1f}%")        
        with col4:
            taux_execution_global = (total_depenses / total_budget * 100) if total_budget > 0 else 0
            st.metric("📈 Taux d'exécution", f"{taux_execution_global:.1f}%")
        
        st.markdown("---")
        
        # Graphiques de synthèse
        col1, col2 = st.columns(2)
        
        with col1:
            # Répartition par service
            df_service_budget = df_filtered.groupby('id_service').agg({
                'budget_initial': 'sum',
                'total_depenses': 'sum'
            }).reset_index()
            
            df_service_budget = df_service_budget.merge(df_services[['id_service', 'nom_service']], on='id_service')
            
            # Couleurs personnalisées ONCF
            colors_oncf = ['#E31E24', '#FFB300', '#2E7D32', '#1565C0', '#FF5722', '#9C27B0', '#607D8B', '#795548', '#FF9800', '#4CAF50']

            fig_service = px.pie(df_service_budget, values='budget_initial', names='nom_service',
                               title="Répartition du budget par service",
                               color_discrete_sequence=colors_oncf)
            fig_service.update_traces(textposition='inside', textinfo='percent+label')
            fig_service.update_layout(
                title_font_size=16,
                title_font_color='#E31E24',
                font_size=12
            )
            st.plotly_chart(fig_service, use_container_width=True)
        
        with col2:
            # Évolution des dépenses
            df_depenses_month = df_depenses.copy()
            df_depenses_month['mois'] = df_depenses_month['date_depense'].dt.to_period('M')
            df_monthly = df_depenses_month.groupby('mois')['montant'].sum().reset_index()
            df_monthly['mois'] = df_monthly['mois'].astype(str)
            
            fig_evolution = px.line(df_monthly, x='mois', y='montant',
                                  title="Évolution des dépenses mensuelles",
                                  markers=True)
            fig_evolution.update_traces(line_color='#E31E24', marker_color='#E31E24')
            fig_evolution.update_layout(
                xaxis_title="Mois", 
                yaxis_title="Montant (DH)",
                title_font_size=16,
                title_font_color='#E31E24',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_evolution, use_container_width=True)
    
    with tab2:
        st.header("Analyse budgétaire détaillée")
        
        # Tableau de bord budgétaire

        df_filtered = df_filtered.copy()

        # Calculer les colonnes si elles ne sont pas déjà calculées
        df_display = df_filtered[['nom_projet', 'id_service', 'budget_initial', 'total_engagements', 
                                 'total_depenses', 'taux_engagement', 'taux_execution', 'reste_budget', 'statut']].copy()

        # Ajouter des couleurs selon les seuils
        def color_budget(val):
            if val > 100:
                return 'background-color: #ffebee'
            #elif val > 70:
                #return 'background-color: #fff3e0'
            return ''
        
        st.subheader("📋 Tableau de suivi budgétaire")
        styled_df = df_display.style.applymap(color_budget, subset=['taux_execution'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Graphique des dépassements
        st.subheader("📊 Analyse des risques de dépassement")
        
        fig_risk = go.Figure()
        
        # Ajouter les barres pour budget initial
        fig_risk.add_trace(go.Bar(
            name='Budget Initial',
            x=df_filtered['nom_projet'],
            y=df_filtered['budget_initial'],
            marker_color='lightblue'
        ))
        
        # Ajouter les barres pour engagements
        fig_risk.add_trace(go.Bar(
            name='Engagements',
            x=df_filtered['nom_projet'],
            y=df_filtered['total_engagements'],
            marker_color='orange'
        ))
        
        # Ajouter les barres pour dépenses
        fig_risk.add_trace(go.Bar(
            name='Dépenses',
            x=df_filtered['nom_projet'],
            y=df_filtered['total_depenses'],
            marker_color='red'
        ))
        
        fig_risk.update_layout(
            title="Comparaison Budget vs Engagements vs Dépenses",
            xaxis_title="Projets",
            yaxis_title="Montant (DH)",
            barmode='group',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with tab3:
        st.header("Suivi des projets")
        
        # Métriques par projet
        projet_selectionne = st.selectbox('Sélectionner un projet', df_filtered['nom_projet'].unique())
        
        if projet_selectionne:
            projet_data = df_filtered[df_filtered['nom_projet'] == projet_selectionne].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💼 Budget initial", f"{projet_data['budget_initial']:,.0f} DH")
                st.metric("📑 Engagements", f"{projet_data['total_engagements']:,.0f} DH")
            
            with col2:
                st.metric("💸 Dépenses", f"{projet_data['total_depenses']:,.0f} DH")
                st.metric("🧮 Reste à dépenser", f"{projet_data['reste_budget']:,.0f} DH")
            
            with col3:
                st.metric("📌 Taux d'engagement", f"{projet_data['taux_engagement']:.1f}%")
                st.metric("📈 Taux d'exécution", f"{projet_data['taux_execution']:.1f}%")
            
            # Graphique en gauge pour le projet sélectionné
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = projet_data['taux_execution'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Taux d'exécution budgétaire"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Timeline du projet
            st.subheader("📍 Timeline du projet")
            
            # Engagements pour ce projet
            eng_projet = df_engagements[df_engagements['id_projet'] == projet_data['id_projet']]
            dep_projet = df_depenses[df_depenses['id_projet'] == projet_data['id_projet']]
            
            if not eng_projet.empty or not dep_projet.empty:
                fig_timeline = go.Figure()
                
                # Ajouter les engagements
                if not eng_projet.empty:
                    fig_timeline.add_trace(go.Scatter(
                        x=eng_projet['date_engagement'],
                        y=eng_projet['montant'].cumsum(),
                        mode='lines+markers',
                        name='Engagements cumulés',
                        line=dict(color='orange')
                    ))
                
                # Ajouter les dépenses
                if not dep_projet.empty:
                    fig_timeline.add_trace(go.Scatter(
                        x=dep_projet['date_depense'],
                        y=dep_projet['montant'].cumsum(),
                        mode='lines+markers',
                        name='Dépenses cumulées',
                        line=dict(color='red')
                    ))
                
                fig_timeline.update_layout(
                    title=f"Évolution financière - {projet_selectionne}",
                    xaxis_title="Date",
                    yaxis_title="Montant cumulé (DH)"
                )
                
                st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab4:
        st.header("Statistiques des alertes")
        
        # Recharger les alertes les plus récentes
        df_alertes_fresh = pd.read_excel("BD_ONCF.xlsx", sheet_name="alertes")
        
        # Filtrer les alertes actives
        #alertes_actives = df_alertes_fresh[df_alertes_fresh['statut'] == 'Active']
        alertes_actives = df_alertes_fresh.copy()

        # Statistiques des alertes
        #.subheader("📊 Statistiques des Alertes")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nb_alertes_critiques = len(alertes_actives[alertes_actives['type'] == 'Dépassement Budget'])
            st.metric("🔥 Alertes critiques", nb_alertes_critiques)
        
        with col2:
            nb_alertes_attention = len(alertes_actives[alertes_actives['type'] == 'Dépenses > Engagements'])
            st.metric("⚠️ Dépenses > Engagements", nb_alertes_attention)
        
        with col3:
            nb_alertes_risque = len(alertes_actives[alertes_actives['type'] == 'Risque Dépassement'])
            st.metric("⚡ Risques", nb_alertes_risque)
        
        if not alertes_actives.empty:
            # Séparer par type de criticité
            alertes_critiques = alertes_actives[alertes_actives['type'] == 'Dépassement Budget']
            alertes_attention = alertes_actives[alertes_actives['type'].isin(['Dépenses > Engagements', 'Risque Dépassement'])]
            
            if not alertes_critiques.empty:
                st.subheader("🚨 Alertes critiques")
                for _, alerte in alertes_critiques.iterrows():
                    st.markdown(f"""
                    <div class="alert-danger">
                        <strong>🔥 CRITIQUE</strong> - Projet {alerte['id_projet']}<br>
                        Taux: {alerte['valeur_actuelle']}% | Date: {alerte['date_detection']}<br>
                        {alerte['message']}
                    </div>
                    """, unsafe_allow_html=True)
            
            if not alertes_attention.empty:
                st.subheader("⚠️ Alertes d'attention")
                for _, alerte in alertes_attention.iterrows():
                    if alerte['type'] == 'Dépenses > Engagements':
                        st.markdown(f"""
                        <div class="alert-danger">
                            <strong>⚠️ ATTENTION</strong> - {alerte['type']}<br>
                            Projet: {alerte['id_projet']} | Ratio: {alerte['valeur_actuelle']}%<br>
                            Date: {alerte['date_detection']}<br>
                            {alerte['message']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="alert-warning">
                            <strong>⚡ RISQUE</strong> - {alerte['type']}<br>
                            Projet: {alerte['id_projet']} | Utilisation: {alerte['valeur_actuelle']}%<br>
                            Date: {alerte['date_detection']}<br>
                            {alerte['message']}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.success("✅ Aucune alerte active actuellement")
        

    with tab6:

        # Affichage des prédictions détaillées
        afficher_onglet_predictions_detaille(df_projets, df_engagements, df_depenses)
        st.markdown("---")

        # Analyse du portfolio
        analyser_risques_portfolio(df_projets, df_engagements, df_depenses)


    with tab5:
        st.header("Saisie de nouvelles données")
        
        # Formulaire de saisie de projet
        with st.expander("➕ Ajouter un nouveau projet"):
            # Initialiser un compteur pour forcer la réinitialisation du formulaire
            if 'form_key' not in st.session_state:
                st.session_state.form_key = 0

            # Utiliser le compteur comme suffixe pour créer une nouvelle instance du formulaire
            form_key = f"nouveau_projet_{st.session_state.form_key}"
            with st.form(form_key):
                col1, col2 = st.columns(2)
                
                with col1:
                    nom_projet = st.text_input("Nom du projet")
                    service = st.selectbox("Service", df_services['nom_service'])
                budget = st.number_input("Budget initial (DH)", min_value=0, value=100000)
                
                with col2:
                    date_debut = st.date_input("Date de début",value=date.today())
                    date_fin = st.date_input("Date de fin prévue",value=date.today())
                    #statut = st.selectbox("Statut", ["En cours", "Clôturé", "Suspendu"])
                
                submitted = st.form_submit_button("Ajouter le projet")
                id_genere = generer_id_projet(df_projets,date_debut)
                id_service_selectionne = ""
                if not df_services.empty and service:
                    # filtre la ligne où nom_service == service_selectionne
                    ligne_service = df_services[df_services["nom_service"] == service]
                    if not ligne_service.empty:
                        id_service_selectionne = ligne_service.iloc[0]["id_service"]
                if submitted:
                    erreurs = []
                    if not nom_projet.strip():
                        erreurs.append("Le champ **Nom du projet** est obligatoire")
                    if not service:
                        erreurs.append("Le champ **Service** est obligatoire")
                    if not date_debut:
                        erreurs.append("Le champ **Date de début** est obligatoire")
                    if not date_fin:
                        erreurs.append("Le champ **Date de fin prévue** est obligatoire")
                    if date_debut and date_fin and date_fin <= date_debut:
                            erreurs.append("La **Date de fin prévue** doit être **ultérieure** à la date de début")
                    if budget <= 0:
                        erreurs.append("Le champ **Budget** est obligatoire  et doit être supérieur à 0")

                    if erreurs:
                        for err in erreurs:
                            st.error(err)
                    else:
                        # Comparaison des dates
                        aujourd_hui = date.today()

                        if date_fin < aujourd_hui:
                            statut_auto = "Clôturé"
                        else:
                            statut_auto = "En cours"
                        # ✅ Créer une nouvelle ligne
                        nouvelle_ligne = {
                            'id_service': id_service_selectionne,
                            'id_projet': id_genere,
                            'nom_projet': nom_projet,
                            'date_debut': date_debut,
                            'date_fin_prev': date_fin,
                            'budget_initial': budget,
                            'statut': statut_auto,
                        }
                        # ✅ Charger toutes les feuilles du fichier
                        with pd.ExcelFile(excel_file, engine='openpyxl') as xls:
                            all_sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

                        # ✅ Modifier la feuille "projets"
                        df_projets = all_sheets["projets"]
                        df_projets = pd.concat([df_projets, pd.DataFrame([nouvelle_ligne])], ignore_index=True)

                        # Remplacer la feuille "projets" dans le dictionnaire
                        all_sheets["projets"] = df_projets

                        # ✅ Réécrire tout le fichier en gardant toutes les feuilles, avec le bon format de date
                        with pd.ExcelWriter(excel_file, engine='xlsxwriter', datetime_format='dd/mm/yyyy') as writer:
                            for sheet_name, df_sheet in all_sheets.items():
                                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        st.session_state["nom_projet_value"] = ""
                        st.session_state["service_index"] = 0
                        st.session_state["budget_value"] = 100000
                        st.session_state["date_debut_value"] = date.today()
                        st.session_state["date_fin_value"] = date.today()

                        st.success(f"✅ Projet '{nom_projet}' ajouté avec succès!")
                        # ✅ Incrémenter le compteur pour créer un nouveau formulaire
                        st.session_state.form_key += 1
                        st.rerun()


                        #df_indicateurs = calculer_indicateurs(df_projets, df_engagements, df_depenses)
         
        # Formulaire de saisie d'engagement
        with st.expander("📝 Ajouter un engagement"):
            if 'form_key' not in st.session_state:
                st.session_state.form_key = 0
            # Utiliser le compteur comme suffixe pour créer une nouvelle instance du formulaire
            form_key = f"nouvel_engagement{st.session_state.form_key}"
            
            with st.form(form_key):
                col1, col2 = st.columns(2)
                
                with col1:
                    projet_eng = st.selectbox("Projet", df_projets['nom_projet'])
                    fournisseur = st.text_input("Fournisseur")
                    montant_eng = st.number_input("Montant engagement (DH)", min_value=0)
                
                with col2:
                    date_eng = st.date_input("Date d'engagement")
                    objet_eng = st.text_area("Objet de l'engagement")
                
                submitted_eng = st.form_submit_button("Enregistrer l'engagement")
                id_eng_genere = generer_id_engagement(df_engagements,date_eng)
                id_projet_selectionne = ""
                if not df_projets.empty and projet_eng:
                    ligne_projet = df_projets[df_projets["nom_projet"] == projet_eng]
                    if not ligne_projet.empty:
                        id_projet_selectionne = ligne_projet.iloc[0]["id_projet"]
                        date_debut_projet = ligne_projet.iloc[0]["date_debut"]
                        date_fin_projet = ligne_projet.iloc[0]["date_fin_prev"]
                        budget_projet = ligne_projet.iloc[0]["budget_initial"]
                
                if submitted_eng:
                    erreurs = []
                    if not projet_eng.strip():
                        erreurs.append("Le champ **Projet** est obligatoire")
                    if not fournisseur:
                        erreurs.append("Le champ **Fournisseur** est obligatoire")
                    if not montant_eng:
                        erreurs.append("Le champ **Montant Engagement** est obligatoire")
                    if not date_eng:
                        erreurs.append("Le champ **Date d'engagement** est obligatoire")
                    if not objet_eng:
                        erreurs.append("Le champ **Objet de l'engagement** est obligatoire")
                    if date_eng < date_debut_projet.date() or date_eng > date_fin_projet.date():
                        st.error(" La **Date d'engagement** doit être comprise entre la date de début et de fin du projet")
                    #if montant_eng > budget_projet: 
                        #st.error("Le montant d'engagement dépasse le budget initial du projet.")

                    if erreurs:
                        for err in erreurs:
                            st.error(err)
                    else:
                        # ✅ Créer une nouvelle ligne
                        nouvelle_ligne_engagement = {
                            'id_engagement': id_eng_genere,
                            'id_projet': id_projet_selectionne,
                            'date_engagement': date_eng,
                            'montant': montant_eng,
                            'fournisseur': fournisseur,
                            'objet': objet_eng,
                        }
                        # ✅ Charger toutes les feuilles du fichier
                        with pd.ExcelFile(excel_file, engine='openpyxl') as xls:
                            all_sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

                        # ✅ Modifier la feuille "projets"
                        df_engagements = all_sheets["engagements"]
                        df_engagements = pd.concat([df_engagements, pd.DataFrame([nouvelle_ligne_engagement])], ignore_index=True)

                        # Remplacer la feuille "projets" dans le dictionnaire
                        all_sheets["engagements"] = df_engagements

                        # ✅ Réécrire tout le fichier en gardant toutes les feuilles, avec le bon format de date
                        with pd.ExcelWriter(excel_file, engine='xlsxwriter', datetime_format='dd/mm/yyyy') as writer:
                            for sheet_name, df_sheet in all_sheets.items():
                                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

                        st.success("✅ Engagement enregistré avec succès!")
                        # ✅ Incrémenter le compteur pour créer un nouveau formulaire
                        st.session_state.form_key += 1
                        st.rerun()
        
        # Formulaire de saisie de dépense
        with st.expander("💸 Enregistrer une dépense"):
            if 'form_key' not in st.session_state:
                st.session_state.form_key = 0
            # Utiliser le compteur comme suffixe pour créer une nouvelle instance du formulaire
            form_key = f"nouvelle_depense{st.session_state.form_key}"
            with st.form(form_key):
                col1, col2 = st.columns(2)
                
                with col1:
                    projet_dep = st.selectbox("Projet ", df_projets['nom_projet'])
                    montant_dep = st.number_input("Montant dépense (DH)", min_value=0)
                
                with col2:
                    date_dep = st.date_input("Date de dépense")
                    categorie = st.selectbox("Catégorie", ["Matériel", "Logiciel", "Service", "Infrastructure", "Formation"])
                    #justificatif = st.text_input("N° Justificatif")
                
                submitted_dep = st.form_submit_button("Enregistrer la dépense")
                id_dep_genere = generer_id_depense(df_depenses,date_dep)
                id_projet_selectionne = ""
                if not df_projets.empty and projet_dep:
                    ligne_projet = df_projets[df_projets["nom_projet"] == projet_dep]
                    if not ligne_projet.empty:
                        id_projet_selectionne = ligne_projet.iloc[0]["id_projet"]
                        date_debut_projet = ligne_projet.iloc[0]["date_debut"]
                        date_fin_projet = ligne_projet.iloc[0]["date_fin_prev"]

                if submitted_dep:
                    erreurs = []
                    if not projet_dep.strip():
                        erreurs.append("Le champ **Projet** est obligatoire")
                    if not montant_dep:
                        erreurs.append("Le champ **Montant Dépense** est obligatoire")
                    if not date_dep:
                        erreurs.append("Le champ **Date de dépense** est obligatoire")
                    if not categorie:
                        erreurs.append("Le champ **Catégorie** est obligatoire")
                    #if not justificatif:
                        #erreurs.append("Le champ **N° Justificatif** est obligatoire")
                    if date_dep < date_debut_projet.date() or date_dep > date_fin_projet.date():
                        st.error(" La **Date de dépense** doit être comprise entre la date de début et de fin du projet")
                    
                    if erreurs:
                        for err in erreurs:
                            st.error(err)
                    else:
                        # ✅ Créer une nouvelle ligne
                        nouvelle_ligne_depense = {
                            'id_depense': id_dep_genere,
                            'id_projet': id_projet_selectionne,
                            'date_depense': date_dep,
                            'montant': montant_dep,
                            'categorie': categorie,
                             #'justificatif': justificatif,
                        }
                        try:
                            # ✅ Charger toutes les feuilles du fichier
                            with pd.ExcelFile(excel_file, engine='openpyxl') as xls:
                                all_sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

                            # ✅ Modifier la feuille "projets"
                            df_depenses = all_sheets["dépenses"]
                            df_depenses = pd.concat([df_depenses, pd.DataFrame([nouvelle_ligne_depense])], ignore_index=True)

                            # Remplacer la feuille "projets" dans le dictionnaire
                            all_sheets["dépenses"] = df_depenses

                            # ✅ Réécrire tout le fichier en gardant toutes les feuilles, avec le bon format de date
                            with pd.ExcelWriter(excel_file, engine='xlsxwriter', datetime_format='dd/mm/yyyy') as writer:
                            #with pd.ExcelWriter(excel_file, engine='openpyxl', datetime_format='dd/mm/yyyy') as writer:
                                for sheet_name, df_sheet in all_sheets.items():
                                    df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

                            st.success("✅ Dépense enregistrée avec succès!")
                            # Recharger les données mises à jour
                            df_projets_updated = pd.read_excel(excel_file, sheet_name="projets")
                            df_engagements_updated = pd.read_excel(excel_file, sheet_name="engagements") 
                            df_depenses_updated = pd.read_excel(excel_file, sheet_name="dépenses")
                
                            # Générer les alertes après ajout de la dépense
                            nouvelles_alertes_dep = generer_alertes_automatiques(
                                df_projets_updated, df_engagements_updated, df_depenses_updated, excel_file
                            )
                            
                            # Afficher les alertes spécifiques à cette dépense
                            if nouvelles_alertes_dep:
                                st.warning("🚨 Cette dépense a déclenché de nouvelles alertes:")
                                afficher_alertes_streamlit(nouvelles_alertes_dep)
                            # ✅ Incrémenter le compteur pour créer un nouveau formulaire
                            st.session_state.form_key += 1
                            st.rerun()
                        except PermissionError:
                            st.error("❌ Accès refusé au fichier. Fermez Excel s’il est ouvert.")



    # Pied de page avec informations
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>ONCF - Office National des Chemins de Fer</strong></p>
        <p>Système de Surveillance Budgétaire | Développé avec Streamlit</p>
        <p>Projet de Fin d'Études - ENSAM Casablanca</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()