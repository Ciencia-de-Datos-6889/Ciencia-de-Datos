from flask import Flask, render_template, request, redirect, url_for, make_response
from flask import Flask
from database import db
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# Configuración de la base de datos
USER = "root"
PASSWORD = ""
SERVER = "DESKTOP-A24L29P\\SQLEXPRESS"
DATABASE = "RuedaDeVida"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://@{SERVER}/{DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

# Modelo de la tabla
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    salud = db.Column(db.Integer, nullable=False)
    crecimiento_personal = db.Column(db.Integer, nullable=False)
    familia_amigos = db.Column(db.Integer, nullable=False)
    amor = db.Column(db.Integer, nullable=False)
    ocio = db.Column(db.Integer, nullable=False)
    trabajo = db.Column(db.Integer, nullable=False)
    dinero = db.Column(db.Integer, nullable=False)

# Crear la base de datos (ejecutar solo una vez)
with app.app_context():
    db.create_all()

# Ruta principal: Mostrar usuarios
@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template("index.html", usuarios=usuarios)

# Ruta para agregar usuario
@app.route("/agregar", methods=["POST"])
def agregar_usuario():
    nuevo_usuario = Usuario(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        edad=int(request.form["edad"]),
        salud=int(request.form["salud"]),
        crecimiento_personal=int(request.form["crecimiento_personal"]),
        familia_amigos=int(request.form["familia_amigos"]),
        amor=int(request.form["amor"]),
        ocio=int(request.form["ocio"]),
        trabajo=int(request.form["trabajo"]),
        dinero=int(request.form["dinero"])
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for("index"))

# Ruta para eliminar usuario
@app.route("/eliminar/<int:id>")
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for("index"))

# Ruta para mostrar formulario de edición
@app.route("/editar/<int:id>")
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    return render_template("editar.html", usuario=usuario)

# Ruta para actualizar usuario
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar_usuario(id):
    usuario = Usuario.query.get(id)
    usuario.nombre = request.form["nombre"]
    usuario.apellido = request.form["apellido"]
    usuario.edad = int(request.form["edad"])
    usuario.salud = int(request.form["salud"])
    usuario.crecimiento_personal = int(request.form["crecimiento_personal"])
    usuario.familia_amigos = int(request.form["familia_amigos"])
    usuario.amor = int(request.form["amor"])
    usuario.ocio = int(request.form["ocio"])
    usuario.trabajo = int(request.form["trabajo"])
    usuario.dinero = int(request.form["dinero"])

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/descargar_grafica")
def descargar_grafica():
    usuarios = Usuario.query.all()

    # Crear la gráfica
    nombres = [usuario.nombre for usuario in usuarios]
    dimensiones = ['salud', 'crecimiento_personal', 'familia_amigos', 'amor', 'ocio', 'trabajo', 'dinero']
    
    plt.figure(figsize=(10, 6))
    for dim in dimensiones:
        valores = [getattr(usuario, dim) for usuario in usuarios]
        plt.plot(nombres, valores, label=dim, marker='o')

    plt.title('Gráfica de la Rueda de la Vida')
    plt.xlabel('Usuarios')
    plt.ylabel('Puntuación')
    plt.legend()
    plt.grid(True)

    # Guardar la gráfica en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Crear PDF
    response = make_response()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=grafica_rueda_de_la_vida.pdf'

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []

    elements.append(Paragraph("Gráfica de la Rueda de la Vida", getSampleStyleSheet()['Title']))
    elements.append(Image(buffer, width=500, height=300))
    doc.build(elements)
    pdf_buffer.seek(0)

    response.data = pdf_buffer.getvalue()
    return response

@app.route("/descargar_pdf")
def descargar_pdf():
    usuarios = Usuario.query.all()

    response = make_response()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=usuarios.pdf'

    buffer = response.stream
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Lista de Usuarios", styles['Title']))

    data = [['ID', 'Nombre', 'Apellido', 'Edad', 'Salud', 'Crecimiento', 'Familia/Amigos', 'Amor', 'Ocio', 'Trabajo', 'Dinero']]
    for usuario in usuarios:
        data.append([
            usuario.id,
            usuario.nombre,
            usuario.apellido,
            usuario.edad,
            usuario.salud,
            usuario.crecimiento_personal,
            usuario.familia_amigos,
            usuario.amor,
            usuario.ocio,
            usuario.trabajo,
            usuario.dinero
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    return response

@app.route('/analisis')
def mostrar_analisis():
    from analytics import generar_analisis_completo
    resultados = generar_analisis_completo()
    return render_template('analisis_completo.html', datos=resultados)

if __name__ == "__main__":
    app.run(debug=True)