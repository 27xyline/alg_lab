import math
from pathlib import Path

import matplotlib.pyplot as plt

GRAVITY = 9.81
AIR_DENSITY = 1.2041
DRAG_FACTOR = 0.47
IRON_DENSITY = 7200
DIAMETER = 0.1
INITIAL_SPEED = 1000
ANGLE = math.radians(45)
STEP = 0.5
RESULTS = Path(__file__).resolve().parent / 'results'

def derivatives(state: tuple[float, ...], drag: float) -> tuple[float, ...]:
    """Производные координат и скоростей для заданного состояния."""
    _, _, vx, vy = state
    speed = math.hypot(vx, vy)
    return vx, vy, -drag * speed * vx, -drag * speed * vy - GRAVITY


def rk4_step(state: tuple[float, ...], drag: float, step: float) -> tuple[float, ...]:
    """Один шаг метода Рунге — Кутты четвёртого порядка."""
    k1 = derivatives(state, drag)
    k2 = derivatives(tuple(y + step * k / 2 for y, k in zip(state, k1)), drag)
    k3 = derivatives(tuple(y + step * k / 2 for y, k in zip(state, k2)), drag)
    k4 = derivatives(tuple(y + step * k for y, k in zip(state, k3)), drag)

    return tuple(
        y + step * (a + 2 * b + 2 * c + d) / 6
        for y, a, b, c, d in zip(state, k1, k2, k3, k4)
    )


def simulate_flight(drag: float) -> list[tuple[float, ...]]:
    """Рассчитать полёт от выстрела до падения на землю."""
    state = (
        0, 0, INITIAL_SPEED * math.cos(ANGLE), INITIAL_SPEED * math.sin(ANGLE)
    )
    time = 0.0
    points = [(time, *state)]

    while True:
        next_state = rk4_step(state, drag, STEP)

        if next_state[1] <= 0:
            # Оцениваем момент падения между последней и следующей точкой.
            fraction = state[1] / (state[1] - next_state[1])
            landing = [a + fraction * (b - a) for a, b in zip(state, next_state)]
            points.append((time + fraction * STEP, landing[0], 0, landing[2], landing[3]))
            return points

        time += STEP
        state = next_state
        points.append((time, *state))


def save_plot(
    filename: str,
    x_index: int,
    y_index: int,
    x_label: str,
    y_label: str,
    flights: list,
) -> None:
    """Сохранить графики с сопротивлением и без него."""
    figure, axes = plt.subplots(1, 2, figsize=(12, 5), layout='constrained')
    for axis, (name, color, points) in zip(axes, flights):
        axis.plot([p[x_index] for p in points], [p[y_index] for p in points], color=color)
        axis.set_title(name)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.grid(True)
        axis.set_xlim(left=0)
        axis.set_ylim(bottom=0)
    figure.savefig(RESULTS / filename)
    plt.close(figure)


def main() -> None:
    area = math.pi * DIAMETER**2 / 4
    mass = IRON_DENSITY * math.pi * DIAMETER**3 / 6  # Снаряд считается шаром.
    drag = DRAG_FACTOR * AIR_DENSITY * area / (2 * mass)

    flights = [
        ('Без сопротивления', 'blue', simulate_flight(0)),
        ('С сопротивлением', 'red', simulate_flight(drag)),
    ]
    for name, _, points in flights:
        print(f'{name}: время {points[-1][0]:.2f} с, дальность {points[-1][1]:.2f} м, '
              f'максимальная высота {max(p[2] for p in points):.2f} м')

    RESULTS.mkdir(exist_ok=True)
    save_plot('x1_of_t.svg', 0, 1, 'Время, с', 'Расстояние, м', flights)
    save_plot('x2_of_t.svg', 0, 2, 'Время, с', 'Высота, м', flights)
    save_plot('trajectory.svg', 1, 2, 'Расстояние, м', 'Высота, м', flights)
    print(f'Графики сохранены в {RESULTS}')


if __name__ == '__main__':
    main()
