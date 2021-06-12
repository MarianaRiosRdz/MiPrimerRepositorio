from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, send_from_directory
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db
from . models import User, Producto
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/img/<filename>')
def img(filename):
    ruta = os.path.join("C:\\Users\\LENOVO\Desktop\\Seguridad\\Examen\\project\\img")
    return send_from_directory(ruta, filename)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('/security/aboutus.html')


#Definimos la ruta a la página catalogo de productos
@main.route('/catalogoProductos')
def catalogoProductos():
    productos = db.session.query(Producto).all()
    if productos is not None:
        return render_template('catalogoProductos.html', productos=productos)
    return render_template('catalogoProductos.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
@roles_required('admin')#autorización para el rol admin
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/consultarProductos')
@login_required
@roles_required('admin')#autorización para el rol administrador
def consultarProductos():
    productos = db.session.query(Producto).all()
    print("GET_CONSULTAR")
    if productos is not None:
        return render_template('consultarProductos.html', productos=productos)
    return render_template('consultarProductos.html')

@main.route('/consultarProductos', methods=['POST'])
def consultarProductos_post():
    print("POST_CONSULTAR")
    idProducto = request.form['idProducto']
    print(idProducto)
    opcion = request.form['opcion_m']
    if (opcion == "Modificar"):
        response = make_response(redirect(url_for('main.modificar')))
        response.set_cookie('id',idProducto)
        return response
    else:
        response = make_response(redirect(url_for('main.eliminar')))
        response.set_cookie('id',idProducto)
        return response
    return render_template('consultarProductos.html')

@main.route('/productos')
def productos():
    return render_template('productos.html')

@main.route('/productos', methods=['POST'])
def productos_post():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    descripcion = request.form.get('descripcion')
    stock = request.form.get('stock')
    
    foto = request.files['foto']            
        
    # if user does not select file, browser also
    # submit a empty part without filename
    if foto.filename == '':
        print("no se eligio nada")
        return redirect(request.url)

    if foto and allowed_file(foto.filename):
        filename = secure_filename(foto.filename)

        # Ruta absoluta 
        foto.save(os.path.join("C:\\Users\\LENOVO\Desktop\\Seguridad\\Examen\\project\\img", filename))
    
    prod = Producto( nombre=nombre, precio=precio, descripcion=descripcion,
                    stock=stock, foto=filename)
    db.session.add(prod)
    db.session.commit()

    print("POST_REGISTRAR")

    #productos = db.session.query(Producto).all()

    return redirect(url_for('main.consultarProductos'))

@main.route('/modificar')
def modificar():
    print("GET_MODIFICAR")
    id = request.cookies.get('id')
    prod = Producto.query.get(id)
    print(id, prod)
    print(prod.nombre, prod.precio, prod.descripcion, prod.stock, prod.foto)
    #print(datos)
    return render_template('modificar.html', datos=prod)

@main.route('/modificar', methods=['POST'])
def modificar_post():
    print("POST_MODIFICAR")
    id = request.cookies.get('id')
    print(id)

    prod= Producto.query.get(id)
    produc= db.session.query(Producto).filter(Producto.id == id).first()
    print(prod.descripcion)

    produc.nombre = request.form.get('nombre')
    produc.precio = request.form.get('precio')
    produc.descripcion = request.form.get('descripcion')
    produc.stock = request.form.get('stock')

    foto = request.files['foto']            
    
    # if user does not select file, browser also
    # submit a empty part without filename
    if foto.filename == '':
        print("no se eligio nada")
        

    if foto and allowed_file(foto.filename):
        filename = secure_filename(foto.filename)

        # Ruta absoluta 
        foto.save(os.path.join("C:\\Users\\LENOVO\Desktop\\Seguridad\\Examen\\project\\img", filename))
        produc.foto = filename

    db.session.add(produc)
    db.session.commit()

    return redirect(url_for('main.consultarProductos'))

@main.route('/eliminar')
def eliminar():
    print("GET_ELIMINAR")
    id = request.cookies.get('id')
    prod = Producto.query.get(id)
    print(id, prod)
    print(prod.nombre, prod.precio, prod.descripcion, prod.stock, prod.foto)
    return render_template('eliminar.html', datos=prod)

@main.route('/eliminar', methods=['POST'])
def eliminar_post():
    print("POST_ELIMINAR")
    id = request.cookies.get('id')
    prod = Producto.query.get(id)
    print(id, prod)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('main.consultarProductos'))


