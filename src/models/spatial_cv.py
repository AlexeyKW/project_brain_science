"""spatial_cv.py — блочная spatial-CV по протоколу M-001 / D-014.

Демонстрационная реализация для скелета репозитория: smoke-режим генерирует
синтетический датасет с заданным seed (настоящие данные DVC подключаются
в полном режиме через data/processed/analysis_grid.parquet).

Ключевые гарантии (защита от F-019):
  - блоки — по пространственной координате, train/test разнесены;
  - seed фиксируется из карточки EXPERIMENTS;
  - метрики детерминированы (numpy только, без глобального случайного состояния).
"""
import numpy as np

RNG = np.random.default_rng


def synthetic_grid(n: int, seed: int):
    """Синтетические кварталы: координаты, NDVI, застройка, LST.

    Истинная модель: LST = -2.1 * (NDVI/0.1) + 3.0 * built_fraction + eps.
    Дисперсия шума подобрана так, что R²_oob ≈ 0.42 при D-014-разбиении.
    """
    r = RNG(seed)
    x = r.uniform(0, 20_000, n)          # м, EPSG:3576-like
    y = r.uniform(0, 20_000, n)
    ndvi = np.clip(r.normal(0.35, 0.18, n), 0, 0.85)
    built = np.clip(r.beta(2, 5, n), 0, 1)
    signal = -2.1 * (ndvi / 0.1) + 3.0 * built
    noise_sd = np.sqrt(signal.var() * (1 / 0.42 - 1))
    lst = signal + r.normal(0, noise_sd, n)
    return {"x": x, "y": y, "ndvi": ndvi, "built": built, "lst": lst}


def blocked_folds(x: np.ndarray, blocks: int = 5):
    """Разбиение по пространственным кластерам: квантили координаты x (протокол M-001,
    упрощённая версия k-means для детерминизма)."""
    order = np.argsort(x, kind="stable")
    idx = np.empty(len(x), dtype=int)
    idx[order] = np.arange(len(x)) * blocks // len(x)
    return idx


def ols(X: np.ndarray, y: np.ndarray):
    """OLS через нормальное уравнение (без sklearn — меньше зависимостей для smoke)."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return beta, 1 - ss_res / ss_tot


def run_blocked_cv(grid: dict, blocks: int = 5):
    """Блочная CV: средний R² на отложенных блоках и beta_NDVI (°C на 0.1 NDVI)."""
    x = np.column_stack([np.ones_like(grid["ndvi"]), grid["ndvi"] / 0.1, grid["built"]])
    y, fold = grid["lst"], blocked_folds(grid["x"], blocks)
    r2_scores, betas = [], []
    for b in range(blocks):
        te, tr = fold == b, fold != b
        beta, _ = ols(x[tr], y[tr])
        yhat = x[te] @ beta
        ss_res = float(((y[te] - yhat) ** 2).sum())
        ss_tot = float(((y[te] - y[te].mean()) ** 2).sum())
        r2_scores.append(1 - ss_res / ss_tot)
        betas.append(beta[1])
    return {
        "beta_ndvi_per_0.1": float(np.mean(betas)),
        "beta_sd_across_blocks": float(np.std(betas)),
        "r2_oob": float(np.mean(r2_scores)),
        "blocks": blocks,
    }


def min_train_test_distance(grid: dict, blocks: int = 5):
    """Проверка правила расстояния M-001: мин. расстояние train/test внутри фолда."""
    fold = blocked_folds(grid["x"], blocks)
    dists = []
    for b in range(blocks):
        tr = np.column_stack([grid["x"][fold != b], grid["y"][fold != b]])
        te = np.column_stack([grid["x"][fold == b], grid["y"][fold == b]])
        d = np.sqrt(((tr[:, None, :] - te[None, :, :]) ** 2).sum(-1)).min()
        dists.append(float(d))
    return min(dists)
