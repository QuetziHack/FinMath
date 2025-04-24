import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Definir esquemas de colores
# Modo claro
COLOR_FONDO_CLARO = "#f5f5f7"
COLOR_PANEL_CLARO = "#ffffff"
COLOR_ACENTO_CLARO = "#0066cc"
COLOR_TEXTO_CLARO = "#333333"
COLOR_SIMPLE_CLARO = "#4287f5"  # Azul para interés simple
COLOR_COMPUESTO_CLARO = "#f5a742"  # Naranja para interés compuesto
COLOR_CAPITAL_CLARO = "#a0a0a0"  # Gris para capital inicial

# Modo oscuro
COLOR_FONDO_OSCURO = "#1e1e1e"
COLOR_PANEL_OSCURO = "#2d2d2d"
COLOR_ACENTO_OSCURO = "#3a8ee6"
COLOR_TEXTO_OSCURO = "#e0e0e0"
COLOR_SIMPLE_OSCURO = "#64a0ff"  # Azul más claro para interés simple
COLOR_COMPUESTO_OSCURO = "#ffb74d"  # Naranja más claro para interés compuesto
COLOR_CAPITAL_OSCURO = "#c0c0c0"  # Gris más claro para capital inicial

class EstiloModerno(ttk.Style):
    def __init__(self, modo_oscuro=False):
        super().__init__()
        self.modo_oscuro = modo_oscuro
        self.actualizar_estilo()
        
    def actualizar_estilo(self):
        if self.modo_oscuro:
            COLOR_FONDO = COLOR_FONDO_OSCURO
            COLOR_PANEL = COLOR_PANEL_OSCURO
            COLOR_ACENTO = COLOR_ACENTO_OSCURO
            COLOR_TEXTO = COLOR_TEXTO_OSCURO
        else:
            COLOR_FONDO = COLOR_FONDO_CLARO
            COLOR_PANEL = COLOR_PANEL_CLARO
            COLOR_ACENTO = COLOR_ACENTO_CLARO
            COLOR_TEXTO = COLOR_TEXTO_CLARO
            
        self.configure('TFrame', background=COLOR_PANEL)
        self.configure('TLabelframe', background=COLOR_PANEL)
        self.configure('TLabelframe.Label', background=COLOR_PANEL, foreground=COLOR_TEXTO, font=('Helvetica', 10, 'bold'))
        self.configure('TLabel', background=COLOR_PANEL, foreground=COLOR_TEXTO, font=('Helvetica', 14))
        self.configure('TButton', background=COLOR_ACENTO, foreground='white', font=('Helvetica', 12, 'bold'))
        self.map('TButton', background=[('active', COLOR_ACENTO), ('pressed', '#004080')])
        self.configure('TEntry', foreground=COLOR_TEXTO, fieldbackground='white' if not self.modo_oscuro else '#3d3d3d', font=('Helvetica', 14))
        self.configure('TCombobox', foreground=COLOR_TEXTO, fieldbackground='white' if not self.modo_oscuro else '#3d3d3d', font=('Helvetica', 14))
        self.configure('Heading.TLabel', font=('Helvetica', 14, 'bold'))
        self.configure('Result.TLabel', font=('Helvetica', 12, 'bold'))
        self.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), foreground=COLOR_ACENTO)
        self.configure('Switch.TCheckbutton', background=COLOR_PANEL, foreground=COLOR_TEXTO)
        
    def cambiar_modo(self, modo_oscuro):
        self.modo_oscuro = modo_oscuro
        self.actualizar_estilo()

class CalculadoraIntereses(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Variable para el modo oscuro
        self.modo_oscuro = tk.BooleanVar(value=False)
        
        # Aplicar estilo moderno
        self.style = EstiloModerno()
        
        # Configuración de la ventana principal
        self.title("Calculadora de Interés - Matemáticas Financieras UNAM")
        self.geometry("1200x800")
        self.configure(bg=COLOR_FONDO_CLARO)
        self.iconphoto(False, tk.PhotoImage(data=""))  # Placeholder para ícono
        
        # Variables para los inputs
        self.capital = tk.DoubleVar(value=10000)
        self.tasa = tk.DoubleVar(value=3)
        self.tiempo = tk.IntVar(value=15)
        self.capitalizacion = tk.IntVar(value=12)
        
        # Crear el frame principal
        self.main_frame = ttk.Frame(self, padding="10 10 10 10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        ttk.Label(self.main_frame, text="Comparación de Interés Simple y Compuesto", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Panel de controles (izquierda)
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Parámetros", padding="15 15 15 15")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Agregar controles
        ttk.Label(self.control_frame, text="Capital Inicial ($):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
        capital_entry = ttk.Entry(self.control_frame, textvariable=self.capital, width=15)
        capital_entry.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(self.control_frame, text="Tasa de Interés Anual (%):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        tasa_entry = ttk.Entry(self.control_frame, textvariable=self.tasa, width=15)
        tasa_entry.grid(row=1, column=1, padx=5, pady=10)
        
        ttk.Label(self.control_frame, text="Plazo (años):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=10)
        tiempo_entry = ttk.Entry(self.control_frame, textvariable=self.tiempo, width=15)
        tiempo_entry.grid(row=2, column=1, padx=5, pady=10)
        
        ttk.Label(self.control_frame, text="Periodos de Capitalización por Año:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=10)
        capitalizacion_combobox = ttk.Combobox(self.control_frame, 
                                              textvariable=self.capitalizacion,
                                              values=[1, 2, 4, 12, 365],
                                              width=13)
        capitalizacion_combobox.grid(row=3, column=1, padx=5, pady=10)
        capitalizacion_combobox.current(0)
        
        # Opción de modo oscuro
        modo_oscuro_frame = ttk.Frame(self.control_frame)
        modo_oscuro_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(modo_oscuro_frame, text="Modo Oscuro:").pack(side=tk.LEFT, padx=(0, 10))
        modo_oscuro_check = ttk.Checkbutton(modo_oscuro_frame, variable=self.modo_oscuro, 
                                          command=self.cambiar_tema, style='Switch.TCheckbutton')
        modo_oscuro_check.pack(side=tk.LEFT)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.control_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Botones con mejor estilo
        calc_btn = ttk.Button(btn_frame, text="Calcular", command=self.actualizar_graficas, width=12)
        calc_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Limpiar", command=self.limpiar, width=12)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Tabla de resultados
        self.resultado_frame = ttk.LabelFrame(self.control_frame, text="Resultados", padding="10 10 10 10")
        self.resultado_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W+tk.E)
        
        # Inicializar tabla de resultados vacía
        self.crear_tabla_resultados()
        
        # Botón para teoría
        theory_btn = ttk.Button(self.control_frame, text="Teoría y Conceptos", command=self.mostrar_explicacion, width=25)
        theory_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Panel de gráficas (derecha)
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Visualización", padding="15 15 15 15")
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar estilo de la gráfica
        plt.style.use('seaborn-v0_8')
        
        # Crear figura de matplotlib
        self.fig = plt.Figure(figsize=(10, 6), dpi=100)
        self.fig.patch.set_facecolor(COLOR_PANEL_CLARO)
        
        # Crear un solo eje para la gráfica combinada
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#f9f9f9')
        
        # Agregar la gráfica al frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Inicializar con valores predeterminados
        self.actualizar_graficas()
    
    def cambiar_tema(self):
        modo_oscuro = self.modo_oscuro.get()
        
        # Actualizar el estilo
        self.style.cambiar_modo(modo_oscuro)
        
        # Cambiar colores de la ventana principal
        self.configure(bg=COLOR_FONDO_OSCURO if modo_oscuro else COLOR_FONDO_CLARO)
        
        # Actualizar la gráfica
        self.actualizar_graficas()
        
    def crear_tabla_resultados(self):
        # Limpiar el frame de resultados
        for widget in self.resultado_frame.winfo_children():
            widget.destroy()
        
        # Crear tabla con mejor formato
        # Encabezados
        encabezados = ["Concepto", "Interés Simple", "Interés Compuesto"]
        for i, header in enumerate(encabezados):
            label = ttk.Label(self.resultado_frame, text=header, style='Heading.TLabel')
            if i == 0:
                label.grid(row=0, column=i, padx=5, pady=(5, 10), sticky=tk.W)
            else:
                label.grid(row=0, column=i, padx=5, pady=(5, 10))
        
        # Separador
        separator = ttk.Separator(self.resultado_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # Datos
        conceptos = ["Monto Final ($):", "Interés Generado ($):", "Diferencia ($):"]
        for i, concepto in enumerate(conceptos):
            ttk.Label(self.resultado_frame, text=concepto).grid(
                row=i+2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Valores - se llenarán más tarde
        self.monto_simple_label = ttk.Label(self.resultado_frame, text="-", style='Result.TLabel')
        self.monto_simple_label.grid(row=2, column=1, padx=5, pady=5)
        
        self.monto_compuesto_label = ttk.Label(self.resultado_frame, text="-", style='Result.TLabel')
        self.monto_compuesto_label.grid(row=2, column=2, padx=5, pady=5)
        
        self.interes_simple_label = ttk.Label(self.resultado_frame, text="-", style='Result.TLabel')
        self.interes_simple_label.grid(row=3, column=1, padx=5, pady=5)
        
        self.interes_compuesto_label = ttk.Label(self.resultado_frame, text="-", style='Result.TLabel')
        self.interes_compuesto_label.grid(row=3, column=2, padx=5, pady=5)
        
        self.diferencia_label = ttk.Label(self.resultado_frame, text="-", style='Result.TLabel')
        self.diferencia_label.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
    
    def calcular_interes_simple(self, principal, tasa_anual, tiempo_anios):
        """Calcula el monto final con interés simple."""
        tasa_decimal = tasa_anual / 100
        monto_final = principal * (1 + tasa_decimal * tiempo_anios)
        return monto_final
    
    def calcular_interes_compuesto(self, principal, tasa_anual, tiempo_anios, periodos_por_anio=1):
        """Calcula el monto final con interés compuesto."""
        tasa_decimal = tasa_anual / 100
        n_total = tiempo_anios * periodos_por_anio
        tasa_por_periodo = tasa_decimal / periodos_por_anio
        monto_final = principal * (1 + tasa_por_periodo) ** n_total
        return monto_final
    
    def generar_datos_para_grafica(self, principal, tasa_anual, tiempo_anios, periodos_por_anio=1):
        """Genera datos para graficar el crecimiento año por año."""
        anios = np.linspace(0, tiempo_anios, int(tiempo_anios*12) + 1)  # Puntos mensuales
        
        # Calculamos valores para interés simple
        valores_simple = [self.calcular_interes_simple(principal, tasa_anual, t) for t in anios]
        
        # Calculamos valores para interés compuesto
        valores_compuesto = [self.calcular_interes_compuesto(principal, tasa_anual, t, periodos_por_anio) for t in anios]
        
        return anios, valores_simple, valores_compuesto
    
    def actualizar_graficas(self):
        try:
            # Obtener valores de los inputs
            principal = self.capital.get()
            tasa = self.tasa.get()
            tiempo = self.tiempo.get()
            periodos = self.capitalizacion.get()
            modo_oscuro = self.modo_oscuro.get()
            
            # Elegir los colores según el modo
            if modo_oscuro:
                COLOR_FONDO = COLOR_FONDO_OSCURO
                COLOR_PANEL = COLOR_PANEL_OSCURO
                COLOR_SIMPLE = COLOR_SIMPLE_OSCURO
                COLOR_COMPUESTO = COLOR_COMPUESTO_OSCURO
                COLOR_CAPITAL = COLOR_CAPITAL_OSCURO
                COLOR_GRAFICA_FONDO = '#1f1f1f'
                COLOR_TEXTO = COLOR_TEXTO_OSCURO
            else:
                COLOR_FONDO = COLOR_FONDO_CLARO
                COLOR_PANEL = COLOR_PANEL_CLARO
                COLOR_SIMPLE = COLOR_SIMPLE_CLARO
                COLOR_COMPUESTO = COLOR_COMPUESTO_CLARO
                COLOR_CAPITAL = COLOR_CAPITAL_CLARO
                COLOR_GRAFICA_FONDO = '#f9f9f9'
                COLOR_TEXTO = COLOR_TEXTO_CLARO
            
            # Validar inputs
            if principal <= 0 or tasa <= 0 or tiempo <= 0 or periodos <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser positivos.")
                return
            
            # Generar datos para la gráfica
            anios, valores_simple, valores_compuesto = self.generar_datos_para_grafica(
                principal, tasa, tiempo, periodos)
            
            # Limpiar la figura actual
            self.fig.clear()
            
            # Actualizar el color de fondo de la figura
            self.fig.patch.set_facecolor(COLOR_PANEL)
            
            # Crear un único gráfico que muestre toda la información
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor(COLOR_GRAFICA_FONDO)
            
            # Configurar colores de texto y ejes para el modo oscuro
            if modo_oscuro:
                self.ax.tick_params(colors=COLOR_TEXTO)
                self.ax.xaxis.label.set_color(COLOR_TEXTO)
                self.ax.yaxis.label.set_color(COLOR_TEXTO)
                self.ax.title.set_color(COLOR_TEXTO)
                self.ax.spines['bottom'].set_color(COLOR_TEXTO)
                self.ax.spines['left'].set_color(COLOR_TEXTO)
            
            # Añadir la línea del interés simple
            self.ax.plot(anios, valores_simple, color=COLOR_SIMPLE, linewidth=2.5, 
                        label='Interés Simple', linestyle='-')
            
            # Añadir la línea del interés compuesto
            self.ax.plot(anios, valores_compuesto, color=COLOR_COMPUESTO, linewidth=2.5, 
                        label='Interés Compuesto', linestyle='-')
            
            # Sombreado bajo las curvas para mostrar el área
            self.ax.fill_between(anios, valores_simple, color=COLOR_SIMPLE, alpha=0.2)
            self.ax.fill_between(anios, valores_compuesto, color=COLOR_COMPUESTO, alpha=0.2)
            
            # Línea horizontal para el capital inicial
            self.ax.axhline(y=principal, color=COLOR_CAPITAL, linestyle='--', linewidth=1.5, 
                         label='Capital Inicial')
            
            # Cálculos para montos finales
            monto_simple = self.calcular_interes_simple(principal, tasa, tiempo)
            monto_compuesto = self.calcular_interes_compuesto(principal, tasa, tiempo, periodos)
            interes_simple = monto_simple - principal
            interes_compuesto = monto_compuesto - principal
            diferencia = monto_compuesto - monto_simple
            
            # Mejorar la posición de las anotaciones para evitar superposición
            # Anotación para interés simple (posición hacia abajo)
            self.ax.annotate(f'${monto_simple:,.2f}', 
                         xy=(tiempo, monto_simple), 
                         xytext=(tiempo-2, monto_simple*0.93),  # Movido abajo
                         fontsize=9,
                         fontweight='bold',
                         color=COLOR_SIMPLE,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor=COLOR_PANEL, alpha=0.8),
                         arrowprops=dict(arrowstyle='->', color=COLOR_SIMPLE))
            
            # Anotación para interés compuesto (posición hacia arriba)
            self.ax.annotate(f'${monto_compuesto:,.2f}', 
                         xy=(tiempo, monto_compuesto), 
                         xytext=(tiempo-2, monto_compuesto*1.07),  # Movido arriba
                         fontsize=9,
                         fontweight='bold',
                         color=COLOR_COMPUESTO,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor=COLOR_PANEL, alpha=0.8),
                         arrowprops=dict(arrowstyle='->', color=COLOR_COMPUESTO))
            
            # Añadir texto para mostrar la diferencia en una posición clara
            self.ax.annotate(f'Diferencia: ${diferencia:,.2f}', 
                         xy=(tiempo/2, (monto_simple + monto_compuesto)/2), 
                         xytext=(tiempo/2, (monto_simple + monto_compuesto)/2 - (monto_compuesto - monto_simple)/4),
                         fontsize=10,
                         fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor=COLOR_PANEL, alpha=0.8),
                         ha='center')
            
            # Añadir información sobre el interés generado (separado para evitar superposición)
            self.ax.text(tiempo/8, principal*1.2, 
                      f'Interés Simple: ${interes_simple:,.2f}', 
                      fontsize=9, fontweight='bold', color=COLOR_SIMPLE,
                      bbox=dict(facecolor=COLOR_PANEL, alpha=0.8, pad=2))
            
            self.ax.text(tiempo/8, principal*1.35, 
                      f'Interés Compuesto: ${interes_compuesto:,.2f}', 
                      fontsize=9, fontweight='bold', color=COLOR_COMPUESTO,
                      bbox=dict(facecolor=COLOR_PANEL, alpha=0.8, pad=2))
            
            # Configurar títulos y etiquetas
            self.ax.set_title('Comparación: Interés Simple vs. Compuesto', fontsize=12, fontweight='bold')
            self.ax.set_xlabel('Años', fontsize=10)
            self.ax.set_ylabel('Monto ($)', fontsize=10)
            
            # Colocar la leyenda en una posición que no interfiera con los datos
            self.ax.legend(loc='upper left', framealpha=0.9, facecolor=COLOR_PANEL)
            
            # Ajustar la cuadrícula según el modo
            self.ax.grid(True, linestyle='--', alpha=0.5 if modo_oscuro else 0.7, color=COLOR_TEXTO if modo_oscuro else '#bbbbbb')
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            
            # Ajustar el rango del eje y para dejar espacio para etiquetas
            self.ax.set_ylim(principal * 0.8, monto_compuesto * 1.15)
            
            # Actualizar la tabla de resultados
            self.monto_simple_label.config(text=f"${monto_simple:,.2f}")
            self.monto_compuesto_label.config(text=f"${monto_compuesto:,.2f}")
            self.interes_simple_label.config(text=f"${interes_simple:,.2f}")
            self.interes_compuesto_label.config(text=f"${interes_compuesto:,.2f}")
            self.diferencia_label.config(text=f"${diferencia:,.2f}")
            
            # Redibujar la gráfica
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def limpiar(self):
        """Reinicia todos los valores a su estado por defecto."""
        self.capital.set(10000)
        self.tasa.set(5)
        self.tiempo.set(10)
        self.capitalizacion.set(1)
        self.actualizar_graficas()
    
    def mostrar_explicacion(self):
        """Muestra la ventana con explicación teórica de los conceptos."""
        explicacion_window = tk.Toplevel(self)
        explicacion_window.title("Conceptos Teóricos - Interés Simple y Compuesto")
        explicacion_window.geometry("750x600")
        
        modo_oscuro = self.modo_oscuro.get()
        COLOR_PANEL = COLOR_PANEL_OSCURO if modo_oscuro else COLOR_PANEL_CLARO
        COLOR_TEXTO = COLOR_TEXTO_OSCURO if modo_oscuro else COLOR_TEXTO_CLARO
        
        explicacion_window.configure(bg=COLOR_PANEL)
        
        # Crear un widget de texto con scroll
        frame = ttk.Frame(explicacion_window, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="CONCEPTOS FINANCIEROS BÁSICOS", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Notebook para organizar el contenido en pestañas
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Interés Simple
        tab_simple = ttk.Frame(notebook, padding=10)
        notebook.add(tab_simple, text="Interés Simple")
        
        scroll_simple = ttk.Scrollbar(tab_simple)
        scroll_simple.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_simple = tk.Text(tab_simple, wrap=tk.WORD, yscrollcommand=scroll_simple.set, 
                             font=("Helvetica", 11), bg=COLOR_PANEL, fg=COLOR_TEXTO)
        text_simple.pack(fill=tk.BOTH, expand=True)
        scroll_simple.config(command=text_simple.yview)
        
        simple_text = """
Interés Simple

El interés simple se calcula únicamente sobre el capital inicial. Los intereses generados en cada periodo no se suman al capital para el cálculo de los intereses futuros.

Fórmula:
M = P * (1 + r * t)

Donde:
- M = Monto final
- P = Principal (capital inicial)
- r = Tasa de interés (en forma decimal)
- t = Tiempo (en años)

Ejemplo:
Para $10,000 a una tasa anual del 5% durante 10 años:
M = $10,000 * (1 + 0.05 * 10) = $10,000 * 1.5 = $15,000

Características principales:
- Crecimiento lineal
- El interés es siempre el mismo en cada periodo
- Fácil de calcular
- Se usa principalmente en préstamos a corto plazo

Ejemplo gráfico:
Año 0: $10,000
Año 1: $10,000 + $500 = $10,500
Año 2: $10,000 + $1,000 = $11,000
Año 3: $10,000 + $1,500 = $11,500
...y así sucesivamente
        """
        text_simple.insert(tk.END, simple_text)
        text_simple.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
        
        # Pestaña de Interés Compuesto
        tab_compuesto = ttk.Frame(notebook, padding=10)
        notebook.add(tab_compuesto, text="Interés Compuesto")
        
        scroll_compuesto = ttk.Scrollbar(tab_compuesto)
        scroll_compuesto.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_compuesto = tk.Text(tab_compuesto, wrap=tk.WORD, yscrollcommand=scroll_compuesto.set, 
                                font=("Helvetica", 11), bg=COLOR_PANEL, fg=COLOR_TEXTO)
        text_compuesto.pack(fill=tk.BOTH, expand=True)
        scroll_compuesto.config(command=text_compuesto.yview)
        
        compuesto_text = """
Interés Compuesto

El interés compuesto se calcula sobre el capital inicial y sobre los intereses generados en períodos anteriores. Esto produce un efecto de "interés sobre interés" que resulta en un crecimiento exponencial.

Fórmula:
M = P * (1 + r/n)^(n*t)

Donde:
- M = Monto final
- P = Principal (capital inicial)
- r = Tasa de interés anual (en forma decimal)
- n = Número de veces que el interés se capitaliza por año
- t = Tiempo (en años)

Ejemplo:
Para $10,000 a una tasa anual del 5% durante 10 años, con capitalización anual (n=1):
M = $10,000 * (1 + 0.05/1)^(1*10) = $10,000 * (1.05)^10 = $10,000 * 1.6289 = $16,289

Características principales:
- Crecimiento exponencial
- El interés aumenta en cada periodo
- Es el tipo de interés más común en el mundo financiero
- Se usa en inversiones, hipotecas, créditos, etc.

Ejemplo gráfico con capitalización anual:
Año 0: $10,000
Año 1: $10,000 * 1.05 = $10,500
Año 2: $10,500 * 1.
Año 2: $10,500 * 1.05 = $11,025
Año 3: $11,025 * 1.05 = $11,576.25
...y así sucesivamente
        """
        text_compuesto.insert(tk.END, compuesto_text)
        text_compuesto.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
        
        # Pestaña de Comparación
        tab_comparacion = ttk.Frame(notebook, padding=10)
        notebook.add(tab_comparacion, text="Comparación")
        
        scroll_comparacion = ttk.Scrollbar(tab_comparacion)
        scroll_comparacion.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_comparacion = tk.Text(tab_comparacion, wrap=tk.WORD, yscrollcommand=scroll_comparacion.set, 
                                  font=("Helvetica", 11), bg=COLOR_PANEL, fg=COLOR_TEXTO)
        text_comparacion.pack(fill=tk.BOTH, expand=True)
        scroll_comparacion.config(command=text_comparacion.yview)
        
        comparacion_text = """
Comparación entre Interés Simple y Compuesto

La diferencia clave entre ambos tipos de interés es que:

- El interés simple genera un crecimiento lineal
- El interés compuesto genera un crecimiento exponencial

Esto explica por qué, a largo plazo, el interés compuesto siempre generará mayores rendimientos que el interés simple para las mismas condiciones iniciales.

Aplicaciones Prácticas:
- El interés simple suele usarse en préstamos a corto plazo, documentos comerciales y algunas cuentas bancarias.
- El interés compuesto se utiliza en la mayoría de instrumentos financieros como inversiones a plazo fijo, hipotecas, tarjetas de crédito y fondos de inversión.

Efecto de la frecuencia de capitalización:
Mientras mayor sea la frecuencia de capitalización (n) en el interés compuesto, mayor será el monto final. Los periodos más comunes son:

- Anual (n=1)
- Semestral (n=2)
- Trimestral (n=4)
- Mensual (n=12)
- Diario (n=365)

A medida que n tiende a infinito, el interés compuesto se acerca al interés continuo, cuya fórmula es:
M = P * e^(r*t)

Donde e es la constante de Euler (aproximadamente 2.71828).

La Regla del 72:
Un atajo mental para calcular aproximadamente cuánto tiempo tardará en duplicarse una inversión con interés compuesto:
Tiempo (años) ≈ 72 / Tasa de interés (%)

Ejemplo: Con una tasa del 6%, una inversión se duplica aproximadamente en 72/6 = 12 años.
        """
        text_comparacion.insert(tk.END, comparacion_text)
        text_comparacion.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
        
        # Botón para cerrar
        ttk.Button(frame, text="Cerrar", command=explicacion_window.destroy, width=15).pack(pady=10)

if __name__ == "__main__":
    app = CalculadoraIntereses()
    app.mainloop()
