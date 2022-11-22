from tkinter import *
from tkinter import ttk
from input_win import InputDataWin
from notif import DequeueNotification
import pandas as pd

# Membuat class dashboard yang berisi tabel data antrean
# Dapat membuat instance dari objek InputDataWin dengan
# menekan button '+' pada bagian kanan atas

class Dashboard(Tk):
    # Di-derive dari class Tk agar dapat bisa langsung jadi window
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.configure('.', background="#f0f0ed")

        # Container utama Dashboard
        mainframe = ttk.Frame(self, padding=5)
        mainframe.grid(row=0, column=0, sticky="N E W S", padx=20)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)

        # Membuat top container yang berisi label dashboard dan button '+'
        topframe = ttk.Frame(mainframe, padding=5, relief="sunken")
        topframe.grid(row=0, column=0, sticky="news")
    
        print(self.winfo_screenmmwidth())
        ttk.Label(topframe, text="Dashboard Antrean", font=(
            "Times New Roman", 21, "bold")).pack(side=LEFT)
        ttk.Button(topframe, text='+', width=3,
                   command=self.get_data).pack(side=RIGHT)
        self.make_table(mainframe)
        # Ngebuat lambda function biar bisa ngerefresh dari window lain
        self.refresh_table = lambda: self.make_table(mainframe)

    # Fungsi buat instance objek InputDataWin
    def get_data(self):
        self.input_win = InputDataWin(self)
        self.input_win.mainloop()

    # Fungsi untuk membuat dan merefresh tabel (ngga bisa dipanggil langsung
    # dari window lain karena harus ngepass argumen mainframe dashboardnya
    # yang cuma ada di constructor aja, makanya dibuatlah lambda function
    # di constructornya)
    def make_table(self, mainframe):
        # Membuat bot container
        botframe = ttk.Frame(mainframe, padding=5, border=5, relief="sunken")
        botframe.grid(row=1, column=0)

        # Membuat container untuk setiap tabel dr. Tulus & dr. Gisel
        tabel_tulus = ttk.Frame(botframe, border=5, relief=RAISED)
        tabel_tulus.grid(row=0, column=0)

        tabel_gisel = ttk.Frame(botframe, border=5, relief="raised")
        tabel_gisel.grid(row=0, column=1)

        # Membaca data dari csv setiap dokter
        data_tulus = pd.read_csv("data_antrean/tulus.csv")
        data_gisel = pd.read_csv("data_antrean/gisel.csv")

        # Membuat Label di row paling atas pada container/frame
        label_tulus = ttk.Label(tabel_tulus, text="dr. Tulus", font=(
            "Times New Roman", 14, "bold"))
        label_tulus.grid(row=0, column=0, columnspan=2)

        label_gisel = ttk.Label(tabel_gisel, text="dr. Gisel", font=(
            "Times New Roman", 14, "bold"))
        label_gisel.grid(row=0, column=0, columnspan=2)

        # Melakukan pembuatan tabel
        for i in range(10):
            # ============== Data Tulus ======================
            no_antrean_tulus = ttk.Entry(
                tabel_tulus, width=3, justify="center")
            nama_tulus = ttk.Entry(tabel_tulus, justify="center")

            no_antrean_tulus.grid(row=i+1, column=0)
            nama_tulus.grid(row=i+1, column=1)

            # Kalau besar i sudah samadengan atau lebih besar dari
            # banyak row pada dataframe, maka akan memasukkan empty
            # string pada tabel
            if len(data_tulus) <= i:
                no_antrean_tulus.insert(0, '')
                nama_tulus.insert(0, '')
            else:
                no_antrean_tulus.insert(0, data_tulus.iloc[i, 0])
                nama_tulus.insert(0, data_tulus.iloc[i, 1])
            # =============== Data Gisel =======================
            no_antrean_gisel = ttk.Entry(
                tabel_gisel, width=3, justify="center")
            nama_gisel = ttk.Entry(tabel_gisel, justify="center")

            no_antrean_gisel.grid(row=i+1, column=0)
            nama_gisel.grid(row=i+1, column=1)

            # Sebenernya sama aja untuk nanganin index yang lebih
            # besar, cuma beda gaya doang
            no_antrean_gisel.insert(0, '' if len(
                data_gisel) <= i else data_gisel.iloc[i, 0])
            nama_gisel.insert(0, '' if len(data_gisel) <=
                              i else data_gisel.iloc[i, 1])

        # Membuat button next untuk setiap tabel, melakukan
        # dequeue (NOT IMPLEMENTED)
        ttk.Button(tabel_tulus, text='=>', command=lambda: self.dq_table(0)).grid(
            row=11, column=0, columnspan=2)
        ttk.Button(tabel_gisel, text='=>', command=lambda: self.dq_table(1)).grid(
            row=11, column=0, columnspan=2)
    
    def dq_table(self, id):
        dr = "tulus" if not id else "gisel"
        csv_data = pd.read_csv(f"data_antrean/{dr}.csv")
        pass_data = csv_data.iloc[0, :].values.tolist()
        csv_data = csv_data.iloc[1:, :]
        #csv_data.to_csv(f"data_antrean/{dr}.csv", index=False)
        pass_data = [pass_data[0], pass_data[1], dr]

        
        DequeueNotification(self, pass_data)
        self.after(3000, self.refresh_table)