from typing import Final


class entities:
    scene: Final = "scene"
    info: Final = "info"
    charts: Final = "charts"

    @staticmethod
    def rendering(name: str) -> str:
        return f"{entities.scene}/{name}"

    @staticmethod
    def chart(chart_id: str) -> str:
        return f"{entities.charts}/{chart_id}"

    @staticmethod
    def line(chart_id: str, *, index: int) -> str:
        return f"{entities.chart(chart_id)}/{index}"
