from typing import List, Dict, Tuple

class DpTsp:

    def __init__(self, distance_matrix: List[List[float]]) -> None:
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.memoization: Dict[Tuple[int, int], float] = {}
        self.previous_city: Dict[Tuple[int, int], int] = {}
        self.optimal_tour_cost: float = float('inf')

    def calculate_min_cost(self, current_city: int, visited_mask: int) -> float:
        if visited_mask == (1 << current_city) | 1:
            return self.distance_matrix[0][current_city]

        current_state = (current_city, visited_mask)
        if current_state in self.memoization:
            return self.memoization[current_state]

        min_cost = float('inf')
        remaining_cities = visited_mask & (~(1 << current_city))
        
        for next_city in range(self.num_cities):
            if (visited_mask & (1 << next_city)) and next_city != current_city and next_city != 0:
                total_cost = self.calculate_min_cost(next_city, remaining_cities) + self.distance_matrix[next_city][current_city]
                if total_cost < min_cost:
                    min_cost = total_cost
                    self.previous_city[current_state] = next_city

        self.memoization[current_state] = min_cost
        return min_cost

    def find_optimal_tour(self) -> List[int]:
        all_cities_visited = (1 << self.num_cities) - 1
        min_total_cost = float('inf')
        last_city = -1

        for city in range(1, self.num_cities):
            tour_cost = self.calculate_min_cost(city, all_cities_visited) + self.distance_matrix[city][0]
            if tour_cost < min_total_cost:
                min_total_cost = tour_cost
                last_city = city

        optimal_path = self.reconstruct_path(last_city, all_cities_visited)
        optimal_path.append(0)
        self.optimal_tour_cost = min_total_cost
        return optimal_path[::-1] + [0]

    def reconstruct_path(self, current_city: int, visited_mask: int) -> List[int]:
        path = []
        while current_city != -1:
            path.append(current_city)
            current_state = (current_city, visited_mask)
            next_city = self.previous_city.get(current_state, -1)
            visited_mask &= ~(1 << current_city)
            current_city = next_city
        return path

    def get_optimal_cost(self) -> float:
        return self.optimal_tour_cost
