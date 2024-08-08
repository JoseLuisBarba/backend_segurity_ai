from pydantic import BaseModel
from typing import List, Tuple

class OptimizationRequest(BaseModel):
    points: List[Tuple[float, float]]
    demands: List[float]
    facilities: List[int]
    max_facilities: int
    coverage_radius: float

class OptimizationResult(BaseModel):
    id: int
    target: List[float]
    Fitness: float
    solution: List[int]