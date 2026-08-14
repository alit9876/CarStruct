import pandas as pd
import os

class QueueNode:
    def __init__(self, car, customer_name):
        self.car = car
        self.customer_name = customer_name
        self.next = None


class TestDriveQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, car, customer_name):
        new_node = QueueNode(car, customer_name)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            dequeued_node = self.front
            self.front = self.front.next
            if self.front is None:
                self.rear = None
            return dequeued_node

    def get_queue_data(self):
        queue_data = []
        current_node = self.front
        while current_node:
            queue_data.append((current_node.car, current_node.customer_name))
            current_node = current_node.next
        return queue_data

    def save_data(self, path):
        data = self.get_queue_data()
        file_path = path  # File path where you want to save the CSV
        df = pd.DataFrame(data, columns=['Name', 'Car'])
        df.to_csv(file_path, index=False)

    def load_data(self, path):
        test = TestDriveQueue()
        file_path = path  # File path of the CSV file
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            data = df.values.tolist()
            for x in range(len(data)):
                test.enqueue(data[x][0], data[x][1])
            return test
        else:
            return TestDriveQueue()
