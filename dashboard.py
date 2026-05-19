import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# LEER ARCHIVOS CSV
productos = pd.read_csv("productos.csv")
ventas = pd.read_csv("ventas.csv")

# UNIR TABLAS
datos = ventas.merge(
    productos,
    left_on="producto_id",
    right_on="id"
)

# LIMPIAR DATOS NULOS
datos = datos.dropna()

# CREAR COLUMNA DE INGRESOS
datos["ingreso"] = datos["cantidad"] * datos["precio"]

# =========================
# METRICA 1
# INGRESOS POR CATEGORIA
# =========================

ventas_categoria = datos.groupby("categoria")["ingreso"].sum()

plt.figure(figsize=(8,5))
sns.barplot(
    x=ventas_categoria.index,
    y=ventas_categoria.values
)

plt.title("Ingresos por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Ingresos")

plt.savefig("ventas_categoria.png")
plt.close()

# =========================
# METRICA 2
# PRODUCTOS MAS VENDIDOS
# =========================

top_productos = datos.groupby("nombre")["cantidad"].sum()

plt.figure(figsize=(8,8))

plt.pie(
    top_productos.values,
    labels=top_productos.index,
    autopct='%1.1f%%'
)

plt.title("Productos Mas Vendidos")

plt.savefig("top_productos.png")
plt.close()

# =========================
# TOP 3 PRODUCTOS
# =========================

top3 = (
    datos.groupby("nombre")["cantidad"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)

top3_html = top3.to_frame().to_html()

# =========================
# GENERAR HTML
# =========================

html = f"""
<html>

<head>
    <title>Panel Administrativo</title>

    <style>
        body {{
            font-family: Arial;
            margin: 40px;
            background-color: #f4f4f4;
        }}

        h1 {{
            color: #333;
        }}

        img {{
            width: 600px;
            margin-bottom: 30px;
            border-radius: 10px;
        }}

        table {{
            border-collapse: collapse;
            width: 50%;
            background: white;
        }}

        table, th, td {{
            border: 1px solid black;
            padding: 10px;
        }}
    </style>
</head>

<body>

<h1>Panel Administrativo de Mi Tienda</h1>

<h2>Ingresos por Categoria</h2>
<img src="ventas_categoria.png">

<h2>Productos Mas Vendidos</h2>
<img src="top_productos.png">

<h2>Top 3 Productos Estrella</h2>

{top3_html}

</body>

</html>
"""

# GUARDAR HTML
with open("admin_dashboard.html", "w", encoding="utf-8") as archivo:
    archivo.write(html)

print("Dashboard generado correctamente")