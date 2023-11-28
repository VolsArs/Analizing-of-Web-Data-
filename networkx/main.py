import networkx as nx
import matplotlib.pyplot as plt
import random




def first():
    G = nx.Graph()
    #(1,2),(1,3),(2,3), (2,4), (3,4)`'
    node_list = [1,2,3,4]
    G.add_nodes_from(node_list)
    G.add_edge(1, 2)  # default edge data=1
    G.add_edge(1, 3)
    G.add_edge(2, 3)
    G.add_edge(2, 4)
    G.add_edge(3, 4)
    print(G)
    nx.draw(G, with_labels = True)
    plt.show()


def second():
    G = nx.cubical_graph()
    print(G)
    nx.draw(G)
    plt.show()
    print(' В кубическом графе')
    print(nx.cycle_basis(G, 0))

def third():
    G = nx.DiGraph()
    G.add_edges_from([(1, 1), (1, 7), (2, 1), (2, 2), (2, 3),
                      (2, 6), (3, 5), (4, 3), (5, 4), (5, 8),
                      (5, 9), (6, 4), (7, 2), (7, 6), (8, 7)])

    nx.draw(G)
    print(sorted(nx.simple_cycles(G)))
    plt.show()

def fourth():

    G = nx.Graph()


    G.add_nodes_from(range(10))

    # Проходим по каждой паре вершин
    for i in range(10):
        for j in range(i + 1, 10):
            # Генерируем случайное число от 0 до 1
            probability = random.random()

            # Если случайное число меньше или равно 0.1,
            # то добавляем ребро между вершинами i и j
            if probability <= 0.1:
                G.add_edge(i, j)

    nx.draw(G)

    plt.show()

    print(G.edges)


def fifth():
    G = nx.Graph()
    vertices = range(100)
    probabilities = [random.uniform(0.005, 0.03) for _ in range(1000)]

    for p in probabilities:
        graph = nx.erdos_renyi_graph(100, p)

        G.add_edges_from(graph.edges())

        largest_component = max(nx.connected_components(G), key=len)

        # Размер наибольшей компоненты связности
        size = len(largest_component)

        plt.scatter(p, size)

    # Настройка осей графика
    plt.xlabel('Вероятность p')
    plt.ylabel('Размер наибольшей компоненты связности')

    # Отображение графика
    plt.show()

fifth()
#fourth()
#third()
#second()
#first()



