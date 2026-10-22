import tkinter as tk
from tkinter import messagebox
import math


# Error propio para valores inválidos o geométricamente imposibles
class ErrorGeometrico(Exception):
    pass


# Clase padre
class FiguraGeometrica:
    def __init__(self):
        self.volumen = 0
        self.superficie = 0

    def set_volumen(self, volumen):
        self.volumen = volumen

    def set_superficie(self, superficie):
        self.superficie = superficie

    def get_volumen(self):
        return self.volumen

    def get_superficie(self):
        return self.superficie


# Clase Cilindro
class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        super().__init__()
        self.radio = radio
        self.altura = altura

        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return math.pi * self.altura * self.radio ** 2

    def calcular_superficie(self):
        area_lateral = 2 * math.pi * self.radio * self.altura
        area_bases = 2 * math.pi * self.radio ** 2
        return area_lateral + area_bases


# Clase Esfera
class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        super().__init__()
        self.radio = radio

        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = (4/3) * pi * r^3
        return (4 / 3) * math.pi * self.radio ** 3

    def calcular_superficie(self):
        return 4 * math.pi * self.radio ** 2


# Clase Piramide (base cuadrada)
class Piramide(FiguraGeometrica):
    def __init__(self, base, altura, apotema):
        super().__init__()

        # apotema^2 = altura^2 + (base/2)^2
        if apotema <= altura:
            raise ErrorGeometrico("El apotema debe ser mayor que la altura.")
        if apotema <= base / 2:
            raise ErrorGeometrico(
                "El apotema debe ser mayor que la mitad de la base."
            )

        self.base = base
        self.altura = altura
        self.apotema = apotema

        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return (self.base ** 2 * self.altura) / 3

    def calcular_superficie(self):
        area_base = self.base ** 2
        area_lateral = 2 * self.base * self.apotema
        return area_base + area_lateral


# Clase Cubo
class Cubo(FiguraGeometrica):
    def __init__(self, arista):
        super().__init__()
        self.arista = arista

        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return self.arista ** 3

    def calcular_superficie(self):
        return 6 * self.arista ** 2


# Clase Prisma (rectangular)
class Prisma(FiguraGeometrica):
    def __init__(self, largo, ancho, altura):
        super().__init__()
        self.largo = largo
        self.ancho = ancho
        self.altura = altura

        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return self.largo * self.ancho * self.altura

    def calcular_superficie(self):
        return 2 * (
            self.largo * self.ancho
            + self.largo * self.altura
            + self.ancho * self.altura
        )


# ---------------------------------------------------------------
# Imágenes: se dibujan con Canvas (no necesitan archivos externos)
# ---------------------------------------------------------------
ANCHO_IMG = 200
ALTO_IMG = 160
COLOR_LINEA = "#1f3b73"
COLOR_RELLENO = "#cfe0ff"
COLOR_RELLENO_2 = "#9fbcf2"


def dibujar_cilindro(c):
    # Cuerpo
    c.create_rectangle(50, 35, 150, 120, fill=COLOR_RELLENO, outline="")
    c.create_oval(50, 105, 150, 135, fill=COLOR_RELLENO, outline=COLOR_LINEA,
                  width=2)
    c.create_rectangle(51, 35, 149, 120, fill=COLOR_RELLENO, outline="")
    c.create_line(50, 35, 50, 120, fill=COLOR_LINEA, width=2)
    c.create_line(150, 35, 150, 120, fill=COLOR_LINEA, width=2)
    c.create_oval(50, 105, 150, 135, outline="", fill="")
    c.create_arc(50, 105, 150, 135, start=180, extent=180,
                 style=tk.ARC, outline=COLOR_LINEA, width=2)
    # Tapa superior
    c.create_oval(50, 20, 150, 50, fill=COLOR_RELLENO_2, outline=COLOR_LINEA,
                  width=2)


def dibujar_esfera(c):
    c.create_oval(40, 15, 160, 135, fill=COLOR_RELLENO, outline=COLOR_LINEA,
                  width=2)
    c.create_arc(40, 60, 160, 90, start=180, extent=180,
                 style=tk.ARC, outline=COLOR_LINEA, width=2)
    c.create_arc(40, 60, 160, 90, start=0, extent=180,
                 style=tk.ARC, outline=COLOR_LINEA, dash=(4, 3))


def dibujar_piramide(c):
    apice = (95, 20)
    f_izq, f_der = (30, 125), (110, 125)
    d_der, d_izq = (165, 98), (85, 98)  # esquina oculta: d_izq

    # Aristas ocultas
    c.create_line(*d_izq, *f_izq, fill=COLOR_LINEA, dash=(4, 3))
    c.create_line(*d_izq, *d_der, fill=COLOR_LINEA, dash=(4, 3))
    c.create_line(*apice, *d_izq, fill=COLOR_LINEA, dash=(4, 3))
    # Caras visibles
    c.create_polygon(*apice, *f_izq, *f_der, fill=COLOR_RELLENO,
                     outline=COLOR_LINEA, width=2)
    c.create_polygon(*apice, *f_der, *d_der, fill=COLOR_RELLENO_2,
                     outline=COLOR_LINEA, width=2)


def _dibujar_caja(c, x0, y0, x1, y1, dx, dy):
    """Caja en proyección oblicua: frente (x0,y0)-(x1,y1), fondo desplazado."""
    # Aristas ocultas
    c.create_line(x0 + dx, y1 - dy, x0, y1, fill=COLOR_LINEA, dash=(4, 3))
    c.create_line(x0 + dx, y1 - dy, x1 + dx, y1 - dy, fill=COLOR_LINEA,
                  dash=(4, 3))
    c.create_line(x0 + dx, y1 - dy, x0 + dx, y0 - dy, fill=COLOR_LINEA,
                  dash=(4, 3))
    # Cara superior
    c.create_polygon(x0, y0, x1, y0, x1 + dx, y0 - dy, x0 + dx, y0 - dy,
                     fill=COLOR_RELLENO_2, outline=COLOR_LINEA, width=2)
    # Cara lateral derecha
    c.create_polygon(x1, y0, x1 + dx, y0 - dy, x1 + dx, y1 - dy, x1, y1,
                     fill=COLOR_RELLENO_2, outline=COLOR_LINEA, width=2)
    # Cara frontal
    c.create_rectangle(x0, y0, x1, y1, fill=COLOR_RELLENO,
                       outline=COLOR_LINEA, width=2)


def dibujar_cubo(c):
    _dibujar_caja(c, 30, 65, 110, 145, 45, 45)


def dibujar_prisma(c):
    _dibujar_caja(c, 15, 75, 130, 145, 50, 45)


# Cada figura: nombre -> (clase, campos que se piden, función de dibujo)
FIGURAS = {
    "Cilindro": (Cilindro, ["Radio", "Altura"], dibujar_cilindro),
    "Esfera": (Esfera, ["Radio"], dibujar_esfera),
    "Pirámide": (Piramide, ["Base", "Altura", "Apotema"], dibujar_piramide),
    "Cubo": (Cubo, ["Arista"], dibujar_cubo),
    "Prisma": (Prisma, ["Largo", "Ancho", "Altura"], dibujar_prisma),
}


# Clase para crear las ventanas de las figuras
class VentanaFigura:
    def __init__(self, nombre):
        self.clase, campos, dibujo = FIGURAS[nombre]

        self.ventana = tk.Toplevel()
        self.ventana.title(nombre)
        self.ventana.resizable(False, False)

        # Imagen de la figura
        lienzo = tk.Canvas(
            self.ventana, width=ANCHO_IMG, height=ALTO_IMG,
            bg="white", highlightthickness=1, highlightbackground="#cccccc"
        )
        lienzo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        dibujo(lienzo)

        self.campos = {}

        for i, campo in enumerate(campos):
            fila = i + 1
            etiqueta = tk.Label(self.ventana, text=f"{campo} (cm):")
            etiqueta.grid(row=fila, column=0, padx=10, pady=7, sticky="w")

            entrada = tk.Entry(self.ventana)
            entrada.grid(row=fila, column=1, padx=10, pady=7)

            self.campos[campo] = entrada

        fila_boton = len(campos) + 1

        tk.Button(
            self.ventana, text="Calcular", command=self.calcular
        ).grid(row=fila_boton, column=0, columnspan=2, pady=10)

        self.resultado_volumen = tk.Label(self.ventana, text="Volumen (cm³):")
        self.resultado_volumen.grid(
            row=fila_boton + 1, column=0, columnspan=2, pady=5
        )

        self.resultado_superficie = tk.Label(
            self.ventana, text="Superficie (cm²):"
        )
        self.resultado_superficie.grid(
            row=fila_boton + 2, column=0, columnspan=2, pady=(5, 12)
        )

    def leer_valores(self):
        """Lee y valida las entradas; devuelve los valores en orden."""
        valores = []

        for campo, entrada in self.campos.items():
            texto = entrada.get().strip().replace(",", ".")

            try:
                valor = float(texto)
            except ValueError:
                raise ErrorGeometrico(f"'{campo}' debe ser un número.")

            if not math.isfinite(valor) or valor <= 0:
                raise ErrorGeometrico(
                    f"'{campo}' debe ser un número mayor que cero."
                )

            valores.append(valor)

        return valores

    def calcular(self):
        try:
            valores = self.leer_valores()
            objeto = self.clase(*valores)

        except ErrorGeometrico as error:
            messagebox.showerror("Error", str(error))
            return

        self.resultado_volumen.config(
            text=f"Volumen (cm³): {objeto.get_volumen():.2f}"
        )
        self.resultado_superficie.config(
            text=f"Superficie (cm²): {objeto.get_superficie():.2f}"
        )


# Clase VentanaPrincipal
class VentanaPrincipal:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Figuras geométricas")
        self.raiz.resizable(False, False)

        tk.Label(
            raiz,
            text="Selecciona una figura geométrica",
            font=("Arial", 12)
        ).pack(padx=20, pady=15)

        # Un botón por cada figura registrada en FIGURAS
        for nombre in FIGURAS:
            tk.Button(
                raiz,
                text=nombre,
                width=15,
                command=lambda n=nombre: VentanaFigura(n)
            ).pack(pady=5)

        tk.Label(raiz, text="").pack(pady=2)


# Punto de entrada del programa
if __name__ == "__main__":
    raiz = tk.Tk()
    aplicacion = VentanaPrincipal(raiz)
    raiz.mainloop()