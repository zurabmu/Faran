import asyncio

from faran import access, metrics
from faran.numpy import (
    collectors,
    extract,
    filters,
    model,
    mppi,
    sampler,
    trajectory,
    types,
)
from faran_visualizer import MpccSimulationResult, visualizer

HORIZON = 30  # Planning steps. Try 10 or 50.
TIME_STEP = 0.1

reference = trajectory.waypoints(
    points=[(0.0, 0.0), (10.0, 0.0), (20.0, 10.0), (10.0, 20.0), (0.0, 20.0)],
    path_length=30.0,
)
planner, augmented_model, contouring, lag = mppi.mpcc(
    model=model.bicycle.dynamical(
        time_step_size=TIME_STEP,
        wheelbase=2.5,
        speed_limits=(0.0, 15.0),
        steering_limits=(-0.5, 0.5),
        acceleration_limits=(-3.0, 3.0),
    ),
    sampler=sampler.gaussian(
        standard_deviation=[0.5, 0.2],
        rollout_count=128,
        to_batch=types.bicycle.control_input_batch.create,
        seed=42,
    ),
    reference=reference,
    position_extractor=extract.from_physical(lambda states: states.positions),
    config={
        "weights": {"contouring": 50.0, "lag": 100.0, "progress": 1000.0},
        "virtual": {"velocity_limits": (0.0, 15.0)},
    },
    filter_function=filters.savgol(window_length=11, polynomial_order=3),
)
planner = states = collectors.states.decorating(
    planner,
    transformer=types.augmented.state_sequence.of_states(
        physical=types.bicycle.state_sequence.of_states,
        virtual=types.simple.state_sequence.of_states,
    ),
)
planner = trajectories = collectors.trajectories.decorating(
    planner, model=augmented_model
)
registry = metrics.registry(
    errors := metrics.mpcc_error(contouring=contouring, lag=lag),
    collectors=collectors.registry(states, trajectories),
)

state = types.augmented.state.of(
    physical=types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=0.0),
    virtual=types.simple.state.zeroes(dimension=1),
)
nominal = types.augmented.control_input_sequence.of(
    physical=types.bicycle.control_input_sequence.zeroes(horizon=HORIZON),
    virtual=types.simple.control_input_sequence.zeroes(horizon=HORIZON, dimension=1),
)
for _ in range(100):
    control = planner.step(temperature=50.0, nominal_input=nominal, initial_state=state)
    nominal = control.nominal
    state = augmented_model.step(inputs=control.optimal, state=state)
    if state.virtual.array[0] >= 0.95 * reference.path_length:
        break

plans = registry.data(access.trajectories.require())
asyncio.run(
    visualizer.mpcc()(
        MpccSimulationResult(
            reference=reference,
            states=registry.data(access.states.require()),
            optimal_trajectories=[plan.optimal for plan in plans],
            nominal_trajectories=[plan.nominal for plan in plans],
            contouring_errors=registry.get(errors).contouring,
            lag_errors=registry.get(errors).lag,
            time_step_size=TIME_STEP,
            wheelbase=2.5,
            vehicle_width=1.2,
        ),
        key="horizon",
    )
)
