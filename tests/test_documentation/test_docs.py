from typing import (
    Sequence,
    Final,
    Protocol,
    get_protocol_members,
    runtime_checkable,
)
from types import ModuleType
from importlib import import_module
from pathlib import Path
from functools import lru_cache

from faran import Trajectory, MpccErrorMetricResult
from faran_visualizer import (
    RerunRenderer,
    MpccSimulationResult,
    visualizer,
    configure as configure_visualizer,
)

from docs.lab import dusk
from tests.utilities import VisualizationData, doc_example, project_root
from pytest import mark, fixture

EXAMPLES_DIRECTORY: Final = Path("docs/examples")


@fixture(scope="session", autouse=True)
def configure_visualization_output_directory() -> None:
    configure_visualizer(
        output_directory=project_root() / "docs" / "content" / "visualizations",
        theme=dusk,
        renderer=RerunRenderer(),
    )


class ExampleResult(Protocol):
    reached_goal: bool
    progress: float
    visualization: MpccSimulationResult
    tracking_errors: MpccErrorMetricResult
    collision_detected: bool


@runtime_checkable
class ExampleModule(Protocol):
    @property
    def SEED(self) -> str:
        """Key that the visualization of the example is saved under."""
        ...

    @property
    def REFERENCE(self) -> Trajectory:
        """Path that the vehicle follows."""
        ...

    @property
    def MAX_CONTOURING_ERROR(self) -> float:
        """Upper bound on the contouring error in meters, exclusive."""
        ...

    @property
    def MAX_LAG_ERROR(self) -> float:
        """Upper bound on the lag error in meters, exclusive."""
        ...

    @property
    def GOAL_FRACTION(self) -> float:
        """Fraction of the path length the vehicle must reach, between 0 and 1."""
        ...

    def create(self) -> Sequence[object]:
        """Builds the components that `run` takes, in the order it takes them."""
        ...

    def run(self, *components: object) -> ExampleResult:
        """Runs the simulation with the components from `create`."""
        ...


@lru_cache
def discover() -> Sequence[str]:
    """Return module paths for all numbered example scripts."""
    return [
        f"docs.examples.{path.stem}"
        for path in sorted(EXAMPLES_DIRECTORY.glob("[0-9]*.py"))
    ]


class extract:
    @staticmethod
    def module_id(module_path: str) -> str:
        return module_path.rsplit(".", 1)[-1]

    @staticmethod
    def missing_members(module: ModuleType) -> Sequence[str]:
        return sorted(
            member
            for member in get_protocol_members(ExampleModule)
            if not hasattr(module, member)
        )


def load(module_path: str) -> ExampleModule:
    module = import_module(module_path)

    assert isinstance(module, ExampleModule), (
        f"Module {module_path} does not define the members of ExampleModule. "
        f"Missing: {', '.join(extract.missing_members(module))}"
    )

    return module


@mark.parametrize(
    ["module_path"],
    [doc_example(path) for path in discover()],
    ids=[extract.module_id(path) for path in discover()],
)
@mark.visualize.with_args(visualizer.mpcc, lambda seed: seed)
@mark.filterwarnings("ignore:.*'obstacle_states'.*not.*data.*")
def test_that_documentation_example_produces_valid_plan(
    visualization: VisualizationData[MpccSimulationResult], module_path: str
) -> None:
    example = load(module_path)

    components = example.create()
    result = example.run(*components)

    configure_visualizer(
        output_directory=project_root() / "docs" / "content" / "visualizations",
        theme=dusk,
        renderer=RerunRenderer(),
    )
    visualization.data_is(result.visualization).seed_is(example.SEED)

    assert result.reached_goal, (
        f"Vehicle did not make sufficient progress along the path. "
        f"Final progress: {result.progress:.1f}, "
        f"expected >= {example.REFERENCE.path_length * example.GOAL_FRACTION:.1f}"
    )

    assert result.tracking_errors.max_contouring < example.MAX_CONTOURING_ERROR, (
        f"Max contouring error {result.tracking_errors.max_contouring:.2f} m "
        f"exceeds threshold {example.MAX_CONTOURING_ERROR:.2f} m"
    )

    assert result.tracking_errors.max_lag < example.MAX_LAG_ERROR, (
        f"Max lag error {result.tracking_errors.max_lag:.2f} m "
        f"exceeds threshold {example.MAX_LAG_ERROR:.2f} m"
    )

    assert not result.collision_detected, (
        "Vehicle collided with an obstacle during the simulation."
    )
