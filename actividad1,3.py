import math
import tkinter as tk
from tkinter import messagebox


class VentanaPrincipal:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Cálculo de notas")
        self.ventana.resizable(False, False)

        self.campos = []
        for i in range(5):
            tk.Label(self.ventana, text=f"Nota {i + 1}:").grid(
                row=i, column=0, padx=8, pady=4, sticky="e"
            )
            campo = tk.Entry(self.ventana, width=12)
            campo.grid(row=i, column=1, padx=8, pady=4)
            self.campos.append(campo)

        tk.Button(self.ventana, text="Calcular", command=self.calcular).grid(
            row=5, column=0, padx=8, pady=8
        )
        tk.Button(self.ventana, text="Limpiar", command=self.limpiar).grid(
            row=5, column=1, padx=8, pady=8
        )

        self.promedio = tk.Label(self.ventana, text="Promedio = ")
        self.promedio.grid(row=6, column=0, columnspan=2, sticky="w", padx=8)
        self.desviacion = tk.Label(self.ventana, text="Desviación estándar = ")
        self.desviacion.grid(row=7, column=0, columnspan=2, sticky="w", padx=8)
        self.mayor = tk.Label(self.ventana, text="Nota mayor = ")
        self.mayor.grid(row=8, column=0, columnspan=2, sticky="w", padx=8)
        self.menor = tk.Label(self.ventana, text="Nota menor = ")
        self.menor.grid(row=9, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

    def leer_notas(self):
        """Devuelve la lista de 5 notas, o None si hay algún error (ya avisado al usuario)."""
        notas = []
        for i, campo in enumerate(self.campos, start=1):
            texto = campo.get().strip()

            # Validación 1: la nota es obligatoria
            if texto == "":
                messagebox.showwarning(
                    "Dato faltante",
                    f"La nota {i} no ha sido ingresada.\n"
                    "Es obligatorio ingresar las cinco notas.",
                )
                campo.focus_set()
                return None

            # Validación 2: debe ser un número
            try:
                valor = float(texto.replace(",", "."))
                if not math.isfinite(valor):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Dato no válido",
                    f"La nota {i} no es numérica: '{texto}'.\n"
                    "Ingresa solamente números.",
                )
                campo.focus_set()
                campo.select_range(0, tk.END)
                return None

            notas.append(valor)
        return notas

    def calcular(self):
        notas = self.leer_notas()
        if notas is None:
            return

        n = len(notas)
        promedio = sum(notas) / n
        desviacion = math.sqrt(sum((x - promedio) ** 2 for x in notas) / n)

        self.promedio.config(text=f"Promedio = {promedio:.2f}")
        self.desviacion.config(text=f"Desviación estándar = {desviacion:.2f}")
        self.mayor.config(text=f"Nota mayor = {max(notas):.2f}")
        self.menor.config(text=f"Nota menor = {min(notas):.2f}")

    def limpiar(self):
        for campo in self.campos:
            campo.delete(0, tk.END)

        self.promedio.config(text="Promedio = ")
        self.desviacion.config(text="Desviación estándar = ")
        self.mayor.config(text="Nota mayor = ")
        self.menor.config(text="Nota menor = ")
        self.campos[0].focus_set()

    def ejecutar(self):
        self.ventana.mainloop()


# Clase principal: punto de entrada del programa
class Principal:

    @staticmethod
    def main():
        miVentanaPrincipal = VentanaPrincipal()
        miVentanaPrincipal.ejecutar()


if __name__ == "__main__":
    Principal.main()