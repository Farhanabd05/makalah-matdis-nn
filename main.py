from helper import Countries,Country
from nn_solver import NnTsp
import time


def main():
    countries = Countries()
    countries.parse_json_countries(44)

    adj_matrix = countries.get_adj_matrix()

    start_time_nn = time.perf_counter()
    start_time_alter = time.perf_counter()
    nn_tsp = NnTsp(adj_matrix)
    path_nn = nn_tsp.nearest_neighbor()
    cost_nn = nn_tsp.calculate_tsp_cost(path_nn)
    end_time_nn = time.perf_counter()
    elapsed_time_nn = (end_time_nn - start_time_nn) * 1000

    alter_nn = nn_tsp.improve_tour_2opt(path_nn, cost_nn)
    alter_cost = (int)(nn_tsp.calculate_tsp_cost(alter_nn))
    end_time_alter = time.perf_counter()
    print("TSP Using NN")
    countries.print_countries_path(path_nn)
    print("\nTotal distance traveled:", cost_nn)
    print("Time taken to execute: {:.10f} ms".format(elapsed_time_nn))
    countries.plot_lines(path_nn)

    print("TSP Using NN and 2-Opt")
    countries.print_countries_path(alter_nn)
    print("\nTotal distance traveled:", alter_cost)
    print("Time taken to execute:", (end_time_alter - start_time_alter) * 1000, "ms")
    countries.plot_lines(alter_nn)

main()
