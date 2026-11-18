from typing import Any, Sequence, Callable

from faran import (
    CollectorRegistry,
    Mppi,
    ObstacleStateObserver,
    StateSequence,
    NoCollectedDataWarning,
    collectors,
    access,
    types,
    model,
    obstacles,
)

from numtypes import array

import numpy as np

from tests.dsl import stubs, costs, planners, mppi as data
from pytest import mark, warns
from pytest_subtests import SubTests
from tests.dsl import backends


class test_that_collector_registry_discards_incomplete_data_for_time_step:
    @staticmethod
    def cases(data, types, collectors) -> Sequence[tuple]:
        states = data.state_batch(
            np.random.rand(T := 4, D_x := 5, M := 1),
        )
        obstacle_states = data.obstacle_2d_poses(
            x=(x_data := np.random.rand(T, K := 3)),
            y=(y_data := np.random.rand(T, K)),
            heading=(heading_data := np.random.rand(T, K)),
        )

        return [
            (
                registry := collectors.registry(
                    mppi := collectors.states.decorating(
                        stubs.Mppi.create(),
                        transformer=types.simple.state_sequence.of_states,
                    ),
                    # Can also be collected without a transformer
                    observer := collectors.obstacle_states.decorating(
                        stubs.ObstacleStateObserver.create()
                    ),
                ),
                mppi,
                observer,
                horizon := 4,
                nominal_input := data.control_input_sequence(
                    np.random.rand(T, D_u := 2)
                ),
                state_at := lambda t: states.at(time_step=t, rollout=0),
                obstacle_states_at := lambda t: obstacle_states.at(time_step=t),
                expected_states := lambda missing: [
                    states.at(time_step=t, rollout=0) for t in range(T - missing)
                ],
                expected_obstacle_states := lambda missing: [
                    obstacle_states.at(time_step=t) for t in range(T - missing)
                ],
            ),
        ]

    @backends.parametrize(
        [
            "registry",
            "mppi",
            "observer",
            "horizon",
            "nominal_input",
            "state_at",
            "obstacle_states_at",
            "expected_states",
            "expected_obstacle_states",
        ],
        numpy=cases(data=data.numpy, types=types.numpy, collectors=collectors.numpy),
        jax=lambda cases=cases: cases(
            data=data.jax, types=types.jax, collectors=collectors.jax
        ),
    )
    @mark.filterwarnings("error")
    def test[StateT, InputSequenceT, ObstacleStatesForTimeStepT](
        self,
        registry: CollectorRegistry,
        mppi: Mppi[StateT, InputSequenceT],
        observer: ObstacleStateObserver[ObstacleStatesForTimeStepT],
        horizon: int,
        nominal_input: InputSequenceT,
        state_at: Callable[[int], StateT],
        obstacle_states_at: Callable[[int], ObstacleStatesForTimeStepT],
        expected_states: Callable[[int], StateSequence],
        expected_obstacle_states: Callable[[int], Sequence[ObstacleStatesForTimeStepT]],
        subtests: SubTests,
    ) -> None:
        def mppi_step(step: int) -> None:
            mppi.step(
                temperature=1.0,
                nominal_input=nominal_input,
                initial_state=state_at(step),
            )

        def observe(step: int) -> None:
            observer.observe(obstacle_states_at(step))

        for step in range(horizon - 2):
            mppi_step(step)
            observe(step)

        with subtests.test("missing obstacle state"):
            mppi_step(horizon - 2)

            assert np.allclose(registry.data(access.states), expected_states(missing=2))
            assert np.allclose(
                registry.data(access.obstacle_states),
                expected_obstacle_states(missing=2),
            )

        with subtests.test("equal number of collected states and obstacle states"):
            observe(horizon - 2)

            assert np.allclose(registry.data(access.states), expected_states(missing=1))
            assert np.allclose(
                registry.data(access.obstacle_states),
                expected_obstacle_states(missing=1),
            )

        with subtests.test("missing state"):
            observe(horizon - 1)

            assert np.allclose(registry.data(access.states), expected_states(missing=1))
            assert np.allclose(
                registry.data(access.obstacle_states),
                expected_obstacle_states(missing=1),
            )

        with subtests.test("complete data"):
            mppi_step(horizon - 1)

            assert np.allclose(registry.data(access.states), expected_states(missing=0))
            assert np.allclose(
                registry.data(access.obstacle_states),
                expected_obstacle_states(missing=0),
            )


class test_that_collector_registry_emits_warnings_when_collectors_do_not_collect_data:
    @staticmethod
    def cases(data, collectors) -> Sequence[tuple]:
        states = data.state_batch(
            np.random.rand(T := 4, D_x := 5, M := 1),
        )

        return [
            (
                registry := collectors.registry(
                    mppi := collectors.states.decorating(stubs.Mppi.create()),
                    # This collector is registered, but it never collects any data.
                    # In such cases, the registry ignores this collector and only issues a warning.
                    collectors.controls.decorating(mppi),
                ),
                mppi,
                horizon := 4,
                nominal_input := data.control_input_sequence(
                    np.random.rand(T, D_u := 2)
                ),
                state_at := lambda t: states.at(time_step=t, rollout=0),
            ),
        ]

    @backends.parametrize(
        ["registry", "mppi", "horizon", "nominal_input", "state_at"],
        numpy=cases(data=data.numpy, collectors=collectors.numpy),
        jax=lambda cases=cases: cases(data=data.jax, collectors=collectors.jax),
    )
    def test[StateT, InputSequenceT, ObstacleStatesForTimeStepT](
        self,
        registry: CollectorRegistry,
        mppi: Mppi[StateT, InputSequenceT],
        horizon: int,
        nominal_input: InputSequenceT,
        state_at: Callable[[int], StateT],
    ) -> None:
        for step in range(horizon):
            mppi.step(
                temperature=1.0,
                nominal_input=nominal_input,
                initial_state=state_at(step),
            )

        with warns(NoCollectedDataWarning):
            registry.data(access.states)


class test_that_obstacle_state_collector_works_when_number_of_obstacles_varies:
    @staticmethod
    def cases(data, types, collectors) -> Sequence[tuple]:
        obstacle_states = [
            data.obstacle_2d_poses_for_time_step(
                x=array([0.0, 1.0], shape=(K_0 := 2,)),
                y=array([1.0, 2.0], shape=(K_0,)),
                heading=array([0.0, 3.0], shape=(K_0,)),
            ),
            data.obstacle_2d_poses_for_time_step(
                x=array([0.0, 1.0, 2.0], shape=(K_1 := 3,)),
                y=array([1.0, 2.0, 3.0], shape=(K_1,)),
                heading=array([0.0, 3.0, 6.0], shape=(K_1,)),
            ),
            data.obstacle_2d_poses_for_time_step(
                x=array([0.0], shape=(K_2 := 1,)),
                y=array([1.0], shape=(K_2,)),
                heading=array([0.0], shape=(K_2,)),
            ),
            data.obstacle_2d_poses_for_time_step(
                x=array([], shape=(K_3 := 0,)),
                y=array([], shape=(K_3,)),
                heading=array([], shape=(K_3,)),
            ),
        ]

        return [
            (
                registry := collectors.registry(
                    observer := collectors.obstacle_states.decorating(
                        stubs.ObstacleStateObserver.create(),
                        transformer=types.obstacle_2d_poses.of_states,
                    ),
                ),
                observer,
                horizon := (T := 4),
                obstacle_states_at := lambda t: obstacle_states[t],
                expected_obstacle_states := array(
                    [
                        [[0.0, 1.0, np.nan], [1.0, 2.0, np.nan], [0.0, 3.0, np.nan]],
                        [[0.0, 1.0, 2.0], [1.0, 2.0, 3.0], [0.0, 3.0, 6.0]],
                        [
                            [0.0, np.nan, np.nan],
                            [1.0, np.nan, np.nan],
                            [0.0, np.nan, np.nan],
                        ],
                        [
                            [np.nan, np.nan, np.nan],
                            [np.nan, np.nan, np.nan],
                            [np.nan, np.nan, np.nan],
                        ],
                    ],
                    shape=(T, D_o := 3, K := 3),
                ),
            ),
        ]

    @backends.parametrize(
        [
            "registry",
            "observer",
            "horizon",
            "obstacle_states_at",
            "expected_obstacle_states",
        ],
        numpy=cases(data=data.numpy, types=types.numpy, collectors=collectors.numpy),
        jax=lambda cases=cases: cases(
            data=data.jax, types=types.jax, collectors=collectors.jax
        ),
    )
    def test[ObstacleStatesForTimeStepT](
        self,
        registry: CollectorRegistry,
        observer: ObstacleStateObserver[ObstacleStatesForTimeStepT],
        horizon: int,
        obstacle_states_at: Callable[[int], ObstacleStatesForTimeStepT],
        expected_obstacle_states: Sequence[ObstacleStatesForTimeStepT],
    ) -> None:
        for step in range(horizon):
            observer.observe(obstacle_states_at(step))

        assert np.allclose(
            registry.data(access.obstacle_states),
            expected_obstacle_states,
            equal_nan=True,
        )


class test_that_collectors_collect_data:
    @staticmethod
    def cases(
        data, model, types, obstacles, planners, costs, collectors
    ) -> Sequence[tuple]:
        def controls() -> tuple:
            mppi = collectors.controls.decorating(stubs.Mppi.create())
            state = data.state(array([0.0], shape=(D_x := 1,)))
            inputs = [
                data.control_input_sequence(np.random.rand(T := 3, D_u := 2))
                for _ in range(2)
            ]

            return (
                registry := collectors.registry(mppi),
                collect := lambda step: mppi.step(
                    temperature=1.0, nominal_input=inputs[step], initial_state=state
                ),
                read := lambda registry: [
                    it.optimal for it in registry.data(access.controls.require())
                ],
                expected := inputs,
            )

        def trajectories() -> tuple:
            mppi = collectors.trajectories.decorating(
                stubs.Mppi.create(),
                model=model.integrator.dynamical(time_step_size=0.1),
            )
            no_input = data.control_input_sequence(np.zeros((T := 3, D_u := 1)))
            initial_states = [1.0, 2.0]

            return (
                registry := collectors.registry(mppi),
                collect := lambda step: mppi.step(
                    temperature=1.0,
                    nominal_input=no_input,
                    initial_state=data.state(
                        array([initial_states[step]], shape=(D_x := 1,))
                    ),
                ),
                read := lambda registry: [
                    (it.optimal, it.nominal)
                    for it in registry.data(access.trajectories.require())
                ],
                expected := [
                    (np.full((T, 1), state), np.full((T, 1), state))
                    for state in initial_states
                ],
            )

        def risks() -> tuple:
            metric = collectors.risk.decorating(
                stubs.RiskMetric.returns(risk := np.random.rand(T := 3, M := 4))
            )
            states = data.state_batch(np.random.rand(T, D_x := 3, M))
            obstacle_states = data.obstacle_2d_poses(
                x=np.random.rand(T, K := 2), y=np.random.rand(T, K)
            )
            sampler = stubs.ObstacleStateSampler.returns(
                data.obstacle_2d_pose_samples(
                    x=np.random.rand(T, K, N := 1), y=np.random.rand(T, K, N)
                ),
                when_obstacle_states_are=obstacle_states,
                and_sample_count_is=N,
            )

            def cost_function(*, states, samples):
                return np.zeros((T, M, N))

            return (
                registry := collectors.registry(metric),
                collect := lambda step: metric.compute(
                    cost_function,
                    states=states,
                    obstacle_states=obstacle_states,
                    sampler=sampler,
                ),
                read := lambda registry: registry.data(access.risks.require()),
                expected := [risk, risk],
            )

        def obstacle_observations() -> tuple:
            observer = collectors.obstacle_observations.decorating(
                stubs.ObstacleStateObserver.create()
            )
            observations = [
                data.obstacle_2d_poses_for_time_step(
                    x=np.random.rand(K := 3), y=np.random.rand(K)
                )
                for _ in range(2)
            ]

            return (
                registry := collectors.registry(observer),
                collect := lambda step: observer.observe(observations[step]),
                read := lambda registry: registry.data(
                    access.obstacle_observations.require()
                ),
                expected := observations,
            )

        def obstacle_forecasts() -> tuple:
            provider = collectors.obstacle_forecasts.decorating(
                stubs.ObstacleStateProvider.returns(
                    forecast := data.obstacle_2d_poses(
                        x=np.random.rand(T := 3, K := 2), y=np.random.rand(T, K)
                    )
                )
            )

            return (
                registry := collectors.registry(provider),
                collect := lambda step: provider(),
                read := lambda registry: registry.data(
                    access.obstacle_forecasts.require()
                ),
                expected := [forecast, forecast],
            )

        def risks_in_planner() -> tuple:
            metric = collectors.risk.decorating(
                stubs.RiskMetric.returns(risk := np.random.rand(T := 3, M := 2))
            )
            step_planner = planners.stepping_with(
                stubs.RiskComputingCostFunction.wrapping(
                    costs.energy(), computing_risk_with=metric
                )
            )

            return (
                registry := collectors.registry(metric),
                collect := lambda step: step_planner(),
                read := lambda registry: registry.data(access.risks.require()),
                expected := [risk, risk],
            )

        def obstacle_forecasts_in_planner() -> tuple:
            provider = obstacles.provider.predicting(
                predictor=stubs.EchoingObstacleMotionPredictor.create(),
                history=types.obstacle_states_running_history.empty(
                    creator=types.obstacle_2d_poses, horizon=1, obstacle_count=(K := 2)
                ),
            )
            forecasts = collectors.obstacle_forecasts.decorating(provider)
            step_planner = planners.stepping_with(
                stubs.ObstacleStatesReadingCostFunction.wrapping(
                    costs.energy(), reading_obstacle_states_from=forecasts
                )
            )
            poses = [np.random.rand(D_o := 3, K) for _ in range(2)]
            observations = [
                data.obstacle_2d_poses_for_time_step(x=x, y=y, heading=heading)
                for x, y, heading in poses
            ]

            def observe_and_step(step: int) -> None:
                provider.observe(observations[step])
                step_planner()

            return (
                registry := collectors.registry(forecasts),
                collect := observe_and_step,
                read := lambda registry: registry.data(
                    access.obstacle_forecasts.require()
                ),
                expected := [
                    data.obstacle_2d_poses(
                        x=x[np.newaxis], y=y[np.newaxis], heading=heading[np.newaxis]
                    )
                    for x, y, heading in poses
                ],
            )

        return [
            controls(),
            trajectories(),
            risks(),
            obstacle_observations(),
            obstacle_forecasts(),
            risks_in_planner(),
            obstacle_forecasts_in_planner(),
        ]

    @backends.parametrize(
        ["registry", "collect", "read", "expected"],
        numpy=cases(
            data=data.numpy,
            model=model.numpy,
            types=types.numpy,
            obstacles=obstacles.numpy,
            planners=planners.numpy,
            costs=costs.numpy,
            collectors=collectors.numpy,
        ),
        jax=lambda cases=cases: cases(
            data=data.jax,
            model=model.jax,
            types=types.jax,
            obstacles=obstacles.jax,
            planners=planners.jax,
            costs=costs.jax,
            collectors=collectors.jax,
        ),
    )
    def test_that_data_from_every_step_is_collected(
        self,
        registry: CollectorRegistry,
        collect: Callable[[int], Any],
        read: Callable[[CollectorRegistry], Sequence[Any]],
        expected: Sequence[Any],
    ) -> None:
        for step in range(len(expected)):
            collect(step)

        assert np.allclose(read(registry), expected)

    @backends.parametrize(
        ["registry", "collect", "read", "expected"],
        numpy=cases(
            data=data.numpy,
            model=model.numpy,
            types=types.numpy,
            obstacles=obstacles.numpy,
            planners=planners.numpy,
            costs=costs.numpy,
            collectors=collectors.numpy,
        ),
        jax=lambda cases=cases: cases(
            data=data.jax,
            model=model.jax,
            types=types.jax,
            obstacles=obstacles.jax,
            planners=planners.jax,
            costs=costs.jax,
            collectors=collectors.jax,
        ),
    )
    def test_that_new_data_is_collected_in_registry_when_registry_data_was_previously_read(
        self,
        registry: CollectorRegistry,
        collect: Callable[[int], Any],
        read: Callable[[CollectorRegistry], Sequence[Any]],
        expected: Sequence[Any],
    ) -> None:
        for step in range(len(expected)):
            collect(step)
            read(registry)

        assert np.allclose(read(registry), expected)
