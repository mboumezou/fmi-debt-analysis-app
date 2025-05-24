import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np


def load_data() :
    Holdings = pd.read_csv("Holdings.csv", sep=";", index_col=0)
    DebtToGDP = pd.read_csv("DebtToGDP.csv", sep="|", index_col=0)
    Holdings2 = Holdings[Holdings.index.str.endswith('Q4')]
    DebtToGDP2 = DebtToGDP[DebtToGDP.index.str.endswith('Q4')]
    return Holdings, DebtToGDP, Holdings2, DebtToGDP2

def decomposition_dette(pays, data):
    colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]
    if not colonnes_pays:
        st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données.")
        return None

    data_mod = data.drop(columns=[col for col in data.columns if not col.split('_')[1] in ['Foreign', 'Domestic']])
    colonnes_a_afficher = [col for col in data_mod.columns if col.startswith(f"{pays}_")]
    colonnes_a_afficher = colonnes_a_afficher[::-1]

    x = data_mod.index.tolist()

    fig = go.Figure()

    for col in colonnes_a_afficher:
        y = data_mod[col].values
        name = col.split('_')[1]
        color = 'red' if 'Foreign' in name else 'gray'
        fig.add_trace(go.Scatter(x=x, y=y, stackgroup='one', name=name, line=dict(color=color)))

    fig.update_layout(
        title=f"{pays} - Évolution de la dette par type d'investisseur",
        xaxis_title="Date",
        yaxis_title="Montant",
        legend_title="Types d'investisseurs",
        hovermode="x unified"
    )

    return fig

def decomposition_dette_en_pc(pays, data):
    colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]

    if not colonnes_pays:
        st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données, vérifier majuscule/accent.")
        return None

    data_mod = data.drop(
        columns=[col for col in data.columns if not col.split('_')[1] in ['Foreign', 'Domestic']]
    )

    colonnes_a_afficher = [col for col in data_mod.columns if col.startswith(f"{pays}_")]
    colonnes_a_afficher = colonnes_a_afficher[::-1]

    total = data_mod[colonnes_a_afficher].sum(axis=1)
    data_percent = data_mod[colonnes_a_afficher].div(total, axis=0) * 100

    x = data_percent.index.tolist()

    fig = go.Figure()

    for col in colonnes_a_afficher:
        y = data_percent[col].values
        name = col.split('_')[1]
        color = 'red' if 'Foreign' in name else 'gray'
        fig.add_trace(go.Scatter(x=x, y=y, stackgroup='one', name=name, line=dict(color=color)))

    fig.update_layout(
        title=f"{pays} - Répartition de la dette en pourcentage",
        xaxis_title="Date",
        yaxis_title="Pourcentage (%)",
        legend_title="Types d'investisseurs",
        hovermode="x unified",
        yaxis=dict(range=[0, 100])
    )

    return fig

def decomposition_dette_details(pays, data):

    color_map = {
    'ForeignOfficial': '#D62728',   # rouge vif
    'ForeignNonbank': '#FF7F0E',    # orange
    'ForeignBank': '#9467BD',       # violet
    'DomesticNonbank': '#1F77B4',   # bleu
    'DomesticCentralBank': '#2CA02C', # vert
    'DomesticBank': '#8C564B'       # marron
}


    colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]

    if not colonnes_pays:
        st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données, vérifier majuscule/accent.")
        return None

    data_mod = data.drop(
        columns=[col for col in data.columns if col.split('_')[1] in ['Domestic', 'Foreign', 'Total']]
    )

    colonnes_a_afficher = [col for col in data_mod.columns if col.startswith(f"{pays}_")]

    colonnes_a_afficher = sorted(
        colonnes_a_afficher,
        key=lambda col: (1 if "Foreign" in col else 0, col)
    )

    x = data_mod.index.tolist()

    fig = go.Figure()

    for col in colonnes_a_afficher:
        y = data_mod[col].values
        name = col.split('_')[1]
        color = color_map.get(name, 'black')  # couleur par défaut si nom inconnu
        fig.add_trace(go.Scatter(
        x=x,
        y=y,
        stackgroup='one',
        name=name,
        line=dict(width=0.5, color=color),
        fillcolor=color,
        opacity=0.8
    ))

    fig.update_layout(
        title=f"Évolution de la dette par type d'investisseur - {pays}",
        xaxis_title="Date",
        yaxis_title="Montant",
        legend_title="Types d'investisseurs",
        hovermode="x unified"
    )

    return fig

def decomposition_dette_details_en_pc(pays, data):
    colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]

    if not colonnes_pays:
        st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données, vérifier majuscule/accent.")
        return None

    # Supprimer les colonnes 'Domestic', 'Foreign' et 'Total'
    data_mod = data.drop(
        columns=[col for col in data.columns if col.split('_')[1] in ['Domestic', 'Foreign', 'Total']]
    )

    colonnes_a_afficher = [col for col in data_mod.columns if col.startswith(f"{pays}_")]

    # Tri : mettre les colonnes avec 'Foreign' en dernier
    colonnes_a_afficher = sorted(
        colonnes_a_afficher,
        key=lambda col: (1 if "Foreign" in col else 0, col)
    )

    total = data_mod[colonnes_a_afficher].sum(axis=1)
    data_percent = data_mod[colonnes_a_afficher].div(total, axis=0) * 100

    x = data_percent.index.tolist()

    color_map = {
        'ForeignOfficial': '#D62728',    # rouge vif
        'ForeignNonbank': '#FF7F0E',     # orange
        'ForeignBank': '#9467BD',        # violet
        'DomesticNonbank': '#1F77B4',    # bleu
        'DomesticCentralBank': '#2CA02C',# vert
        'DomesticBank': '#8C564B'        # marron
    }

    fig = go.Figure()

    for col in colonnes_a_afficher:
        y = data_percent[col].values
        name = col.split('_')[1]
        color = color_map.get(name, 'black')
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            stackgroup='one',
            name=name,
            line=dict(width=0.3, color=color),
            fillcolor=color,
            opacity=0.8
        ))

    fig.update_layout(
        title=f"Évolution de la dette par type d'investisseur - {pays}",
        xaxis_title="Date",
        yaxis_title="Pourcentage (%)",
        legend_title="Types d'investisseurs",
        legend=dict(x=1.05, y=1),
        hovermode="x unified",
        yaxis=dict(range=[0, 100])
    )

    return fig

def barchart_plotly(date, liste_pays, data):
    pc_domestic = []
    pc_foreign = []

    for pays in liste_pays:
        colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]

        if not colonnes_pays:
            st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données.")
            return None

        colonnes_to_plot = [col for col in colonnes_pays if col.split('_')[1] in ['Domestic', 'Foreign']]
        colonnes_to_plot = colonnes_to_plot[::-1]

        try:
            y = [data.loc[date, col] for col in colonnes_to_plot]
        except KeyError:
            st.error(f"Erreur : La date {date} n'est pas présente pour le pays {pays}.")
            return None

        total = sum(y)
        if total == 0:
            pc_domestic.append(0)
            pc_foreign.append(0)
        else:
            pc_domestic.append((y[0] / total) * 100)
            pc_foreign.append((y[1] / total) * 100)

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Domestic', x=liste_pays, y=pc_domestic, marker_color='gray'))
    fig.add_trace(go.Bar(name='Foreign', x=liste_pays, y=pc_foreign, marker_color='red'))

    fig.update_layout(
        barmode='stack',
        title=f"Répartition de la dette par type d'investisseur ({date})",
        yaxis=dict(title="Pourcentage (%)", range=[0, 100]),
        legend_title="Types d'investisseurs"
    )

    return fig

def barchart_detail_plotly(date, liste_pays, data):
   
    pc_DB = []
    pc_DCB = []
    pc_DNB = []
    pc_FB = []
    pc_FNB = []
    pc_FO = []

    labels = ['DomesticCentralBank', 'DomesticBank', 'DomesticNonBank', 'ForeignOfficial', 'ForeignBank', 'ForeignNonbank']
    colors = ['lightgray', 'red', 'tan', 'lightblue', 'darkgray', 'pink']

    for pays in liste_pays:
        colonnes_pays = [col for col in data.columns if col.startswith(f"{pays}_")]

        if not colonnes_pays:
            st.error(f"Erreur : Le pays {pays} n'est pas présent dans les données.")
            return None

        colonnes_to_plot = [col for col in colonnes_pays if col.split('_')[1] not in ['Domestic', 'Foreign', 'Total']]
        colonnes_to_plot = colonnes_to_plot[::-1]

        try:
            y = [data.loc[date, col] for col in colonnes_to_plot]
        except KeyError:
            st.error(f"Erreur : La date {date} n'est pas présente pour le pays {pays}.")
            return None

        total = sum(y)
        if total == 0:
            y_percent = [0] * len(y)
        else:
            y_percent = [(val / total) * 100 for val in y]

        
        pc_DNB.append(y_percent[0])
        pc_DB.append(y_percent[1])
        pc_DCB.append(y_percent[2])
        pc_FNB.append(y_percent[3])
        pc_FB.append(y_percent[4])
        pc_FO.append(y_percent[5])

    fig = go.Figure()


    affichage = [pc_DCB, pc_DB, pc_DNB, pc_FO, pc_FB, pc_FNB]

    for i in range(len(affichage)):
        fig.add_trace(go.Bar(
            x=liste_pays,
            y=affichage[i],
            name=labels[i],
            marker_color=colors[i],
            opacity=0.8
        ))

    fig.update_layout(
        barmode='stack',
        title=f"Barchart répartition de la dette ({date})",
        yaxis=dict(title="Pourcentage (%)", range=[0, 100]),
        legend=dict(title="Types d'investisseurs", x=1.05, y=1),
        margin=dict(r=150),
        xaxis_title="Pays"
    )

    return fig


    fig = go.Figure()
    key_years = ['2004Q4', '2023Q4']

    for Pays in liste_pays:
        colonnes_pays = [col for col in data.columns if col.startswith(f"{Pays}_")]
        if not colonnes_pays:
            st.error(f"Erreur : Le pays {Pays} n'est pas présent dans les données.")
            return None

        colonnes_foreign = [f'{Pays}_ForeignBank', f'{Pays}_ForeignNonbank']
        colonne_total = f'{Pays}_Total'

        foreign_total = data[colonnes_foreign[0]] + data[colonnes_foreign[1]]
        total = data[colonne_total]

    
        x = foreign_total / total

        dtogdp_cols = [col for col in data2.columns if col.startswith(f'{Pays}')]
        y = data2[dtogdp_cols]
        if isinstance(y, pd.DataFrame):
            y = y.squeeze()

        fig.add_trace(go.Scatter(
            x=x.index,
            y=x.values,
            mode='lines+markers',
            name=Pays,
            marker=dict(size=6),
            line=dict(width=2),
            hovertemplate='%{x}<br>IRI: %{y:.2f}<extra></extra>'
        ))

        for year in key_years:
            if year in x.index:
                fig.add_annotation(
                    x=year,
                    y=y[year],
                    text=year.split('Q')[0],
                    showarrow=True,
                    arrowhead=1,
                    ax=20,
                    ay=-20,
                    font=dict(size=12, color=fig.data[-1].line.color),
                    opacity=0.6
                )

    fig.update_layout(
        title='Indice IRI',
        xaxis_title='Foreign private share %',
        yaxis_title='% GDP',
        legend_title='Pays',
        legend=dict(x=1.05, y=1),
        xaxis=dict(range=[0, 0.75]),
        yaxis=dict(range=[50, 250]),
        margin=dict(r=150),
        hovermode='closest',
        template='plotly_white',
        grid=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
    )

    return fig

def index_IRI_plotly(liste_pays, data, data2):
    fig = go.Figure()
    key_years = ['2004Q4', '2023Q4']

    for Pays in liste_pays:
        colonnes_pays = [col for col in data.columns if col.startswith(f"{Pays}_")]
        if not colonnes_pays:
            st.error(f"Erreur : Le pays {Pays} n'est pas présent dans les données.")
            return None

        colonnes_foreign = [f'{Pays}_ForeignBank', f'{Pays}_ForeignNonbank']
        colonne_total = f'{Pays}_Total'

        foreign_total = data[colonnes_foreign[0]] + data[colonnes_foreign[1]]
        total = data[colonne_total]

        if isinstance(total, pd.DataFrame):
            total = total[colonne_total]

        x = foreign_total / total

        dtogdp_cols = [col for col in data2.columns if col.startswith(f'{Pays}')]
        y = data2[dtogdp_cols]

        if isinstance(y, pd.DataFrame):
            y = y.squeeze()

        # Aligner les index pour éviter des erreurs et assurer cohérence
        common_index = x.index.intersection(y.index)
        x = x.loc[common_index]
        y = y.loc[common_index]

        fig.add_trace(go.Scatter(
            x=x.values,
            y=y.values,
            mode='lines+markers',
            name=Pays,
            marker=dict(size=6),
            line=dict(width=2),
            hovertemplate='Foreign share: %{x:.3f}<br>% GDP: %{y:.2f}<extra></extra>'
        ))

        # Ajouter les annotations pour les années clés
        for year in key_years:
            if year in common_index:
                idx = common_index.get_loc(year)
                fig.add_annotation(
                    x=x.iloc[idx],
                    y=y.iloc[idx],
                    text=year.split('Q')[0],
                    showarrow=True,
                    arrowhead=1,
                    ax=20,
                    ay=-20,
                    font=dict(size=12, color=fig.data[-1].line.color),
                    opacity=0.6
                )

    fig.update_layout(
        title='Indice IRI',
        xaxis_title='Foreign private share %',
        yaxis_title='% GDP',
        legend_title='Pays',
        legend=dict(x=1.05, y=1),
        margin=dict(r=150),
        xaxis=dict(range=[0, 0.75]),
        yaxis=dict(range=[50, 250]),
        hovermode='closest',
        template='plotly_white'
    )

    return fig



# ---- Début Streamlit ---- 

Holdings, DebtToGDP, Holdings2, DebtToGDP2 = load_data()

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #007bff;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: bold;
    margin-right: 10px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #0056b3;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 2])
with col1:
    if st.button("🏠 Présentation du logiciel"):
        st.session_state.page = "Accueil"
with col2:
    if st.button("📈 Générer les graphiques de répartition pour un pays"):
        st.session_state.page = "Décomposition"
with col3:
    if st.button("📊 Comparaison de plusieurs pays à une date"):
        st.session_state.page = "Comparaison"
with col4:
    if st.button("🔍 Ratio Dette/PIB vs IRI pour un ou plusieurs pays"):
        st.session_state.page = "IRI"

if st.session_state.page == "Accueil":
    st.title("Bienvenue dans le Visualisateur Dette & Indicateurs")
    st.markdown("Cliquez sur l'un des boutons en haut pour démarrer.")

if st.session_state.page == "Accueil":
    st.title("Présentation")
    st.markdown("""
    Cette application interactive permet d'analyser les ratios de dette souveraine selon les données officielles du **Fonds Monétaire International (FMI)**.

    ### À propos des données
    - Source : Département des Marchés Monétaires et des Capitaux du FMI.
    - Période couverte : 1989 Q4 à 2024 Q2.
    - Catégories d'investisseurs : Banque centrale nationale, banques domestiques, non-banques domestiques, institutions étrangères officielles, banques étrangères, non-banques étrangères.

    Utilisez les boutons en haut pour explorer les analyses disponibles.
    """)

elif st.session_state.page == "Décomposition":
    st.title("Décomposition de la dette par pays")
    pays = st.selectbox("Choisissez un pays", sorted({col.split('_')[0] for col in Holdings.columns}))
    if st.button("Afficher la décomposition de la dette"):
        with st.spinner("Génération des graphiques..."):
            fig = decomposition_dette(pays, Holdings)
            if fig:
                st.plotly_chart(fig)
            fig2 = decomposition_dette_en_pc(pays, Holdings)
            if fig2:
                st.plotly_chart(fig2)
            fig3 = decomposition_dette_details(pays, Holdings)
            if fig3:
                st.plotly_chart(fig3)
            fig4 = decomposition_dette_details_en_pc(pays, Holdings)
            if fig4:
                st.plotly_chart(fig4)

elif st.session_state.page == "Comparaison":
    st.title("Comparaison de plusieurs pays à une date")
    date_input = st.text_input("Entrez une date (exemple : 2024Q2)")
    pays_input = st.text_input("Entrez une liste de pays séparés par des virgules (exemple : France, Germany)")
    liste_pays = [p.strip() for p in pays_input.split(',') if p.strip()]
    if st.button("Comparer plusieurs pays pour cette date"):
        if date_input and liste_pays:
            with st.spinner("Génération des graphiques..."):
                fig = barchart_plotly(date_input, liste_pays, Holdings)
                if fig:
                    st.plotly_chart(fig)
                fig2 = barchart_detail_plotly(date_input, liste_pays, Holdings)
                if fig2:
                    st.plotly_chart(fig2)
        else:
            st.error("Veuillez renseigner une date ET au moins un pays.")

elif st.session_state.page == "IRI":
    st.title("Indice Dette/PIB vs IRI")
    pays_input_iri = st.text_input("Entrez une liste de pays séparés par des virgules (exemple : France,Germany)", key="iri_pays")
    liste_pays_iri = [p.strip() for p in pays_input_iri.split(',') if p.strip()]
    if st.button("Afficher l'indice Dette/PIB vs IRI"):
        if liste_pays_iri:
            with st.spinner("Génération du graphique..."):
                fig = index_IRI_plotly(liste_pays_iri, Holdings2, DebtToGDP2)
                if fig:
                    st.plotly_chart(fig)
        else:
            st.error("Veuillez entrer au moins un pays.")

st.markdown("---")
st.markdown("""
<p style="font-size:0.9rem; color:gray; text-align:center;">
    Données officielles extraites du <a href="https://www.imf.org" target="_blank">Fonds Monétaire International (FMI)</a>.<br>
    Logiciel réalisé par <strong><a href="https://www.linkedin.com/in/mohamed-boumezou-a8a0052ab/" target="_blank">Mohamed Boumezou</a></strong>.
</p>
""", unsafe_allow_html=True)

