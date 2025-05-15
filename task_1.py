from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        for neighbor in range(len(capacity_matrix)):
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False


def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float("Inf")
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow
    return max_flow


def build_flow_report(capacity_matrix, source_nodes, target_nodes):
    report = []
    for source in source_nodes:
        for target in target_nodes:
            flow = edmonds_karp(capacity_matrix, source, target)
            if flow > 0:
                report.append((f"Термінал {source + 1}", f"Магазин {target - 5}", flow))
    return report


def print_flow_report(report):
    print("Термінал\tМагазин\tФактичний Потік")
    for terminal, shop, flow in report:
        print(f"{terminal}\t{shop}\t{flow}")


def find_bottlenecks(capacity_matrix, flow_matrix):
    bottlenecks = []
    for i in range(len(capacity_matrix)):
        for j in range(len(capacity_matrix[i])):
            if capacity_matrix[i][j] > 0:
                residual_capacity = capacity_matrix[i][j] - flow_matrix[i][j]
                if residual_capacity > 0:
                    bottlenecks.append((i, j, residual_capacity))
    bottlenecks.sort(key=lambda x: x[2])
    return bottlenecks


def find_min_supply_shops(capacity_matrix, target_nodes):
    shop_flows = {
        f"Магазин {node - 5}": sum(
            capacity_matrix[i][node] for i in range(len(capacity_matrix))
        )
        for node in target_nodes
    }
    min_supply_shop = min(shop_flows, key=shop_flows.get)
    return shop_flows, min_supply_shop


if __name__ == "__main__":
    capacity_matrix = [
        [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 1
        [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Термінал 2
        [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],  # Склад 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],  # Склад 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],  # Склад 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 10
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Магазин 14
    ]

    source = 0  # Термінал 1
    sink = 14  # Магазин 9
    max_flow = edmonds_karp(capacity_matrix, source, sink)
    print(f"Максимальний потік для Терміналу 1 до Магазину 9: {max_flow}")

    source_nodes = [0, 1]
    target_nodes = list(range(6, 20))

    flow_report = build_flow_report(capacity_matrix, source_nodes, target_nodes)
    print_flow_report(flow_report)

    G = nx.DiGraph()
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    G.add_weighted_edges_from(edges)

    pos = {
        "Термінал 1": (2, 4),
        "Термінал 2": (10, 4),
        "Склад 1": (4, 6),
        "Склад 2": (8, 6),
        "Склад 3": (4, 2),
        "Склад 4": (8, 2),
        "Магазин 1": (0, 8),
        "Магазин 2": (2, 8),
        "Магазин 3": (4, 8),
        "Магазин 4": (6, 8),
        "Магазин 5": (8, 8),
        "Магазин 6": (10, 8),
        "Магазин 7": (0, 0),
        "Магазин 8": (2, 0),
        "Магазин 9": (4, 0),
        "Магазин 10": (6, 0),
        "Магазин 11": (8, 0),
        "Магазин 12": (10, 0),
        "Магазин 13": (12, 0),
        "Магазин 14": (14, 0),
    }

    plt.figure(figsize=(16, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        arrows=True,
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Логістична мережа")
    plt.show()
