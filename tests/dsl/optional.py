from typing import Callable, Sequence

from needy import needs
from pytest import MarkDecorator, mark


class probe:
    @staticmethod
    def jax() -> None:
        import jax as jax


class backends:
    @staticmethod
    def parametrize[CaseT](
        names: Sequence[str],
        *,
        numpy: Sequence[CaseT],
        jax: Callable[[], Sequence[CaseT]],
    ) -> MarkDecorator:
        """Parametrizes a test over the cases of every backend.

        The JAX cases are built only when JAX is installed, and are reported as
        skipped otherwise.
        """
        return mark.parametrize(
            names,
            [
                *numpy,
                *needs.to_run(probe.jax, cases=jax, arguments_per_case=len(names)),
            ],
        )
