![Banner del scraper](banner.png)
# 🏠 PortalInmobiliario Scraper

🔍 De una necesidad concreta a una solución automatizada con Python e IA

Todo partió con una necesidad simple: encontrar el mejor arriendo posible para vivir con dos amigos. En lugar de revisar portales manualmente, decidí automatizar el proceso.

💡 En una conversación con una IA surgió la idea de resolverlo usando web scraping. Hasta ese momento, solo conocía el concepto; nunca había hecho un scraper real.

Tras unas 5 horas de trabajo iterativo (sí, quizás más de las que hubiese invertido solo buscando arriendos 😂), alrededor de 15 versiones de código y varios ajustes, logré construir un script en Python que:

✅ Aplica filtros por comuna, tipo de propiedad y cantidad de dormitorios  
✅ Navega automáticamente por los resultados en Portal Inmobiliario  
✅ Extrae datos clave como precios (UF o CLP), ubicación y links  
✅ Convierte valores en UF a CLP  
✅ Guarda los resultados en archivos Excel listos para análisis  

No se trató solo de automatizar un proceso: fue una forma concreta de resolver un problema real con código, entendiendo las restricciones de la plataforma y adaptando la lógica paso a paso.

🎯 Aprendí a construir soluciones desde cero, a depurar errores y a iterar con foco en resultados.  
🤝 Si estás trabajando en algo similar o te interesa automatizar procesos para toma de decisiones, feliz de compartir el código o colaborar en ideas.

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- ChromeDriver compatible (debe estar en la misma carpeta o en el PATH)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

1. Ejecuta el script:

```bash
python scraping_portalinmobiliario.py
```

2. Ingresa los filtros según se te indiquen.
3. Los archivos se guardarán en la carpeta `Resultados/`.

---

## 🧪 Ejemplo de uso

```plaintext
Ingrese valor actual de la UF en CLP sin puntos: 37800
Selecciona operación(es):
1. venta
2. arriendo
Ingresa los números separados por coma (ej: 1,2): 2
...
```

---

## 📁 Estructura de salida

Cada archivo CSV generado tendrá un nombre como:

```
resultados_arriendo_departamento_metropolitana_nunoa_2-dormitorios_20250514_120402.csv
```

Y contendrá columnas como:

- Link
- Comuna
- Propiedad
- Tipo
- Precio
- Precio_CLP
- Dormitorios
- Baños
- Metros
- Entrega
- Disponibles

---

## 🧑‍💻 Autor

**Sebastián Padilla**  
📍 Santiago, Chile  
💼 Ingeniero Civil Industrial | Data Analyst

---

## ✅ Contribuciones

¡Bienvenidas! Puedes abrir issues o hacer un fork para mejoras.
