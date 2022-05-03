#include "iostream"
#include "string"
#include "fstream"
#include "vector"
#include "stdexcept"
#include "cstdlib"
#include "cassert"
#include "time.h"
#include "cstring"
using namespace std;

class MyStack;
class MyNode
{
    public:
        friend class MyStack;

        MyNode(const int &d) : _value(d), _left(this), _right(this) {}

        friend ostream &operator<<(ostream &out, MyNode *myNode);
        friend ostream &operator<<(ostream &out, MyStack *myStack);

    private:
        int _value;
        MyNode *_left;
        MyNode *_right;
};

ostream &operator<<(ostream &out, MyNode *myNode)
{
    out << "Node" << myNode->_value << "";ㄋ
    return out;
}

class MyStack
{
    public:
        MyStack()
        {
            _root = new MyNode(-1);
            _num_element = 0;
        }
        ~MyStack() { clear(); }
        void pop()
        {
            if (_num_element == 0)
            {
                throw invalid_argument("Can not execute pop() on an empty stack");
            }
            else
            {
                _num_element -= 1;
                // ---TODO:
                MyNode *swap;
                static MyNode *curr_temp,*prev_temp;
                curr_temp = this->_root[0]._left;
                prev_temp = curr_temp[0]._left;



                if (this->_num_element + 1 > 1){
                    // Connect the second last element >> root
                    swap = prev_temp[0]._right;
                    prev_temp[0]._right = curr_temp[0]._right;
                    curr_temp[0]._right = swap;
                    // Connect root >> the second last element
                    swap = curr_temp[0]._left;
                    curr_temp[0]._left = this->_root[0]._left;
                    this->_root[0]._left = swap;
                }
                
                else{
                    // Connect the second last element >> root
                    swap = curr_temp[0]._left;
                    curr_temp[0]._left = this->_root[0]._left;
                    this->_root[0]._left = swap;
                    // Connect root >> the second last element
                    swap = curr_temp[0]._right;
                    curr_temp[0]._right = this->_root[0]._left;
                    this->_root[0]._left = swap;
                }

                // ---
            }
        }
        void push(MyNode *node)
        {
            _num_element += 1;
            // ---TODO:
            MyNode *swap;
            static MyNode *current,*previous;

            if (this->_num_element > 1){
                previous = previous[0]._right;
                current = node;
                // Connect the last element >> inserted node
                swap = current[0]._right;
                current[0]._right = previous[0]._right;
                previous[0]._right = swap;
                // Connect the inserted node >> root
                swap = current[0]._left;
                current[0]._left = this->_root[0]._left;
                this->_root[0]._left = swap;

            }
            else{
                current = node;
                previous = this->_root;
                // Connect the last element >> inserted node
                swap = this->_root[0]._right;
                this->_root[0]._right = current[0]._left;
                current[0]._left = swap;
                // Connect the inserted node >> root
                swap = this->_root[0]._left;
                this->_root[0]._left = current[0]._right;
                current[0]._right = swap;
                
            }
            
            // ---
            //evaluate g++ -g -o stack.cpp; ./stack input_1.txt output_1.txt
        }

        void clear()
        {
            MyNode *temp = _root->_right;
            MyNode *temp2 = temp->_right;
            while (temp != _root)
            {
                delete temp;
                temp = temp2;
                temp2 = temp2->_right;
            }
            delete _root;
        }

        friend ostream &operator<<(ostream &out, MyStack *myStack);

    private:
        MyNode *_root;
        int _num_element;
};

ostream &operator<<(ostream &out, MyStack *myStack)
{
    MyNode *node = myStack->_root->_right;
    while (node != myStack->_root)
    {
        out << ">>" << node;
        node = node->_right;
    }
    return out;
}

vector<string> split_string(string s)
{
    vector<string> v;
    string temp = "";
    for (int i = 0; i < s.length(); ++i)
    {
        if (s[i] == ' ')
        {
            v.push_back(temp);
            temp = "";
        }
        else
        {
            temp.push_back(s[i]);
        }
    }
    v.push_back(temp);
    return v;
}

int main(int argc, char **argv)
{
    clock_t tStart = clock();
    string ifile_name = "input_1.txt";
    string ofile_name = "";
    string mem_str = "mem";
    int index;
    bool has_ofile = false;
    ifstream ifile;
    ofstream ofile;
    vector<string> args(argv, argv + argc);
    if (argc == 3)
    {
        ifile_name = args[1];
        ofile_name = args[2];
        has_ofile = true;
    }
    else if (argc == 2)
    {
        ifile_name = args[1];
    }
    ifile.open(ifile_name);
    if (has_ofile)
    {
        ofile.open(ofile_name);
    }
    if ((index = ifile_name.find(mem_str, 0)) != string::npos)
    {
        printf("Please press any key to start\n");
        cin.ignore();
        printf("start..\n");
    }
    string str;
    MyStack *myStack = new MyStack;
    while (getline(ifile, str))
    {
        vector<string> v = split_string(str);
        if (v[0] == "PUSH")
        {
            int myVal = atoi(v[1].c_str());
            MyNode *myNode = new MyNode(myVal);
            myStack->push(myNode);
        }
        else
        {
            myStack->pop();
        }
        if (has_ofile)
        {
            ofile << myStack << "\n";
        }
    }
    if (has_ofile)
    {
        ofile.close();
    }
    delete myStack;
    if ((index = ifile_name.find(mem_str, 0)) != string::npos)
    {
        printf("Please press any key to exit\n");
        cin.ignore();
        printf("end..\n");
    }
    if (has_ofile == false)
    {
        printf("stack.cpp run time of %s: %.5fs\n", ifile_name.c_str(), (double)(clock() - tStart) / CLOCKS_PER_SEC);
    }
    return 0;
}
