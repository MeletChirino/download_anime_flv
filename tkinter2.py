import Tkinter as tk
from PIL import ImageTk, Image
from download_client import *
'''

'''
class UI(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Aqui colocariamos los widgets."""
        self.parent.title("Descarga AnimeFLV")
        self.nombre = tk.Label(self.parent, text="Coloca el nombre del anime")

        self.boton = tk.Button(self.parent, text="Revisar link", command=self.print1)

        self.headless_var = tk.IntVar()
        self.headless = tk.Checkbutton(self.parent, text="Ver browser", variable=self.headless_var)

        self.link_bar = tk.Text(self.parent, width=50, height=2)

        self.sinopsis_title = tk.Label(self.parent, text="Sinopsis")
        self.sinopsis_text = tk.Text(self.parent, width=70, height=8)
        #self.sinopsis_text.pack(padx=10, pady=10)
        self.download_button = tk.Button(self.parent, text="Descargar anime", command=self.download)
        self.cover_label = tk.Label(self.parent)

        self.nombre.grid(row=1, columnspan=4)
        self.link_bar.grid(row=2, columnspan=4)
        self.headless.grid(row=3, column=0)
        self.sinopsis_title.grid(row=4, columnspan=4)
        self.sinopsis_text.grid(row=5, column=0, rowspan=4, columnspan=4)
        self.boton.grid(row=3,column=2)
        self.download_button.grid(row=3, column=3)
        self.cover_label.grid(row=1, rowspan=7, column=4, columnspan=2)

    def print1(self):
        texto = self.link_bar.get("1.0",'end-1c')
        self.boton.configure({'text':'Cargando'})
        self.animes = anime(texto, self.headless_var.get())
        #print texto
        self.nombre.configure({'text':self.animes.name})
        self.boton.configure({'text':'Listo'})
        path = mother_path + '/' + self.animes.name + '/cover.jpg'

        image = Image.open(path)
        MyImage = ImageTk.PhotoImage(image)
        self.cover_label.image = MyImage
        self.cover_label.configure(image=MyImage)
        self.sinopsis_text.insert('1.0',self.animes.sinopsis)

    def download(self):
        try:
            print 'Descargando...'
            self.boton.configure({'text':'Descargando...'})
            self.animes.download()
            self.boton.configure({'text':'Descargado'})
            self.animes.driver.quit()
        except Exception as er:
            print 'Error: '
            print er
            self.animes.driver.quit()

if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.geometry("850x400")
    APP = UI(parent=ROOT)
    APP.mainloop()
    ROOT.destroy()
