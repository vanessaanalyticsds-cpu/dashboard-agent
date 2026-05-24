import pandas as pd
import plotly.express as px
from pathlib import Path

# Ruta del CSV
csv_path = "data/disney_movies.csv"

# Leer data
df = pd.read_csv(csv_path)

# Limpieza básica
df.columns = df.columns.str.strip()

# Detectar columnas
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

# Elegir columnas automáticamente
categoria = categorical_cols[0] if categorical_cols else None
valor = numeric_cols[0] if numeric_cols else None

# Crear gráficos
fig_bar = px.bar(
    df,
    x=categoria,
    y=valor,
    title=f"{valor} por {categoria}",
    template="plotly_white"
)

fig_line = px.line(
    df,
    y=valor,
    title=f"Evolución de {valor}",
    template="plotly_white"
)

fig_hist = px.histogram(
    df,
    x=valor,
    title=f"Distribución de {valor}",
    template="plotly_white"
)

# Convertir gráficos a HTML
bar_html = fig_bar.to_html(full_html=False, include_plotlyjs="cdn")
line_html = fig_line.to_html(full_html=False, include_plotlyjs=False)
hist_html = fig_hist.to_html(full_html=False, include_plotlyjs=False)

# KPIs
total_registros = len(df)
total_valor = df[valor].sum() if valor else 0
promedio_valor = df[valor].mean() if valor else 0

# HTML final
html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Generado</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f6fb;
            color: #1f2937;
        }}

        header {{
            background: linear-gradient(135deg, #111827, #2563eb);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .container {{
            padding: 30px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .kpi {{
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            text-align: center;
        }}

        .kpi h2 {{
            margin: 0;
            color: #2563eb;
            font-size: 32px;
        }}

        .kpi p {{
            margin: 8px 0 0;
            color: #6b7280;
        }}

        .filter-box {{
            background: white;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        }}

        select {{
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            min-width: 250px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            position: relative;
        }}

        .card.fullscreen {{
            position: fixed;
            top: 20px;
            left: 20px;
            width: calc(100% - 40px);
            height: calc(100% - 40px);
            z-index: 999;
            overflow: auto;
        }}

        .btn {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: #2563eb;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 8px;
            cursor: pointer;
        }}

        @media(max-width: 900px) {{
            .grid, .kpi-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>

<header>
    <h1>Dashboard Automático</h1>
    <p>Visualización generada desde CSV con estilo tipo Power BI</p>
</header>

<div class="container">

    <div class="kpi-grid">
        <div class="kpi">
            <h2>{total_registros}</h2>
            <p>Total registros</p>
        </div>
        <div class="kpi">
            <h2>{total_valor:,.0f}</h2>
            <p>Total {valor}</p>
        </div>
        <div class="kpi">
            <h2>{promedio_valor:,.2f}</h2>
            <p>Promedio {valor}</p>
        </div>
    </div>

    <div class="filter-box">
        <label>Filtro visual por categoría:</label>
        <select id="categoryFilter" onchange="filterCards()">
            <option value="all">Ver todo</option>
            <option value="bar">Gráfico de barras</option>
            <option value="line">Gráfico de línea</option>
            <option value="hist">Histograma</option>
        </select>
    </div>

    <div class="grid">
        <div class="card chart-card bar">
            <button class="btn" onclick="toggleFullscreen(this)">Agrandar</button>
            {bar_html}
        </div>

        <div class="card chart-card line">
            <button class="btn" onclick="toggleFullscreen(this)">Agrandar</button>
            {line_html}
        </div>

        <div class="card chart-card hist">
            <button class="btn" onclick="toggleFullscreen(this)">Agrandar</button>
            {hist_html}
        </div>
    </div>

</div>

<script>
    function toggleFullscreen(button) {{
        const card = button.parentElement;
        card.classList.toggle("fullscreen");
        button.innerText = card.classList.contains("fullscreen") ? "Cerrar" : "Agrandar";
    }}

    function filterCards() {{
        const value = document.getElementById("categoryFilter").value;
        const cards = document.querySelectorAll(".chart-card");

        cards.forEach(card => {{
            if (value === "all" || card.classList.contains(value)) {{
                card.style.display = "block";
            }} else {{
                card.style.display = "none";
            }}
        }});
    }}
</script>

</body>
</html>
"""

# Guardar archivo
Path("dashboard.html").write_text(html, encoding="utf-8")

print("Dashboard generado correctamente: dashboard.html")