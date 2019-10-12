import sys
import bisect

class B_Node:
    def __init__(self):
        self.keys = []
        self.child = []
        self.leaf = True
        self.next = None

    def Split(self):
        newnode = B_Node()
        if self.leaf:
            newnode.leaf = True

            mid = int(len(self.keys) / 2)
            midKey = self.keys[mid]

            newnode.keys = self.keys[mid:]
            newnode.child = self.child[mid:]

            self.keys = self.keys[:mid]
            self.child = self.child[:mid]

            newnode.next = self.next
            self.next = newnode

        else:
            newnode.leaf = False
            mid = int(len(self.keys) / 2)
            midKey = self.keys[mid]

            newnode.keys = self.keys[mid+1:]
            newnode.child = self.child[mid+1:]
            
            self.keys = self.keys[:mid]
            self.child = self.child[:mid+1]

        return midKey, newnode

class BPlus_Init:
    def __init__(self, order):
        self.order = order
        self.root = B_Node()
        self.root.leaf = True
        self.root.keys = []
        self.root.child = []
        self.root.next = None

    def print_order(self):
        print("Printing the B+ Tree")
        this_level = [self.root]
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.child and node.leaf == False:
                    next_level.extend(node.child)
                    output += str(node.keys) + " "
            print(output)
            this_level = next_level
            for node in this_level:
                    output += str(node.keys) + " "
            print(output)

    def insert_node(self, key):
        n1, n2 = self.insert_key(key, self.root)
        if n1:
            newroot = B_Node()
            newroot.leaf = False
            newroot.keys = [n1]
            newroot.child = [self.root, n2]
            self.root = newroot

    def insert_key(self, key, node):
        if node.leaf:
            idx = bisect.bisect(node.keys, key)
            node.keys[idx:idx] = [key]
            node.child[idx:idx] = [key]

            if len(node.keys) <= self.order - 1:
                return None, None
            else:
                mid, new = node.Split()
                return mid, new
        
        else:
            if key < node.keys[0]:
                n1, n2 = self.insert_key(key, node.child[0])
                
            for i in range(len(node.keys) - 1):
                if key >= node.keys[i] and key < node.keys[i + 1]:
                    n1, n2 = self.insert_key(key, node.child[i + 1])
            
            if key >= node.keys[-1]:
                n1, n2 = self.insert_key(key, node.child[-1])
        
        if n1:
            idx = bisect.bisect(node.keys, n1)
            node.keys[idx:idx] = [n1]
            node.child[idx + 1:idx + 1] = [n2]
            if len(node.keys) <= self.order - 1:
                return None, None
            else:
                mid, new = node.Split()
                return mid, new
        else:
            return None, None

    def find(self, key, node):
        if node.leaf:
            return node

        else:
            if key <= node.keys[0]:
                return self.find(key, node.child[0])
            
            for i in range(len(node.keys) - 1):
                if key > node.keys[i] and key < node.keys[i + 1]:
                    return self.find(key, node.child[i])
                if key == node.keys[i + 1]:
                    return self.find(key, node.child[i + 1])

            if key > node.keys[-1]:
                return self.find(key, node.child[-1])

    def range_keys(self, key1, key2, node):
        cnt = 0
        for i in range(len(node.keys)):
            key = node.keys[i]
            if key >= key1 and key <= key2:
                cnt += 1
        if len(node.keys) == 0:
            return 0, None
        
        if node.keys[-1] > key2:
            next_node = None
        
        else:
            if node.next and node.next.keys[0] <= key2:
                next_node = node.next
            else:
                next_node = None
        return cnt, next_node

    def count_number(self, key):
        cnt = 0
        l1 = self.find(key, self.root)

        count, next_node = self.range_keys(key, key, l1)
        cnt += count

        while next_node:
            count, next_node = self.range_keys(key, key, next_node)
            cnt += count
        return cnt

    def range_count(self, key1, key2):
        cnt = 0
        l1 = self.find(key1, self.root)

        count, next_node = self.range_keys(key1, key2, l1)
        cnt += count

        while next_node:
            count, next_node = self.range_keys(key1, key2, next_node)
            cnt += count

        return cnt


filename = sys.argv[1]
ip_buffer = []
out_buffer = []

ptr_count = 4
B_tree = BPlus_Init(ptr_count)


def execute(cmd,i):
    global out_buffer
    if cmd[0] == "INSERT":
        B_tree.insert_node(int(cmd[1]))
    
    elif cmd[0] == "FIND":
        cnt = B_tree.count_number(int(cmd[1]))
        if cnt == 0:
            out_buffer.append("NO")
        else:
            out_buffer.append("YES")
    
    elif cmd[0] == "COUNT":
        cnt = B_tree.count_number(int(cmd[1]))
        out_buffer.append(str(cnt))

    elif cmd[0] == "RANGE":
        out = B_tree.range_count(int(cmd[1]), int(cmd[2]))
        out_buffer.append(str(out))
    
    if len(out_buffer) >= 1:
        for out in out_buffer:
            print(out)
        out_buffer = []

ip_file = open(filename)
i = 0
for line in ip_file:
    cmd = line.strip().split()
    ip_buffer.append(cmd)
    if len(ip_buffer) >= 1:
        for cmd in ip_buffer:
            i += 1
            execute(cmd,i)
        ip_buffer = []
B_tree.print_order()
