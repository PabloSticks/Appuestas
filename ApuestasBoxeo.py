import tkinter as tk
from tkinter import messagebox

class SistemaApuestas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Apuestas de Boxeo")
        self.root.geometry("400x400")
        self.root.configure(bg="#2c3e50")

        self.peleadores = []
        self.apuestas = []
        self.pelea_activa = False
        self.total_apostado = 0

        # Widgets principales
        self.label_info = tk.Label(self.root, text="Sistema de Apuestas", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        self.label_info.pack(pady=10)

        self.btn_crear_pelea = tk.Button(self.root, text="Crear Pelea", command=self.crear_pelea, width=20, bg="#3498db", fg="white", font=("Arial", 12))
        self.btn_crear_pelea.pack(pady=5)

        self.btn_registrar_apuesta = tk.Button(self.root, text="Registrar Apuesta", command=self.registrar_apuesta, state=tk.DISABLED, width=20, bg="#2980b9", fg="white", font=("Arial", 12))
        self.btn_registrar_apuesta.pack(pady=5)

        self.btn_calcular_ganancias = tk.Button(self.root, text="Calcular Ganancias", command=self.calcular_ganancias, state=tk.DISABLED, width=20, bg="#27ae60", fg="white", font=("Arial", 12))
        self.btn_calcular_ganancias.pack(pady=5)

        self.label_odds = tk.Label(self.root, text="", bg="#2c3e50", fg="white", font=("Arial", 12))
        self.label_odds.pack(pady=10)

        self.btn_salir = tk.Button(self.root, text="Salir", command=self.root.quit, width=20, bg="#e74c3c", fg="white", font=("Arial", 12))
        self.btn_salir.pack(pady=5)

    def crear_pelea(self):
        if self.pelea_activa:
            messagebox.showerror("Error", "Ya hay una pelea activa.")
            return

        self.peleadores = []
        self.apuestas = []
        self.pelea_activa = True
        self.total_apostado = 0

        self.ventana_pelea = tk.Toplevel(self.root)
        self.ventana_pelea.title("Crear Pelea")
        self.ventana_pelea.geometry("300x200")
        self.ventana_pelea.configure(bg="#34495e")

        tk.Label(self.ventana_pelea, text="Nombre del primer peleador:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=5)
        self.entry_peleador1 = tk.Entry(self.ventana_pelea)
        self.entry_peleador1.pack(pady=5)

        tk.Label(self.ventana_pelea, text="Nombre del segundo peleador:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=5)
        self.entry_peleador2 = tk.Entry(self.ventana_pelea)
        self.entry_peleador2.pack(pady=5)

        tk.Button(self.ventana_pelea, text="Guardar", command=self.guardar_pelea, bg="#1abc9c", fg="white", font=("Arial", 10)).pack(pady=10)

    def guardar_pelea(self):
        peleador1 = self.entry_peleador1.get().strip()
        peleador2 = self.entry_peleador2.get().strip()

        if not peleador1 or not peleador2:
            messagebox.showerror("Error", "Debes ingresar el nombre de ambos peleadores.")
            return

        self.peleadores = [peleador1, peleador2]
        self.ventana_pelea.destroy()
        self.btn_registrar_apuesta.config(state=tk.NORMAL)
        self.btn_calcular_ganancias.config(state=tk.NORMAL)
        self.actualizar_odds()
        messagebox.showinfo("Éxito", f"Pelea creada: {peleador1} vs {peleador2}")

    def registrar_apuesta(self):
        if not self.pelea_activa:
            messagebox.showerror("Error", "No hay ninguna pelea activa.")
            return

        self.ventana_apuesta = tk.Toplevel(self.root)
        self.ventana_apuesta.title("Registrar Apuesta")
        self.ventana_apuesta.geometry("300x300")
        self.ventana_apuesta.configure(bg="#34495e")

        tk.Label(self.ventana_apuesta, text="Nombre del apostador:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=5)
        self.entry_apostador = tk.Entry(self.ventana_apuesta)
        self.entry_apostador.pack(pady=5)

        tk.Label(self.ventana_apuesta, text="Seleccione el peleador:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=10)

        self.btn_peleador1 = tk.Button(self.ventana_apuesta, text=self.peleadores[0], command=lambda: self.seleccionar_peleador(self.peleadores[0]), bg="#3498db", fg="white", font=("Arial", 10))
        self.btn_peleador1.pack(pady=5)

        self.btn_peleador2 = tk.Button(self.ventana_apuesta, text=self.peleadores[1], command=lambda: self.seleccionar_peleador(self.peleadores[1]), bg="#3498db", fg="white", font=("Arial", 10))
        self.btn_peleador2.pack(pady=5)

        tk.Label(self.ventana_apuesta, text="Monto:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=5)
        self.entry_monto = tk.Entry(self.ventana_apuesta)
        self.entry_monto.pack(pady=5)

        tk.Button(self.ventana_apuesta, text="Registrar", command=self.guardar_apuesta, bg="#1abc9c", fg="white", font=("Arial", 10)).pack(pady=10)

    def seleccionar_peleador(self, peleador):
        self.peleador_seleccionado = peleador
        messagebox.showinfo("Selección", f"Has seleccionado a {peleador}.")

    def guardar_apuesta(self):
        apostador = self.entry_apostador.get().strip()
        monto = self.entry_monto.get().strip()

        if not apostador or not monto or not hasattr(self, 'peleador_seleccionado'):
            messagebox.showerror("Error", "Debes completar todos los campos y seleccionar un peleador.")
            return

        try:
            monto = float(monto)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser numérico.")
            return

        self.apuestas.append({"apostador": apostador, "peleador": self.peleador_seleccionado, "monto": monto})
        self.total_apostado += monto
        self.ventana_apuesta.destroy()
        self.actualizar_odds()
        messagebox.showinfo("Éxito", f"Apuesta registrada: {apostador} apuesta ${monto:.2f} por {self.peleador_seleccionado}.")

    def actualizar_odds(self):
        if not self.peleadores:
            self.label_odds.config(text="")
            return

        apuestas_por_peleador = {peleador: 0 for peleador in self.peleadores}
        for apuesta in self.apuestas:
            apuestas_por_peleador[apuesta["peleador"]] += apuesta["monto"]

        odds_text = "\n--- Odds Actualizados ---\n"
        for peleador, monto in apuestas_por_peleador.items():
            if monto > 0:
                odds = self.total_apostado / monto
            else:
                odds = 0
            odds_text += f"{peleador}: {odds:.2f}\n"

        self.label_odds.config(text=odds_text)

    def calcular_ganancias(self):
        if not self.pelea_activa:
            messagebox.showerror("Error", "No hay ninguna pelea activa.")
            return

        self.ventana_ganador = tk.Toplevel(self.root)
        self.ventana_ganador.title("Calcular Ganancias")
        self.ventana_ganador.geometry("300x200")
        self.ventana_ganador.configure(bg="#34495e")

        tk.Label(self.ventana_ganador, text="Seleccione el ganador:", bg="#34495e", fg="white", font=("Arial", 10)).pack(pady=10)
        tk.Button(self.ventana_ganador, text=self.peleadores[0], command=lambda: self.mostrar_ganancias(self.peleadores[0]), bg="#3498db", fg="white", font=("Arial", 10)).pack(pady=5)
        tk.Button(self.ventana_ganador, text=self.peleadores[1], command=lambda: self.mostrar_ganancias(self.peleadores[1]), bg="#3498db", fg="white", font=("Arial", 10)).pack(pady=5)

    def mostrar_ganancias(self, ganador):
        total_apostado = sum(apuesta["monto"] for apuesta in self.apuestas)
        apuestas_ganadoras = [apuesta for apuesta in self.apuestas if apuesta["peleador"] == ganador]

        if not apuestas_ganadoras:
            messagebox.showinfo("Sin Ganadores", f"Nadie apostó por {ganador}.")
            return

        total_ganador = sum(apuesta["monto"] for apuesta in apuestas_ganadoras)
        mensaje = f"\n--- Resultados: {ganador} Ganador ---\n\n"
        for apuesta in apuestas_ganadoras:
            porcentaje = apuesta["monto"] / total_ganador
            ganancia = porcentaje * total_apostado
            mensaje += f"{apuesta['apostador']} gana ${ganancia:.2f} (apostó ${apuesta['monto']:.2f}).\n"

        self.ventana_ganador.destroy()
        self.pelea_activa = False
        self.btn_registrar_apuesta.config(state=tk.DISABLED)
        self.btn_calcular_ganancias.config(state=tk.DISABLED)
        self.label_odds.config(text="")
        messagebox.showinfo("Resultados", mensaje)


# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaApuestas(root)
    root.mainloop()
