"""Genera solo el Draw.io teórico del balanceo, en blanco y negro.
--preview RUTA crea una vista temporal para revisar la maquetación.
No modifica el notebook ni ejecuta entrenamientos.
"""
from pathlib import Path
import argparse
import math
import xml.etree.ElementTree as ET
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'prueba7.1' / 'salidas_v6'
WIDTH, HEIGHT = 1900, 2320
shapes, texts, edges, bounds = [], [], [], {}


def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if bold else 'arial.ttf'), size)


def text(value, x, y, width, size=24, bold=False, parent=None):
    f, lh = font(size, bold), math.ceil(size * 1.30)
    lines = []
    for paragraph in value.split('\n'):
        current = ''
        for word in paragraph.split():
            candidate = (current + ' ' + word).strip()
            if current and f.getlength(candidate) > width:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    for i, line in enumerate(lines):
        assert f.getlength(line) <= width + 1, line
        texts.append(dict(value=line,x=x,y=y+i*lh,w=width,h=lh,size=size,bold=bold,parent=parent))
    return y + len(lines)*lh


def box(key, x, y, w, h, parts, rounded=False, pad=24):
    bounds[key] = (x,y,w,h)
    shapes.append(dict(key=key,x=x,y=y,w=w,h=h,rounded=rounded))
    start = len(texts)
    for shrink in range(4):
        del texts[start:]
        yy = y+pad
        for value,size,bold in parts:
            yy = text(value,x+pad,yy,w-2*pad,max(21,size-shrink),bold,parent=key)+10
        if yy-10 <= y+h-pad:
            return
    raise ValueError(f'Texto fuera de la caja {key}: {yy-10} > {y+h-pad}')


def arrow(source,target,via=None):
    a,b=bounds[source],bounds[target]
    edges.append(dict(source=source,target=target,points=[(a[0]+a[2]/2,a[1]+a[3])]+(via or [])+[(b[0]+b[2]/2,b[1])]))


def graphic(key,x,y,w,h,kind='rect',fill='none',thick=2):
    bounds[key]=(x,y,w,h)
    shapes.append(dict(key=key,x=x,y=y,w=w,h=h,rounded=False,kind=kind,fill=fill,thick=thick))


def line(points,head=False,thick=2):
    edges.append(dict(source=None,target=None,points=points,head=head,thick=thick))


def row(key,x,y,label='X | 1',w=80):
    graphic(key,x,y,w,34,fill='#FFFFFF')
    text(label,x+8,y+3,w-16,19,True,parent=key)


def first_rank(filename):
    means=pd.read_csv(DATA/filename).groupby('metodo')[['AUC','p@100','p@250','brier']].mean()
    ranks=means[['AUC','p@100','p@250']].rank(ascending=False)
    ranks['brier']=means.brier.rank()
    result=ranks.mean(axis=1)
    assert result.idxmin()=='ninguno'
    return f"{result['ninguno']:.2f}".replace('.',',')


rank8=first_rank('balanceo_lightgbm.csv')
rank4=first_rank('balanceo_cuatro_modelos.csv')
text('¿Por qué mi tesis puede entrenar sin balanceo?',56,28,1688,40,True)
text('Porque su objetivo es ordenar los casos con mayor probabilidad de cambio, y la validación respalda esa elección.',56,86,1688,25)

# 1: datos -> aprendizaje -> selección, con objetos gráficos editables.
text('1   DEL DESBALANCE OBSERVADO A UNA LISTA DE PRIORIDADES',56,148,1688,29,True)
graphic('data_panel',56,206,450,400)
text('DATOS: X + RESPUESTA Y',78,226,406,25,True,parent='data_panel')
for i in range(100):
    graphic(f'dot{i}',82+(i%10)*23,285+(i//10)*23,13,13,'ellipse','#000000' if i<13 else '#FFFFFF')
text('13',337,290,140,44,True,parent='data_panel')
text('cambian',337,348,140,23,parent='data_panel')
text('87',337,396,140,44,True,parent='data_panel')
text('no cambian',337,454,140,22,parent='data_panel')
text('Cada punto representa una fila.',78,523,406,20,parent='data_panel')
text('X: precio, historial, mercado…\nY: cambió (1) o no cambió (0).',78,553,406,20,parent='data_panel')

graphic('model',650,272,400,240)
text('EL MODELO APRENDE',674,292,352,25,True,parent='model')
text('Relaciona X con Y',714,333,302,23,parent='model')
# Árbol esquemático, sin representar un algoritmo particular.
line([(850,386),(850,408),(757,408),(757,438)])
line([(850,408),(943,408),(943,438)])
line([(757,450),(757,469),(716,469),(716,487)])
line([(757,469),(798,469),(798,487)])
for i,(x,y) in enumerate([(838,374),(745,426),(931,426),(704,475),(786,475)]):
    graphic(f'tree{i}',x,y,24,24,'ellipse','#FFFFFF')
text('p = probabilidad de cambiar\nen los próximos 5 días',650,538,400,23)
line([(506,390),(650,390)],True,3)
text('entrenar',527,351,112,20,True)
line([(1050,390),(1190,390)],True,3)
text('ordenar',1071,351,112,20,True)

graphic('rank_panel',1190,206,554,400)
text('ELEGIR SEGÚN LA CAPACIDAD',1212,226,510,25,True,parent='rank_panel')
text('Ejemplo: 6 casos, solo 3 cupos',1212,264,510,22,parent='rank_panel')
graphic('top3',1208,306,514,144,thick=3)
for i,(name,prob) in enumerate(zip('ABCDEF',[.80,.60,.40,.25,.10,.05])):
    y=321+i*43
    text(f'{i+1}.  {name}',1224,y,84,23,i<3,parent='rank_panel')
    graphic(f'prob{i}',1330,y+6,250*prob,19,fill='#000000' if i<3 else '#FFFFFF')
    text(f'{prob:.0%}',1610,y,86,23,i<3,parent='rank_panel')
text('Se seleccionan A, B y C.',1212,578,510,20,True,parent='rank_panel')
text('EDA 2025: ≈13,1 % de positivos. El esquema de puntos redondea a 13 %. Las probabilidades A–F son ilustrativas; en la tesis se usa K = 100.',56,624,1688,20)

# 2: demostración intuitiva del objetivo, con dos selecciones del mismo tamaño.
text('2   CON LOS MISMOS CUPOS, CONVIENE ELEGIR LAS PROBABILIDADES MÁS ALTAS',56,690,1688,28,True)
graphic('best',56,746,800,164,thick=3)
graphic('other',944,746,800,164)
text('A + B + C   ·   Los 3 primeros',82,764,748,26,True,parent='best')
text('0,80 + 0,60 + 0,40 = 1,80',82,812,748,34,True,parent='best')
text('aciertos esperados en 3 casos',82,864,748,23,parent='best')
text('A + B + F   ·   Se omite al tercero',970,764,748,26,True,parent='other')
text('0,80 + 0,60 + 0,05 = 1,45',970,812,748,34,True,parent='other')
text('aciertos esperados en los mismos 3 casos',970,864,748,23,parent='other')
line([(944,829),(856,829)],True,3)
text('El caso C entra aunque su probabilidad sea 40 %: importa su puesto, no superar un umbral fijo de 50 %.',56,930,1688,24,True)
text('Regla teórica: aciertos esperados = suma de las probabilidades seleccionadas. Supuesto: igual costo y valor por caso.',56,968,1688,22)
text('Aprender ese orden no exige que el entrenamiento tenga 50 % de cada clase.',56,1004,1688,27,True)

# 3: cada intervención se dibuja sobre filas completas, no sobre etiquetas aisladas.
text('3   ENTONCES, ¿QUÉ CAMBIA CUANDO SE BALANCEA?',56,1070,1688,29,True)
cards=[('sub',56,'ELIMINAR FILAS','Submuestreo'),('over',486,'REPETIR FILAS','Sobremuestreo aleatorio'),
       ('syn',916,'GENERAR FILAS','SMOTENC / ADASYN'),('weight',1346,'CAMBIAR PESOS','Ponderación de clases')]
for key,x,title,subtitle in cards:
    graphic(key,x,1124,398,264)
    text(title,x+20,1140,358,24,True,parent=key)
    text(subtitle,x+20,1176,358,21,parent=key)
for i in range(3):row(f'neg{i}',90,1218+i*37,'X | 0')
line([(197,1272),(284,1272)],True)
row('retained',314,1255,'X | 0')
text('Se conservan menos negativos.',76,1347,358,20,parent='sub')
row('positive',514,1255,'X | 1')
line([(610,1272),(670,1272)],True)
for i in range(3):row(f'copy{i}',716,1218+i*37,'X | 1')
text('Se duplican positivos existentes.',506,1347,358,20,parent='over')
row('parent1',944,1230,'X1 | 1',90)
row('parent2',944,1283,'X2 | 1',90)
line([(1034,1247),(1074,1247),(1074,1272),(1152,1272)],True)
line([(1034,1300),(1074,1300),(1074,1272)])
row('synthetic',1174,1255,'X* | 1',105)
text('Se interpolan variables de positivos.',936,1347,358,20,parent='syn')
row('w0',1374,1230,'X | 0')
row('w1',1374,1283,'X | 1')
line([(1470,1247),(1536,1247)],True)
line([(1470,1300),(1536,1300)],True)
text('peso × 1',1550,1233,166,22,True,parent='weight')
text('peso × 6,7',1550,1286,166,22,True,parent='weight')
text('Ejemplo relativo con 13 % positivos.',1366,1347,358,20,parent='weight')
text('Cada ficha representa una fila completa (X, Y). No se cambia una respuesta real de 0 a 1 ni se iguala cada variable predictora.',56,1406,1688,21)

# 4: selección empírica después del fundamento, sin atribuir causalidad no medida.
text('4   ¿AYUDA A MI OBJETIVO? SE COMPRUEBA CON DATOS FUTUROS',56,1472,1688,29,True)
for key,x in [('options',56),('months',650),('result',1244)]:graphic(key,x,1526,500,224)
text('8 OPCIONES',80,1542,452,25,True,parent='options')
for i in range(8):
    xx,yy=84+(i%4)*109,1594+(i//4)*48
    graphic(f'option{i}',xx,yy,88,34,thick=3 if i==0 else 1)
    text('sin bal.' if i==0 else str(i),xx+9,yy+4,70,19,i==0,parent=f'option{i}')
text('Sin balanceo + 7 técnicas',80,1704,452,23,parent='options')
line([(556,1640),(650,1640)],True,3)
text('12 MESES DE 2025',674,1542,452,25,True,parent='months')
for i in range(12):
    xx,yy=678+(i%6)*72,1594+(i//6)*48
    graphic(f'month{i}',xx,yy,57,34)
    text(str(i+1),xx+16,yy+4,38,19,parent=f'month{i}')
text('Evaluación sin balancear',674,1704,452,23,parent='months')
line([(1150,1640),(1244,1640)],True,3)
text('MEJOR CRITERIO AGREGADO',1268,1542,452,24,True,parent='result')
graphic('medal',1276,1600,66,66,'ellipse')
text('1',1296,1610,35,34,True,parent='medal')
text('SIN BALANCEO',1364,1607,350,28,True,parent='result')
text(f'Posición media: {rank8} (1.º de 8).\nConfirmación: {rank4} (1.º de 4).',1268,1680,452,22,parent='result')
text('Primera etapa con LightGBM; cuatro finalistas se confirman con los cuatro modelos. Criterio: AUC, precisión@100, precisión@250 y Brier.',56,1772,1688,21)

# Conclusión visible: fundamento + evidencia -> decisión.
graphic('theory_end',56,1862,500,132)
graphic('evidence_end',650,1862,500,132)
graphic('choice_end',1244,1862,500,132,thick=3)
text('LA TEORÍA PERMITE',78,1878,456,24,True,parent='theory_end')
text('Ordenar probabilidades sin\nexigir clases 50/50.',78,1918,456,25,parent='theory_end')
text('LA VALIDACIÓN RESPALDA',672,1878,456,24,True,parent='evidence_end')
text('La mejor opción agregada\nfue «sin balanceo».',672,1918,456,25,parent='evidence_end')
text('DECISIÓN DE ESTA TESIS',1266,1878,456,24,True,parent='choice_end')
text('Entrenar conservando\nla distribución original.',1266,1918,456,25,True,parent='choice_end')
line([(556,1928),(650,1928)],True,3)
line([(1150,1928),(1244,1928)],True,3)
line([(1494,1750),(1780,1750),(1780,1828),(1494,1828),(1494,1862)],True)

text('¿Por qué otras tesis sí balancean?',56,2030,780,25,True)
text('Puede ayudar cuando mejora su objetivo o la detección de la clase minoritaria. Su utilidad se valida; no es una obligación universal.',56,2070,780,22)
text('¿Qué revisar aunque no se balancee?',944,2030,800,25,True)
text('Los positivos por periodo y combustible. Muchas filas relacionadas no equivalen a muchos eventos independientes.',944,2070,800,22)
text('Fundamento: maximización del número esperado de aciertos con capacidad fija. Evidencia: notebook, secciones 11.1–11.2; CSV de balanceo.',56,2180,1688,18)


def export_drawio():
    mx=ET.Element('mxfile',host='app.diagrams.net',type='device')
    diagram=ET.SubElement(mx,'diagram',id='balanceo_teorico',name='Balanceo — página única')
    graph=ET.SubElement(diagram,'mxGraphModel',grid='1',gridSize='10',guides='1',tooltips='1',connect='1',arrows='1',fold='1',page='1',pageScale='1',pageWidth=str(WIDTH),pageHeight=str(HEIGHT),math='0',shadow='0',background='#FFFFFF')
    root=ET.SubElement(graph,'root')
    ET.SubElement(root,'mxCell',id='0')
    ET.SubElement(root,'mxCell',id='1',parent='0')
    for i,e in enumerate(edges):
        attrs=dict(id=f'e{i}',edge='1',parent='1')
        if e['source'] is not None:
            attrs.update(source=e['source'],target=e['target'])
        attrs['style']=f"rounded=0;html=0;endArrow={'block' if e.get('head',True) else 'none'};endFill=1;strokeColor=#000000;strokeWidth={e.get('thick',2)};"
        cell=ET.SubElement(root,'mxCell',**attrs)
        geo=ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if e['source'] is None:
            for key,point in [('sourcePoint',e['points'][0]),('targetPoint',e['points'][-1])]:
                ET.SubElement(geo,'mxPoint',x=str(point[0]),y=str(point[1]),attrib={'as':key})
        if len(e['points'])>2:
            arr=ET.SubElement(geo,'Array',attrib={'as':'points'})
            for x,y in e['points'][1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    for s in shapes:
        kind='ellipse;' if s.get('kind')=='ellipse' else ''
        cell=ET.SubElement(root,'mxCell',id=s['key'],vertex='1',parent='1',style=f"{kind}rounded={int(s['rounded'])};arcSize=12;whiteSpace=wrap;html=0;fillColor={s.get('fill','none')};strokeColor=#000000;strokeWidth={s.get('thick',2)};fontColor=#000000;")
        ET.SubElement(cell,'mxGeometry',x=str(s['x']),y=str(s['y']),width=str(s['w']),height=str(s['h']),attrib={'as':'geometry'})
    for i,t in enumerate(texts):
        parent=t['parent'] or '1'
        px,py=bounds[parent][:2] if parent!='1' else (0,0)
        cell=ET.SubElement(root,'mxCell',id=f't{i}',vertex='1',parent=parent,value=t['value'],style=f"text;html=0;whiteSpace=wrap;overflow=hidden;align=left;verticalAlign=middle;spacing=0;fontFamily=Arial;fontSize={t['size']};fontStyle={int(t['bold'])};fontColor=#000000;strokeColor=none;fillColor=none;")
        ET.SubElement(cell,'mxGeometry',x=str(t['x']-px),y=str(t['y']-py),width=str(t['w']),height=str(t['h']),attrib={'as':'geometry'})
    ET.indent(mx,space='  ')
    path=HERE/'balanceo_por_que_no.drawio'
    ET.ElementTree(mx).write(path,encoding='utf-8',xml_declaration=True)
    return path


def preview(path):
    im=Image.new('RGB',(WIDTH*2,HEIGHT*2),'white')
    draw=ImageDraw.Draw(im)
    for e in edges:
        points=e['points']
        draw.line([(2*x,2*y) for x,y in points],fill='black',width=2*e.get('thick',2))
        if e.get('head',True):
            a,b=points[-2:];angle=math.atan2(b[1]-a[1],b[0]-a[0])
            tri=[b,(b[0]-13*math.cos(angle)+5*math.sin(angle),b[1]-13*math.sin(angle)-5*math.cos(angle)),(b[0]-13*math.cos(angle)-5*math.sin(angle),b[1]-13*math.sin(angle)+5*math.cos(angle))]
            draw.polygon([(2*x,2*y) for x,y in tri],fill='black')
    for s in shapes:
        x,y,w,h=s['x'],s['y'],s['w'],s['h']
        fill=None if s.get('fill','none')=='none' else s['fill']
        xy=(2*x,2*y,2*(x+w),2*(y+h))
        if s.get('kind')=='ellipse':
            draw.ellipse(xy,fill=fill,outline='black',width=2*s.get('thick',2))
        else:
            draw.rounded_rectangle(xy,radius=24 if s['rounded'] else 0,fill=fill,outline='black',width=2*s.get('thick',2))
    for t in texts:
        draw.text((t['x']*2,(t['y']+t['h']/2)*2),t['value'],font=font(t['size']*2,t['bold']),fill='black',anchor='lm')
    im.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS).save(path)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',type=Path)
    args=parser.parse_args()
    out=export_drawio()
    if args.preview:preview(args.preview)
    print(f'Draw.io: {out.name}; 1 pagina; {len(shapes)} cajas; {len(edges)} flechas; blanco y negro.')
