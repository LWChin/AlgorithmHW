# -*- coding: utf-8 -*-
"""
Created on Fri May 14 19:21:57 2021

@author: User
"""
#Reference：https://ithelp.ithome.com.tw/articles/10211706

import random as rd
import copy
from matplotlib import pyplot as plt
import time
import numpy as np


class Location: #城市 vertex
    def __init__(self, name):
        self.name = name


def create_locations(n):
    locations = []
    name = [i for i in range(0, n)]
    for i in name:
        locations.append(Location(i))
    return locations


class Route: #路徑
    def __init__(self, path, W):
        # path is a list of Location obj
        self.path = path #一個list 裡面裝著一個個Location物件 20個(x, y)
        self.length = self._set_length(W) #這條路徑的長度
    
    def _set_length(self, W): #透過path來計算路徑長度的函式
        total_length = 0
        path_copy = self.path[:]
        from_here = path_copy.pop(0)
        init_node = copy.deepcopy(from_here)
        while path_copy:
            to_there = path_copy.pop(0)
            total_length += W[int(from_here.name)][int(to_there.name)]
            from_here = copy.deepcopy(to_there)
        total_length += W[int(from_here.name)][int(init_node.name)]
        return total_length


class GeneticAlgo:
    #Step1. 初始化重要參數
    def __init__(self, locs, matrix, level=10, populations=100, variant=3, mutate_percent=0.1, elite_save_percent=0.1):
        self.locs = locs #要走的城市有哪些（注意locs是一個list裡面裝著Location物件）
        self.level = level #子代的代數（進化次數）
        self.variant = variant #父母代跟子代的變異度
        self.populations = populations #由幾個不同路徑組成一個群體
        self.mutates = int(populations * mutate_percent) #一個群體當中有多少比例是突變來的
        self.elite = int(populations * elite_save_percent) #一群路徑當中，最短的幾％路徑被視為精英路徑
        self.matrix = matrix
        
    #Step2. 建立第一代的路徑群體
    def _find_path(self): #從self.locs(要走的城市)當中隨機生成可行的路徑（每個都要走到），然後回傳這個路徑回來
        # locs is a list containing all the Location obj
        locs_copy = self.locs[:]
        path = []
        while locs_copy:
            to_there = locs_copy.pop(locs_copy.index(rd.choice(locs_copy))) #pop():把東西拿出來
            path.append(to_there)
        return path

    def _init_routes(self): #負責呼叫_find_path來取得路徑，再用這個路徑來生成Route物件
        routes = []
        for _ in range(self.populations): #次數:可行的路徑數
            path = self._find_path()
            routes.append(Route(path, self.matrix))
        return routes #一個list，可行性物件們，裡面裝著許多的Route物件

    #Step3. 產生下一代
    def _get_next_route(self, routes):
        routes.sort(key=lambda x: x.length, reverse=False) #把一個群體（路徑們）按照他們的路徑長度做排序
        elites = routes[:self.elite][:] #取出前面幾％的路徑做為菁英群體
        crossovers = self._crossover(elites) #呼叫_crossover來取得繁衍後的子代(直接讓菁英群體保送到下一代)
        return crossovers[:] + elites

    def _crossover(self, elites):
        # Route is a class type
        normal_breeds = []
        mutate_ones = []
        for _ in range(self.populations - self.mutates):
            father, mother = rd.choices(elites[:4], k=2) #從菁英路徑們當中的前四名隨機取出兩個作為父和母
            index_start = rd.randrange(0, len(father.path) - self.variant - 1) #隨機擷取父親染色體的一部分
            # list of Location obj
            father_gene = father.path[index_start: index_start + self.variant] #隨機擷取父親染色體的一部分
            father_gene_names = [loc.name for loc in father_gene]
            mother_gene = [gene for gene in mother.path if gene.name not in father_gene_names] #移除母親染色體當中含有父親那小節染色體的部分，同時決定要從哪裡放入父親那小節染色體
            mother_gene_cut = rd.randrange(1, len(mother_gene))
            # create new route path
            next_route_path = mother_gene[:mother_gene_cut] + father_gene + mother_gene[mother_gene_cut:]
            next_route = Route(next_route_path, self.matrix) #子代路徑
            # add Route obj to normal_breeds
            normal_breeds.append(next_route)

            # for mutate purpose
            copy_father = copy.deepcopy(father)
            idx = range(len(copy_father.path))
            gene1, gene2 = rd.sample(idx, 2)
            copy_father.path[gene1], copy_father.path[gene2] = copy_father.path[gene2], copy_father.path[gene1] #隨機調換父路徑當中的兩座城市作為突變
            mutate_ones.append(copy_father)
        mutate_breeds = rd.choices(mutate_ones, k=self.mutates) #只要self.mutates這麼多個突變個數
        return normal_breeds + mutate_breeds

    #Step4. 進化
    #初始化群體 -> 繁衍新群體(重複self.level次（子代代數）) -> 得到最後的群體
    def evolution(self):
        routes = self._init_routes()
        for _ in range(self.level):
            routes = self._get_next_route(routes)
        routes.sort(key=lambda x: x.length)
        return routes[0].path, routes[0].length

def traveling_salesperson_genetic(n, W):
    start_time = time.time()
    my_locs = create_locations(n)
    my_algo = GeneticAlgo(my_locs, W, level=100, populations=150, variant=2, mutate_percent=0.02, elite_save_percent=0.15)
    # variant:決定基因的長度 level:子代代數
    best_route, best_route_length = my_algo.evolution()
    best_route.append(best_route[0])
#    print("Shortest length:", best_route_length)
#    print("Path:", [loc.name for loc in best_route])
    #print([(loc.loc[0], loc.loc[1]) for loc in best_route], best_route_length)
    end_time = time.time()
#    print("Run time:", end_time-start_time)
    return best_route_length, end_time-start_time