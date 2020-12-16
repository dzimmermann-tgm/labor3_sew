import requests
import sys
from PyQt5 import QtWidgets, QtCore, uic
import json
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import traceback

class Controller:
    def __init__(self, ui, model):
        
        """
        Konstruktor eines Controller-Objekts, zuweisung der Callbacks (analog zu listenern) für die
        entsprechenden Buttons. Übernimmt 
        ui und model wobei
        
        ui -- Subklasse eines QMainwWindow Objekts ist
        model -- funktionalitöt für get-requests an den lokalen Backendservice bereitstellt
        """
        
        
        self.ui = ui
        self.model = model

        self.ui.set_verify_callback(self.verify)
        self.ui.set_reset_callback(self.reset)
        self.ui.set_close_callback(self.close)

    def verify(self):
        
        """
        Verfiy methode. Versucht vom Backendservice die entsprechenden
        Kennwerte der übergebenen Sprache (anhand des texts) herauszufinden. 
        
        Gelingt dies nicht wird statt der Sprache eine Fehlermeldung ausgegeben.
        """
        
        s = ""
        try:
            t = self.ui.get_text().strip()
            
            if(len(t) < 1):
                s = "Bitte geben sie mehr Text ein"
            else:
                result = self.model.get_lang(t)
                for key in result:
                    s = s + key + ": " + str(result[key]) + "\n" 
            
            
        except:
            traceback.print_exc()
            s = "Something went wrong :( \n" 

        self.ui.set_text(s)

    def reset(self):
        
        """
        Stellt die gui auf den Ursprungszustand zurück
        """
        
        self.ui.clear_ui()

    def close(self):
        
        """
        Close Methode
        """
        self.ui.close_application()

class Model:
    def get_lang(self, text):
        
        """
        Schickt eine GET-Request den lokalen Backendservice und retuniert die Antwort.
        """
        
        uri = "http://127.0.0.1:5000/lg?text="+text
        result = requests.get(uri)
        return result.json()

class Ui(QMainWindow):
    def __init__(self):
        
        """
        Konstruktor für ein Ui-Objekt. 
        """
        super(Ui, self).__init__()
        self.setWindowTitle("Lang. detector")
        uic.loadUi("lang.ui",self)
        
        # -- Setzten der entsprechenden Methoden wenn ein Button geklickt wird -- 
        self.verify.clicked.connect(self.verify_clicked)
        self.reset.clicked.connect(self.reset_clicked)
        self.closebtn.clicked.connect(self.close_clicked)


    def set_verify_callback(self, fn):
        self.verify_callback = fn

    def verify_clicked(self):
        self.verify_callback()


    def set_reset_callback(self, fn):
        self.reset_callback = fn

    def reset_clicked(self):
        self.reset_callback()

    def set_close_callback(self, fn):
        self.close_callback = fn

    def close_clicked(self):
        self.close_callback()

    def get_text(self):
        return self.text_in.toPlainText()

    def set_text(self, text):
        self.text_out.setPlainText(text)

    def clear_ui(self):
        self.text_in.clear()
        self.text_out.clear()

    def close_application(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui()
    Controller(ui, Model())
    ui.show()


    app.exec_()