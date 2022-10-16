import sqlite3

def ver_enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreusuario from usuarios u, mensajeria m where u.correo=m.destino and m.origen='"+correo+"' order by fecha desc,hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def ver_recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreusuario from usuarios u, mensajeria m where u.correo=m.origen and m.destino='"+correo+"' order by fecha desc,hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def comprobarusuario(correo,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select  *from usuarios where correo='"+correo+"' and password='"+password+"'and estado='1' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def listausuarios(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select  *from usuarios where estado='1' and correo<>'"+correo+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def actualizapass(password,correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set password='"+password+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"

def registrar_mail(origen, destino, asunto, mensaje):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,origen,destino,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def registrarUsuario(nombre,correo,password,codigo):

    try:
        db=sqlite3.connect("mensajes.s3db")
        db.row_factory=sqlite3.Row
        cursor=db.cursor()
        consulta="insert into usuarios (nombreusuario,correo,password,estado,codigoactivacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
        cursor.execute(consulta)
        db.commit()
        return "Usuario Registrado Satisfactoriamente"
    except:
        return "ERROR! No es posible regustrar al usuario debido a que el CORREO y/o NOMBRE DE USUARIO ya existen. Lo invitamos a cambiar los campos pertinentes."


    

def activarUsuario(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()
    
    consulta2="select  *from usuarios where codigoactivacion='"+codigo+"' and estado='1'"
    cursor.execute(consulta2)
    resultado=cursor.fetchall()
    return resultado

