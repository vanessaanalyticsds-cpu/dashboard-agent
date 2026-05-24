import pandas as pd
import plotly.express as px
import plotly.io as pio

archivo_csv = "disney_movies.csv"
df = pd.read_csv(archivo_csv)

columnas_numericas = df.select_dtypes(include="number").columns.tolist()
columnas_texto = df.select_dtypes(include="object").columns.tolist()

graficos = []

if columnas_numericas:
    col_num = columnas_numericas[0]
    fig = px.histogram(df, x=col_num, title=f"Distribución de {col_num}")
    graficos.append(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

if columnas_texto and columnas_numericas:
    col_cat = columnas_texto[0]
    col_val = columnas_numericas[0]

    resumen = df.groupby(col_cat)[col_val].sum().reset_index()
    resumen = resumen.sort_values(col_val, ascending=False).head(10)

    fig = px.bar(
        resumen,
        x=col_cat,
        y=col_val,
        title=f"Top 10 {col_cat} por {col_val}"
    )
    graficos.append(pio.to_html(fig, full_html=False, include_plotlyjs=False))

tabla_html = df.head(10).to_html(index=False, classes="tabla")

html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Generativo CSV</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            background: #f4f6f8;
            color: #222;
        }}
        header {{
            background: linear-gradient(135deg, #1f2937, #4f46e5);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        section {{
            max-width: 1100px;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        h1 {{
            font-size: 36px;
        }}
        h2 {{
            color: #4f46e5;
        }}
        .tabla {{
            width: 100%;
            border-collapse: collapse;
        }}
        .tabla th {{
            background: #4f46e5;
            color: white;
            padding: 10px;
        }}
        .tabla td {{
            border-bottom: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
</head>
<body>

<header>
    <h1>Dashboard Generativo de Datos</h1>
    <p>Visualización automática creada desde un archivo CSV</p>
</header>

<section>
    <h2>Vista previa de datos</h2>
    {tabla_html}
</section>

<section>
    <h2>Visualizaciones</h2>
    {''.join(graficos)}
</section>

</body>
</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard creado correctamente: dashboard.html")