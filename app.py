
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])

app = dash.Dash(__name__)
app.title = "Dashboard de Ventas"

app.layout = html.Div([
    html.H1("Dashboard de Ventas", style={"textAlign": "center"}),

    dcc.Dropdown(
        id='product-dropdown',
        options=[{"label": p, "value": p} for p in df["product"].unique()],
        value=df["product"].unique()[0],
        clearable=False,
        style={"width": "300px", "margin": "10px auto"}
    ),

    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    [Output("line-chart", "figure"),
     Output("bar-chart", "figure")],
    [Input("product-dropdown", "value")]
)
def update_charts(selected_product):
    filtered_df = df[df["product"] == selected_product]

    line_fig = px.line(
        filtered_df, x="date", y="sales",
        title=f"Ventas en el tiempo – Producto {selected_product}"
    )

    bar_fig = px.bar(
        df[df["product"] == selected_product].groupby("category").sum(numeric_only=True).reset_index(),
        x="category", y="sales",
        title="Ventas por Categoría"
    )

    return line_fig, bar_fig

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
