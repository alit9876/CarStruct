from .Data_Structures.Hashing import MyHashTable
from .Data_Structures.Hashing import KeyNode
from .Data_Structures.AVL import AVLTree
from .Data_Structures.queues import TestDriveQueue
from .Data_Structures.Cars import Car
import csv
import pandas  as pd
import os
class Showroom:
    def __init__(self):
        self.CarTable = MyHashTable()
        self.treesDict = {}
        self.test_drive_queue = TestDriveQueue()
    
    def GetTable(self):
        return self.CarTable
    
    def InsertCar(self,serialNumber,name,model,color,manufacturer,Features,mileage,engineCC,price,Reviews):
        try:
            car = Car(serialNumber,name,model,color,manufacturer,Features,mileage,engineCC,price,Reviews)
            node = KeyNode(car.serialNumber,car)
            self.CarTable.Insert(node)
            if manufacturer not in self.treesDict:
                self.treesDict[manufacturer] = AVLTree(car)
                return True
            else:
                self.treesDict[manufacturer].insert(car)
                return True
        except Exception as e:
            print("Exception: ", e)

    def updateCar(self,serialNumber,name,model,color,manufacturer,Features,mileage,engineCC,price,Reviews):
        try:
            car = Car(serialNumber,name,model,color,manufacturer,Features,mileage,engineCC,price,Reviews)
            node = KeyNode(car.serialNumber,car)
            flag = self.CarTable.Update(node)
            return flag
        except Exception as e:
            print("Exception ", e)

    def GetCarBySerialNumber(self,serialNumber):
        try:
            key = self.CarTable.HashFunction(serialNumber)
            if self.CarTable.HashTable[key] is None:
                return False
            else:
                temp = self.CarTable.HashTable[key]
                while temp is not None:
                    if temp.key_node.key == serialNumber:
                        return temp.key_node.value
                    temp = temp.next
                return False
        except Exception as e:
            print("Exception: ", e)
    
    def DeleteCar(self, serialNumber):
        try:
            car = self.GetCarBySerialNumber(serialNumber)
            
            if car:
                manufacturer = car.manufacturer
                self.CarTable.Delete(serialNumber)

                if manufacturer in self.treesDict:
                    self.treesDict[manufacturer].delete(car)
                    return True
                else:
                    print(f"Manufacturer '{manufacturer}' not found in treesDict.")
                    return False
            else:
                print(f"Car with serial number '{serialNumber}' not found.")
        except Exception as e:
            print("Exception: ", e)

    
    def ReadDataFromFile(self, file_path):
        try:
            cars = []
            visited = set()  # Change this to a set
            with open(file_path, 'r') as file:
                for line in file:
                    # Assuming columns are separated by a comma
                    values = line.strip().split(',')
                    if len(values) >= 10:   
                        serialNumber, name, model, color, manufacturer, Features, mileage, engineCC, price, Reviews =values[:10]
                        u = Car(serialNumber, name, model, color, manufacturer, Features, mileage, engineCC, price, Reviews)
                        
                        # if manufacturer is not visited yet
                        if u.manufacturer not in visited:
                            visited.add(u.manufacturer)
                            self.CarTable.Insert(KeyNode(u.serialNumber, u))
                            cars.append([u])
                        else:
                            self.CarTable.Insert(KeyNode(u.serialNumber, u))
                            for i in range(len(cars)):
                                if cars[i][0].manufacturer == u.manufacturer:
                                    cars[i].append(u)
            self.MakeTrees(cars)
        except Exception as e:
            print("Exception: ", e)

    def WriteDataToFile(self, file_path):
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)

                # Iterate through the hash table
                for bucket in self.CarTable.HashTable:
                    temp = bucket
                    while temp is not None:
                        # Use the to_list method to get the list representation of the car
                        car_list = temp.key_node.value.to_list()
                        writer.writerow(car_list)
                        temp = temp.next

            print(f"Data saved to {file_path}")
        except Exception as e:
            print("Exception: ", e)

    def MakeTrees(self,arr):
        try:
            for i in arr:
                if i is not None:
                    t = AVLTree(i)
                    self.treesDict[i[0].manufacturer] = t
        except Exception as e:
            print("Exception: ", e)

    def GetTreeDict(self):
        return self.treesDict

    def inorderTraversal(self, node, arr):
        try:
            if node:
                self.inorderTraversal(node.left, arr)
                arr.append(node.car)
                self.inorderTraversal(node.right, arr)
            return arr
        except Exception as e:
            print("Exception: ", e)

    
    def GetTreeOfManufacturer(self,manufacturer):
        try:
            if manufacturer in self.treesDict:
                return self.treesDict[manufacturer]
            else:
                False
        except Exception as e:
            print("Exception: ", e)
    
    def GetCarsInSpecificRange(self,node,startingPoint,endingPoint,arr):
        try:
            if node:
                self.GetCarsInSpecificRange(node.left, startingPoint, endingPoint, arr)
                
                # Use the get_numeric_price method to retrieve the numeric representation
                car_price = node.car.get_numeric_price()
                if car_price is not None and startingPoint <= car_price <= endingPoint:
                    arr.append(node.car)
                
                self.GetCarsInSpecificRange(node.right, startingPoint, endingPoint, arr)
            return arr
        except Exception as e:
            print("Exception: ", e)
    
    #queue implementation for test drives
    def EnqueueForTestDrive(self, car, customer_name):
        self.test_drive_queue.enqueue(car, customer_name)

    def DequeueForTestDrive(self):
        return self.test_drive_queue.dequeue()

    def SaveTestDriveQueueToFile(self, file_path):
        data = self.test_drive_queue.get_queue_data()
        file_path = file_path  # File path where you want to save the CSV
        df = pd.DataFrame(data, columns=['Name', 'Car'])
        df.to_csv(file_path, index=False)

    def RetrieveTestDriveQueueFromFile(self, file_path):
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                data = df.values.tolist()
                for x in range(len(data)):
                    self.test_drive_queue.enqueue(data[x][0], data[x][1])
            print(f"Test drive queue data retrieved from {file_path}")
        except Exception as e:
            print("Exception: ", e)

            
# if __name__ == "__main__":
    # s = Showroom()
    # s.ReadDataFromFile('./Components/car_showroom_data.csv')
    # # print(s.GetTreeDict())
    
    # tree = s.GetTreeOfManufacturer('Alfa Romeo')
    # # print(tree.root.car.serialNumber)
    # array = s.inorderTraversal(tree.root,[])
    # # array2 = s.GetCarInSpecificRange(tree.root,50000,60000,array2)
    # for i in array:
    #     print('printing',i.serialNumber,i.price,i.manufacturer)
    
    # array2 = s.GetCarsInSpecificRange(tree.root,50000,60000,[])
    # for i in array2:
    #     print('price ranges',i.serialNumber,i.price,i.manufacturer)
    
    # s.DeleteCar('S1GM96SB')

    # tree = s.GetTreeOfManufacturer('Alfa Romeo')
    # array = s.inorderTraversal(tree.root,[])
    # for i in array:
    #     print('Deleted',i.serialNumber,i.price,i.manufacturer,i.Features)
     
    # details = s.GetCarBySerialNumber('S1GM96SB')
    # print('printing car details',details.price,details.manufacturer)
    

