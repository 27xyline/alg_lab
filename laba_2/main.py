import csv
import math
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


A = 0.0
B = 1.0
H = 0.05
Y0 = 1.0
STEPS = int((B - A) / H)
RESULTS = Path(__file__).resolve().parent / 'results'


def f(x, y):
    return x * math.exp(-x * x) - 2 * x * y


def exact(x):
    return (1 + x * x / 2) * math.exp(-x * x)


def euler(x_values):
    y_values = [Y0]

    for i in range(1, len(x_values)):
        x = x_values[i - 1]
        y = y_values[-1]
        y_values.append(y + H * f(x, y))

    return y_values


def runge_kutta(x_values):
    y_values = [Y0]

    for i in range(1, len(x_values)):
        x = x_values[i - 1]
        y = y_values[-1]

        k1 = H * f(x, y)
        k2 = H * f(x + H / 2, y + k1 / 2)
        k3 = H * f(x + H / 2, y + k2 / 2)
        k4 = H * f(x + H, y + k3)

        y_values.append(y + (k1 + 2 * k2 + 2 * k3 + k4) / 6)

    return y_values


def main():
    folder = RESULTS
    x_values = [A + i * H for i in range(STEPS + 1)]

    exact_values = [exact(x) for x in x_values]
    euler_values = euler(x_values)
    rk_values = runge_kutta(x_values)

    with open(folder / "results.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y_exact", "y_euler", "y_rk4"])

        for i in range(len(x_values)):
            writer.writerow([
                f"{x_values[i]:.12f}",
                f"{exact_values[i]:.12f}",
                f"{euler_values[i]:.12f}",
                f"{rk_values[i]:.12f}",
            ])

    # Строим точную кривую и численные решения.
    smooth_x = [A + (B - A) * i / 500 for i in range(501)]
    smooth_y = [exact(x) for x in smooth_x]

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.figure(figsize=(9, 5.5))
    plt.plot(smooth_x, smooth_y, label="Точное решение", linewidth=2.4)
    plt.plot(x_values, euler_values, "o--", label="Метод Эйлера", markersize=3.5)
    plt.plot(x_values, rk_values, "s-", label="Рунге — Кутта 4-го порядка", markersize=3)
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.title("Численное решение задачи Коши, h = 0,05")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(folder / "solution_plot.png", dpi=180)
    plt.close()

    exact_b = exact(B)
    euler_error = abs(euler_values[-1] - exact_b)
    rk_error = abs(rk_values[-1] - exact_b)

    print(f"Точное y(1): {exact_b:.12f}")
    print(f"Эйлер:       {euler_values[-1]:.12f}; погрешность: {euler_error:.3g}")
    print(f"Рунге — Кутта: {rk_values[-1]:.12f}; погрешность: {rk_error:.3g}")
    print(f"Таблица: {folder / 'results.csv'}")
    print(f"График:   {folder / 'solution_plot.png'}")


if __name__ == "__main__":
    main()
