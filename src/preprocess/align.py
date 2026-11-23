"""align.py — выравнивание сеток DS-001 (SLSTR LST, 1 км) и DS-002 (OSM).

Единственное место перепроекции (X-06): площади — EPSG:3576, веб-карты — EPSG:3857,
исходные сцены — EPSG:32639. Другие модули не должны перепроецировать сами.

Полный прогон читает data/raw через DVC; см. DATA/DATACARDS/. Для smoke-режима
не используется (reproduce.py работает на синтетике spatial_cv.synthetic_grid).
"""
EPSG_SCENES = 32639   # UTM 39N, исходные Sentinel-сцены
EPSG_AREA = 3576      # Asia North Albers Equal Area — площади/буферы
EPSG_WEB = 3857       # веб-карты


def align(lst_path, osm_path, out_path, target_epsg=EPSG_AREA):
    """Выравнивание: репроекция в target_epsg, ресемплинг LST до сетки кварталов,
    маски воды/облаков (QC-канал, см. F-017), zonal stats."""
    raise NotImplementedError(
        "Подключите DVC-данные (DS-001, DS-002) и реализуйте по протоколу M-001. "
        "Smoke-режим CI не требует этого модуля."
    )
