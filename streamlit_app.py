import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np


def load_data():
    Holdings = pd.read_csv("Holdings.csv", sep=";", index_col=0)
    DebtToGDP = pd.read_csv("DebtToGDP.csv", sep="|", index_col=0)
    Holdings2 = Holdings[Holdings.index.str.endswith('Q4')]
    DebtToGDP2 = DebtToGDP[DebtToGDP.index.str.endswith('Q4')]
    return Holdings, DebtToGDP, Holdings2, DebtToGDP2


def debt_breakdown(country, data):
    country_cols = [col for col in data.columns if col.startswith(f"{country}_")]
    if not country_cols:
        st.error(f"Error: Country {country} is not present in the dataset.")
        return None

    data_mod = data.drop(columns=[col for col in data.columns if not col.split('_')[1] in ['Foreign', 'Domestic']])
    cols_to_plot = [col for col in data_mod.columns if col.startswith(f"{country}_")]
    cols_to_plot = cols_to_plot[::-1]

    x = data_mod.index.tolist()

    fig = go.Figure()

    for col in cols_to_plot:
        y = data_mod[col].values
        name = col.split('_')[1]
        color = 'red' if 'Foreign' in name else 'gray'
        fig.add_trace(go.Scatter(x=x, y=y, stackgroup='one', name=name, line=dict(color=color)))

    fig.update_layout(
        title=f"{country} - Debt evolution by investor type",
        xaxis_title="Date",
        yaxis_title="Amount",
        legend_title="Investor types",
        hovermode="x unified"
    )

    return fig


def debt_breakdown_percent(country, data):
    country_cols = [col for col in data.columns if col.startswith(f"{country}_")]

    if not country_cols:
        st.error(f"Error: Country {country} is not present in the dataset. Check uppercase or accents.")
        return None

    data_mod = data.drop(
        columns=[col for col in data.columns if not col.split('_')[1] in ['Foreign', 'Domestic']]
    )

    cols_to_plot = [col for col in data_mod.columns if col.startswith(f"{country}_")]
    cols_to_plot = cols_to_plot[::-1]

    total = data_mod[cols_to_plot].sum(axis=1)
    data_percent = data_mod[cols_to_plot].div(total, axis=0) * 100

    x = data_percent.index.tolist()

    fig = go.Figure()

    for col in cols_to_plot:
        y = data_percent[col].values
        name = col.split('_')[1]
        color = 'red' if 'Foreign' in name else 'gray'
        fig.add_trace(go.Scatter(x=x, y=y, stackgroup='one', name=name, line=dict(color=color)))

    fig.update_layout(
        title=f"{country} - Debt composition in percentage",
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Investor types",
        hovermode="x unified",
        yaxis=dict(range=[0, 100])
    )

    return fig


def debt_breakdown_details(country, data):

    color_map = {
        'ForeignOfficial': '#D62728',
        'ForeignNonbank': '#FF7F0E',
        'ForeignBank': '#9467BD',
        'DomesticNonbank': '#1F77B4',
        'DomesticCentralBank': '#2CA02C',
        'DomesticBank': '#8C564B'
    }

    country_cols = [col for col in data.columns if col.startswith(f"{country}_")]

    if not country_cols:
        st.error(f"Error: Country {country} is not present in the dataset. Check uppercase or accents.")
        return None

    data_mod = data.drop(
        columns=[col for col in data.columns if col.split('_')[1] in ['Domestic', 'Foreign', 'Total']]
    )

    cols_to_plot = [col for col in data_mod.columns if col.startswith(f"{country}_")]

    cols_to_plot = sorted(
        cols_to_plot,
        key=lambda col: (1 if "Foreign" in col else 0, col)
    )

    x = data_mod.index.tolist()

    fig = go.Figure()

    for col in cols_to_plot:
        y = data_mod[col].values
        name = col.split('_')[1]
        color = color_map.get(name, 'black')
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
        title=f"Debt evolution by detailed investor type - {country}",
        xaxis_title="Date",
        yaxis_title="Amount",
        legend_title="Investor types",
        hovermode="x unified"
    )

    return fig


def debt_breakdown_details_percent(country, data):
    country_cols = [col for col in data.columns if col.startswith(f"{country}_")]

    if not country_cols:
        st.error(f"Error: Country {country} is not present in the dataset. Check uppercase/accent.")
        return None

    # Remove 'Domestic', 'Foreign' and 'Total' columns
    data_mod = data.drop(
        columns=[col for col in data.columns if col.split('_')[1] in ['Domestic', 'Foreign', 'Total']]
    )

    cols_to_plot = [col for col in data_mod.columns if col.startswith(f"{country}_")]

    # Sort: put columns containing 'Foreign' at the end
    cols_to_plot = sorted(
        cols_to_plot,
        key=lambda col: (1 if "Foreign" in col else 0, col)
    )

    total = data_mod[cols_to_plot].sum(axis=1)
    data_percent = data_mod[cols_to_plot].div(total, axis=0) * 100

    x = data_percent.index.tolist()

    color_map = {
        'ForeignOfficial': '#D62728',
        'ForeignNonbank': '#FF7F0E',
        'ForeignBank': '#9467BD',
        'DomesticNonbank': '#1F77B4',
        'DomesticCentralBank': '#2CA02C',
        'DomesticBank': '#8C564B'
    }

    fig = go.Figure()

    for col in cols_to_plot:
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
        title=f"Debt evolution by investor type (percent) - {country}",
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend_title="Investor types",
        legend=dict(x=1.05, y=1),
        hovermode="x unified",
        yaxis=dict(range=[0, 100])
    )

    return fig


def barchart_plotly(date, country_list, data):
    pc_domestic = []
    pc_foreign = []

    for country in country_list:
        country_cols = [col for col in data.columns if col.startswith(f"{country}_")]

        if not country_cols:
            st.error(f"Error: Country {country} is not present in the dataset.")
            return None

        cols_to_plot = [col for col in country_cols if col.split('_')[1] in ['Domestic', 'Foreign']]
        cols_to_plot = cols_to_plot[::-1]

        try:
            y = [data.loc[date, col] for col in cols_to_plot]
        except KeyError:
            st.error(f"Error: Date {date} is not present for country {country}.")
            return None

        total = sum(y)
        if total == 0:
            pc_domestic.append(0)
            pc_foreign.append(0)
        else:
            pc_domestic.append((y[0] / total) * 100)
            pc_foreign.append((y[1] / total) * 100)

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Domestic', x=country_list, y=pc_domestic, marker_color='gray'))
    fig.add_trace(go.Bar(name='Foreign', x=country_list, y=pc_foreign, marker_color='red'))

    fig.update_layout(
        barmode='stack',
        title=f"Debt composition by investor type ({date})",
        yaxis=dict(title="Percentage", range=[0, 100]),
        legend_title="Investor types"
    )

    return fig


def barchart_detail_plotly(date, country_list, data):

    pc_DB = []
    pc_DCB = []
    pc_DNB = []
    pc_FB = []
    pc_FNB = []
    pc_FO = []

    labels = ['DomesticCentralBank', 'DomesticBank', 'DomesticNonBank', 'ForeignOfficial', 'ForeignBank', 'ForeignNonbank']
    colors = ['lightgray', 'red', 'tan', 'lightblue', 'darkgray', 'pink']

    for country in country_list:
        country_cols = [col for col in data.columns if col.startswith(f"{country}_")]

        if not country_cols:
            st.error(f"Error: Country {country} is not present in the dataset.")
            return None

        cols_to_plot = [col for col in country_cols if col.split('_')[1] not in ['Domestic', 'Foreign', 'Total']]
        cols_to_plot = cols_to_plot[::-1]

        try:
            y = [data.loc[date, col] for col in cols_to_plot]
        except KeyError:
            st.error(f"Error: Date {date} is not present for country {country}.")
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

    series = [pc_DCB, pc_DB, pc_DNB, pc_FO, pc_FB, pc_FNB]

    for i in range(len(series)):
        fig.add_trace(go.Bar(
            x=country_list,
            y=series[i],
            name=labels[i],
            marker_color=colors[i],
            opacity=0.8
        ))

    fig.update_layout(
        barmode='stack',
        title=f"Detailed debt composition ({date})",
        yaxis=dict(title="Percentage", range=[0, 100]),
        legend=dict(title="Investor types", x=1.05, y=1),
        margin=dict(r=150),
        xaxis_title="Country"
    )

    return fig



def index_IRI_plotly(liste_pays, data, data2):
    fig = go.Figure()
    key_years = ['2004Q4', '2023Q4']

    for country in liste_pays:
        country_cols = [col for col in data.columns if col.startswith(f"{country}_")]
        if not country_cols:
            st.error(f"Error: Country {country} is not present in the dataset.")
            return None

        foreign_cols = [f'{country}_ForeignBank', f'{country}_ForeignNonbank']
        total_col = f'{country}_Total'

        foreign_total = data[foreign_cols[0]] + data[foreign_cols[1]]
        total = data[total_col]

        if isinstance(total, pd.DataFrame):
            total = total[total_col]

        x = foreign_total / total

        dtogdp_cols = [col for col in data2.columns if col.startswith(f'{country}')]
        y = data2[dtogdp_cols]

        if isinstance(y, pd.DataFrame):
            y = y.squeeze()

        # Align indices to ensure consistency
        common_index = x.index.intersection(y.index)
        x = x.loc[common_index]
        y = y.loc[common_index]

        fig.add_trace(go.Scatter(
            x=x.values,
            y=y.values,
            mode='lines+markers',
            name=country,
            marker=dict(size=6),
            line=dict(width=2),
            hovertemplate='Foreign share: %{x:.3f}<br>% GDP: %{y:.2f}<extra></extra>'
        ))

        # Add annotations for key years
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
        title='IRI Index',
        xaxis_title='Foreign private share (%)',
        yaxis_title='Debt to GDP (%)',
        legend_title='Country',
        legend=dict(x=1.05, y=1),
        margin=dict(r=150),
        xaxis=dict(range=[0, 0.75]),
        yaxis=dict(range=[50, 250]),
        hovermode='closest',
        template='plotly_white'
    )

    return fig


def index_IRI_plotly_with_dates(liste_pays, data, data2):
    fig = go.Figure()
    key_years = ['2004Q4', '2023Q4']

    for country in liste_pays:
        country_cols = [col for col in data.columns if col.startswith(f"{country}_")]
        if not country_cols:
            st.error(f"Error: Country {country} is not present in the dataset.")
            return None

        foreign_cols = [f'{country}_ForeignBank', f'{country}_ForeignNonbank']
        total_col = f'{country}_Total'

        foreign_total = data[foreign_cols[0]] + data[foreign_cols[1]]
        total = data[total_col]

        x = foreign_total / total

        dtogdp_cols = [col for col in data2.columns if col.startswith(f'{country}')]
        y = data2[dtogdp_cols]

        if isinstance(y, pd.DataFrame):
            y = y.squeeze()

        fig.add_trace(go.Scatter(
            x=x.index,
            y=x.values,
            mode='lines+markers',
            name=country,
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
        title='IRI Index',
        xaxis_title='Foreign private share (%)',
        yaxis_title='Debt to GDP (%)',
        legend_title='Country',
        legend=dict(x=1.05, y=1),
        xaxis=dict(range=[0, 0.75]),
        yaxis=dict(range=[50, 250]),
        margin=dict(r=150),
        hovermode='closest',
        template='plotly_white'
    )

    return fig


# ---- Start Streamlit ----

Holdings, DebtToGDP, Holdings2, DebtToGDP2 = load_data()

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

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
    if st.button("Software Presentation"):
        st.session_state.page = "Home"

with col2:
    if st.button("Generate Debt Composition Charts for a Country"):
        st.session_state.page = "Breakdown"

with col3:
    if st.button("Compare Multiple Countries at a Given Date"):
        st.session_state.page = "Comparison"

with col4:
    if st.button("Debt-to-GDP Ratio vs IRI Index"):
        st.session_state.page = "IRI"


# --------------------------- HOME PAGE ---------------------------

if st.session_state.page == "Home":
    st.title("Welcome to the Sovereign Debt Visualizer")
    st.markdown("Click one of the buttons above to get started.")

if st.session_state.page == "Home":
    st.title("Presentation")
    st.markdown("""
    This interactive application allows you to analyze sovereign debt ratios using official data from the **International Monetary Fund (IMF)**.

    ### About the Data
    - Source: IMF Monetary and Capital Markets Department.
    - Coverage: 1989 Q4 to 2024 Q2.
    - Investor categories: National central bank, domestic banks, domestic non-banks, foreign official institutions, foreign banks, foreign non-banks.

    Use the buttons above to explore the available analyses.
    """)


# --------------------------- BREAKDOWN PAGE ---------------------------

elif st.session_state.page == "Breakdown":
    st.title("Debt Breakdown by Country")
    country = st.selectbox("Choose a country", sorted({col.split('_')[0] for col in Holdings.columns}))

    if st.button("Display Debt Breakdown Charts"):
        with st.spinner("Generating charts..."):
            fig = debt_breakdown(country, Holdings)
            if fig:
                st.plotly_chart(fig)

            fig2 = debt_breakdown_details_percent(country, Holdings)
            if fig2:
                st.plotly_chart(fig2)

            fig3 = debt_breakdown_details(country, Holdings)
            if fig3:
                st.plotly_chart(fig3)

            fig4 = debt_breakdown_details_percent(country, Holdings)
            if fig4:
                st.plotly_chart(fig4, key = "fig_4_breakdown)


# --------------------------- COMPARISON PAGE ---------------------------

elif st.session_state.page == "Comparison":
    st.title("Comparison of Multiple Countries on a Given Date")
    date_input = st.text_input("Enter a date (example: 2024Q2)")
    countries_input = st.text_input("Enter a list of countries separated by commas (example: France, Germany)")
    country_list = [p.strip() for p in countries_input.split(',') if p.strip()]

    if st.button("Compare Countries"):
        if date_input and country_list:
            with st.spinner("Generating charts..."):
                fig = barchart_plotly(date_input, country_list, Holdings)
                if fig:
                    st.plotly_chart(fig)

                fig2 = barchart_detail_plotly(date_input, country_list, Holdings)
                if fig2:
                    st.plotly_chart(fig2)
        else:
            st.error("Please enter both a date and at least one country.")


# --------------------------- IRI PAGE ---------------------------

elif st.session_state.page == "IRI":
    st.title("Debt-to-GDP Ratio vs IRI Index")
    countries_input_iri = st.text_input("Enter a list of countries separated by commas (example: France, Germany)", key="iri_countries")
    country_list_iri = [p.strip() for p in countries_input_iri.split(',') if p.strip()]

    if st.button("Display IRI Index Chart"):
        if country_list_iri:
            with st.spinner("Generating chart..."):
                fig = index_IRI_plotly(country_list_iri, Holdings2, DebtToGDP2)
                if fig:
                    st.plotly_chart(fig)
        else:
            st.error("Please enter at least one country.")


# --------------------------- FOOTER ---------------------------

st.markdown("---")
st.markdown("""
<p style="font-size:0.9rem; color:gray; text-align:center;">
    Official data extracted from the <a href="https://www.imf.org" target="_blank">International Monetary Fund (IMF)</a>.<br>
    Software developed by <strong><a href="https://www.linkedin.com/in/mohamed-boumezou-a8a0052ab/" target="_blank">Mohamed Boumezou</a></strong>.
</p>
""", unsafe_allow_html=True)

