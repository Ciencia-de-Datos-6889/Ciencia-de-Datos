from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
USER = "root"
PASSWORD = ""
SERVER = "DESKTOP-A24L29P\\SQLEXPRESS"
DATABASE = "RuedaDeVida"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://@{SERVER}/{DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

if __name__ == "__main__":
    app.run(debug=True)
