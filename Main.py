from typing import Optional, Union

class Node:
    

    def __init__(self, value: object, color: str) -> None:
        
        self.value = value
        self.color = color
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None



class RBTree:
   
    def __init__(self) -> None:
        
        self.root: Optional[Node] = None

    def _check_type(self, value):
       
        return type(self.root.value) == type(value)

    def insert(self, value: object) -> None:
        
        new_node = Node(value, "красный")

        
        if self.root is None:
            self.root = new_node
            self.root.color = "черный"

        
        elif self._check_type(value):
            self._insert_node(self.root, new_node)
        else:
            print(f"работать с {type(self.root.value)}")

    def _insert_node(self, current: Node, new_node: Node) -> None:
       
        if new_node.value < current.value:
            if current.left is None:
                
                current.left = new_node
                new_node.parent = current
            else:
                
                self._insert_node(current.left, new_node)
        else:
            if current.right is None:
                
                current.right = new_node
                new_node.parent = current
            else:
                
                self._insert_node(current.right, new_node)

       
        self._fix_insertion(new_node)

    def _fix_insertion(self, node: Node) -> None:
       
        while node.parent is not None and node.parent.color == "красный":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color == "красный":
                   
                    node.parent.color = "черный"
                    uncle.color = "черный"
                    node.parent.parent.color = "красный"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        
                        node = node.parent
                        self._rotate_left(node)
                    
                    node.parent.color = "черный"
                    node.parent.parent.color = "красный"
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color == "красный":
                    
                    node.parent.color = "черный"
                    uncle.color = "черный"
                    node.parent.parent.color = "красный"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        
                        node = node.parent
                        self._rotate_right(node)
                   
                    node.parent.color = "черный"
                    node.parent.parent.color = "красный"
                    self._rotate_left(node.parent.parent)

        
        self.root.color = "черный"

    def _rotate_left(self, node: Node) -> None:
        
        new_node = node.right
        node.right = new_node.left
        if new_node.left is not None:
            new_node.left.parent = node
        new_node.parent = node.parent
        if node.parent is None:
            self.root = new_node
        elif node == node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        new_node.left = node
        node.parent = new_node

    def _rotate_right(self, node: Node) -> None:
       
        new_node = node.left
        node.left = new_node.right
        if new_node.right is not None:
            new_node.right.parent = node
        new_node.parent = node.parent
        if node.parent is None:
            self.root = new_node
        elif node == node.parent.right:
            node.parent.right = new_node
        else:
            node.parent.left = new_node
        new_node.right = node
        node.parent = new_node

    def search(self, value: object) -> Union[object, None]:
       
        res = self._find_node(self.root, value)
        return res if res is None else res.value

    def delete(self, value: object) -> None:
       
        if self._check_type(value):
            node_to_delete = self._find_node(self.root, value)
            if node_to_delete is None:
                return

           
            self._delete_helper(node_to_delete)

    def _find_node(self, current: Node, value: object) -> Optional[Node]:
        
        if current is None or current.value == value:
            return current
        if value < current.value:
            return self._find_node(current.left, value)
        return self._find_node(current.right, value)

    def _delete_helper(self, node: Node) -> None:
        
        if node.left is not None and node.right is not None:
            successor = self._minimum(node.right)
            node.value = successor.value
            node = successor

        
        child = node.left if node.left is not None else node.right

        
        if node.color == "черный" and child is Node:
            node.color = child.color
            self._delete_case1(node)
        self._swap_node(node, child)

    @staticmethod
    def _minimum(node: Node) -> Node:
        
        while node.left is not None:
            node = node.left
        return node

    def _delete_case1(self, node: Node) -> None:
        
        if node.parent is None:
            return
        self._delete_case2(node)

    def _delete_case2(self, node: Node) -> None:
        
        sibling = self._sibling(node)
        if sibling.color == "красный":
            node.parent.color = "красный"
            sibling.color = "черный"
            if node == node.parent.left:
                self._rotate_left(node.parent)
            else:
                self._rotate_right(node.parent)
        self._delete_case3(node)

    def _delete_case3(self, node: Node) -> None:
      
        sibling = self._sibling(node)
        if (node.parent.color == "черный" and sibling.color == "черный" and
                sibling.left.color == "черный" and sibling.right.color == "черный"):
            sibling.color = "красный"
            self._delete_case1(node.parent)
        else:
            self._delete_case4(node)

    def _delete_case4(self, node: Node) -> None:
       
        sibling = self._sibling(node)
        if sibling is not None and (node.parent.color == "красный" and sibling.color == "черный" and
                                    sibling.left is not None and sibling.left.color == "черный" and
                                    sibling.right is not None and sibling.right.color == "черный"):
            sibling.color = "красный"
            node.parent.color = "черный"
        else:
            self._delete_case5(node)

    def _delete_case5(self, node: Node) -> None:
        """
        Правило 5 для удаления узла из дерева.

        Args:
            node (Node): Узел для удаления
        """
        if node.parent is None:
           
            return

        sibling = self._sibling(node)
        if sibling is None:
            
            return

        if sibling.color == "черный":
            if (node == node.parent.left and
                    (sibling.right is None or sibling.right.color == "черный") and
                    sibling.left.color == "красный"):
                sibling.color = "красный"
                sibling.left.color = "черный"
                self._rotate_right(sibling)
            elif (node == node.parent.right and sibling.left.color == "черный" and
                  sibling.right.color == "красный"):
                sibling.color = "красный"
                sibling.right.color = "черный"
                self._rotate_left(sibling)
        self._delete_case6(node)

    def _delete_case6(self, node: Node) -> None:
       
        sibling = self._sibling(node)
        sibling.color = node.parent.color
        node.parent.color = "черный"
        if node == node.parent.left:
            sibling.right.color = "черный"
            self._rotate_left(node.parent)
        else:
            sibling.left.color = "черный"
            self._rotate_right(node.parent)

    @staticmethod
    def _sibling(node: Node) -> Node:
        
        if node == node.parent.left:
            return node.parent.right
        return node.parent.left

    def _swap_node(self, node: Node, child: Node) -> None:
        
        if child is not None:
            child.parent = node.parent
        if node.parent is None:
            self.root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child

    def to_list(self) -> list:
        
        result = []
        self._traverse_inorder(self.root, result)
        return result

    def _traverse_inorder(self, node: Node, result: list) -> None:
       
        if node is not None:
            self._traverse_inorder(node.left, result)
            result.append(node.value)
            self._traverse_inorder(node.right, result)

    def print_tree(self) -> None:
        """
        Вывод дерева в терминал.
        """
        self._print_tree_helper(self.root, "", True)

    def _print_tree_helper(self, node: Node, indent: str, last: bool) -> None:
        
        if node is not None:
            print(indent, end="")
            if last:
                print("\\-- ", end="")
                indent += "   "
            else:
                print("|-- ", end="")
                indent += "|  "

            print(f"{node.value} ({node.color})")

            self._print_tree_helper(node.left, indent, False)
            self._print_tree_helper(node.right, indent, True)




def go():
  
    tree_str = RBTree()
    tree_str.insert("avocado")
    tree_str.insert("apricot")
    tree_str.insert("banana")
    tree_str.insert("papaya")
    tree_str.insert("date")
    tree_str.insert("pineapple")
    tree_str.insert("fig")
    tree_str.insert("peach")
    tree_str.insert(True)

    tree_str.print_tree()
    print()
    tree_digit = RBTree()

    tree_digit.insert(10)
    tree_digit.insert(20)
    tree_digit.insert(40)
    tree_digit.insert(60)
    tree_digit.insert(50.5)
    tree_digit.insert(80)
    tree_digit.insert(60)
    tree_digit.insert("100")
    tree_digit.insert(45)
    tree_digit.insert(90)
    tree_digit.insert(100)
    tree_digit.insert(45)
    tree_digit.insert(90)
    tree_digit.insert(25)
    tree_digit.print_tree()
    print()
    print(tree_digit.to_list(), tree_str.to_list(), sep="\n")
    print(">>> ", tree_str.search("python"))
    print(">>> ", tree_str.search("Python"))
    print(">>> ", tree_digit.search(40))
    tree_digit.delete(20)

    tree_digit.print_tree()


if __name__ == '__main__':
    go()