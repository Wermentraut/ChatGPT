import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from pathlib import Path


MAX_CHILD = 1_950_000
MIN_SPOUSE_WITH_CHILDREN = 520_000
MIN_SPOUSE_NO_CHILDREN = 780_000


def calculate():
    try:
        marital = float(entry_marital.get().replace(",", "."))
        personal = float(entry_personal.get().replace(",", "."))
        children = int(entry_children.get())

        spouse_alive = spouse_var.get()
        has_testament = testament_var.get()

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа.")
        return

    # --- Наследственная масса ---
    if spouse_alive:
        estate = marital / 2 + personal
    else:
        estate = marital + personal

    # --- Обязательные доли ---
    forced_children = min(estate * 2 / 3, children * MAX_CHILD)

    forced_spouse = 0
    if spouse_alive:
        forced_spouse = (
            MIN_SPOUSE_WITH_CHILDREN if children > 0 else MIN_SPOUSE_NO_CHILDREN
        )

    free_part = estate - forced_children - forced_spouse
    if free_part < 0:
        free_part = 0

    shares = {}

    if children > 0:
        shares["Дети (обязательная доля)"] = forced_children

    if spouse_alive:
        shares["Супруг(а), минимум"] = forced_spouse

    # --- Завещание ---
    if has_testament and free_part > 0:
        testament_text = text_testament.get("1.0", tk.END).strip()
        total_percent = 0

        for line in testament_text.splitlines():
            if not line.strip():
                continue
            try:
                name, percent = line.split()
                percent = float(percent)
                shares[name] = free_part * percent / 100
                total_percent += percent
            except:
                messagebox.showerror(
                    "Ошибка",
                    "Завещание вводи в формате:\nИмя 50\nФонд 50",
                )
                return

        if total_percent > 100:
            messagebox.showerror("Ошибка", "Сумма процентов в завещании больше 100%.")
            return

    distributed = sum(shares.values())
    remaining = estate - distributed

    # --- Вывод результата ---
    result = f"Наследственная масса: {estate:,.2f} NOK\n\n"

    for k, v in shares.items():
        result += f"{k}: {v:,.2f} NOK\n"

    if remaining > 0:
        result += f"\nНераспределено: {remaining:,.2f} NOK\n"

    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result)


def save_report():
    content = text_result.get("1.0", tk.END).strip()
    if not content:
        messagebox.showerror("Ошибка", "Сначала сделай расчёт.")
        return

    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text file", "*.txt")],
        initialfile=f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
    )

    if not file:
        return

    with open(file, "w", encoding="utf-8") as f:
        f.write("ОТЧЁТ О РАСЧЁТЕ НАСЛЕДСТВА\n\n")
        f.write(content)

    messagebox.showinfo("Готово", f"Отчёт сохранён:\n{file}")


# ----------------- GUI -----------------

root = tk.Tk()
root.title("Калькулятор наследства (Норвегия)")
root.geometry("540x700")

tk.Label(root, text="Деньги в браке (NOK):").pack()
entry_marital = tk.Entry(root)
entry_marital.pack()

tk.Label(root, text="Личные деньги (NOK):").pack()
entry_personal = tk.Entry(root)
entry_personal.pack()

spouse_var = tk.BooleanVar()
tk.Checkbutton(root, text="Есть супруг(а)", variable=spouse_var).pack()

tk.Label(root, text="Сколько детей:").pack()
entry_children = tk.Entry(root)
entry_children.pack()

testament_var = tk.BooleanVar()
tk.Checkbutton(root, text="Есть завещание", variable=testament_var).pack()

tk.Label(root, text="Завещание (Имя Процент):").pack()
text_testament = tk.Text(root, height=6)
text_testament.pack()

btn_calc = tk.Button(root, text="РАССЧИТАТЬ", command=calculate)
btn_calc.pack(pady=10)

tk.Label(root, text="Результат:").pack()
text_result = tk.Text(root, height=12)
text_result.pack()

btn_save = tk.Button(root, text="СОХРАНИТЬ В ФАЙЛ", command=save_report)
btn_save.pack(pady=10)

root.mainloop()
