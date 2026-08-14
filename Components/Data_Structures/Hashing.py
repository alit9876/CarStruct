import pandas as pd

class KeyNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class LinkedListNode:
    def __init__(self, key_node):
        self.key_node = key_node
        self.next = None

class MyHashTable:
    def __init__(self, Arr=None, size=6, KeysOccupied=0):
        self.size = size
        self.KeysOccupied = KeysOccupied
        self.HashTable = [None] * size
        if not Arr is None:
            for node in Arr:
                self.Insert(node)

    def GetHashTableSize(self):
        return self.size

    def HashFunction(self, key):
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value

    def CheckValuekey(self, key):
        key_hash = self.HashFunction(key)
        temp = self.HashTable[key_hash]

        while temp is not None:
            if temp.key_node.key == key:
                # Return True if the key exists irrespective of the value
                return True
            temp = temp.next

        # Key not found in the hash table
        return False
    def Insert(self, key_node):
        key = self.HashFunction(key_node.key)
        new_node = LinkedListNode(key_node)

        # Check if the slot is empty
        if self.HashTable[key] is None:
            self.HashTable[key] = new_node
            self.KeysOccupied += 1
            return True
        elif self.KeysOccupied / self.size >= 0.70:
            self.Rehash()
            self.Insert(key_node)
        else:
            # Check if there are collisions and update existing values
            temp = self.HashTable[key]
            while temp.next is not None:
                if temp.key_node.key == key_node.key:
                    return False
                temp = temp.next

            # If no collisions, append the new node
            temp.next = new_node
            self.KeysOccupied += 1
            return True
    
    def Update(self, key_node):
        key = self.HashFunction(key_node.key)
        new_node = LinkedListNode(key_node)

        # Check if the slot is empty
        if self.HashTable[key] is None:
            return False
        else:
            # Check if there are collisions and update existing values
            temp = self.HashTable[key]
            while temp is not None:
                if temp.key_node.key == key_node.key:
                    temp.key_node.value = key_node.value
                    return True
                temp = temp.next

        # If the key is not found, append the new node
        temp = self.HashTable[key]
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node
        self.KeysOccupied += 1
        return True



    def Delete(self, key):
        hash_value = self.HashFunction(key)
        temp = self.HashTable[hash_value]

        # Check if the slot is not empty
        if temp is not None:
            if temp.key_node.key == key:
                self.HashTable[hash_value] = temp.next
                self.KeysOccupied -= 1
                print(f"Deleted key: {key}")
                return

            while temp.next is not None:
                if temp.next.key_node.key == key:
                    temp.next = temp.next.next
                    self.KeysOccupied -= 1
                    print(f"Deleted key: {key}")
                    return
                temp = temp.next

        print(f"Key not found: {key}")
    
    def CheckValue(self, key_node):
        key = self.HashFunction(key_node.key)
        temp = self.HashTable[key]
        while temp is not None:
            if temp.key_node.key == key_node.key:
                if temp.key_node.value == key_node.value:
                    return True
                else:
                    return False
            temp = temp.next
        return False

    def PrintTable(self):
        for i in range(self.size):
            temp = self.HashTable[i]
            while temp is not None:
                print(temp.key_node.key, temp.key_node.value)
                temp = temp.next

    def WriteToFile(self, file_path):
        try:
            data = { 'key': [],'value': []}

            for i in range(self.size):
                temp = self.HashTable[i]
                while temp is not None:
                    data['value'].append(temp.key_node.value)
                    data['key'].append(temp.key_node.key)
                    temp = temp.next

            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, header=False)
            print(f"Data written to {file_path}")
        except Exception as e:
            print("Exception: ", e)

    def Rehash(self):
        try:
            print("Rehashing")
            self.size = self.size * 2
            new_table = [None] * self.size
            for i in range(len(self.HashTable)):
                temp = self.HashTable[i]
                while temp is not None:
                    key = self.HashFunction(temp.key_node.key)
                    new_node = LinkedListNode(temp.key_node)

                    if new_table[key] is None:
                        new_table[key] = new_node
                    else:
                        new_temp = new_table[key]
                        while new_temp.next is not None:
                            new_temp = new_temp.next
                        new_temp.next = new_node

                    temp = temp.next

            self.HashTable = new_table
        except Exception as e:
            print("Exception: ", e)

    def retriveDataFromFile(self, file_path):
        try:
            DATA = []
            with open(file_path, 'r') as file:
                for line in file:
                    # Assuming columns are separated by a comma
                    key, value = line.strip().split(',')
                    u = KeyNode(key, value)
                    DATA.append(u)
            for data in DATA:
                self.Insert(data)
        except Exception as e:
            print("Exception: ", e)


if __name__ == "__main__":
    pass
    # hash_table = MyHashTable()
    # hash_table.retriveDataFromFile("output.csv")
    # hash_table.Forgotten_Insertion(KeyNode("garellano", "garellano"))
    # hash_table.PrintTable()
