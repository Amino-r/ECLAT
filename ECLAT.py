class a_rule:
    def __init__(self):
        self.right = {}
        self.left = {}


class itemset:
    def __init__(self,item):
        if isinstance(item, (list, tuple, set)):
            self.item_tid = list(item)
        else:
            self.item_tid =[item]
        self.trans_id =set()
        self.a_rule = a_rule()

    def add_trans_id(self, trans_id):
        if isinstance(trans_id, set):
            self.trans_id.update(trans_id)
        else:
            self.trans_id.add(trans_id)



import pandas as pd
horz_data = pd.read_csv('horz_data.csv')
horz_data.info()
print(horz_data.head())

freqs = []


LVL =1
min_supp = 2
def vertical_data_transform(horz_data):
    vertical_data ={}
    for row in horz_data[["TiD", "items"]].itertuples(index=False):
            for items in row.items:
                if items == ",":
                    continue
                if items not in vertical_data:
                    # print (items , row.TiD)
                    x = itemset(items)
                    x.add_trans_id(row.TiD)
                    vertical_data[items]=x
                else:
                    # print(items, row.TiD)
                    vertical_data[items].add_trans_id(row.TiD)

    for trans_id in horz_data["TiD"]:
        for item_row in horz_data["items"]:
            for n in item_row:
                if n == ",":
                    continue
                if n in vertical_data:
                    if min_supp > len(vertical_data[n].trans_id):
                        del vertical_data[n]
                        vertical_data.pop(n, None)
                # if n in vertical_data:
                #     print(vertical_data[n].trans_id, vertical_data[n].item_tid)
    return vertical_data
def ECLAT(horz_data):
    global LVL
    loop = True
    vertical_data = vertical_data_transform(horz_data)
    freqs.append(vertical_data)
    map_level = {}
    for item1 , t1 in vertical_data.items():
        for item2 , t2 in vertical_data.items():
            if item1 == item2:
                continue
            # print(item1 ,t1.trans_id, item2 , t2.trans_id)
            temp = t1.trans_id & t2.trans_id
            # print(temp)
            if len(temp) >= min_supp:
                hnai = (item1 , item2)
                hnai = tuple(sorted(hnai))
                # print(hnai)
                if hnai  not in map_level:
                    map_level[hnai] = itemset(hnai)
                    map_level[hnai].add_trans_id(temp)
    freqs.append(map_level)
    LVL +=1
    while loop :
        print("loop" , LVL,len(freqs))
        map_level = {}
        k = LVL - 1
        for items1 , tr1 in freqs[k].items():
            for items2 , tr2 in freqs[k].items():
                merge = True
                if items1 == items2:
                   continue
                for a in range(k):
                    if items1[a] != items2[a]:
                       merge = False
                if not merge:
                    continue
                temp = tr1.trans_id & tr2.trans_id
                # print(temp)
                if len(temp) >= min_supp:
                    newitemset = tuple(set(items1) | set(items2))
                    newitemset = tuple(sorted(newitemset))
                    if newitemset not in map_level:
                        map_level[newitemset] = itemset(newitemset)
                        map_level[newitemset].add_trans_id(tr1.trans_id)
        if not map_level:
            break
        LVL+= 1
        freqs.append(map_level)

ECLAT(horz_data)
for ana , inta in freqs[4].items():
    print(ana)
    print(inta.trans_id)



