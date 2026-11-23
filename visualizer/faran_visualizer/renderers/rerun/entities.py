from typing import Final


class entities:
    scene: Final = "scene"
    info: Final = "info"
    charts: Final = "charts"
    legend: Final = "legend"

    @staticmethod
    def rendering(name: str) -> str:
        return f"{entities.scene}/{name}"

    @staticmethod
    def chart(chart_id: str) -> str:
        return f"{entities.charts}/{chart_id}"

    @staticmethod
    def line(chart_id: str, *, index: int) -> str:
        return f"{entities.chart(chart_id)}/{index}"

    @staticmethod
    def legend_sample(row: int, *, index: int) -> str:
        return f"{entities.legend}/{row}/sample/{index}"

    @staticmethod
    def legend_label(row: int) -> str:
        return f"{entities.legend}/{row}/label"
