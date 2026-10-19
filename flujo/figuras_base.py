# -*- coding: utf-8 -*-
"""Utilidades comunes para dibujar las figuras en draw.io (605 px = 16 cm; letra 11 px ≈ 8 pt)."""
import os
import textwrap

AQUI = os.path.dirname(os.path.abspath(__file__))
FS, LH = 11, 14
W, X0, FULLW = 605, 12, 581
INK, GRIS, GRIS_F = "#000000", "#6B7280", "#F2F2F2"


class Lienzo:
    def __init__(self):
        self.cells, self.n, self.y = [], 0, 8

    def _id(self, p):
        self.n += 1
        return f"{p}{self.n}"

    @staticmethod
    def alto(lineas, chars):
        return sum(max(1, len(textwrap.wrap(l, chars))) for l in lineas) * LH + 10

    @staticmethod
    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def html(self, lineas, titulo=True):
        out = []
        for i, l in enumerate(lineas):
            t = self.esc(l)
            out.append(f"<b>{t}</b>" if (i == 0 and titulo) else t)
        return "<br>".join(out)

    def vertex(self, value, x, y, w, h, style):
        i = self._id("v")
        v = value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        self.cells.append(f'<mxCell id="{i}" value="{v}" style="{style}" vertex="1" parent="1">'
                          f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        return i

    def edge(self, a, b, exit_=(1, 0.5), entry=(0, 0.5), pts=None, extra=""):
        st = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endSize=5;strokeColor={INK};"
              f"exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;" + extra)
        geo = '<mxGeometry relative="1" as="geometry">'
        if pts:
            geo += '<Array as="points">' + "".join(f'<mxPoint x="{p:.1f}" y="{q:.1f}"/>' for p, q in pts) + "</Array>"
        self.cells.append(f'<mxCell id="{self._id("e")}" value="" style="{st}" edge="1" parent="1" source="{a}" target="{b}">{geo}</mxGeometry></mxCell>')

    def caja(self, lineas, x, y, w, h=None, grosor=1, relleno="#FFFFFF", centrado=False, punteado=False, titulo=True):
        h = h or self.alto(lineas, max(8, int((w - 12) / 6.1)))
        st = (f"rounded=0;whiteSpace=wrap;html=1;align={'center' if centrado else 'left'};verticalAlign=middle;"
              f"spacingLeft=6;spacingRight=4;fontSize={FS};fontColor={INK};strokeColor={INK};fillColor={relleno};"
              f"strokeWidth={grosor};" + ("dashed=1;" if punteado else ""))
        return self.vertex(self.html(lineas, titulo), x, y, w, h, st), h

    def texto(self, t, y=None, x=X0, w=FULLW, negrita=False, gris=False, chars=96):
        y = self.y if y is None else y
        h = self.alto([t], chars) - 6
        st = (f"text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize={FS};spacingLeft=0;"
              f"fontColor={GRIS if gris else INK};" + ("fontStyle=1;" if negrita else ""))
        self.vertex(self.esc(t), x, y, w, h, st)
        return h

    def banda(self, t):
        self.y += 4
        st = (f"text;html=1;align=left;verticalAlign=bottom;fontSize={FS + 1};fontStyle=1;fontColor={INK};"
              f"spacingLeft=0;strokeColor=none;")
        self.vertex(self.esc(t), X0, self.y, FULLW, 18, st)
        # línea bajo el título de la banda
        self.vertex("", X0, self.y + 19, FULLW, 1, f"rounded=0;html=1;fillColor={INK};strokeColor=none;")
        self.y += 28

    def fila(self, cajas, gap=22, flechas=True, grosores=None):
        n = len(cajas)
        w = (FULLW - gap * (n - 1)) / n
        h = max(self.alto(c, max(8, int((w - 12) / 6.1))) for c in cajas)
        ids = []
        for k, c in enumerate(cajas):
            g = (grosores or [1] * n)[k]
            i, _ = self.caja(c, X0 + k * (w + gap), self.y, w, h, grosor=g)
            ids.append(i)
        if flechas:
            for a, b in zip(ids, ids[1:]):
                self.edge(a, b)
        self.y += h
        return ids, h

    def tabla(self, filas, anchos, resaltar=(), tenue=(), centrar_desde=1):
        x0 = X0
        for r, fila in enumerate(filas):
            hs = [self.alto([str(v)], max(6, int((a - 10) / 6.1))) - 4 for v, a in zip(fila, anchos)]
            h = max(18, max(hs))
            x = x0
            for c, (v, a) in enumerate(zip(fila, anchos)):
                cab = r == 0
                st = (f"rounded=0;whiteSpace=wrap;html=1;fontSize={FS};spacingLeft=5;spacingRight=3;verticalAlign=middle;"
                      f"align={'left' if c < centrar_desde else 'center'};strokeColor={INK};strokeWidth=0.6;"
                      f"fillColor={GRIS_F if cab else '#FFFFFF'};fontColor={GRIS if r in tenue else INK};"
                      + ("fontStyle=1;" if (cab or r in resaltar) else ""))
                self.vertex(self.esc(str(v)), x, self.y, a, h, st)
                x += a
            self.y += h

    def guardar(self, nombre, titulo):
        H = int(self.y + 10)
        xml = (f'<mxfile host="Electron"><diagram id="{nombre}" name="{titulo}">'
               f'<mxGraphModel dx="{W}" dy="{H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
               f'fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>'
               '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(self.cells) + "</root></mxGraphModel></diagram></mxfile>")
        ruta = os.path.join(AQUI, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(xml)
        print("ok", ruta, W, H)


