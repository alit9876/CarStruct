import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from math import cos, sin


class WeightedGraph:
    def __init__(self):
        self.graph = {}
        self.mst = None
        self.add_node('Receptionist')  # Adding Receptionist node by default

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight  # Assuming edges are bidirectional

    def connect_brands_to_each_other(self, brand_list):
        for i in range(len(brand_list)):
            for j in range(i + 1, len(brand_list)):
                self.add_edge(brand_list[i], brand_list[j], weight=2)  # Arbitrary weight

    def dijkstra_shortest_path(self, source, target):
        visited = {node: False for node in self.graph}
        distance = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}

        distance[source] = 0

        while True:
            min_distance = float('inf')
            current_node = None

            for node in self.graph:
                if not visited[node] and distance[node] < min_distance:
                    min_distance = distance[node]
                    current_node = node

            if current_node is None:
                break

            visited[current_node] = True

            for neighbor, weight in self.graph[current_node].items():
                if distance[current_node] + weight < distance[neighbor]:
                    distance[neighbor] = distance[current_node] + weight
                    previous[neighbor] = current_node

        shortest_path = []
        current_node = target
        while current_node is not None:
            shortest_path.append(current_node)
            current_node = previous[current_node]

        return shortest_path[::-1] if distance[target] != float('inf') else None

    def draw_graph(self, shortest_path=None):
        fig, ax = plt.subplots()
        pos = self.calculate_positions()

        for node, connections in self.graph.items():
            x, y = pos[node]
            ax.scatter(x, y, s=300)
            ax.text(x, y, node, ha='center', va='center', fontsize=10)

            for connected_node, _ in connections.items():
                x_c, y_c = pos[connected_node]
                ax.plot([x, x_c], [y, y_c], 'k-', alpha=0.5)

        if shortest_path:
            for i in range(len(shortest_path) - 1):
                node1 = shortest_path[i]
                node2 = shortest_path[i + 1]
                x1, y1 = pos[node1]
                x2, y2 = pos[node2]
                ax.plot([x1, x2], [y1, y2], 'r-', linewidth=3)

        ax.axis('off')  # Remove axis numbers
        plt.close(fig)
        return fig

    def calculate_positions(self):
        pos = {}
        num_brands = len([node for node in self.graph if node != 'Receptionist'])

        # Receptionist positioned to the left
        pos['Receptionist'] = (-2, 0)

        # Calculate positions for brands
        brand_radius = 1.5
        for i, brand in enumerate([node for node in self.graph if node != 'Receptionist']):
            angle = (2 * i * 3.1416) / num_brands
            x = brand_radius * cos(angle)
            y = brand_radius * sin(angle)
            pos[brand] = (x, y)

        return pos

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def node_exists(self, node_name):
        return node_name in self.graph

    def kruskal_mst(self):
        edges = []
        mst = WeightedGraph()

        for node, connections in self.graph.items():
            for neighbor, weight in connections.items():
                edges.append((node, neighbor, weight))

        edges.sort(key=lambda x: x[2])  # Sort edges by weight

        parent = {node: node for node in self.graph}
        rank = {node: 0 for node in self.graph}

        for edge in edges:
            node1, node2, weight = edge
            root1 = self.find(parent, node1)
            root2 = self.find(parent, node2)

            if root1 != root2:
                mst.add_edge(node1, node2, weight)
                mst.add_edge(node2, node1, weight)
                self.union(parent, rank, root1, root2)

        return mst


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi('untitled.ui', self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.graph_display_layout = QVBoxLayout(self.Graph_display)
        self.source = "Receptionist"
        self.source_display.setText(self.source)
        self.car_show = self.getgraph()
        self.plot()
        self.find.clicked.connect(self.find_location)
        self.reset.clicked.connect(self.plot)
        self.mst.clicked.connect(self.display_mist)

    def getgraph(self):
        car_show = WeightedGraph()

        graph_data = {
            'Receptionist': {'Chevrolet': 8, 'Suzuki': 25, 'Mitsubishi': 3, 'BMW': 3, 'Audi': 2, 'Rolls-Royce': 15},
            'Chevrolet': {'Receptionist': 8, 'Suzuki': 6, 'Mitsubishi': 5, 'BMW': 7, 'Audi': 13, 'Rolls-Royce': 12},
            'Suzuki': {'Receptionist': 25, 'Chevrolet': 6, 'Mitsubishi': 3, 'BMW': 7, 'Audi': 5, 'Rolls-Royce': 9},
            'Mitsubishi': {'Receptionist': 3, 'Chevrolet': 5, 'Suzuki': 3, 'BMW': 1, 'Audi': 2, 'Rolls-Royce': 3},
            'BMW': {'Receptionist': 3, 'Chevrolet': 7, 'Suzuki': 7, 'Mitsubishi': 1, 'Audi': 1, 'Rolls-Royce': 1},
            'Audi': {'Receptionist': 2, 'Chevrolet': 13, 'Suzuki': 5, 'Mitsubishi': 2, 'BMW': 1, 'Rolls-Royce': 2},
            'Rolls-Royce': {'Receptionist': 15, 'Chevrolet': 12, 'Suzuki': 9, 'Mitsubishi': 3, 'BMW': 1, 'Audi': 2}
        }

        for node, connections in graph_data.items():
            for neighbor, weight in connections.items():
                if node != neighbor:  # Avoiding self-loop edges
                    car_show.add_edge(node, neighbor, weight)

        car_show.mst = car_show.kruskal_mst()
        return car_show

    def update_graph(self, fig):
        for i in reversed(range(self.graph_display_layout.count())):
            widget = self.graph_display_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        canvas = FigureCanvas(fig)
        self.graph_display_layout.addWidget(canvas)

    def find_location(self):
        try:
            destination = self.inputText.text()
            if self.car_show.node_exists(destination):
                shortest_path = self.car_show.dijkstra_shortest_path(self.source, destination)
                print(shortest_path)
                fig = self.car_show.draw_graph(shortest_path)
                self.update_graph(fig)
                self.source = destination
                self.source_display.setText(self.source)
            else:
                QMessageBox.information(None, "Invalid Name", 'Car brand with such name does not exist')
                self.inputText.setText('')
        except Exception as e:
            print(e)

    def display_mist(self):
        try:
            self.inputText.setText('')
            fig = self.car_show.mst.draw_graph()
            self.update_graph(fig)
        except Exception as e:
            print(e)

    def plot(self):
        try:
            self.inputText.setText('')
            self.source = 'Receptionist'
            fig = self.car_show.draw_graph(None)
            self.source_display.setText(self.source)
            self.update_graph(fig)
        except Exception as e:
            print(e)


# app = QApplication(sys.argv)
# window = Mainwindow()
# window.show()
# sys.exit(app.exec_())

