class AVLNode:
    def __init__(self, car):
        self.car = car
        self.left = None
        self.right = None
        self.height = 1  # Height of the node in the AVL tree


class AVLTree:
    def __init__(self,arr = None):
        self.root = None
        if not arr is None:
            for i in arr:
                self.insert(i)

    def insert(self, car):
        self.root = self._insert(self.root, car)

    def _insert(self, root, car):
        if not root:
            return AVLNode(car)

        # Compare based on price
        if car.price < root.car.price:
            root.left = self._insert(root.left, car)
        else:
            root.right = self._insert(root.right, car)

        # Update the height of the current node
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Perform balancing
        return self._balance(root, car)

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, z):
        y = z.left

        # Check if y is None
        if not y:
            return z

        # Check if y has a right child
        if y.right:
            T2 = y.right
        else:
            T2 = None

        y.right = z
        z.left = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y


    def _rotate_left(self, y):
        x = y.right

        # Check if x is None
        if not x:
            return y

        # Check if x has a left child
        if x.left:
            T2 = x.left
        else:
            T2 = None

        x.left = y
        y.right = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x


    def _balance(self, node, car):
        if not node:
            return None

        # Update height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Get the balance factor
        balance = self._get_balance(node)

        # Left Heavy
        if balance > 1:
            if node.left and car.price < node.left.car.price:
                return self._rotate_right(node)
            if node.left and car.price > node.left.car.price:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        # Right Heavy
        if balance < -1:
            if node.right and car.price > node.right.car.price:
                return self._rotate_left(node)
            if node.right and car.price < node.right.car.price:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node
    def delete(self, car):
        self.root = self._delete(self.root, car)

    def _delete(self, root, car):
        if not root:
            return root

        if car.price < root.car.price:
            root.left = self._delete(root.left, car)
        elif car.price > root.car.price:
            root.right = self._delete(root.right, car)
        else:
            # Node to be deleted found
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            root.car = self._get_min_value_node(root.right).car
            root.right = self._delete(root.right, root.car)

        # Update the height of the current node
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Perform balancing
        return self._balance(root, car)

    def _get_min_value_node(self, root):
        while root.left:
            root = root.left
        return root
    
    