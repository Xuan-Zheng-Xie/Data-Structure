import argparse
import time


class MyNode(object):
    # this class infor testing
    # Do Not Modify
    def __init__(self, value):
        self.value = value
        self.right = self
        self.left = self

    def __repr__(self):
        return 'Node%s' % (self.value)


class MyStack(object):
    def __init__(self):
        self.num_element = 0
        self.root = MyNode(None)

    def pop(self):
        if self.num_element == 0:
            raise ValueError('Can not execute pop() on an empty stack')
        else:
            self.num_element -= 1
            # ---TODO:
            
            self.curr_temp = self.current
            self.prev_temp = self.previous

            self.current = self.current.left
            if (self.num_element + 1 ) > 2:
                self.previous = self.previous.left

            if self.num_element + 1 > 1:
                # Connect the second last element >> root
                self.prev_temp.right,self.curr_temp.right = self.curr_temp.right,self.prev_temp.right
                # Connect root >> the second last element
                self.curr_temp.left,self.root.left = self.root.left,self.curr_temp.left
                
            else:
                self.curr_temp.left,self.root.right = self.root.right,self.curr_temp.left
                self.curr_temp.right,self.root.left = self.root.left,self.curr_temp.right

            
            
            
            # ---
            #evaluate: python stack.py --input input_2.txt --output output_py_2.txt
            #evaluate: python stack.py --input input_3.txt --output output_py_3.txt


    def push(self, node):
        self.num_element += 1
        # ---TODO:
        self.temp = node
        if self.num_element > 1:
            self.previous = self.current
            self.current = self.temp
            # Connect the last element >> inserted node
            self.current.right,self.previous.right = self.previous.right,self.current.right
            # Connect the inserted node >> root
            self.current.left,self.root.left = self.root.left,self.current.left
            
        else:
            self.previous = self.temp
            self.current = self.temp
            # Connect the inserted node >> root
            self.root.right,self.current.left = self.current,self.root.right
            self.root.left,self.current.right = self.current.right,self.root.left
            
        
        # ---
        #evaluate: python stack.py --input input_1.txt --output output_py_1.txt

    def __repr__(self):
        ret = ''
        node = self.root.right
        while node != self.root:
            ret = ret + '>>' + str(node)
            node = node.right
        return ret


def main(input_file, output_file, has_ofile):
    myStack = MyStack()

    ifile = open(input_file)
    if has_ofile:
        ofile = open(output_file, 'w')
    else:
        ofile = None
    for line in ifile.readlines():
        items = line.strip().split(" ")
        if items[0] == 'PUSH':
            myVal = int(items[1])
            myStack.push(MyNode(myVal))
        else:
            myStack.pop()
        if has_ofile:
            ofile.write(str(myStack) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='./input_1.txt')
    parser.add_argument('--output', default='')
    args = parser.parse_args()
    if len(args.output) > 0:
        has_ofile = True
    else:
        has_ofile = False
    ts = time.time()
    main(args.input, args.output, has_ofile)
    te = time.time()
    if not has_ofile:
        print('stack.py run time of %s: %.5fs' % (args.input, te - ts))
