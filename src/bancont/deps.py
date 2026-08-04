"""Injectable app dependencies (forecast fetcher seam for tests)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from bancont.weather import fetch_bratislava_forecast


@dataclass
class AppDeps:
    forecast_fetcher: Callable[[], str] = field(default=fetch_bratislava_forecast)


_deps = AppDeps()


def get_deps() -> AppDeps:
    return _deps


def set_deps(deps: AppDeps) -> None:
    global _deps
    _deps = deps
