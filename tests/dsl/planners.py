from typing import Callable

from faran import Control, mppi as create_mppi, types

import numpy as np

from tests.dsl import stubs, mppi as data


class numpy:
    @staticmethod
    def stepping_with(
        cost_function: types.numpy.CostFunction,
    ) -> Callable[
        [], Control[types.numpy.simple.ControlInputSequence, types.numpy.Weights]
    ]:
        """Returns a function that runs one step of a planner with the given cost function."""
        mppi = create_mppi.numpy.base(
            model=stubs.DynamicalModel.returns(
                rollouts=data.numpy.state_batch(
                    np.random.rand(T := 3, D_x := 2, M := 2)
                ),
                when_control_inputs_are=(
                    samples := data.numpy.control_input_batch(
                        np.random.rand(T, D_u := 2, M)
                    )
                ),
                and_initial_state_is=(initial_state := data.numpy.state(np.zeros(D_x))),
            ),
            cost_function=cost_function,
            sampler=stubs.Sampler.returns(
                samples,
                when_nominal_input_is=(
                    nominal_input := data.numpy.control_input_sequence(
                        np.zeros((T, D_u))
                    )
                ),
            ),
        )

        return lambda: mppi.step(
            temperature=1.0, nominal_input=nominal_input, initial_state=initial_state
        )


class jax:
    @staticmethod
    def stepping_with(
        cost_function: types.jax.CostFunction,
    ) -> Callable[
        [], Control[types.jax.simple.ControlInputSequence, types.jax.Weights]
    ]:
        """Returns a function that runs one step of a planner with the given cost function."""
        mppi = create_mppi.jax.base(
            model=stubs.DynamicalModel.returns(
                rollouts=data.jax.state_batch(np.random.rand(T := 3, D_x := 2, M := 2)),
                when_control_inputs_are=(
                    samples := data.jax.control_input_batch(
                        np.random.rand(T, D_u := 2, M)
                    )
                ),
                and_initial_state_is=(initial_state := data.jax.state(np.zeros(D_x))),
            ),
            cost_function=cost_function,
            sampler=stubs.Sampler.returns(
                samples,
                when_nominal_input_is=(
                    nominal_input := data.jax.control_input_sequence(np.zeros((T, D_u)))
                ),
            ),
        )

        return lambda: mppi.step(
            temperature=1.0, nominal_input=nominal_input, initial_state=initial_state
        )
