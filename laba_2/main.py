import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["x", "y_exact", "y_euler", "y_rk4"])

        for i in range(len(x_values)):
            writer.writerow([
                f"{x_values[i]:.6f}",
                f"{exact_values[i]:.6f}",
                f"{euler_values[i]:.6f}",
                f"{rk_values[i]:.6f}",
            ])

    plt.plot(x_values, exact_values)
    plt.plot(x_values, euler_values)
    plt.plot(x_values, rk_values)
    plt.savefig(folder / "solution_plot.png")
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
