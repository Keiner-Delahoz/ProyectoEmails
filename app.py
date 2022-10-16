import email
from flask import Flask, render_template, request
import hashlib
import controlador
import random
import envioemail

app = Flask(__name__)

email_origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verificarUsuario",methods=["GET","POST"])
def verificarUsuario():
        correo=request.form["txtusuario"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        password=request.form["txtpass"]
        password=password.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        password2=password.encode()
        password2=hashlib.sha384(password2).hexdigest()
        
        respuesta=controlador.comprobarusuario(correo,password2)

        global email_origen

        if len(respuesta)==0:
            email_origen=""
            mensaje="Error de Autenticacion, por favor verifica tu usuario y contraseña"
            return render_template("informacion.html",data=mensaje)
        else:
            email_origen=correo
            respuesta2=controlador.listausuarios(correo)
            return render_template("principal.html",data=respuesta2,infoUsuario=respuesta)
        
@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email=request.form["txtusuarioregistro"]
        email=email.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        password=request.form["txtpassregistro"]
        password=password.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        password2=password.encode()
        password2=hashlib.sha384(password2).hexdigest()

        codigo=random.randint(100000,999999)
        codigo2=str(codigo)
        
        respuesta=controlador.registrarUsuario(nombre,email,password2,codigo2)

        asunto="Codigo de Activacion"
        mensaje="Hola "+nombre+".\n\nSu codigo de activacion es: \n\n"+codigo2+"\n\nRecuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta. \n\nMuchas Gracias"
        envioemail.enviar(email,asunto,mensaje)
        
        
        
        #mensaje="El Usuario "+nombre+", se ha registrado satisfactoriamente."
        return render_template("informacion.html",data=respuesta)


@app.route("/enviarMAIL",methods=["GET","POST"])
def enviarMAIL():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        emailDestino=emailDestino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")

        controlador.registrar_mail(email_origen,emailDestino,asunto,mensaje)

        mensaje2="Sr Usuario, usted recibio un mensaje nuevo, por favor ingrese a la plataforma para observar su email, en la pestaña historial. \n\n Muchas gracias. "
        envioemail.enviar(emailDestino,"Nuevo Mensaje Enviado",mensaje2)
        return"Email Enviado Satisfactoriamente"

@app.route("/activarUsuario",methods=["GET","POST"])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        
        respuesta=controlador.activarUsuario(codigo)
        
        if len(respuesta)==0:
            mensaje="El codigo de activación es erroneo, verifiquelo."
        else:
            mensaje="El usuario se ha activado exitosamente."
        return render_template("informacion.html",data=mensaje)


@app.route("/HistorialEnviados",methods=["GET","POST"])
def HistorialEnviados():
    
        resultado=controlador.ver_enviados(email_origen)

        return render_template("respuesta.html",data=resultado)


@app.route("/HistorialRecibidos",methods=["GET","POST"])
def HistorialRecibidos():
    
        resultado=controlador.ver_recibidos(email_origen)

        return render_template("respuesta.html",data=resultado)

@app.route("/actualizacionPassword",methods=["GET","POST"])
def actualizacionPassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        pass1=pass1.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        password2=pass1.encode()
        password2=hashlib.sha384(password2).hexdigest()
        controlador.actualizapass(password2,email_origen)
        
        return "Actualizacion de Contraseña Existosa"


        
    