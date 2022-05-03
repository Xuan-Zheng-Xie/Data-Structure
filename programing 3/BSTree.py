import argparse
from lib2to3.pgen2.token import NEWLINE

class Node():
    #########################
    # DO NOT MODIFY CODES HERE
    #########################
    def __init__(self, key):
        self.value = key
        self.left_child = None
        self.right_child = None

    def __repr__(self):
        return str(self.value)

class Stack():
    def __init__(self):
        self.data = []
    
    def push(self,key):
        self.data.append(key)

    def pop(self):
        return self.data.pop()

    def is_empty(self):
        return self.data == []

class Dequeue():
    def __init__(self):
        self.data = []
    
    def add_front(self,key):
        self.data.append(key)
    
    def add_rear(self,key):
        self.data.insert(0,key)

    def remove_front(self):
        # pop the last item
        return self.data.pop()

    def remove_rear(self):
        # pop the item which index is 0
        return self.data.pop(0)

    def is_empty(self):
        return self.data == []

    def size(self):
        return len(self.data)

    def front(self):
        return self.data[0]
    
    def rear(self):
        return self.data[-1]

class BS_tree():
    def __init__(self):
        self.root = None
        self.treelist = []

    def inorder(self, output):      # print the in-order traversal of binary search tree
        # create a stack
        stack = Stack()

        # the tree is empty
        if not self.root:
            # inorder is none
            output.write('\n')
        # the tree is non-empty
        else:
            # use curr to traversal
            curr = self.root
            while curr or not stack.is_empty():
                # find the most left node and record the path
                while curr:
                    stack.push(curr)
                    curr = curr.left_child
                # as finding the most left node,pop the most left node
                curr = stack.pop()
                self.update_output(curr)

                # change curr to right child
                curr = curr.right_child
            #output the result
            for node in self.treelist:
                output.write(str(node)+' ')
            output.write('\n')
        self.treelist = []

    def preorder(self, output):     # print the pre-order traversal of binary search tree
        # create a stack
        stack = Stack()
        # the tree is empty
        if not self.root:
            # preorder is none
            output.write('\n')
        # the tree is non-empty
        else:
            curr = self.root
            stack.push(curr)
            while not stack.is_empty():
                # change the curr to curr.right_child 
                curr = stack.pop()
                self.update_output(curr)
                if curr.right_child:
                    stack.push(curr.right_child)
                if curr.left_child:
                    stack.push(curr.left_child)
            #output the result
            for node in self.treelist:
                output.write(str(node)+' ')
            output.write('\n')
        self.treelist = []

    def postorder(self, output):    # print the post-order traversal of binary search tree
        stack = Stack()
        if not self.root:
            output.write('\n')
            return

        curr = self.root
        prev = None
        stack.push(curr)
        while not stack.is_empty():
            curr = stack.data[-1]
            is_leaf = (curr.left_child==None) and (curr.right_child==None)
            visited_child = (prev != None) and ((prev==curr.left_child)or(prev==curr.right_child))
            if is_leaf or visited_child:
                self.update_output(stack.pop())
                prev =curr
            else:
                if not (curr.right_child == None):
                    stack.push(curr.right_child)
                if not (curr.left_child == None):
                    stack.push(curr.left_child)
        # output the result
        for node in self.treelist:
            output.write(str(node)+' ')
        output.write('\n')
        self.treelist = []

    def find_max(self, output):     # print the maximum number in binary search tree
        max = None
        
        # if the tree is empty,then no maximum
        if not self.root:
            pass
        # if the tree is non-empty,then fing the rightest node in the tree
        else:
            # node of currently traversal
            curr = self.root
            # start traversal to the rightest from the root
            while curr.right_child:
                curr = curr.right_child
                max = curr
        # output the result
        output.write(str(max)+'\n')
        
    def find_min(self, output):     # print the minimum number in binary search tree
        min = None
        # if the tree is empty,then no minimum
        if not self.root:
            pass
        else:
            # node of currently traversal
            curr = self.root

            # start traversal to the leftest from the root
            while curr.left_child:
                curr = curr.left_child
                min = curr
        # output the result
        output.write(str(min)+'\n')
        
    def insert(self, key):          # insert one node
        if self.root:
            self._insert(key, self.root)
        else:
            self.root = Node(key)
        
    def delete(self, key):          # delete one node
        # pointer of the parent of the current node
        parent = None

        # start with the current node
        curr = self.root

        # search key in the BST and set its parent pointer
        while curr and curr.value!=key:
            parent = curr
            if curr.value < key:
                curr = curr.right_child
            else:
                curr = curr.left_child
        if curr == None:
            return

        # Inorder to delete a node,only needed is to justify the pointer of parent and the pointer of children
        # case1: node to be delete has no children
        if not curr.left_child and not curr.right_child:
            # delete the node immediately
            
            # if the node is not root,then set the parent left/right child to None
            if curr != self.root:
                if parent.left_child:
                    parent.left_child = None
                else:
                    parent.right_child = None
            else:
            # if the node is root,then set the root to None
                self.root = None
        # case2: node to be delete has two children
        elif curr.left_child and curr.right_child:
            # find the maximum node of left subteree
            max_left_subtree = curr.left_child
            while max_left_subtree.right_child:
                max_left_subtree = max_left_subtree.right_child

            # firstly,store the vak=lue of maximum of leftsubtree
            temp = max_left_subtree.value

            # recursively delete the maximum node
            self.delete(max_left_subtree.value)

            # substitude the maximum value to the node
            curr.value = temp

        # case3: node to be delete has one children
        else:
            # there are 4 cases of the node of parent and the node of target
            # when the node only has one child
            
            # find the parent and child saperately can handle the 4 cases
            # choose the child node
            if curr.left_child:
                child = curr.left_child
            else:
                child = curr.right_child

            # if the node to be deleted is not root,then set its parent to its child
            if curr != self.root:
                if parent.left_child == curr:
                    parent.left_child = child
                else:
                    parent.right_child = child
            
            # if the node to be deleted is root,then set the root to its child
            else:
                self.root = child 
        
    def level(self, output):        # print the height of binary search tree(leaf = 0)
        # height of a node is number of edges on the longest downward path between that node and leaf node
        # depth of a node is number of edges on the downward path between root to that node
        # level is depth +1
        dequeue = Dequeue()
        # level of the tree
        height = 0

        # if the tree is empty,then return 0
        if not self.root:
            # height is  0
            pass
            
        else:
            # start from empty,hence height is initially -1
            dequeue.add_rear(self.root)
            height = -1
            while not dequeue.is_empty():
                height += 1
                # number of nodes in the level
                number = dequeue.size()

                # find all nodes in the level
                while number > 0:
                    number -= 1
                    node = dequeue.front()
                    # add their children to the front
                    if node.left_child:
                        dequeue.add_front(node.left_child)
                    if node.right_child:
                        dequeue.add_front(node.right_child)

                    # remove the nodes in the level
                    dequeue.remove_rear()

        output.write(str(height)+'\n')
        
    def internalnode(self, output): # print the internal node in binary search tree from the smallest to the largest
        # the node grom smallest to largest is the inorder of sorted bst
        # create a stack
        stack = Stack()

        # the tree is empty
        if not self.root:
            # inorder is none
            output.write('\n')
        # the tree is non-empty
        else:
            # use curr to traversal
            curr = self.root
            while curr or not stack.is_empty():
                # find the most left node and record the path
                while curr:
                    stack.push(curr)
                    curr = curr.left_child
                # as finding the most left node,pop the most left node
                curr = stack.pop()
                
                if curr.left_child or curr.right_child: # check if curr is internal node
                    self.update_output(curr)

                # change curr to right child
                curr = curr.right_child
            #output the result
            for node in self.treelist:
                output.write(str(node)+' ')
            output.write('\n')
        self.treelist = []
        
    def leafnode(self, output):     # print the leafnode in BST from left to right
        # implmenting inorder traversl(from left to right) and check if is leafnode        
        # create a stack
        stack = Stack()

        # if it is empty tree,then inorder is none 
        if not self.root:
            output.write('\n')
            return
        
        # use curr to traversal
        curr = self.root
        while curr or not stack.is_empty():
            # find the leftest node and record the path
            while curr:
                stack.push(curr)
                curr = curr.left_child
            # as finding the most left node,pop the leftest node
            curr = stack.pop()
            
            if not curr.left_child and not curr.right_child: # check if curr is leaf
                self.update_output(curr)

            # change curr to right child
            curr = curr.right_child
        
        #output the result
        for node in self.treelist:
            output.write(str(node)+' ')
        output.write('\n')
        self.treelist = []

    def _insert(self, key, curNode):  # recursively insert node
        if key < curNode.value:
            if curNode.left_child:
                self._insert(key, curNode.left_child)
            else:
                curNode.left_child = Node(key)
        elif key > curNode.value:
            if curNode.right_child:
                self._insert(key, curNode.right_child)
            else:
                curNode.right_child = Node(key)
        else:
            print("No way!!! There is the same value in this tree.")

    def update_output(self, curNode):
        self.treelist.append(curNode.value)
         
    def main(self, input_path, output_path):
        #########################
        # DO NOT MODIFY CODES HERE
        #########################
        output = open(output_path, 'w')
        with open(input_path, 'r') as file_in:  #, newline=''
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("insert"):
                    value_list = lines.split(' ')
                    for value in value_list[1:]:
                        self.insert(int(value))
                if lines.startswith('inorder'):
                    self.inorder(output)
                if lines.startswith('preorder'):
                    self.preorder(output)
                if lines.startswith('postorder'):
                    self.postorder(output)
                if lines.startswith('max'):
                    self.find_max(output)
                if lines.startswith('min'):
                    self.find_min(output)
                if lines.startswith('delete'):
                    value_list = lines.split(' ')
                    self.delete(int(value_list[1]))
                if lines.startswith('level'):
                    self.level(output)
                if lines.startswith('internalnode'):
                    self.internalnode(output)
                if lines.startswith('leafnode'):
                    self.leafnode(output)
        output.close()

if __name__ == '__main__':
    #########################
    # DO NOT MODIFY CODES HERE
    #########################
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str,
                        default='./input_1.txt', help="Input file root.")
    parser.add_argument("--output", type=str,
                        default='./output_1.txt', help="Output file root.")
    args = parser.parse_args()

    BS = BS_tree()
    BS.main(args.input, args.output)
