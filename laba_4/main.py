"""Корреляционный и регрессионный анализ данных лабораторной работы № 4."""

from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent / "results"


def regression(x, y):
    """Ковариация и СКО рассчитаны с делением на n; МНК — с константой."""
    x_mean, y_mean = mean(x), mean(y)
    dx = [value - x_mean for value in x]
    dy = [value - y_mean for value in y]
    sxx = sum(value**2 for value in dx)
    syy = sum(value**2 for value in dy)
    sxy = sum(a * b for a, b in zip(dx, dy))
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    r = sxy / (sxx * syy) ** 0.5
    return sxy / len(x), (sxx / len(x)) ** 0.5, (syy / len(y)) ** 0.5, r, slope, intercept, r**2


def plot(x, y, slope, intercept, title, xlabel, ylabel, filename, forecast=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(x, y, label="Наблюдения")
    start, end = min(x), forecast if forecast is not None else max(x)
    ax.plot([start, end], [slope * start + intercept, slope * end + intercept],
            color="crimson", label=f"Регрессия: y = {slope:.3f}x {intercept:+.3f}")
    if forecast is not None:
        ax.scatter([forecast], [slope * forecast + intercept], color="darkorange",
                   marker="*", s=140, label="Прогноз на 2022 год", zorder=3)
        ax.plot(x, y, color="steelblue", alpha=0.4)
        r2 = regression(x, y)[-1]
        ax.text(0.03, 0.95, f"R² = {r2:.4f}", transform=ax.transAxes, va="top")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / filename, dpi=150)
    plt.close(fig)


def main():
    RESULTS.mkdir(exist_ok=True)
    x1 = [3.9, 6.5, 3.7, 4.5, 5.0, 5.8, 3.3, 6.2, 3.6, 3.9, 5.1, 6.4,
          4.2, 4.9, 6.0, 5.4, 4.4, 3.8, 6.7, 4.6, 4.3, 6.3, 5.2, 6.4,
          6.2, 5.5, 2.7, 2.8, 5.4, 5.8, 6.6, 5.3, 4.2, 4.3, 4.0, 5.4]
    y1 = [56, 55, 43, 55, 46, 54, 42, 63, 48, 45, 50, 58,
          50, 54, 52, 50, 60, 53, 63, 51, 45, 60, 48, 61,
          56, 46, 41, 43, 58, 60, 61, 55, 46, 53, 51, 56]
    x2 = [18, 22, 35, 28, 36, 24, 32, 38, 52, 46, 48, 54]
    y2 = [36, 47, 50, 44, 52, 48, 55, 51, 56, 60, 58, 65]
    years = list(range(2011, 2022))
    tourists = [13062, 14019, 14583, 15590, 20135, 20534, 25292, 28074, 28302, 27328, 28979]

    cov, sx, sy, r, a, b, r2 = regression(x1, y1)
    print(f"Задание 1: ковариация = {cov:.4f}, СКО X = {sx:.4f}, СКО Y = {sy:.4f}")
    print(f"r = {r:.4f}, y = {a:.4f}x {b:+.4f}, R² = {r2:.4f}")
    plot(x1, y1, a, b, "Содержание компонента и твёрдость", "Содержание компонента, %", "Твёрдость по Роквеллу", "task1.png")

    _, _, _, r, a, b, r2 = regression(x2, y2)
    print(f"\nЗадание 2: r = {r:.4f}, y = {a:.4f}x {b:+.4f}, R² = {r2:.4f}")
    print(f"При затратах 40 тыс. руб. доход = {a * 40 + b:.4f} млн руб.")
    print(f"Для дохода 70 млн руб. затраты = {(70 - b) / a:.4f} тыс. руб.")
    plot(x2, y2, a, b, "Расходы на рекламу и доход", "Расходы, тыс. руб.", "Доход, млн руб.", "task2.png")

    _, _, _, _, a, b, r2 = regression(years, tourists)
    forecast = a * 2022 + b
    print(f"\nЗадание 3: y = {a:.4f} × год {b:+.4f}, R² = {r2:.4f}")
    print(f"Прогноз на 2022 год = {forecast:.2f} тыс. чел.")
    print(f"Относительная погрешность = {abs(forecast - 29547) / 29547 * 100:.2f}%")
    plot(years, tourists, a, b, "Численность размещённых туристов", "Год", "Туристы, тыс. чел.", "task3.png", 2022)


if __name__ == "__main__":
    main()
