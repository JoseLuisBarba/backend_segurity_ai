import numpy as np
from mealpy.bio_based import BBO
from mealpy import PSO, BinaryVar
from typing import List, Tuple

def haversine_distance(coord1, coord2):
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Convertir grados a radianes
    lat1, lon1 = np.deg2rad(coord1)
    lat2, lon2 = np.deg2rad(coord2)
    
    # Diferencias
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    
    return distance

class MaximalCoveringLocation(object):

    def __init__(self,
                 points: List[Tuple[float, float]],
                 demands: List[float],  # Cambiado a float
                 facilities: List[int],
                 max_facilities: int,
                 coverage_radius: float) -> None:
        self.num_locations = len(facilities)
        self.num_demand_points = len(points)
        self.dist_matrix_haversine = np.zeros((self.num_demand_points, self.num_demand_points), np.float64)
        
        for i in range(len(points)):
            for j in range(len(points)):
                self.dist_matrix_haversine[i, j] = haversine_distance(points[i], points[j])
        
        self.facilities = np.array(facilities, dtype=np.int32)
        self.distances = self.dist_matrix_haversine
        self.demands = np.array(demands, dtype=np.float64)
        self.max_facilities = max_facilities
        self.coverage_radius = coverage_radius

    def objective_function(self,
                           solution: np.ndarray):
        facilities = solution.copy()
        coverage = np.zeros(self.num_demand_points)

        for i in range(self.num_locations):
            if facilities[i] == 1:
                for j in range(self.num_demand_points):
                    if coverage[j] == 1:
                        continue
                    if self.distances[i, j] <= self.coverage_radius:
                        coverage[j] = 1
        fitness = np.sum(coverage * self.demands)
        penalty = 0
        if np.sum(facilities) > self.max_facilities:
            penalty = np.sum(facilities) - self.max_facilities
        return -fitness + penalty * 1000

    def solve(self):
        problem_constrained = {
            "obj_func": self.objective_function,
            "bounds": BinaryVar(n_vars=self.num_locations),
            "minmax": "min",
        }
        model = BBO.OriginalBBO(epoch=500, pop_size=50)
        result = model.solve(problem_constrained)
        return {
            'id': result.id,
            'target': list(result.target.objectives),
            'Fitness': result.target.fitness,
            'solution': list(result.solution)
        }
