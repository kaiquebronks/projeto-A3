import tkinter as tk
from tkinter import ttk, messagebox

janela = tk.Tk()
janela.title("Conversor de Unidades")
janela.geometry("700x700")
janela.configure(bg="#e8f0fb")
janela.resizable(False, False)

# ── Unidades por categoria ───────────────────────────────
unidades = {
    "Comprimento": ["Metro (m)", "Quilômetro (km)", "Centímetro (cm)", "Milímetro (mm)"],
    "Área":        ["Metro² (m²)", "Quilômetro² (km²)", "Centímetro² (cm²)", "Hectare (ha)"],
    "Peso":        ["Quilograma (kg)", "Grama (g)", "Miligrama (mg)", "Tonelada (t)"],
    "Temperatura": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
    "Tempo":       ["Segundo (s)", "Minuto (min)", "Hora (h)", "Dia (d)"],
}

# ── Função que atualiza os menus ─────────────────────────
def atualizar_menus(evento):
    categoria = menu_categoria.get()
    lista = unidades[categoria]
    menu_de["values"] = lista
    menu_para["values"] = lista
    menu_de.current(0)
    menu_para.current(1)
    label_resultado.config(text="Resultado: ---", fg="#64748b")

# ── Função de conversão ──────────────────────────────────
def converter():
    valor_digitado = campo_valor.get()

    if valor_digitado == "":
        messagebox.showerror("Erro", "Digite um valor!")
        return

    try:
        valor = float(valor_digitado)
    except ValueError:
        messagebox.showerror("Erro", "Digite apenas números!")
        return

    de   = menu_de.get()
    para = menu_para.get()
    cat  = menu_categoria.get()

    # Comprimento → base: metro
    if cat == "Comprimento":
        if de == "Metro (m)":           base = valor
        elif de == "Quilômetro (km)":   base = valor * 1000
        elif de == "Centímetro (cm)":   base = valor / 100
        elif de == "Milímetro (mm)":    base = valor / 1000

        if para == "Metro (m)":         resultado = base
        elif para == "Quilômetro (km)": resultado = base / 1000
        elif para == "Centímetro (cm)": resultado = base * 100
        elif para == "Milímetro (mm)":  resultado = base * 1000

    # Área → base: metro²
    elif cat == "Área":
        if de == "Metro² (m²)":             base = valor
        elif de == "Quilômetro² (km²)":     base = valor * 1_000_000
        elif de == "Centímetro² (cm²)":     base = valor / 10_000
        elif de == "Hectare (ha)":          base = valor * 10_000

        if para == "Metro² (m²)":           resultado = base
        elif para == "Quilômetro² (km²)":   resultado = base / 1_000_000
        elif para == "Centímetro² (cm²)":   resultado = base * 10_000
        elif para == "Hectare (ha)":        resultado = base / 10_000

    # Peso → base: quilograma
    elif cat == "Peso":
        if de == "Quilograma (kg)":     base = valor
        elif de == "Grama (g)":         base = valor / 1000
        elif de == "Miligrama (mg)":    base = valor / 1_000_000
        elif de == "Tonelada (t)":      base = valor * 1000

        if para == "Quilograma (kg)":   resultado = base
        elif para == "Grama (g)":       resultado = base * 1000
        elif para == "Miligrama (mg)":  resultado = base * 1_000_000
        elif para == "Tonelada (t)":    resultado = base / 1000

    # Temperatura (sem unidade base, conversão direta)
    elif cat == "Temperatura":
        if de == "Celsius (°C)":
            if para == "Celsius (°C)":      resultado = valor
            elif para == "Fahrenheit (°F)": resultado = valor * 9/5 + 32
            elif para == "Kelvin (K)":      resultado = valor + 273.15

        elif de == "Fahrenheit (°F)":
            if para == "Fahrenheit (°F)":   resultado = valor
            elif para == "Celsius (°C)":    resultado = (valor - 32) * 5/9
            elif para == "Kelvin (K)":      resultado = (valor - 32) * 5/9 + 273.15

        elif de == "Kelvin (K)":
            if para == "Kelvin (K)":        resultado = valor
            elif para == "Celsius (°C)":    resultado = valor - 273.15
            elif para == "Fahrenheit (°F)": resultado = (valor - 273.15) * 9/5 + 32

    # Tempo → base: segundo
    elif cat == "Tempo":
        if de == "Segundo (s)":         base = valor
        elif de == "Minuto (min)":      base = valor * 60
        elif de == "Hora (h)":          base = valor * 3600
        elif de == "Dia (d)":           base = valor * 86400

        if para == "Segundo (s)":       resultado = base
        elif para == "Minuto (min)":    resultado = base / 60
        elif para == "Hora (h)":        resultado = base / 3600
        elif para == "Dia (d)":         resultado = base / 86400

    # Formata o número (sem casas decimais desnecessárias)
    if resultado == int(resultado):
        resultado_fmt = str(int(resultado))
    else:
        resultado_fmt = f"{resultado:.4f}".rstrip("0")

    label_resultado.config(
        text=f"✔  {resultado_fmt}  {para}",
        fg="#1e40af"
    )

# ══════════════════════════════════════════════════════════
# INTERFACE
# ══════════════════════════════════════════════════════════

# ── Título ───────────────────────────────────────────────
frame_titulo = tk.Frame(janela, bg="#2563eb", pady=18)
frame_titulo.pack(fill="x")

tk.Label(
    frame_titulo,
    text="⚗  Conversor de Unidades",
    font=("Segoe UI", 18, "bold"),
    bg="#2563eb",
    fg="white"
).pack()

tk.Label(
    frame_titulo,
    text="Converta entre diferentes unidades facilmente",
    font=("Segoe UI", 9),
    bg="#2563eb",
    fg="#bfdbfe"
).pack()

# ── Card central ─────────────────────────────────────────
card = tk.Frame(janela, bg="white", padx=30, pady=25,
                highlightthickness=1, highlightbackground="#c7d9f5")
card.pack(padx=30, pady=25, fill="both")

# Categoria
tk.Label(card, text="Categoria", font=("Segoe UI", 9, "bold"),
         bg="white", fg="#64748b").grid(row=0, column=0, sticky="w", pady=(0, 4))

menu_categoria = ttk.Combobox(card, values=list(unidades.keys()),
                               state="readonly", width=34)
menu_categoria.current(0)
menu_categoria.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))
menu_categoria.bind("<<ComboboxSelected>>", atualizar_menus)

# Separador
tk.Frame(card, bg="#e2ecf8", height=1).grid(
    row=2, column=0, columnspan=2, sticky="ew", pady=(0, 14))

# Valor
tk.Label(card, text="Valor", font=("Segoe UI", 9, "bold"),
         bg="white", fg="#64748b").grid(row=3, column=0, sticky="w", pady=(0, 4))

campo_valor = tk.Entry(card, font=("Segoe UI", 13), relief="flat",
                       bg="#f8faff", fg="#1e293b",
                       highlightthickness=1, highlightbackground="#bfcfe8",
                       highlightcolor="#2563eb", width=35)
campo_valor.grid(row=4, column=0, columnspan=2, ipady=8,
                 sticky="ew", pady=(0, 14))

# De / Para
tk.Label(card, text="De", font=("Segoe UI", 9, "bold"),
         bg="white", fg="#64748b").grid(row=5, column=0, sticky="w", pady=(0, 4))

tk.Label(card, text="Para", font=("Segoe UI", 9, "bold"),
         bg="white", fg="#64748b").grid(row=5, column=1, sticky="w",
                                        padx=(10, 0), pady=(0, 4))

menu_de = ttk.Combobox(card, values=unidades["Comprimento"],
                        state="readonly", width=16)
menu_de.current(0)
menu_de.grid(row=6, column=0, ipady=4, sticky="ew", pady=(0, 18))

menu_para = ttk.Combobox(card, values=unidades["Comprimento"],
                          state="readonly", width=16)
menu_para.current(1)
menu_para.grid(row=6, column=1, ipady=4, sticky="ew",
               padx=(10, 0), pady=(0, 18))

# Botão converter
botao = tk.Button(
    card,
    text="Converter  ⇄",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb", fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    pady=8,
    command=converter
)
botao.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 16))

# Separador
tk.Frame(card, bg="#e2ecf8", height=1).grid(
    row=8, column=0, columnspan=2, sticky="ew", pady=(0, 12))

# Resultado
label_resultado = tk.Label(
    card,
    text="Resultado: ---",
    font=("Segoe UI", 14, "bold"),
    bg="white",
    fg="#64748b"
)
label_resultado.grid(row=9, column=0, columnspan=2)

card.columnconfigure(0, weight=1)
card.columnconfigure(1, weight=1)

# ── Estilo dos Comboboxes ────────────────────────────────
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TCombobox",
                 fieldbackground="#f8faff",
                 background="#f8faff",
                 foreground="#1e293b",
                 bordercolor="#bfcfe8",
                 arrowcolor="#0132f5",
                 padding=6)

janela.mainloop()