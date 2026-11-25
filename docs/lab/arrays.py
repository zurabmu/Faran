import numpy as np
from jaxtyping import Float

type Position = Float[np.ndarray, "2"]
type Positions = Float[np.ndarray, "N 2"]
type Radii = Float[np.ndarray, " N"]
