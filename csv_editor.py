import os
import csv
from csv import DictWriter
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askquestion, showerror
import urllib.request
import requests
##import time
##from office365.runtime.auth.authentication_context import AuthenticationContext
##from office365.sharepoint.client_context import ClientContext
##from office365.sharepoint.files.file import File


def _convert_stringval(value):
    """ Converte i dati passati mediante tkinter come delle
        stringhe e non come interi, in questo modo riusciamo
        a mantenere gli zero leadings prima dei ccr
    """
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value


def update1(data):
    # clear the listbox
    my_list1.delete(0, END)

    # add toppings to listbox
    for item in data:
        my_list1.insert(END, item)


def update2(data):
    # clear the listbox
    my_list2.delete(0, END)

    # add toppings to listbox
    for item in data:
        my_list2.insert(END, item)

def fillout1(e):
    Descr_da_entry.delete(0, END)
    Descr_da_entry.insert(0, my_list1.get(ANCHOR))

def fillout2(e):
    Descr_a_entry.delete(0, END)
    Descr_a_entry.insert(0, my_list2.get(ANCHOR))

def check1(e):
    typed = Descr_da_entry.get()
    if typed == '':
        data = []
    else:
        data = []
        for item in toppings:
            if typed.lower() in item.lower():
                data.append(item)
    update1(data)

def check2(e):
    typed = Descr_a_entry.get()
    if typed == '':
        data = []
    if len(typed) == 0:
        data = []
    else:
        data = []
        for item in toppings:
            if typed.lower() in item.lower():
                data.append(item)
    update2(data)


# menubar
def openfile():
    with open("output.csv") as myfile:
        csvread = csv.reader(myfile, delimiter=";")
        header = next(csvread) #salta la riga di intestazione
        for row in csvread:
            tabella.insert("", "end", values=row)

def savefile(): 
    with open("output.csv", "w", newline="") as myfile:
        dict_writer = DictWriter(myfile, delimiter=';', fieldnames=['Ccr1', 'Ccr2', 'Descr_da__', 'Descr_a__', 'Da', 'A', 'Prezzo'])
        if os.stat('output.csv').st_size == 0:        #if file is not empty than header write else not
            dict_writer.writeheader()

            
        csvwriter = csv.writer(myfile, delimiter=";")
        for row_id in tabella.get_children():
            row = tabella.item(row_id)["values"]
            csvwriter.writerow(row)
            
    showinfo("Salva", "Il salvataggio è avvenuto correttamente")

def info_menu():
    info_root = tk.Toplevel()
    info_root.title("Info")
    Label(info_root, text="CSV Editor for Trenitalia v0.1", font="bold").grid(row=1, column=0, sticky="we", pady=5, padx=5)
    Label(info_root, text="Antonio dello Stritto").grid(row=2, column=0, sticky="we", pady=5, padx=5)
    close_button = Button(info_root,text = "Esci",command=lambda:info_root.destroy()).grid(row=3, column=0, pady=5)

def input_record():
    """ impostazione di lettura dei campi di inserimento """
    global count

    if Prezzo_entry.get() == '':
        msg = f'Non sono stati inseriti tutti i campi obbligatori'
        showerror(title='Error', message=msg)
        return
    else:
        pass

    try:        
        tabella.insert(
        parent="",
        index="end",
        iid = count,
        text="",
        values=(
        mydict[Descr_da_entry.get()][0],
        mydict[Descr_a_entry.get()][0],
        Descr_da_entry.get(),
        Descr_a_entry.get(),
        mydict[Descr_da_entry.get()][1],
        mydict[Descr_a_entry.get()][1],
        Prezzo_entry.get()))
    except:
        msg = f'Non sono stati inseriti tutti i campi obbligatori'
        showerror(title='Error', message=msg)
        return

    count += 1   
    Descr_da_entry.delete(0,END)
    Descr_a_entry.delete(0,END)
    Prezzo_entry.delete(0,END)
   
def delete():
    """ Eliminazione dei dati selezionati dalla tabella """
    selected_item = tabella.selection()[0]
    tabella.delete(selected_item)



def main():
       
    global tabella
    global mydict
    global count
    global my_list1
    global my_list2
    global Descr_da_entry
    global Descr_a_entry
    global Prezzo_entry
    global toppings

##    url= "https://gruppofsitaliane-my.sharepoint.com/personal/8931520_fstechnology_it/"
##
##    ctx_auth = AuthenticationContext(url)
##    ctx_auth.acquire_token_for_user('8931520@fstechnology.it', 'Gennaio2023')
##    ctx = ClientContext(url, ctx_auth)
##
##    response = File.open_binary(ctx, "/personal/8931520_fstechnology_it/Documents/DSTASPXN.csv")
##    with open("DSTASPXN_new.csv", "wb") as local_file:
##        local_file.write(response.content)


    github_session = requests.Session()

    # providing raw url to download csv from github
    csv_url = 'https://raw.githubusercontent.com/anto1111/csv_editor/master/DSTASPXN.csv'

    # per mantenere sempre aggiornati i dati dal DSTASPXN vengono scaricati ad ogni apertura
    with open("DSTASPXN.csv", "wb") as local_file:
        local_file.write(github_session.get(csv_url).content)
    
    ttk._convert_stringval = _convert_stringval
    toppings = []
    with open('DSTASPXN.csv', mode='r') as infile:
        reader2 = csv.reader(infile, delimiter=';')
        next(reader2)
        for n, row in enumerate(reader2):
            toppings.append(row[0])

    with open('DSTASPXN.csv', mode='r') as infile:
        #Open a reader to the csv
        reader1 = csv.reader(infile, delimiter=';', skipinitialspace=True)
        next(reader1)
        #Read into the dictionary using dictionary comprehension, key is the first column and row are rest of the columns
        mydict = { key: row for key, *row in reader1 }         
            
    # inizializzazione Tkinter
    root = tk.Tk()
    root.title("Inserimento tariffe")

    mb = Menu(root)
    file_menu = Menu(mb, tearoff=0)
    file_menu.add_command(label="Apri l'ultimo", command=openfile)
    file_menu.add_command(label="Salva", command=savefile)
    file_menu.add_separator()
    file_menu.add_command(label="Esci", command=lambda:root.destroy())
    mb.add_cascade(label="File", menu=file_menu)
    mb.add_command(label="Info", command=info_menu)
    root.config(menu=mb)

    # tabella
    tabella = ttk.Treeview(root)
    tabella.grid(row=4, column=0, sticky="w", padx=5)

    # aggiunta delle colonne alla tabella vista
    tabella["columns"] = ("Ccr1", "Ccr2", "Descr_da__", "Descr_a__", "Da", "A", "Prezzo")
    tabella.column("#0", width=0,  stretch=NO)
    tabella.column("Ccr1", anchor=CENTER, width=80)
    tabella.column("Ccr2", anchor=CENTER, width=80)
    tabella.column("Descr_da__", anchor=CENTER, width=200)
    tabella.column("Descr_a__", anchor=CENTER, width=200)
    tabella.column("Da", anchor=CENTER, width=80)
    tabella.column("A", anchor=CENTER, width=80)
    tabella.column("Prezzo", anchor=CENTER, width=80)

    # aggiunta delle intestazioni alla tabella vista
    tabella.heading("#0",text="",anchor=CENTER)
    tabella.heading("Ccr1",text="Ccr1",anchor=CENTER)
    tabella.heading("Ccr2",text="Ccr2",anchor=CENTER)
    tabella.heading("Descr_da__",text="Descr_da__",anchor=CENTER)
    tabella.heading("Descr_a__",text="Descr_a__",anchor=CENTER)
    tabella.heading("Da",text="Da",anchor=CENTER)
    tabella.heading("A",text="A",anchor=CENTER)
    tabella.heading("Prezzo",text="Prezzo",anchor=CENTER)


    # inserimento dei dati nella tabella vista
    data = []
    count = 1   
    for zaznam in data:      
        tabella.insert(parent='', index="end", iid=count, text="", values=(zaznam[0], 
    zaznam[1], zaznam[2], zaznam[3], zaznam[4], zaznam[5]))       
        count += 1

    # Inserimento del frame dei campi
    Input_frame = Frame(root)
    Input_frame.grid(row=5, column=0)
    # Inserimento etichette dei campi
    Descr_da = Label(Input_frame,text="Descr_da")
    Descr_da.grid(row=0, column=3)
    Descr_a = Label(Input_frame,text="Descr_a")
    Descr_a.grid(row=0,column=4)
    Prezzo = Label(Input_frame,text="Prezzo")
    Prezzo.grid(row=0,column=7)

    # Inserimento campi
    my_list1 = Listbox(Input_frame, width=37)
    my_list1.grid(row=2,column=3)
    my_list2 = Listbox(Input_frame, width=37)
    my_list2.grid(row=2,column=4)
    Descr_da_entry = Entry(Input_frame, width=37)
    Descr_da_entry.grid(row=1,column=3)
    Descr_a_entry = Entry(Input_frame, width=37)
    Descr_a_entry.grid(row=1,column=4)
    Prezzo_entry = Entry(Input_frame, width=8)
    Prezzo_entry.grid(row=1,column=7)

    update1(toppings)
    update2(toppings)
    my_list1.bind("<<ListboxSelect>>", fillout1)
    Descr_da_entry.bind("<KeyRelease>", check1)
    my_list2.bind("<<ListboxSelect>>", fillout2)
    Descr_a_entry.bind("<KeyRelease>", check2)

    # frame dei button
    Button_frame = Frame(root)
    Button_frame.grid(row=6, column=0)
       
    # button di aggiunta riga csv
    butt_plus = PhotoImage(file="plus.png")
    Input_button = Button(Button_frame, command=input_record, image=butt_plus, 
    relief="flat").grid(row=0, column=0, pady=5)

    # button di cancellazione riga csv
    butt_minus = PhotoImage(file="minus.png")
    delete_button = Button(Button_frame, command=delete, image=butt_minus, 
    relief="flat").grid(row=0, column=1, pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
