from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter as Tk
import os
import os.path

class CreateToolTip(object):
  '''
  create a tooltip for a given widget
  '''
  def __init__(self, widget, text='widget info'):
    self.widget = widget
    self.text = text
    self.widget.bind("<Enter>", self.enter)
    self.widget.bind("<Leave>", self.close)
  def enter(self, event=None):
    x = y = 0
    x, y, cx, cy = self.widget.bbox("insert")
    x += self.widget.winfo_rootx() + 25
    y += self.widget.winfo_rooty() + 20
    self.tw = Tk.Toplevel(self.widget)
    self.tw.wm_overrideredirect(True)
    self.tw.wm_geometry("+%d+%d" % (x, y))
    label = Tk.Label(self.tw, text=self.text, justify='left',
                    background='white', relief='solid', borderwidth=1,
                    font=("times", "14", "normal"))
    label.pack(ipadx=1)
  def close(self, event=None):
    if self.tw:
      self.tw.destroy()

fenetre = Tk.Tk()
fenetre.geometry("1215x500")
fenetre.title('listbox choix gx')
fileDir = os.getcwd()
searchTerm = StringVar()
maListe = []
lines = []
c = Canvas(fenetre, width=100, height=100, bg="white")
c.grid(row=0, column=0, sticky="news")
x = 0
""" Raccourci clavier """
fenetre.bind('<Control-s>', lambda a:save())
fenetre.bind('<Control-o>', lambda a:searchFile())
fenetre.bind('<Control-plus>', lambda a:addQspi())
fenetre.bind('<Control-minus>', lambda a:removeQspi())
fenetre.bind('<Control-a>', lambda a:selectAll())
fenetre.bind('<Control-e>', lambda a:selectAllQspi())
fenetre.bind('<Control-q>', lambda a:quit())

""" Tableau sans QSPI """
Tableurarticleprojet = Frame(c , width=410, height=300, bd=8, relief="raise", bg="black")
Tableurarticleprojet.grid(column = 0, row = 3, pady=5, padx=5)
Tableurarticleprojet.grid_propagate(0)
tree = ttk.Treeview(Tableurarticleprojet, columns=("column1"), show='headings', height=12)
scrollbarx = Scrollbar(Tableurarticleprojet, orient='horizontal',command=tree.xview)
scrollbary = Scrollbar(Tableurarticleprojet, orient='vertical',command=tree.yview)
scrollbarx.grid(column = 0, row = 1, sticky='we')
scrollbary.grid(column = 1, row = 0, sticky='ns')
tree['xscrollcommand'] = scrollbarx.set
tree['yscrollcommand'] = scrollbary.set
tree.heading("#1", text="SANS QSPI")
tree.column('#1', stretch=NO, minwidth=0, width=380)
tree.grid(row=0, column=0)  
for line in lines:
  if str(line[4]).startswith('='):
    tree.insert("", END, values=line[3])

""" Tableau QSPI """
TableurQspi = Frame(c , width=410, height=300, bd=8, relief="raise", bg="black")
TableurQspi.grid(column =2, row = 3,sticky='ns',pady=5)
TableurQspi.grid_propagate(0)
treeQspi = ttk.Treeview(TableurQspi, columns=("column1"), show='headings', height=12)
scrollbarx = Scrollbar(TableurQspi, orient='horizontal',command=treeQspi.xview)
scrollbary = Scrollbar(TableurQspi, orient='vertical',command=treeQspi.yview)
scrollbarx.grid(column = 0, row = 1, sticky='we')
scrollbary.grid(column = 1, row = 0, sticky='ns')
treeQspi['xscrollcommand'] = scrollbarx.set
treeQspi['yscrollcommand'] = scrollbary.set
treeQspi.heading("#1", text="AVEC QSPI")
treeQspi.column('#1', stretch=NO, minwidth=0, width=380)
treeQspi.grid(row=0, column=0)  
for line in lines:
  if str(line[4]).startswith('B'):
    treeQspi.insert("", END, values=line[3])

""" Zone de recherche """
rechercheTheme = Frame(c, bd=8, relief="raise", bg="white")
rechercheTheme.grid(column = 1, row = 1,pady=5,padx=10)
rechercheThemeLabel = Tk.Label(rechercheTheme, text="Recherche", fg="black", justify='left', bg="white")
rechercheThemeLabel.grid(row =0, column =0, pady=5, padx=15)
rechercheThemeLabel.config(font=('Century gothic', 10, 'bold'), fg="black", bg="white")
rechercheThemeInput = Entry(rechercheTheme, textvariable=searchTerm, width=45,bg="#55A9FD")
rechercheThemeInput.grid(row=1, column=0, sticky='nwse')
rechercheThemeInput.config(font=('Century gothic', 10, 'bold'))
rechercheThemeInput.bind('<Return>', lambda a:rechercheList())

""" Fonction Charger le fichier """
def searchFile():
  for i in tree.get_children():
    tree.delete(i)
  for i in treeQspi.get_children():
    treeQspi.delete(i)
  modifyFile = filedialog.askopenfilename(initialdir = "C:/",title = "choose your file",filetypes = (("c files","*.c"),("all files","*.*")))
  filin = open(modifyFile, "r")
  lignes = filin.read()
  fichier = open('copy.txt', 'wt')
  fichier.write(lignes)
  text = str('static GX_CONST GX_UBYTE')
  registerLine = open(fileDir+"\\modifyFiles.txt", "wt")
  with open(fileDir+"\\copy.txt") as file_in:
    for line in file_in:
      if line.startswith(text):
        lines.append(line.split(' '))
        registerLine.write(line)
    for line in lines:
      if str(line[4]).startswith('='):
        tree.insert("", END, values=line[3])
      if str(line[4]).startswith('B'):
        treeQspi.insert("", END, values=line[3])
  fichier.close()

""" Fonction rechercher """
def rechercheList():
  pattern = searchTerm.get()
  newList = []
  listing = []
  for i in tree.get_children():
    tree.delete(i)
  for i in treeQspi.get_children():
    treeQspi.delete(i)
  registerLine = open(fileDir+"\\modifyFiles.txt", "wt")
  text = str('static GX_CONST GX_UBYTE')
  with open(fileDir+"\\copy.txt") as file_in:
    for line in file_in:
      if line.startswith(text):
        listing.append(line.split(' '))
        registerLine.write(line)
  if pattern == '':
    for line in listing:
      if str(line[4]).startswith('='):
        tree.insert("", END, values=line[3])
      if str(line[4]).startswith('B'):
        treeQspi.insert("", END, values=line[3])
  if pattern != '':
    for line in listing:
      if pattern in str(line[3]):
        if str(line[4]).startswith('='):
          newList.append(line[3])
          tree.insert("", END, values=line[3])
        if str(line[4]).startswith('B'):
          treeQspi.insert("", END, values=line[3])

""" Fonction ajout le Qspi du fichier"""
def addQspi():
  while 0 < len(tree.selection()):
    selected_item = tree.selection()[0]
    item10 = tree.set(selected_item, 0)
    treeQspi.insert("", 0, values = item10)
    tree.delete(selected_item)
    modifyFile = open(fileDir+"\\copy.txt", "rt")
    lineFile = modifyFile.read()
    index = lineFile.find(str(item10))
    lineFile = lineFile.replace(item10, item10[:index] + ' BSP_PLACE_IN_SECTION(".qspi_flash")' + item10[index:])
    modifyFile.close()
    modifyFile = open(fileDir+"\\copy.txt", "wt")
    modifyFile.write(lineFile)
    modifyFile.close()

""" Fonction enlever le QSPI du fichier """   
def removeQspi():
  while 0 < len(treeQspi.selection()):
    selected_item = treeQspi.selection()[0]
    item10 = treeQspi.set(selected_item,0)
    tree.insert("", 0, values=item10)
    treeQspi.delete(selected_item)
    modifyFile = open(fileDir+"\\copy.txt", "rt")
    lineFile = modifyFile.read()
    index = lineFile.find(str(item10))
    lineFile = lineFile.replace(item10 + ' BSP_PLACE_IN_SECTION(".qspi_flash")', item10[:index] + '')
    modifyFile.close()
    modifyFile = open(fileDir+"\\copy.txt", "wt")
    modifyFile.write(lineFile)
    modifyFile.close()

""" Selectionner toutes les occurrences du tableau sans QSPI """
def selectAll():
  all_items = list(tree.get_children())
  tree.selection_set(all_items)

""" Selectionner toutes les occurrences du tableau avec QSPI """
def selectAllQspi():
  all_items = list(treeQspi.get_children())
  treeQspi.selection_set(all_items)

""" Sauvegarder ses modifs dans un emplacement et nom de fichier voulu """
def save():
  files = [('All Files', '*.*'), 
             ('Text Document', '*.txt')]
  file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
  modifyFile = open(fileDir+"\\copy.txt", "r+")
  lineFile = modifyFile.read()
  modifyFileCopy = open(file.name, "wt")
  modifyFileCopy.write(lineFile)
  modifyFile.close()
  modifyFileCopy.close()

""" Effacer la zone de recherche et recharger les tableaux """
def clear():
  listing = []
  for i in tree.get_children():
    tree.delete(i)
  for i in treeQspi.get_children():
    treeQspi.delete(i)
  registerLine = open(fileDir+"\\modifyFiles.txt", "wt")
  text = str('static GX_CONST GX_UBYTE')
  with open(fileDir+"\\copy.txt") as file_in:
    for line in file_in:
      if line.startswith(text):
        listing.append(line.split(' '))
        registerLine.write(line)
    for line in listing:
      if str(line[4]).startswith('='):
        tree.insert("", END, values=line[3])
      if str(line[4]).startswith('B'):
        treeQspi.insert("", END, values=line[3])

""" quitter """
def quit():
  fenetre.destroy()

tree.update_idletasks()
""" Zone btn """
zoneboutton=Frame(c, bd=8, relief="raise", bg="white")
zoneboutton.grid(column = 0, row = 0,sticky='nw',pady=5)
button2=Tk.Button(zoneboutton, command=searchFile, text='Load File', width=10)
button2.config(font=('Century gothic', 10, 'bold'), bg='white', activebackground="#55A9FD") 
bal_ttp=CreateToolTip(button2, "ctrl+o") 
button2.grid(row =0, column =0)
button5=Tk.Button(zoneboutton, command=save, text='Save', width=10)
button5.config(font=('Century gothic', 10, 'bold'), bg='white', activebackground="#55A9FD") 
bal_ttp=CreateToolTip(button5, "ctrl+s") 
button5.grid(row =0, column =1)

zonebouttonRech=Frame(c, bd=8, relief="raise", bg="white")
zonebouttonRech.grid(column = 1, row = 2,sticky='n',pady=0,padx=0)
button1=Tk.Button(zonebouttonRech, command=rechercheList, text='Recherche', width=10)
button1.config(font=('Century gothic', 10, 'bold'), bg='white', activebackground="#55A9FD") 
button1.grid(row =0, column =0)
button6=Tk.Button(zonebouttonRech, command=clear, text='Clear', width=10)
button6.config(font=('Century gothic', 10, 'bold'), bg='white', activebackground="#55A9FD") 
button6.grid(row =0, column =1)

zonebouttonAddRemove=Frame(c, bd=8, relief="raise", bg="white")
zonebouttonAddRemove.grid(column = 1, row = 3,sticky='ew', pady=0, padx=0)
button2=Tk.Button(zonebouttonAddRemove, command=addQspi, text=u'\u2192', width=8)
button2.config(font=('Century gothic', 12), bg='white', activebackground="#55A9FD") 
bal_ttp=CreateToolTip(button2, "Ajouter le QSPI, ctrl+")
button2.grid(row =0, column =1)
button4=Tk.Button(zonebouttonAddRemove, command=selectAll, text=u'\u2714', width=8)
button4.config(font=('Century gothic', 12), bg='white', activebackground="#55A9FD")
bal_ttp=CreateToolTip(button4, "Select ALL sans QSPI, ctrl+a") 
button4.grid(row =0, column =0)
button5=Tk.Button(zonebouttonAddRemove, command=selectAllQspi, text=u'\u2714', width=8)
button5.config(font=('Century gothic', 12), bg='white', activebackground="#55A9FD") 
bal_ttp=CreateToolTip(button5, "Select ALL avec QSPI, ctrl+e") 
button5.grid(row =0, column =3)
button3=Tk.Button(zonebouttonAddRemove, command=removeQspi, text=u'\u2190', width=8)
button3.config(font=('Century gothic', 12), bg='white', activebackground="#55A9FD") 
bal_ttp=CreateToolTip(button3, "Enlever le QSPI, ctrl-") 
button3.grid(row =0, column =2)

""" Chargement de la fenêtre """
fenetre.rowconfigure(0, weight=1)
fenetre.columnconfigure(0, weight=1)
fenetre.mainloop()
