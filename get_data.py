import time
from helper import Countries,Country
from nn_solver import NnTsp
from held_karp import DpTsp
import timeit
import csv


def main(num_countries):
    countries = Countries()
    countries.parse_json_countries(num_countries)

    adj_matrix = countries.get_adj_matrix()

    start_time_nn = time.perf_counter()
    start_time_alter = time.perf_counter()
    nn_tsp = NnTsp(adj_matrix)
    path_nn = nn_tsp.nearest_neighbor()
    cost_nn = nn_tsp.calculate_tsp_cost(path_nn)
    end_time_nn = time.perf_counter()
    elapsed_time_nn = (end_time_nn - start_time_nn) * 1000


    alter_nn = nn_tsp.improve_tour_2opt(path_nn, cost_nn)
    alter_cost = nn_tsp.calculate_tsp_cost(alter_nn)
    end_time_alter = time.perf_counter()
    elapsed_time_alter = (end_time_alter - start_time_alter) * 1000 

    start_time_dp = time.perf_counter()
    dp_tsp = DpTsp(adj_matrix)
    path_dp = dp_tsp.find_optimal_tour()
    cost_dp = dp_tsp.get_optimal_cost()
    end_time_dp = time.perf_counter()
    elapsed_time_dp = (end_time_dp - start_time_dp) * 1000

    print("\nTSP Using DP")
    countries.print_countries_path(path_dp)
    print("\nTotal distance traveled:", cost_dp)
    print("Time taken to execute: {:.10f} ms".format(elapsed_time_dp))

    print("\nTSP Using NN")
    countries.print_countries_path(path_nn)
    print("\nTotal distance traveled:", cost_nn)
    print("Time taken to execute: {:.10f} ms".format(elapsed_time_nn))


    print("\nTSP Using NN and 2-Opt")
    countries.print_countries_path(alter_nn)
    print("\nTour cost:", alter_cost)
    print("Execution time:", (end_time_alter - start_time_alter) * 1000, "ms")
    ratio_nn = cost_nn/cost_dp
    ratio_alter = alter_cost/cost_dp

    print("Ratio : " , alter_cost/cost_dp)
    return num_countries, cost_nn, elapsed_time_nn, alter_cost, elapsed_time_alter, cost_dp, elapsed_time_dp, ratio_nn, ratio_alter

results = []
for i in range(5, 22):
    print("\nNumber of countries: {}\n".format(i))
    result = main(i)
    results.append(result)

# Write results to CSV
with open('hasil_tsp.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Number of Countries", "NN Distance", "NN Time (ms)", "NN + 2opt Distance", "NN + 2opt Time (ms)", "DP Distance", "DP Time (ms)", "NN Ratio", "NN + 2opt Ratio"])
    writer.writerows(results)

print("Hasil disimpan ke hasil_tsp.csv")