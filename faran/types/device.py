from typing import Literal

from faran.types.array import Array

from jaxtyping import Array as JaxArray

import jax
import jax.numpy as jnp

type Device = Literal["cpu", "default"]


def place(array: Array | JaxArray, *, device: Device) -> JaxArray:
    """Place an array on the specified device.

    Args:
        array: The array to place.
        device: The device to place the array on. Can be "cpu" or "default".

    Returns:
        The array placed on the specified device.
    """
    match device:
        case "cpu":
            return jnp.asarray(array, device=jax.devices("cpu")[0])
        case "default":
            return jnp.asarray(array)
        case _:
            raise ValueError(f"Unsupported device: {device}")
