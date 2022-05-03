import argparse
from itertools import count
from pprint import pprint
import numpy as np
import time


class mono_routing():
    def __init__(self, args):
        pass
    def parser(self): #You can modify it by yourself.
        with open("%s" % args.input, 'r') as file_in:
            f = file_in.read().splitlines()
            
            for lines in f:
                if lines.startswith("BoundaryIndex"):
                    value_list = lines.split(' ')
                    self.Bx1 = int(value_list[1])
                    self.By1 = int(value_list[2])
                    self.Bx2 = int(value_list[3])
                    self.By2 = int(value_list[4])
                if lines.startswith("DefaultCost"):
                    value_list = lines.split(' ')
                    self.default_cost = int(value_list[-1])
                if lines.startswith("NumNonDefaultCost"):
                    value_list = lines.split(' ')
                    self.size = int(value_list[-1])
                    break
            
            source_list = list(f[-2].split(' '))   #change type char into a list!!
            
            target_list = list(f[-1].split(' '))
            
            self.sx = source_list[1]
            self.sy = source_list[2]
            self.tx = target_list[1]
            self.ty = target_list[2]
            """Saving cost"""
            self.NDcost = {}
            for x in range(self.Bx2+1):
                for y in range(self.By2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x,y+1)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x,y+1)] = self.default_cost
            for y in range(self.By2+1):
                for x in range(self.Bx2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x+1,y)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x+1,y)] = self.default_cost
            num_cost = f[3:3+int(self.size)]
            for NDcost in num_cost:
                NDcost_list = NDcost.split(' ')
                self.NDcost[(int(NDcost_list[0]), int(NDcost_list[1]), int(NDcost_list[2]), int(NDcost_list[3]))] += int(NDcost_list[4])
        
        """Print parameters"""
        print('BoundaryIndex:',self.Bx1,self.By1,self.Bx2,self.By2)
        print('DefaultCost:',self.default_cost)
        print('NumNonDefaultCost:',self.size)
        for i in range(len(num_cost)):
            print(num_cost[i])
        print('Source:',self.sx, self.sy)
        print('Target:',self.tx, self.ty)

    def cost(self,x,y):
        
        path1 = (x-1,y,x,y)
        cost1 = self.grid_cost[x-1,y]+self.NDcost[path1]
        path2 = (x,y-1,x,y)
        cost2 = self.grid_cost[x,y-1]+self.NDcost[path2]
        if cost1 == min(cost1,cost2):
            return cost1
        else:
            return cost2

        
    def routing(self):
        self.num_path = self.Bx2+self.By2+1
        self.routing_path = np.zeros((self.Bx2+self.By2+1,2),dtype=int)
        self.grid_cost = np.zeros((self.By2+1,self.Bx2+1),dtype=int)
        # ---TODO:
        # Write down your routing algorithm by using dynamic programming.
        # ---
        #computation
        
        for i in range(min(self.Bx2,self.By2)+1):
            if i>0:
                self.grid_cost[i,i]=self.cost(i,i)
                for j in range(self.Bx2-i):
                    #compare nearby point
                    self.grid_cost[i,i+j+1]=self.cost(i,i+j+1)
                    
                for j in range(self.By2-i):
                    self.grid_cost[i+j+1,i]=self.cost(i+j+1,i)
            else:
                #init
                self.routing_path[0]=[i,i]
                for j in range(self.Bx2): #0~3
                    
                    path = (0,j,0,j+1)
                    self.grid_cost[0,j+1]=self.grid_cost[0,j]+self.NDcost[path]
                for j in range(self.By2):
                    
                    path = (j,0,j+1,0)
                    self.grid_cost[j+1,0]=self.grid_cost[j,0]+self.NDcost[path]
        
        print(self.grid_cost)
        count=0
        current = [self.Bx2,self.By2]
        self.routing_path[self.Bx2+self.By2]=[self.Bx2,self.By2]
        while count<self.Bx2+self.By2+1:
            self.routing_path[self.Bx2+self.By2-count]=[current[0],current[1]]
            if current[0]==0:
                current[1]-=1
            elif current[1]==0:
                current[0]-=1
            else:
                path1 = (current[0]-1,current[1],current[0],current[1])
                print(self.NDcost[path1])
                is_down = self.grid_cost[current[0],current[1]]-self.grid_cost[current[0]-1,current[1]] == self.NDcost[path1]
                path2 = (current[0],current[1]-1,current[0],current[1])
                print(self.NDcost[path2])
                is_left = self.grid_cost[current[0],current[1]]-self.grid_cost[current[0],current[1]-1] == self.NDcost[path2]
                if is_left and is_down:
                    current[1]-=1
                elif is_left:
                    current[1]-=1
                elif is_down:
                    current[0]-=1
                print(is_left,is_down,current,count)
            count+=1
        print(self.routing_path)

            
            
        
        
    def output(self): # You can modify it by yourself, but the output format should be correct.
        with open("%s" % args.output, 'w') as file_out:
            file_out.writelines('RoutingCost %d'% self.grid_cost[self.By2][self.Bx2])
            file_out.writelines('\nRoutingPath %d'% len(self.routing_path))
            for i in range(len(self.routing_path)):
                file_out.writelines('\n%d %d'% (self.routing_path[i][0], self.routing_path[i][1]))
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './500x500.in',help="Input file root.")
    parser.add_argument("--output", type=str, default = './5x5.out',help="Output file root.")
    args = parser.parse_args()

    print('#################################################')
    print('#              Monotonic Routing                #')
    print('################################################# \n')

    routing = mono_routing(args)
    """Parser"""
    routing.parser()
    print('################ Parser Down ####################')
    """monotonic route"""
    start = time.time()
    routing.routing()
    print('run time:', round(time.time()-start,3))
    """output"""
    routing.output()