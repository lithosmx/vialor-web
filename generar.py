"""
Arma la página pública vialor.app/privacidad desde docs/PRIVACIDAD.md del proyecto Vialor (solo lo que va después
de la línea "---": las notas para nosotros no se publican). Uso: python generar.py, y luego subir a GitHub.
"""
import html
import re
from pathlib import Path

AQUI = Path(__file__).parent
ORIGEN = AQUI.parent / "Vialor" / "docs" / "PRIVACIDAD.md"

ESTILO = """
:root { --fondo: #ffffff; --texto: #1c1b1f; --suave: #5f5c66; --linea: #e3e1e8; --acento: #0b6e4f; }
@media (prefers-color-scheme: dark) {
  :root { --fondo: #141317; --texto: #e6e1e9; --suave: #a9a4b0; --linea: #2f2d35; --acento: #5fd3a8; }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--fondo); color: var(--texto);
  font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 720px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 1.8em; line-height: 1.25; margin: 0 0 8px; }
h2 { font-size: 1.25em; margin: 36px 0 8px; padding-top: 16px; border-top: 1px solid var(--linea); }
a { color: var(--acento); }
code { font-size: .9em; }
ul { padding-left: 1.3em; }
li { margin: 4px 0; }
.marca { font-weight: 700; color: var(--acento); text-decoration: none; font-size: 1.1em; }
header { margin-bottom: 24px; }
footer { margin-top: 48px; color: var(--suave); font-size: .9em; }
"""


def en_linea(texto: str) -> str:
    t = html.escape(texto, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\b([\w.+-]+@vialor\.app)\b", r'<a href="mailto:\1">\1</a>', t)
    t = re.sub(r"\b((?:policies|developers)\.google\.com/[\w/.-]*)", r'<a href="https://\1">\1</a>', t)
    return t


def a_html(md: str) -> tuple[str, str]:
    titulo, partes, parrafo, lista = "", [], [], []

    def cerrar():
        if parrafo:
            partes.append("<p>" + "<br>\n".join(en_linea(l) for l in parrafo) + "</p>")
            parrafo.clear()
        if lista:
            partes.append("<ul>\n" + "\n".join(f"<li>{en_linea(l)}</li>" for l in lista) + "\n</ul>")
            lista.clear()

    for linea in md.splitlines():
        linea = linea.rstrip()
        if not linea:
            cerrar()
        elif linea.startswith("# "):
            cerrar()
            titulo = linea[2:]
            partes.append(f"<h1>{en_linea(titulo)}</h1>")
        elif linea.startswith("## "):
            cerrar()
            partes.append(f"<h2>{en_linea(linea[3:])}</h2>")
        elif linea.startswith("- "):
            if parrafo:
                cerrar()
            lista.append(linea[2:])
        else:
            if lista:
                cerrar()
            parrafo.append(linea)
    cerrar()
    return titulo, "\n".join(partes)


def pagina(titulo: str, cuerpo: str, descripcion: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descripcion)}">
<style>{ESTILO}</style>
</head>
<body>
<main>
<header><a class="marca" href="/">Vialor</a></header>
{cuerpo}
<footer>Vialor · <a href="/privacidad/">Política de privacidad</a> · <a href="mailto:soporte@vialor.app">soporte@vialor.app</a></footer>
</main>
</body>
</html>
"""


def main():
    texto = ORIGEN.read_text(encoding="utf-8")
    publico = texto.split("\n---\n", 1)[1]
    titulo, cuerpo = a_html(publico)
    (AQUI / "privacidad").mkdir(exist_ok=True)
    (AQUI / "privacidad" / "index.html").write_text(
        pagina(titulo, cuerpo, "Qué información usa Vialor, dónde la guarda y quién puede verla."),
        encoding="utf-8", newline="\n")
    inicio = """<h1>Vialor</h1>
<p><strong>Tu ganancia por viaje.</strong> Vialor lee las ofertas de viaje que llegan a tu celular y te dice al instante
si te convienen: pesos por kilómetro y por hora, en una burbuja y en voz alta. Hecha por un conductor, para conductores y
repartidores.</p>
<p>Todo se procesa dentro de tu teléfono. Vialor nunca toca la pantalla ni acepta o rechaza viajes por ti.</p>
<p>Muy pronto en Google Play.</p>
<p>Contacto: <a href="mailto:soporte@vialor.app">soporte@vialor.app</a></p>
<p>Vialor es una app independiente y no está afiliada, patrocinada ni aprobada por Uber ni DiDi.</p>"""
    (AQUI / "index.html").write_text(
        pagina("Vialor: Tu ganancia por viaje", inicio, "Vialor te dice al instante si una oferta de viaje te conviene."),
        encoding="utf-8", newline="\n")
    (AQUI / "CNAME").write_text("vialor.app\n", encoding="utf-8", newline="\n")
    (AQUI / ".nojekyll").write_text("", encoding="utf-8")
    print("listo:", titulo)


if __name__ == "__main__":
    main()
