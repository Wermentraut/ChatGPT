import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        estate = float(entry_estate.get())
        G = float(entry_G.get())

        alive_children = int(entry_alive_children.get())
        dead_children = int(entry_dead_children.get())
        grandchildren = int(entry_grandchildren.get())

        has_spouse = spouse_var.get()
        has_parents = parents_var.get()
        has_grandparents = grandparents_var.get()
        has_will = will_var.get()

        original_estate = estate
        distribution = {}
        laws_used = []
        info = ""

        total_branches = alive_children + dead_children

        # ==================================================
        # ✅ ЕСЛИ НЕТ ЗАВЕЩАНИЯ → ВСЁ СТРОГО ПО ЗАКОНУ
        # ==================================================
        if not has_will:

            # ✅ 1. СУПРУГ ПОЛУЧАЕТ ПЕРВЫМ
            if has_spouse:
                spouse_share = max(estate / 4, 4 * G)
                distribution["Супруг"] = round(spouse_share, 2)
                estate -= spouse_share
                laws_used.append("§ 8 Arveloven — доля супруга при наличии детей")

            # ✅ 2. ДЕТИ И ВНУКИ
            if total_branches > 0:
                branch_share = estate / total_branches

                if alive_children > 0:
                    distribution["Каждый живой ребёнок"] = round(branch_share, 2)
                    laws_used.append("§ 4 Arveloven — дети наследуют в первой очереди")

                if dead_children > 0 and grandchildren > 0:
                    per_grandchild = branch_share / grandchildren
                    distribution["Каждый внук"] = round(per_grandchild, 2)
                    laws_used.append("§ 5 Arveloven — внуки наследуют по праву представления")

                info = "✅ Сначала супруг, затем дети и внуки"

            # ✅ 3. РОДИТЕЛИ
            elif has_parents:
                distribution["Каждый родитель"] = round(estate / 2, 2)
                laws_used.append("§ 6 Arveloven — родители наследуют при отсутствии потомков")
                info = "✅ Наследуют родители"

            # ✅ 4. ДЕДУШКИ И БАБУШКИ
            elif has_grandparents:
                distribution["Каждый дедушка и бабушка"] = round(estate / 4, 2)
                laws_used.append("§ 7 Arveloven — дедушки и бабушки наследуют")
                info = "✅ Наследуют дедушки и бабушки"

            else:
                info = "⚠️ Наследников нет → имущество переходит государству"
                laws_used.append("§ 9 Arveloven — наследство государству")

        # ==================================================
        # ✅ ЕСЛИ ЗАВЕЩАНИЕ ЕСТЬ → 2/3 + 15G
        # ==================================================
        else:
            if total_branches > 0:
                pliktdel = estate * 2 / 3
                branch_share = pliktdel / total_branches
                limit_15G = 15 * G
                actual_branch = min(branch_share, limit_15G)

                if alive_children > 0:
                    distribution["Каждый живой ребёнок"] = round(actual_branch, 2)
                    laws_used.append("§ 50 Arveloven — обязательная доля детей")

                if dead_children > 0 and grandchildren > 0:
                    distribution["Каждый внук"] = round(actual_branch / grandchildren, 2)
                    laws_used.append("§ 5 Arveloven — внуки получают долю умершего")

                total_to_children = actual_branch * total_branches
                estate -= total_to_children
                laws_used.append("§ 51 Arveloven — ограничение 15G")

            if has_spouse:
                spouse_share = min(estate, 4 * G)
                distribution["Супруг"] = round(spouse_share, 2)
                estate -= spouse_share
                laws_used.append("§ 8 Arveloven — доля супруга")

            distribution["По завещанию"] = round(estate, 2)
            laws_used.append("§ 40 Arveloven — свобода завещания")
            info = "✅ Применено завещание с обязательными долями"

        # ==================================================
        # ✅ ВЫВОД
        # ==================================================
        output = "\n====== ИТОГ ======\n"
        output += f"Наследство: {original_estate:,.0f} NOK\n\n"

        for k, v in distribution.items():
            output += f"{k}: {v:,.0f} NOK\n"

        output += "\n-------------------\n"
        output += info + "\n\n"
        output += "📚 ПРИМЕНЁННЫЕ СТАТЬИ ЗАКОНА:\n"

        for law in laws_used:
            output += f"• {law}\n"

        label_result.config(text=output)

    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте все поля!")

# ================= GUI =================
root = tk.Tk()
root.title("Калькулятор наследства Норвегия 3.3 (исправленный супруг)")
root.geometry("820x950")

tk.Label(root, text="Сумма наследства (NOK):").pack()
entry_estate = tk.Entry(root)
entry_estate.pack()

tk.Label(root, text="Размер G (например 130000):").pack()
entry_G = tk.Entry(root)
entry_G.insert(0, "130000")
entry_G.pack()

tk.Label(root, text="Живые дети:").pack()
entry_alive_children = tk.Entry(root)
entry_alive_children.insert(0, "0")
entry_alive_children.pack()

tk.Label(root, text="Умершие дети:").pack()
entry_dead_children = tk.Entry(root)
entry_dead_children.insert(0, "0")
entry_dead_children.pack()

tk.Label(root, text="Внуки (от умерших детей):").pack()
entry_grandchildren = tk.Entry(root)
entry_grandchildren.insert(0, "0")
entry_grandchildren.pack()

spouse_var = tk.IntVar()
tk.Checkbutton(root, text="Есть супруг/супруга", variable=spouse_var).pack()

parents_var = tk.IntVar()
tk.Checkbutton(root, text="Есть родители", variable=parents_var).pack()

grandparents_var = tk.IntVar()
tk.Checkbutton(root, text="Есть дедушки и бабушки", variable=grandparents_var).pack()

will_var = tk.IntVar()
tk.Checkbutton(root, text="Есть завещание", variable=will_var).pack()

tk.Button(root, text="РАССЧИТАТЬ", command=calculate, height=2).pack(pady=12)

label_result = tk.Label(root, text="", justify="left", wraplength=780)
label_result.pack()

root.mainloop()
