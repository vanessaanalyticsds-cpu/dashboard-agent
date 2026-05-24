import pandas as pd
import plotly.express as px
from pathlib import Path
import glob

# Ruta del CSV
files = glob.glob("data/*.csv")

if not files:
    raise Exception("No hay CSV en la carpeta data")

csv_path = files[0]

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
html = Path("templates/style.html").read_text(encoding="utf-8")

# Guardar archivo
Path("output/dashboard.html").write_text(html, encoding="utf-8")

print("Dashboard generado correctamente: output/dashboard.html")