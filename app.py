import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import joblib
import pandas as pd

# ============================================================
# Car Price Prediction GUI
# Scrollable version - works on small laptop/desktop screens
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "model.pkl"
CAR_IMAGE = BASE_DIR / "car.png"

BG = "#0b1420"
CARD = "#121e2d"
CARD_2 = "#172333"
BORDER = "#304052"
TEXT = "#646668"
MUTED = "#c4ccd7"
BLUE = "#3d82ff"
GREEN = "#39d56a"

try:
    model = joblib.load(MODEL_FILE)
except Exception:
    model = None


def indian_currency(value):
    value = max(0, int(round(value)))
    s = str(value)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while rest:
        parts.append(rest[-2:])
        rest = rest[:-2]
    return ",".join(reversed(parts)) + "," + last3


def predict_price():
    if model is None:
        messagebox.showerror(
            "Model Missing",
            "model.pkl was not found or could not be loaded.\n\n"
            "First run:\npython train_model.py"
        )
        return

    try:
        values = {
            "Brand": brand_var.get(),
            "Year": int(year_var.get()),
            "Kilometers_Driven": float(km_var.get()),
            "Fuel_Type": fuel_var.get(),
            "Transmission": transmission_var.get(),
            "Owners": int(owners_var.get()),
            "Engine_CC": float(engine_var.get()),
            "Mileage_Kmpl": float(mileage_var.get()),
        }

        input_df = pd.DataFrame([values])
        price_lakh = float(model.predict(input_df)[0])
        price_rupees = price_lakh * 100000

        result_price.config(text=f"₹ {indian_currency(price_rupees)}")
        result_words.config(text="Estimated selling price based on entered car details")

        summary_left.config(
            text=(
                f"Brand                 : {values['Brand']}\n"
                f"Year of Manufacturing : {values['Year']}\n"
                f"Kilometers Driven     : {int(values['Kilometers_Driven']):,} km\n"
                f"Fuel Type             : {values['Fuel_Type']}\n"
                f"Transmission          : {values['Transmission']}\n"
                f"Number of Owners      : {values['Owners']}\n"
                f"Engine Capacity       : {int(values['Engine_CC'])} CC\n"
                f"Mileage               : {values['Mileage_Kmpl']:.1f} kmpl"
            )
        )

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
    except Exception as e:
        messagebox.showerror("Prediction Error", str(e))


def make_entry(parent, variable):
    return tk.Entry(
        parent,
        textvariable=variable,
        bg=CARD_2,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE,
        font=("Segoe UI", 11),
    )


# -------------------------
# Root window
# -------------------------
root = tk.Tk()
root.title("🚗 Car Price Prediction")

# Smaller default size so it fits common laptop screens.
root.geometry("1250x720")
root.minsize(850, 600)
root.configure(bg=BG)

# -------------------------
# Scrollable main canvas
# -------------------------
outer = tk.Frame(root, bg=BG)
outer.pack(fill="both", expand=True)

canvas = tk.Canvas(
    outer,
    bg=BG,
    highlightthickness=0,
    bd=0
)
scrollbar = ttk.Scrollbar(
    outer,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scroll_frame = tk.Frame(canvas, bg=BG)
canvas_window = canvas.create_window(
    (0, 0),
    window=scroll_frame,
    anchor="nw"
)


def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_scroll_frame(event):
    # Keep the content at least as wide as the visible canvas.
    canvas.itemconfigure(canvas_window, width=max(event.width, 850))


scroll_frame.bind("<Configure>", update_scrollregion)
canvas.bind("<Configure>", resize_scroll_frame)


def mouse_wheel(event):
    # Windows
    if event.delta:
        canvas.yview_scroll(int(-event.delta / 120), "units")
    else:
        canvas.yview_scroll(1 if event.num == 5 else -1, "units")


def bind_mousewheel(widget):
    widget.bind("<MouseWheel>", mouse_wheel)
    widget.bind("<Button-4>", mouse_wheel)
    widget.bind("<Button-5>", mouse_wheel)
    for child in widget.winfo_children():
        bind_mousewheel(child)


# ============================================================
# Header
# ============================================================
header = tk.Frame(scroll_frame, bg=BG)
header.pack(fill="x", padx=38, pady=(24, 14))

title_row = tk.Frame(header, bg=BG)
title_row.pack()

tk.Label(
    title_row,
    text="🚗",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI Emoji", 38)
).pack(side="left", padx=(0, 14))

tk.Label(
    title_row,
    text="Car Price Prediction",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 34, "bold")
).pack(side="left")

tk.Label(
    header,
    text="Enter the car details to predict the selling price",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 14)
).pack(pady=(5, 0))


# ============================================================
# Content - two cards
# ============================================================
content = tk.Frame(scroll_frame, bg=BG)
content.pack(fill="x", padx=38, pady=10)

content.grid_columnconfigure(0, weight=4, uniform="cards")
content.grid_columnconfigure(1, weight=6, uniform="cards")


# ============================================================
# LEFT CARD
# ============================================================
left = tk.Frame(
    content,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
    padx=18,
    pady=18
)
left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
left.grid_columnconfigure(0, weight=1)

tk.Label(
    left,
    text="🚙  Car Details",
    bg=CARD,
    fg=BLUE,
    font=("Segoe UI", 17, "bold"),
    anchor="w"
).grid(row=0, column=0, sticky="w", pady=(0, 18))

brand_var = tk.StringVar(value="Toyota")
year_var = tk.StringVar(value="2020")
km_var = tk.StringVar(value="35000")
fuel_var = tk.StringVar(value="Petrol")
transmission_var = tk.StringVar(value="Manual")
owners_var = tk.StringVar(value="1")
engine_var = tk.StringVar(value="1498")
mileage_var = tk.StringVar(value="17.0")


def field(parent, row, label, variable, values=None):
    tk.Label(
        parent,
        text=label,
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 10, "bold"),
        anchor="w"
    ).grid(row=row, column=0, sticky="w", pady=(0, 5))

    if values:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.TCombobox",
            fieldbackground=CARD_2,
            background=CARD_2,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=7,
            font=("Segoe UI", 11)
        )
        widget = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            style="Dark.TCombobox",
            width=25
        )
    else:
        widget = make_entry(parent, variable)

    widget.grid(
        row=row + 1,
        column=0,
        sticky="ew",
        pady=(0, 13),
        ipady=4
    )
    return widget


field(left, 1, "Car Brand", brand_var,
      ["Maruti", "Hyundai", "Tata", "Honda", "Toyota", "Mahindra", "Mercedes", "BMW", "KIA","MG"])
field(left, 3, "Year of Manufacturing", year_var,
      [str(y) for y in range(2026, 2010, -1)])
field(left, 5, "Kilometers Driven", km_var)
field(left, 7, "Fuel Type", fuel_var, ["Petrol", "Diesel", "CNG", "EV", "Hybrid"])
field(left, 9, "Transmission", transmission_var, ["Manual", "Automatic"])
field(left, 11, "Number of Owners", owners_var, ["1", "2", "3"])
field(left, 13, "Engine Capacity (CC)", engine_var)
field(left, 15, "Mileage (kmpl)", mileage_var)

predict_btn = tk.Button(
    left,
    text="▣  Predict Price",
    command=predict_price,
    bg=BLUE,
    fg="white",
    activebackground="#2f70df",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 13, "bold"),
    pady=10,
)
predict_btn.grid(row=17, column=0, sticky="ew", pady=(3, 0))


# ============================================================
# RIGHT CARD
# ============================================================
right = tk.Frame(
    content,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1,
    padx=24,
    pady=18
)
right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
right.grid_columnconfigure(0, weight=1)

tk.Label(
    right,
    text="▥  Prediction Output",
    bg=CARD,
    fg=GREEN,
    font=("Segoe UI", 17, "bold"),
    anchor="w"
).grid(row=0, column=0, sticky="w", pady=(0, 14))

tk.Label(
    right,
    text="Estimated Selling Price",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 14)
).grid(row=1, column=0, pady=(0, 3))

result_price = tk.Label(
    right,
    text="₹ 7,25,000",
    bg=CARD,
    fg=GREEN,
    font=("Segoe UI", 38, "bold")
)
result_price.grid(row=2, column=0, pady=(0, 0))

result_words = tk.Label(
    right,
    text="Estimated selling price based on entered car details",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 11)
)
result_words.grid(row=3, column=0, pady=(0, 12))


# -------------------------
# Car image panel
# -------------------------
image_frame = tk.Frame(right, bg="#343434", height=285)
image_frame.grid(row=4, column=0, sticky="ew", pady=(0, 18))
image_frame.grid_propagate(False)

car_photo = None

if CAR_IMAGE.exists():
    try:
        car_photo = tk.PhotoImage(file=str(CAR_IMAGE))

        # Scale very large PNGs down using PhotoImage subsample.
        max_width = 950
        max_height = 330
        iw = car_photo.width()
        ih = car_photo.height()

        factor = max(1, int(max(iw / max_width, ih / max_height)))
        if factor > 1:
            car_photo = car_photo.subsample(factor, factor)

        image_label = tk.Label(
            image_frame,
            image=car_photo,
            bg="#343434"
        )
        image_label.pack(fill="both", expand=True)
    except Exception:
        tk.Label(
            image_frame,
            text="🚗",
            bg="#343434",
            fg=TEXT,
            font=("Segoe UI", 70)
        ).pack(expand=True)
else:
    tk.Label(
        image_frame,
        text="🚗",
        bg="#343434",
        fg=TEXT,
        font=("Segoe UI", 70)
    ).pack(expand=True)


# -------------------------
# Summary panel
# -------------------------
summary_frame = tk.Frame(
    right,
    bg=CARD_2,
    highlightbackground=BORDER,
    highlightthickness=1,
    padx=16,
    pady=13
)
summary_frame.grid(row=5, column=0, sticky="ew")
summary_frame.grid_columnconfigure(0, weight=1)

tk.Label(
    summary_frame,
    text="☷  Input Summary",
    bg=CARD_2,
    fg=BLUE,
    font=("Segoe UI", 15, "bold"),
    anchor="w"
).grid(row=0, column=0, sticky="w", pady=(0, 10))

summary_left = tk.Label(
    summary_frame,
    text=(
        "Brand                 : Toyota\n"
        "Year of Manufacturing : 2020\n"
        "Kilometers Driven     : 35,000 km\n"
        "Fuel Type             : Petrol\n"
        "Transmission          : Manual\n"
        "Number of Owners      : 1\n"
        "Engine Capacity       : 1498 CC\n"
        "Mileage               : 17.0 kmpl"
    ),
    bg=CARD_2,
    fg=TEXT,
    justify="left",
    anchor="w",
    font=("Segoe UI", 10)
)
summary_left.grid(row=1, column=0, sticky="w")


# ============================================================
# Footer
# ============================================================
footer = tk.Frame(scroll_frame, bg=BG)
footer.pack(fill="x", pady=(12, 25))

tk.Label(
    footer,
    text="Model Accuracy: 91.35%",
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 13)
).pack()

tk.Label(
    footer,
    text="(Random Forest Regressor)",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(pady=(2, 0))


# Bind mouse wheel AFTER all widgets are created.
bind_mousewheel(scroll_frame)

# Start at top.
canvas.yview_moveto(0)

root.mainloop()
