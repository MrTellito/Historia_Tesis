# Genera flujo_metodologico_v6.drawio: 2 filas x 3 fases, pensado para 16 cm de ancho.
# Lienzo de 605 px = 16 cm a 96 ppp; letra de 11 px = 8,25 pt.
import sys, textwrap
from xml.sax.saxutils import escape

OUT = sys.argv[1]
FS = 11          # letra del cuerpo (px)
LH = 14          # alto de línea
CH = 28          # caracteres por línea (estimado, ancho útil ~174 px)
X0, COLW, GAP = 12, 186, 10
COLX = [X0 + i * (COLW + GAP) for i in range(3)]
PAD = 7          # margen interno de la fase
BW = COLW - 2 * PAD

INK, MUTED, LINE = "#1F2937", "#4B5563", "#374151"
FILL, ACCENT, ACCENT_FILL = "#FFFFFF", "#6D28D9", "#F5F3FF"

cells = []
nid = [0]

def new_id(p):
    nid[0] += 1
    return f"{p}{nid[0]}"

def nlines(lines, chars=CH):
    return sum(max(1, len(textwrap.wrap(l, chars))) for l in lines)

def html(lines, bold_first=True):
    out = []
    for i, l in enumerate(lines):
        t = escape(l)
        out.append(f"<b>{t}</b>" if (i == 0 and bold_first) else t)
    return "<br>".join(out)

def vertex(id_, value, x, y, w, h, style):
    cells.append(f'<mxCell id="{id_}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def edge(id_, src, tgt, label="", style="", pts=None, exit_=None, entry=None):
    st = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endSize=5;strokeColor={LINE};strokeWidth=1;fontSize={FS};fontColor={INK};labelBackgroundColor=#FFFFFF;"
    if exit_:
        st += f"exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;"
    if entry:
        st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    st += style
    geo = '<mxGeometry relative="1" as="geometry">'
    if pts:
        geo += '<Array as="points">' + "".join(f'<mxPoint x="{a}" y="{b}"/>' for a, b in pts) + "</Array>"
    geo += "</mxGeometry>"
    cells.append(f'<mxCell id="{id_}" value="{escape(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">{geo}</mxCell>')

BOX = f"rounded=1;arcSize=6;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacingLeft=5;spacingRight=4;fontSize={FS};fontColor={INK};strokeColor={LINE};fillColor={FILL};strokeWidth=1;"
BOX_DASH = BOX + "dashed=1;fillColor=#F3F4F6;"
BOX_KEY = BOX + "strokeWidth=2;"
BOX_STJC = BOX.replace(f"strokeColor={LINE}", f"strokeColor={ACCENT}").replace(f"fillColor={FILL}", f"fillColor={ACCENT_FILL}") + "strokeWidth=2;"
DIAMOND = f"rhombus;whiteSpace=wrap;html=1;fontSize={FS};fontColor={INK};strokeColor={LINE};fillColor={FILL};spacing=2;"
LANE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#9CA3AF;dashed=1;dashPattern=4 3;"
HEAD = f"rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacingLeft=5;fontSize={FS};fontColor=#FFFFFF;fillColor={INK};strokeColor={INK};"
HEAD_STJC = HEAD.replace(f"fillColor={INK};strokeColor={INK}", f"fillColor={ACCENT};strokeColor={ACCENT}")

# ---------------- contenido ----------------
phases = [
    ("Fase 1 · Sección 3.1", "Adquisición de datos y construcción del panel diario", [
        ("box", ["Registro de Precios SCOP", "Osinergmin, público", "Mar. 2020 – set. 2026", "15 163 031 reportes"]),
        ("box", ["Seudonimización", "Código por establecimiento con clave secreta"]),
        ("box", ["Selección y limpieza", "5 combustibles, venta al público", "11 718 907 reportes", "24 771 establecimientos"]),
        ("box", ["Panel diario (Ec. 1)", "Arrastre del precio ≤ 60 días", "39,6 millones de filas"]),
        ("box", ["Análisis exploratorio (3.1.1)", "Rigidez, cambios por mes, región y tipo de local: orienta el diseño"]),
    ]),
    ("Fase 2 · Sección 3.2", "Variable objetivo y variables predictoras", [
        ("box", ["Variable objetivo (Ec. 2)", "¿Cambia el precio (sube o baja) en los próximos 5 días?"]),
        ("box", ["26 variables base", "Grupos de la Tabla 2: precio, historial de cambios, mercado, establecimiento y calendario"]),
        ("dia", ["¿Las 3 nuevas", "mejoran el AUC", "en 2025?", "(Wilcoxon)"]),
        ("key", ["29 variables", "Conjunto final del modelo"]),
    ]),
    ("Fase 3 · Sección 3.3", "Diseño de validación y control de la fuga de información", [
        ("box", ["Establecimientos nunca vistos", "30 % apartado al inicio; solo se evalúa en 2026"]),
        ("box", ["Origen móvil (12 meses de 2025)", "Entrena con 182 días previos y purga de 6 días (Ec. 3)"]),
        ("box", ["Desbalance de clases (3.3.2)", "8 tratamientos con la misma regla; corrección de probabilidades (Ec. 4)"]),
        ("box", ["Tamaño y controles (3.3.3)", "Curva de aprendizaje; prueba negativa; preparación sin información futura"]),
        ("dash", ["2026 reservado", "Prueba usada una sola vez (Fase 6)"]),
    ]),
    ("Fase 4 · Sección 3.4", "Modelos base y estrategias de ensamble", [
        ("box", ["4 modelos base", "CatBoost, LightGBM, XGBoost y Random Forest"]),
        ("box", ["39 ensambles en 10 familias", "Por establecimiento y temporal"]),
        ("dia", ["Regla previa:", "1) más métricas", "superadas;", "2) mejor posición", "media; 3) AUC"]),
        ("key", ["Ensamble elegido", "Votación suave (Ec. 5); pasa a 2026"]),
    ]),
    ("Fase 5 · Sección 3.5", "Método propuesto: Stacking Temporal Jerárquico con Contracción (STJC)", [
        ("stjc", ["STJC (Ec. 7)", "Aprende de 3 meses", "Pesos convexos (≥ 0, suman 1)", "Contracción hacia pesos iguales", "Pesos por combustible y bagging temporal, solo si ayudan", "Compite como uno de los 39 ensambles"]),
        ("box", ["Ablación pieza por pieza", "Se mide el aporte de cada parte"]),
    ]),
    ("Fase 6 · Sección 3.6", "Evaluación, prueba prospectiva e interpretabilidad", [
        ("box", ["Métricas (Tabla 3)", "AUC, p@k (Ec. 8) y Brier (Ec. 9)", "Wilcoxon mensual y bootstrap por bloques, con Holm"]),
        ("key", ["Prueba prospectiva 2026", "Ene.–set., reentreno trimestral", "Frente a reglas simples y modelo congelado; por combustible, nunca vistos y 3 o 7 días"]),
        ("box", ["Interpretabilidad", "SHAP por establecimiento"]),
        ("box", ["Sistema de apoyo y validación Delphi", "Lista diaria por región; juicio de expertos"]),
    ]),
]

def item_h(kind, lines):
    if kind == "dia":
        return max(90, nlines(lines, 20) * LH + 44)
    return nlines(lines) * LH + 10

def head_h(sub, title):
    return (1 + nlines([title], 30)) * LH + 8

VG = 16   # espacio vertical entre cajas (deja ver la flecha)
def lane_h(ph):
    sub, title, items = ph
    return head_h(sub, title) + PAD + sum(item_h(k, l) for k, l in items) + VG * (len(items) - 1) + PAD

Y0 = 8
ROW1_H = max(lane_h(p) for p in phases[:3])
ROW2_Y = Y0 + ROW1_H + 30
ROW2_H = max(lane_h(phases[3]), lane_h(phases[5]))

ids = {}
for pi, ph in enumerate(phases):
    sub, title, items = ph
    col = pi % 3
    x = COLX[col]
    y = Y0 if pi < 3 else ROW2_Y
    h = (ROW1_H if pi < 3 else ROW2_H) if pi != 4 else lane_h(ph)
    lid = f"lane{pi+1}"
    vertex(lid, "", x, y, COLW, h, LANE + ("strokeColor=%s;" % ACCENT if pi == 4 else ""))
    hh = head_h(sub, title)
    vertex(f"head{pi+1}", f"<b>{escape(sub)}</b><br>{escape(title)}", x, y, COLW, hh, HEAD_STJC if pi == 4 else HEAD)
    cy = y + hh + PAD
    prev = None
    for ii, (kind, lines) in enumerate(items):
        bh = item_h(kind, lines)
        bid = f"n{pi+1}_{ii+1}"
        if kind == "dia":
            val = "<br>".join(escape(l) for l in lines)
            st = DIAMOND
            vertex(bid, val, x + PAD, cy, BW, bh, st)
        else:
            st = {"box": BOX, "key": BOX_KEY, "dash": BOX_DASH, "stjc": BOX_STJC}[kind]
            vertex(bid, html(lines), x + PAD, cy, BW, bh, st)
        if prev and kind != "dash":
            lab = "Sí" if (prev.endswith("_3") and pi == 1) else ("Elegida" if (prev.endswith("_3") and pi == 3) else "")
            edge(new_id("e"), prev, bid, lab)
        if kind != "dash":
            prev = bid
        ids[(pi + 1, ii + 1)] = (bid, x + PAD, cy, BW, bh)
        cy += bh + VG

# ----- flechas entre fases -----
def mid_y(k): b = ids[k]; return b[2] + b[4] / 2

# F1 panel -> F2 objetivo
edge("x12", "n1_4", "n2_1", "", exit_=(1, 0.5), entry=(0, 0.5),
     pts=[(COLX[1] - GAP / 2, mid_y((1, 4))), (COLX[1] - GAP / 2, mid_y((2, 1)))])
# F2 29 variables -> F3 validación
edge("x23", "n2_4", "n3_2", "", exit_=(1, 0.5), entry=(0, 0.5),
     pts=[(COLX[2] - GAP / 2, mid_y((2, 4))), (COLX[2] - GAP / 2, mid_y((3, 2)))])
# F3 -> F4 (cruza entre filas)
yb = Y0 + ROW1_H + 15
edge("x34", "lane3", "head4", "", exit_=(0.5, 1), entry=(0.5, 0),
     pts=[(COLX[2] + COLW / 2, yb), (COLX[0] + COLW / 2, yb)])
# STJC -> 39 ensambles (candidato)
edge("x54", "n5_1", "n4_2", "", exit_=(0, 0.5), entry=(1, 0.5),
     style=f"strokeColor={ACCENT};fontColor={ACCENT};",
     pts=[(COLX[1] - GAP / 2, mid_y((5, 1))), (COLX[1] - GAP / 2, mid_y((4, 2)))])
# votación suave -> prueba 2026 (por debajo de la fase 5)
yv = mid_y((4, 4))
edge("x46", "n4_4", "n6_2", "", exit_=(1, 0.5), entry=(0, 0.5),
     pts=[(COLX[2] - GAP / 2, yv), (COLX[2] - GAP / 2, mid_y((6, 2)))])
# reentrenamiento trimestral -> Fase 1
ybot = ROW2_Y + ROW2_H + 14
vertex("loop_lbl", "Reentrenamiento trimestral con nuevos reportes del SCOP", COLX[0] + 40, ybot + 3, 330, 16, f"text;html=1;align=center;verticalAlign=middle;fontSize={FS};fontColor={INK};fillColor=#FFFFFF;")
edge("loop", "lane6", "lane1", "",
     exit_=(0.5, 1), entry=(0, 0.5),
     style="dashed=1;dashPattern=5 3;",
     pts=[(COLX[2] + COLW / 2, ybot), (4, ybot), (4, Y0 + ROW1_H / 2)])

W, H = 605, int(ybot + 24)
xml = ('<mxfile host="Electron"><diagram id="flujo_v6" name="Flujo metodológico v6">'
       f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open(OUT, "w", encoding="utf-8").write(xml)
print("ok", W, H, "fila1", ROW1_H, "fila2", ROW2_H, "f5", lane_h(phases[4]))
