from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv("./result.csv")

def get_map():
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_data=["nome_sancionado"],
        zoom=5,
        height=550,
        color="codigo_sancionado",
        labels={"codigo_sancionado": "CPF/CNPJ dos Sancionados"},
    )
    fig.update_layout(mapbox_style="open-street-map")

    return fig


def get_hist():
    fig = px.histogram(
        df,
        title="Quantidade de Sanções por CPF/CNPJ",
        hover_name="nome_sancionado",
        x="codigo_sancionado",
        text_auto=True,
        labels={"codigo_sancionado": "CPF/CNPJ dos Sancionados"},
    )
    return fig


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Empresas Inidôneas e Suspensas", className="text-center"
                        )
                    ],
                    align="center",
                )
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=get_map())]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=get_hist())]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            page_size=10,
                            style_table={"overflowX": "auto"},
                        )
                    ],
                    class_name="p-3",
                )
            ]
        ),
    ],
    className="p-3",
)

if __name__ == "__main__":
    app.run_server(debug=True)
