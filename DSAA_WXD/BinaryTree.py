import random


class BtNode:
    left_child = None
    right_child = None
    parent = None
    brother = None
    value = None
    depth = None
    travel_count = None

    def __init__(self, input_depth):
        self.value = None
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.brother = None
        self.depth = input_depth
        self.travel_count = 0

    def set_value(self, input_value):
        self.value = input_value

    def get_value(self):
        return self.value

    def init_left_child(self):
        self.left_child = BtNode(self.depth + 1)
        self.left_child.parent = self
        if self.right_child is not None:
            self.right_child.brother = self.left_child
            self.left_child.brother = self.right_child

    def init_right_child(self):
        self.right_child = BtNode(self.depth + 1)
        self.right_child.parent = self
        if self.left_child is not None:
            self.right_child.brother = self.left_child
            self.left_child.brother = self.right_child

    def occupied(self):
        return self.value is not None

    def is_left_empty(self):
        return self.left_child is None

    def is_right_empty(self):
        return self.right_child is None

    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child

    def has_parent(self):
        return self.parent is not None

    def has_brother(self):
        return self.brother is not None

    def get_parent(self):
        return self.parent

    def get_brother(self):
        return self.brother


def build_a_full_tree(i_list):
    input_list = i_list.copy()
    root_node = BtNode(0)
    node_list = [root_node]
    while len(input_list) > 0:
        new_list = []
        for temp_node in node_list:
            if temp_node.occupied():
                if temp_node.is_left_empty() and (len(input_list) - len(new_list)) > 0:
                    temp_node.init_left_child()
                    new_list.append(temp_node.get_left_child())
                if temp_node.is_right_empty() and (len(input_list) - len(new_list)) > 0:
                    temp_node.init_right_child()
                    new_list.append(temp_node.get_right_child())
            else:
                temp_node.set_value(input_list.pop(0))
                new_list.append(temp_node)
        node_list = new_list
    return root_node


def build_a_heap(i_list):
    input_list = i_list.copy()
    root_node = BtNode(0)
    node_list = [root_node]
    while len(input_list) > 0:
        new_list = []
        for temp_node in node_list:
            if temp_node.occupied():
                if temp_node.is_left_empty() and (len(input_list) - len(new_list)) > 0:
                    temp_node.init_left_child()
                    new_list.append(temp_node.get_left_child())
                if temp_node.is_right_empty() and (len(input_list) - len(new_list)) > 0:
                    temp_node.init_right_child()
                    new_list.append(temp_node.get_right_child())
            else:
                temp = input_list.pop(0)
                parent_node = temp_node.get_parent()
                if parent_node is not None and temp > parent_node.get_value():
                    temp_node.set_value(parent_node.get_value())
                    parent_node.set_value(temp)
                else:
                    temp_node.set_value(temp)
                new_list.append(temp_node)
        node_list = new_list
    return root_node


def build_a_bst(i_list):
    input_list = i_list.copy()
    root_node = BtNode(0)
    temp_node = root_node
    while len(input_list) > 0:
        if temp_node.occupied():
            if input_list[0] >= temp_node.get_value():
                if temp_node.is_right_empty():
                    temp_node.init_right_child()
                temp_node = temp_node.get_right_child()
            else:
                if temp_node.is_left_empty():
                    temp_node.init_left_child()
                temp_node = temp_node.get_left_child()
        else:
            temp_node.set_value(input_list.pop(0))
            temp_node = root_node
    return root_node


def travel_all_nodes(root_node, first_time, last_time):
    root_node.travel_count += 1
    if root_node.travel_count == 1:
        first_time.append(root_node.get_value())
        if not root_node.is_left_empty():
            first_time, last_time = travel_all_nodes(root_node.get_left_child(), first_time, last_time)
        else:
            last_time.append(root_node.get_value())
            first_time, last_time = travel_all_nodes(root_node.get_parent(), first_time, last_time)
    elif root_node.travel_count == 2:
        if not root_node.is_right_empty():
            first_time, last_time = travel_all_nodes(root_node.get_right_child(), first_time, last_time)
        else:
            last_time.append(root_node.get_value())
            first_time, last_time = travel_all_nodes(root_node.get_parent(), first_time, last_time)
    elif root_node.travel_count == 3:
        last_time.append(root_node.get_value())
        if root_node.get_parent() is None:
            return first_time, last_time
        first_time, last_time = travel_all_nodes(root_node.get_parent(), first_time, last_time)
    return first_time, last_time


if __name__ == "__main__":
    il = []
    for z in range(10):
        r = random.randint(0, 100)
        il.append(r)
    il = [26, 59, 98, 57, 82, 84, 10, 58, 8, 84]
    result = build_a_full_tree(il)
    # result = build_a_heap(il)
    # result = build_a_bst(il)
    ft, lt = travel_all_nodes(result, [], [])
    print("Done")
