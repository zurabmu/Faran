from pathlib import Path

from tests.dsl import Backend, JaxBackend, MpccData, NumPyBackend, Visualize

from pytest import FixtureRequest, fixture


@fixture(params=[NumPyBackend(), JaxBackend()], ids=["numpy", "jax"])
def mpcc(request: FixtureRequest) -> MpccData:
    backend: Backend = request.param
    return MpccData(backend=backend)


@fixture
def visualize(tmp_path: Path) -> Visualize:
    return Visualize(directory=tmp_path)
