class NnTsp:
    def __init__(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.n = len(adj_matrix)
        
    def nearest_neighbor(self):
        # Use list instead of set for better memory efficiency
        path = [0]  # Start from city 0
        unvisited = list(range(1, self.n))
        current = 0
        
        while unvisited:
            # Find nearest unvisited city using list comprehension
            nearest = min((city for city in unvisited), 
                         key=lambda x: self.adj_matrix[current][x])
            path.append(nearest)
            unvisited.remove(nearest)
            current = nearest
            
        path.append(0)  # Complete the cycle
        return path

    def calculate_tsp_cost(self, path):
        # Use sum with generator expression for better memory efficiency
        return sum(self.adj_matrix[path[i]][path[i + 1]] 
                  for i in range(len(path) - 1))

    def two_opt_swap(self, tour, i, j):
        # More efficient implementation using slicing
        return tour[:i] + tour[i:j][::-1] + tour[j:]

    def improve_tour_2opt(self, tour, tour_cost):
        best_tour = tour
        best_cost = tour_cost
        
        while True:
            improved = False
            # Use range objects for memory efficiency
            for i in range(1, len(tour) - 2):
                # Optimize inner loop to avoid redundant calculations
                for j in range(i + 2, len(tour)):
                    new_tour = self.two_opt_swap(tour, i, j)
                    new_cost = self.calculate_tsp_cost(new_tour)
                    
                    if new_cost < best_cost:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True
                        # Early break when improvement found
                        break
                if improved:
                    break
                    
            if not improved:
                break
                
            tour = best_tour
            tour_cost = best_cost
            
        return best_tour