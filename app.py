import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

dict_colors = {
    "Thématiques_métiers": "#FF5733",  # A vibrant red-orange
    "Thématiques_transversales": "#33FF57",  # A bright green
    "Partenariats": "#3357FF",  # A deep blue
    "Processus_opérations": "#FF33A1",  # A vivid pink
    "Processus_interne": "#33FFF5",  # A refreshing cyan
    "": "#331545",  # A vibrant red-orange
}

st.set_page_config(layout="wide")

st.title("Exemple de graphes")

df_file = st.file_uploader(
    "Charge ton fichier",
    "xlsx",
    False,
    help="Le fichier doit contenir un onglet Répartition",
)

if df_file is not None:
    df = pd.read_excel(
        df_file,
        sheet_name="Répartition",
        skiprows=1,
    )
    df.fillna("", inplace=True)
    st.dataframe(df)

    # Define lists of selection options and sort alphabetically
    worker_list = df["Nom REP"].unique().tolist()
    worker_list.sort()

    categories_list = df["Catégories"].unique().tolist()
    categories_list.sort()

    subcategories_list = df["Sous-catégories"].unique().tolist()
    subcategories_list.sort()

    select_filter_type = st.selectbox(
        "Choisis un filtre",
        ["Nom REP", "Catégories", "Sous-catégories"],
    )
    # Implement multiselect dropdown menu for option selection (returns a list)
    if select_filter_type == "Nom REP":
        selected = st.multiselect(
            "Choisis un ou plusieurs REP", worker_list, worker_list
        )
        df_filtered = df[df["Nom REP"].isin(selected)]
    elif select_filter_type == "Catégories":
        selected = st.multiselect(
            "Choisis une ou plusieurs catégories", categories_list, categories_list
        )
        df_filtered = df[df["Catégories"].isin(selected)]
    else:
        selected = st.multiselect(
            "Choisis une ou plusieurs sous-catégories",
            subcategories_list,
            subcategories_list,
        )
        df_filtered = df[df["Sous-catégories"].isin(selected)]

    if len(selected) == 0:
        st.warning("Choisir au moins une valeur")

    nodes = []
    edges = []

    for index, row in df_filtered.iterrows():
        if row["Sous-catégories"] not in [node.id for node in nodes]:
            nodes.append(
                Node(
                    id=row["Sous-catégories"],
                    label=row["Sous-catégories"],
                    size=50,
                    shape="hexagon",
                    color="darkblue",
                )
            )
        if row["Nom REP"] not in [node.id for node in nodes]:
            nodes.append(
                Node(
                    id=row["Nom REP"],
                    label=row["Nom REP"],
                    size=1,
                    shape="circle",
                )
            )
        edges.append(
            Edge(
                source=row["Nom REP"],
                label=row["Catégories"],
                target=row["Sous-catégories"],
                color=dict_colors[row["Catégories"]],
                # **kwargs
            )
        )

    config = Config(
        width=1500,
        height=1500,
        directed=False,
        physics=False,
        hierarchical=False,
        # **kwargs
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
