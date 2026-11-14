from typing import Sequence, Callable, Protocol
from functools import partial

from faran import (
    mppi as create_mppi,
    model as create_model,
    costs as create_costs,
    obstacles as create_obstacles,
    risk as create_risk,
    trajectory as create_trajectory,
    types,
    UntracedStateError,
)
from faran.jax import register

from numtypes import array

import numpy as np
from numpy.typing import ArrayLike
import jax
import jax.numpy as jnp
from flax import nnx

from tests.dsl import mppi as data, costs, stubs
from pytest import mark, raises


class CompileFunction(Protocol):
    def __call__[C: Callable](self, function: C) -> C:
        """Returns a compiled version of the given function."""
        ...


class test_that_types_can_be_used_in_compiled_functions:
    @staticmethod
    def cases(
        types,
        create_mppi,
        create_model,
        create_costs,
        create_obstacles,
        create_risk,
        create_trajectory,
        data,
        costs,
    ) -> Sequence[tuple]:
        rng = np.random.default_rng(seed=0)

        def bicycle_cases() -> list[tuple]:
            return [
                (
                    types.bicycle.state.create(x=1.0, y=2.0, heading=0.5, speed=3.0),
                    lambda state: state.x_scalar + state.speed_scalar,
                    expected := 4.0,
                ),
                (
                    types.bicycle.state_sequence.of_states(
                        [
                            types.bicycle.state.create(
                                x=1.0, y=2.0, heading=0.5, speed=3.0
                            ),
                            types.bicycle.state.create(
                                x=4.0, y=5.0, heading=0.0, speed=1.0
                            ),
                        ]
                    ),
                    lambda states: states.array * 2.0,
                    expected := array(
                        [
                            [2.0, 4.0, 1.0, 6.0],
                            [8.0, 10.0, 0.0, 2.0],
                        ],
                        shape=(T := 2, D_x := 4),
                    ),
                ),
                (
                    types.bicycle.state_batch.wrap(
                        jnp.asarray(input := rng.random((T := 2, D_x := 4, M := 3)))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.bicycle.state_batch.wrap(
                        jnp.asarray(states := rng.random((T := 2, D_x := 4, M := 3)))
                    ).positions,
                    lambda positions: positions.y_array * 2.0,
                    expected := 2.0 * states[:, 1, :],
                ),
                (
                    types.bicycle.control_input_sequence(
                        jnp.array([[1.0, 2.0], [3.0, 4.0]])
                    ),
                    lambda inputs: inputs.similar(array=inputs.array * 2.0),
                    expected := array(
                        [[2.0, 4.0], [6.0, 8.0]], shape=(T := 2, D_u := 2)
                    ),
                ),
                (
                    types.bicycle.control_input_batch.create(
                        array=(input := rng.random((T := 2, D_u := 2, M := 3)))
                    ),
                    lambda inputs: inputs.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.bicycle.obstacle_states.wrap(
                        input := rng.random((D_o := 4, K := 2))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.bicycle.obstacle_state_sequences.wrap(
                        array=jnp.asarray(rng.random((T := 2, D_o := 6, K := 2))),
                        covariance=jnp.asarray(
                            covariance := rng.random((T, D_o, D_o, K))
                        ),
                    ),
                    lambda sequences: sequences.covariance_array * 2.0,
                    expected := 2.0 * covariance,
                ),
                (
                    types.bicycle.obstacle_inputs.create(
                        accelerations=(accelerations := rng.random(K := 2)),
                        steering_angles=rng.random(K),
                    ),
                    lambda inputs: inputs.accelerations_array * 2.0,
                    expected := 2.0 * accelerations,
                ),
            ]

        def unicycle_cases() -> list[tuple]:
            return [
                (
                    types.unicycle.state.create(x=1.0, y=2.0, heading=0.5),
                    lambda state: state.x_scalar + state.y_scalar,
                    expected := 3.0,
                ),
                (
                    types.unicycle.state_sequence.of_states(
                        [
                            types.unicycle.state.create(x=1.0, y=2.0, heading=0.5),
                            types.unicycle.state.create(x=4.0, y=5.0, heading=0.0),
                        ]
                    ),
                    lambda states: states.array * 2.0,
                    expected := array(
                        [[2.0, 4.0, 1.0], [8.0, 10.0, 0.0]], shape=(T := 2, D_x := 3)
                    ),
                ),
                (
                    types.unicycle.state_batch.wrap(
                        jnp.asarray(input := rng.random((T := 2, D_x := 3, M := 3)))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.unicycle.state_batch.wrap(
                        jnp.asarray(states := rng.random((T := 2, D_x := 3, M := 3)))
                    ).positions,
                    lambda positions: positions.x_array * 2.0,
                    expected := 2.0 * states[:, 0, :],
                ),
                (
                    types.unicycle.control_input_sequence(
                        jnp.array([[1.0, 2.0], [3.0, 4.0]])
                    ),
                    lambda inputs: inputs.similar(array=inputs.array * 2.0),
                    expected := array(
                        [[2.0, 4.0], [6.0, 8.0]], shape=(T := 2, D_u := 2)
                    ),
                ),
                (
                    types.unicycle.control_input_batch.create(
                        array=(input := rng.random((T := 2, D_u := 2, M := 3)))
                    ),
                    lambda inputs: inputs.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.unicycle.obstacle_states.create(
                        x=(x := rng.random(K := 2)),
                        y=rng.random(K),
                        heading=rng.random(K),
                    ),
                    lambda states: states.array[0] * 2.0,
                    expected := 2.0 * x,
                ),
                (
                    types.unicycle.obstacle_state_sequences.wrap(
                        array=jnp.asarray(rng.random((T := 2, D_o := 5, K := 2))),
                        covariance=jnp.asarray(
                            covariance := rng.random((T, D_o, D_o, K))
                        ),
                    ),
                    lambda sequences: sequences.covariance_array * 2.0,
                    expected := 2.0 * covariance,
                ),
                (
                    types.unicycle.obstacle_inputs.create(
                        linear_velocities=(linear_velocities := rng.random(K := 2)),
                        angular_velocities=rng.random(K),
                    ),
                    lambda inputs: inputs.linear_velocities_array * 2.0,
                    expected := 2.0 * linear_velocities,
                ),
            ]

        def simple_cases() -> list[tuple]:
            return [
                (
                    types.simple.state.create(
                        array([1.0, 2.0, 3.0], shape=(D_x := 3,))
                    ),
                    lambda state: jnp.sum(state.array),
                    expected := 6.0,
                ),
                (
                    types.simple.state_sequence.of_states(
                        [
                            types.simple.state.create(array([1.0], shape=(D_x := 1,))),
                            types.simple.state.create(array([2.0], shape=(D_x,))),
                        ]
                    ),
                    lambda states: states.array * 2.0,
                    expected := array([[2.0], [4.0]], shape=(T := 2, D_x)),
                ),
                (
                    types.simple.state_batch.wrap(
                        input := rng.random((T := 2, D_x := 3, M := 3))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.simple.control_input_sequence.create(
                        array([[1.0], [2.0]], shape=(T := 2, D_u := 1))
                    ),
                    lambda inputs: inputs.similar(array=inputs.array * 2.0),
                    expected := array([[2.0], [4.0]], shape=(T, D_u)),
                ),
                (
                    types.simple.control_input_batch.create(
                        input := rng.random((T := 2, D_u := 2, M := 3))
                    ),
                    lambda inputs: inputs.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.simple.costs(
                        jnp.asarray(input := rng.random((T := 2, M := 3)))
                    ),
                    lambda costs: costs.similar(array=costs.array * 2.0),
                    expected := 2.0 * input,
                ),
                (
                    types.simple.obstacle_states_for_time_step.create(
                        input := rng.random((D_o := 2, K := 2))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.simple.obstacle_states.create(
                        states=(input := rng.random((T := 2, D_o := 2, K := 2)))
                    ),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.simple.obstacle_states.create(
                        states=rng.random((T := 2, D_o := 2, K := 2)),
                        covariance=(covariance := rng.random((T, D_o, D_o, K))),
                    ),
                    lambda states: states.covariance_array * 2.0,
                    expected := 2.0 * covariance,
                ),
                (
                    types.simple.obstacle_states.create(
                        states=(states := rng.random((T := 2, D_o := 2, K := 2)))
                    ).single(),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * states[..., np.newaxis],
                ),
            ]

        def integrator_cases() -> list[tuple]:
            estimate = create_model.integrator.estimator.finite_difference(
                time_step_size=0.1
            ).estimate_from(
                types.simple.obstacle_states.create(
                    states=array(
                        [[[1.0, 2.0]], [[1.5, 2.0]]], shape=(T := 2, D_o := 1, K := 2)
                    )
                )
            )

            return [
                (
                    estimate.states,
                    lambda states: states.array * 2.0,
                    expected := array([[3.0, 4.0]], shape=(D_o, K)),
                ),
                (
                    estimate.inputs,
                    lambda inputs: inputs.array * 2.0,
                    expected := array([[10.0, 0.0]], shape=(D_o, K)),
                ),
                (
                    create_model.integrator.obstacle(
                        time_step_size=0.1, state_dimension=D_o
                    ).forward(
                        states=estimate.states,
                        inputs=estimate.inputs,
                        covariances=None,
                        horizon=T,
                    ),
                    lambda sequences: sequences.array,
                    expected := array(
                        [[[2.0, 2.0], [5.0, 0.0]], [[2.5, 2.0], [5.0, 0.0]]],
                        shape=(T, D_x := 2, K),
                    ),
                ),
            ]

        def augmented_cases() -> list[tuple]:
            return [
                (
                    types.augmented.state.of(
                        physical=types.bicycle.state.create(
                            x=1.0, y=2.0, heading=0.5, speed=3.0
                        ),
                        virtual=types.simple.state.create(
                            array([5.0], shape=(D_x := 1,))
                        ),
                    ),
                    lambda state: state.virtual,
                    expected := array([5.0], shape=(D_x,)),
                ),
                (
                    types.augmented.state_sequence.of(
                        physical=types.bicycle.state_sequence.of_states(
                            [
                                types.bicycle.state.create(
                                    x=1.0, y=2.0, heading=0.5, speed=3.0
                                )
                            ]
                        ),
                        virtual=types.simple.state_sequence.of_states(
                            [types.simple.state.create(array([5.0], shape=(1,)))]
                        ),
                    ),
                    lambda sequence: sequence.virtual.array * 2.0,
                    expected := array([[10.0]], shape=(T := 1, D_x := 1)),
                ),
                (
                    types.augmented.state_batch.of(
                        physical=types.bicycle.state_batch.wrap(
                            jnp.asarray(rng.random((T := 2, 4, M := 3)))
                        ),
                        virtual=types.simple.state_batch.wrap(
                            virtual := rng.random((T, D_x := 1, M))
                        ),
                    ),
                    lambda states: states.virtual.array * 2.0,
                    expected := 2.0 * virtual,
                ),
                (
                    types.augmented.control_input_sequence.of(
                        physical=types.bicycle.control_input_sequence(
                            jnp.array([[1.0, 2.0], [3.0, 4.0]])
                        ),
                        virtual=types.simple.control_input_sequence.create(
                            array([[5.0], [6.0]], shape=(T := 2, D_u := 1))
                        ),
                    ),
                    lambda inputs: inputs.similar(array=inputs.array * 2.0),
                    expected := array(
                        [[2.0, 4.0, 10.0], [6.0, 8.0, 12.0]], shape=(T, D_u := 3)
                    ),
                ),
                (
                    types.augmented.control_input_batch.of(
                        physical=types.bicycle.control_input_batch.create(
                            array=rng.random((T := 2, 2, M := 3))
                        ),
                        virtual=types.simple.control_input_batch.create(
                            virtual := rng.random((T, D_u := 1, M))
                        ),
                    ),
                    lambda inputs: inputs.virtual.array * 2.0,
                    expected := 2.0 * virtual,
                ),
            ]

        def obstacle_cases() -> list[tuple]:
            poses = types.obstacle_2d_poses.create(
                x=(x := rng.random((T := 2, K := 2))),
                y=(y := rng.random((T, K))),
                heading=(heading := rng.random((T, K))),
            )
            poses_for_time_step = types.obstacle_2d_poses_for_time_step.create(
                x=(x_for_time_step := rng.random(K)),
                y=(y_for_time_step := rng.random(K)),
                heading=(heading_for_time_step := rng.random(K)),
            )
            sampled_poses = types.obstacle_2d_poses.sampled(
                x=(sampled_x := rng.random((T, K, N := 4))),
                y=(sampled_y := rng.random((T, K, N))),
                heading=(sampled_heading := rng.random((T, K, N))),
            )

            return [
                (poses, lambda poses: poses.x_array * 2.0, expected := 2.0 * x),
                (
                    types.obstacle_2d_poses.create(
                        x=x,
                        y=y,
                        heading=heading,
                        covariance=(covariance := rng.random((T, 3, 3, K))),
                    ),
                    lambda poses: poses.covariance_array * 2.0,
                    expected := 2.0 * covariance,
                ),
                (
                    poses.positions(),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * np.stack([x, y], axis=1),
                ),
                (
                    poses.headings(),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * heading[:, np.newaxis, :],
                ),
                (
                    poses_for_time_step,
                    lambda poses: poses.heading_array * 2.0,
                    expected := 2.0 * heading_for_time_step,
                ),
                (
                    poses_for_time_step.positions(),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * np.stack([x_for_time_step, y_for_time_step]),
                ),
                (
                    poses_for_time_step.headings(),
                    lambda states: states.array * 2.0,
                    expected := 2.0 * heading_for_time_step[np.newaxis, :],
                ),
                (
                    sampled_poses,
                    lambda poses: poses.y_array * 2.0,
                    expected := 2.0 * sampled_y,
                ),
                (
                    sampled_poses.positions(),
                    lambda positions: positions.x_array * 2.0,
                    expected := 2.0 * sampled_x,
                ),
                (
                    sampled_poses.headings(),
                    lambda headings: headings.heading_array * 2.0,
                    expected := 2.0 * sampled_heading,
                ),
                (
                    types.obstacle_ids.create(ids=(input := np.array([3, 7]))),
                    lambda ids: ids.array * 2,
                    expected := 2 * input,
                ),
            ]

        def trajectory_cases() -> list[tuple]:
            return [
                (
                    types.path_parameters(input := rng.random((T := 2, M := 3))),
                    lambda params: params.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.positions(
                        x=(x := rng.random((T := 2, M := 3))), y=rng.random((T, M))
                    ),
                    lambda positions: positions.x_array * 2.0,
                    expected := 2.0 * x,
                ),
                (
                    types.headings(heading=(heading := rng.random((T := 2, M := 3)))),
                    lambda headings: headings.heading_array * 2.0,
                    expected := 2.0 * heading,
                ),
                (
                    types.reference_points(
                        x=rng.random((T := 2, M := 3)),
                        y=(y := rng.random((T, M))),
                        heading=rng.random((T, M)),
                    ),
                    lambda points: points.y_array * 2.0,
                    expected := 2.0 * y,
                ),
                (
                    types.lateral_positions(input := rng.random((T := 2, M := 3))),
                    lambda positions: positions.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.longitudinal_positions(input := rng.random((T := 2, M := 3))),
                    lambda positions: positions.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.normals(
                        x=(x := rng.random((T := 2, M := 3))), y=rng.random((T, M))
                    ),
                    lambda normals: normals.array[:, 0] * 2.0,
                    expected := 2.0 * x,
                ),
            ]

        def cost_cases() -> list[tuple]:
            return [
                (
                    types.distance.create(
                        array=(input := rng.random((T := 2, V := 1, M := 3, N := 4)))
                    ),
                    lambda distances: distances.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.boundary_distance.create(
                        array=(input := rng.random((T := 2, M := 3)))
                    ),
                    lambda distances: distances.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    types.preference(input := rng.random(M := 3)),
                    lambda preferences: preferences.array * 2.0,
                    expected := 2.0 * input,
                ),
                (
                    create_costs.tracking.contouring(
                        reference=create_trajectory.waypoints(
                            points=array([[0.0, 0.0], [10.0, 0.0]], shape=(2, 2)),
                            path_length=10.0,
                        ),
                        path_parameter_extractor=lambda states: types.path_parameters(
                            states.array[:, 0, :]
                        ),
                        position_extractor=lambda states: types.positions(
                            x=states.array[:, 1, :], y=states.array[:, 2, :]
                        ),
                        weight=1.0,
                    ).error(
                        states=types.simple.state_batch.wrap(
                            array(
                                [[[5.0], [5.0], [2.0]]],
                                shape=(T := 1, D_x := 3, M := 1),
                            )
                        )
                    ),
                    lambda errors: errors.array * 2.0,
                    expected := array([[-4.0]], shape=(T, M)),
                ),
                (
                    create_risk.none().compute(
                        lambda *, states, samples: jnp.full((T := 2, M := 3, 1), 0.5),
                        states=types.simple.state_batch.wrap(
                            rng.random((T, D_x := 2, M))
                        ),
                        obstacle_states=types.obstacle_2d_poses.create(
                            x=rng.random((T, K := 2)),
                            y=rng.random((T, K)),
                            heading=rng.random((T, K)),
                        ),
                        sampler=create_obstacles.sampler.gaussian(),
                    ),
                    lambda risks: risks.array * 2.0,
                    expected := np.full((T, M), 1.0),
                ),
            ]

        def planner_cases() -> list[tuple]:
            return [
                (
                    control := create_mppi.base(
                        model=stubs.DynamicalModel.returns(
                            rollouts=data.state_batch(
                                np.random.rand(T := 4, D_x := 2, M := 3)
                            ),
                            when_control_inputs_are=(
                                sampled_inputs := data.control_input_batch(
                                    np.random.rand(T, D_u := 2, M)
                                )
                            ),
                            and_initial_state_is=(
                                initial_state := data.state(
                                    array([1.0, 2.0], shape=(D_x,))
                                )
                            ),
                        ),
                        cost_function=costs.energy(),
                        sampler=stubs.Sampler.returns(
                            sampled_inputs,
                            when_nominal_input_is=(
                                nominal_input := data.control_input_sequence(
                                    np.random.rand(T, D_u)
                                )
                            ),
                        ),
                    ).step(
                        temperature=1.0,
                        nominal_input=nominal_input,
                        initial_state=initial_state,
                    ),
                    lambda control: control.optimal,
                    expected := np.asarray(control.optimal),
                ),
            ]

        return [
            *bicycle_cases(),
            *unicycle_cases(),
            *simple_cases(),
            *integrator_cases(),
            *augmented_cases(),
            *obstacle_cases(),
            *trajectory_cases(),
            *cost_cases(),
            *planner_cases(),
        ]

    @mark.parametrize(
        ["compile", "value", "operation", "expected"],
        [
            (jax.jit, *case)
            for case in cases(
                types=types.jax,
                create_mppi=create_mppi.jax,
                create_model=create_model.jax,
                create_costs=create_costs.jax,
                create_obstacles=create_obstacles.jax,
                create_risk=create_risk.jax,
                create_trajectory=create_trajectory.jax,
                data=data.jax,
                costs=costs.jax,
            )
        ],
    )
    def test[T, R: ArrayLike](
        self,
        compile: CompileFunction,
        value: T,
        operation: Callable[[T], R],
        expected: ArrayLike,
    ) -> None:
        assert np.allclose(compile(operation)(value), expected)


class test_that_compiled_components_return_the_same_results_as_the_uncompiled_components:
    @staticmethod
    def cases(create_obstacles, create_trajectory, types, data) -> Sequence[tuple]:
        def waypoints_trajectory() -> tuple:
            return (
                create_trajectory.waypoints(
                    points=array([[1.0, 2.0], [5.0, 3.0], [10.0, 7.0]], shape=(3, 2)),
                    path_length=20.0,
                ),
                call := lambda trajectory: trajectory.query(
                    types.path_parameters(
                        array([[0.0, 5.0], [10.0, 20.0]], shape=(T := 2, M := 2))
                    )
                ),
                before_each_call := [lambda: None],
            )

        def obstacle_state_provider() -> tuple:
            return (
                provider := create_obstacles.provider.predicting(
                    predictor=stubs.EchoingObstacleMotionPredictor.create(),
                    history=types.obstacle_states_running_history.empty(
                        creator=types.obstacle_2d_poses,
                        horizon=1,
                        obstacle_count=(K := 2),
                    ),
                ),
                call := lambda provider: provider(),
                before_each_call := [
                    partial(
                        provider.observe,
                        data.obstacle_2d_poses_for_time_step(
                            x=np.random.rand(K),
                            y=np.random.rand(K),
                            heading=np.random.rand(K),
                        ),
                    )
                    for _ in range(2)
                ],
            )

        return [waypoints_trajectory(), obstacle_state_provider()]

    @mark.parametrize(
        ["component", "call", "before_each_call"],
        cases(
            create_obstacles=create_obstacles.jax,
            create_trajectory=create_trajectory.jax,
            types=types.jax,
            data=data.jax,
        ),
    )
    def test[ComponentT, ResultT: ArrayLike](
        self,
        component: ComponentT,
        call: Callable[[ComponentT], ResultT],
        before_each_call: Sequence[Callable[[], None]],
    ) -> None:
        register(component)
        compiled_call = nnx.jit(call)

        for prepare in before_each_call:
            prepare()

            assert np.allclose(compiled_call(component), call(component))


class test_that_components_with_state_raise_an_error_when_compiled_in_a_closure:
    @staticmethod
    def cases(create_obstacles, types) -> Sequence[tuple]:
        return [
            (call := lambda: provider(),)
            for provider in [
                create_obstacles.provider.predicting(
                    predictor=stubs.EchoingObstacleMotionPredictor.create(),
                    history=types.obstacle_states_running_history.empty(
                        creator=types.obstacle_2d_poses
                    ),
                )
            ]
        ]

    @mark.parametrize(
        ["call"], cases(create_obstacles=create_obstacles.jax, types=types.jax)
    )
    def test(self, call: Callable[[], object]) -> None:
        with raises(UntracedStateError):
            jax.jit(call)()
