<div align="center">

# 🧱 Raycasting

**Реализация псевдо-3D рендеринга на основе техники бросания лучей (Raycasting)**

![Python](https://shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame-CE](https://shields.io/badge/Pygame--CE-2E8B57?style=for-the-badge&logo=python&logoColor=white)
![Poetry](https://shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![Ruff](https://shields.io/badge/Ruff-FCC21B?style=for-the-badge&logo=ruff&logoColor=black)
![Mypy](https://img.shields.io/badge/mypy-checked-1f425f?style=for-the-badge)

</div>

## 📄 Описание

Этот проект представляет собой собственную реализацию классического псевдо-3D рендеринга (в духе *Wolfenstein 3D*) на **Python** и **Pygame-CE**.

В основе лежит алгоритм **DDA (Digital Differential Analyzer)** для быстрого поиска пересечений лучей со стенами на двумерной сетке, а также математическая коррекция оптического искажения ("рыбьего глаза»).

## 📌 Скриншоты

<img src="./raycasting.png" alt="Демонстрация Raycasting">

## ✨ Возможности

* ⚡ **Алгоритм DDA** - быстрый и точный расчёт столкновений лучей со стенами без фиксированного шага.
* 👁️ **Коррекция "рыбьего глаза»** - проекция расстояний на плоскость камеры для устранения искажений перспективы.
* 🎮 **Плавное управление** - перемещение по карте и вращение камеры в реальном времени.
* 🧱 **Отрисовка сцены** - рендеринг стен с учётом расстояния и стороны столкновения.

## 🚀 Запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ksredkin/raycasting
cd raycasting
```

### 2. Установить зависимости

```bash
poetry install --only main
```

### 3. Запустить проект

```bash
poetry run python3 -m src.raycasting
```

## ⭐ Поддержка

Если проект оказался интересным или полезным - поставьте ⭐ на GitHub!
