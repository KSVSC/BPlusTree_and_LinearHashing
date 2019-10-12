import sys

LHash_ds = {}
blk_size = 4
tot_rec = 0
tot_blk_cnt = 2
blk_cnt = {}
blk_cnt[0] = 1
blk_cnt[1] = 1
mod1 = 2
mod2 = 4
bucket_cnt = 2
split_bkt = 0

filename = sys.argv[1]
out_buffer = []
ip_buffer = []

def insert_into_hash_table(num):
    global out_buffer
    global tot_rec
    global tot_blk_cnt

    hash_clc = num % mod1
    if hash_clc < split_bkt:
        hash_clc = num % mod2
    if hash_clc not in LHash_ds:
        LHash_ds[hash_clc] = [[] for _ in range(1)]

    flg = 0
    for i in range(blk_cnt[hash_clc]):
        if num in LHash_ds[hash_clc][i]:
            flg = 1
    if flg == 0:
        tot_rec += 1
        temp = blk_cnt[hash_clc] - 1
        if len(LHash_ds[hash_clc][temp]) >= 1:
            tot_blk_cnt += 1
            temp += 1
            blk_cnt[hash_clc] += 1
            l = []
            LHash_ds[hash_clc].append(l)
        LHash_ds[hash_clc][temp].append(num)

        out_buffer.append(num)
        if len(out_buffer) >= 1:
            for val in out_buffer:
                print(str(val))
            out_buffer = []
    
    if hash_table_full():
        create_new_bkt()

def hash_table_full():
    global mod1

    density = (tot_rec * 400.0) / (blk_size * tot_blk_cnt)
    if density > 75.0:
        return 1
    return 0

def create_new_bkt():
    global bucket_cnt
    global mod1
    global mod2
    global tot_blk_cnt
    global split_bkt

    bucket_cnt += 1
    rehash_arr = []

    for i in range(blk_cnt[split_bkt]):
        for val in LHash_ds[split_bkt][i]:
            rehash_arr.append(val)

    tot_blk_cnt -= blk_cnt[split_bkt]
    
    LHash_ds[split_bkt] = [[] for _ in range(1)]
    blk_cnt[split_bkt] = 1
    tot_blk_cnt += 1
    
    LHash_ds[bucket_cnt - 1] = [[] for _ in range(1)]
    blk_cnt[bucket_cnt - 1] = 1
    tot_blk_cnt += 1
    
    for val in rehash_arr:
        hash_clc = val % mod2

        if hash_clc not in LHash_ds:
            LHash_ds[hash_clc] = [[] for _ in range(1)]
            blk_cnt[hash_clc] = 1
            tot_blk_cnt += 1
        
        flg = 0
        for j in range(blk_cnt[hash_clc]):
            if val in LHash_ds[hash_clc][j]:
                flg = 1
                
        if flg == 0:
            temp = blk_cnt[hash_clc] - 1
            if len(LHash_ds[hash_clc][temp]) >= 1:
                temp += 1
                blk_cnt[hash_clc] += 1
                tot_blk_cnt += 1
                l = []
                LHash_ds[hash_clc].append(l)
            LHash_ds[hash_clc][temp].append(val)
    split_bkt += 1
    
    if bucket_cnt == mod2:
        mod1 = mod1 * 2
        mod2 = 2 * mod1
        split_bkt = 0

    return

ip_file = open(filename)
for line in ip_file:
    ip = int(line.strip())
    ip_buffer.append(ip)

if len(ip_buffer) >= 1:
    for num in ip_buffer:
        insert_into_hash_table(num) 
    ip_buffer = []
