#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: Shiyu Huang
@contact: huangsy1314@163.com
@file: question2.py
"""
import numpy as np

def generate_data():
    # 从多维高斯分布里面采样训练数据
    np.random.seed(0)
    means = [[0, 0],[4,0],[0,4],[4,4]]
    cov = [[0.5, 0], [0, 0.5]]
    Xs = []
    for i in range(4):
        Xs.append(np.random.multivariate_normal(means[i], cov, 100))
    X = np.concatenate(Xs,axis=0)
    np.random.shuffle(X)
    return X

def distance(a, b):
    # 计算欧几里得距离
    return np.math.sqrt(sum(np.power(a - b, 2)))

class SuperKMeans():
    def __init__(self, k=3, max_iter=500):
        self.k = k
        self.max_iter = max_iter
        self.distance_all = None
        self.labels = None

    def centroid(self):
        # 得到当前中心点
        return self.centroids

    def init_center(self, X):
        # 随机初始化中心
        feature_length = np.shape(X)[1]
        centroids = np.empty((self.k, feature_length))
        for column_index in range(feature_length):
            min_now = min(X[:, column_index])
            range_now = float(max(X[:, column_index] - min_now))
            centroids[:, column_index] = (min_now + range_now * np.random.rand(self.k, 1)).flatten()
        return centroids

    def clustering(self, X):
        # 进行聚类
        X_number = np.shape(X)[0]
        self.distance_all = np.zeros((X_number, 2))
        self.centroids = self.init_center(X)
        for iter_step in range(self.max_iter):
            center_updated = False
            for i in range(X_number):
                min_distance = np.inf
                for j in range(self.k):
                    c_value = self.centroids[j, :]
                    x_value = X[i, :]
                    distance_now = distance(c_value, x_value)  # 计算误差值
                    if distance_now < min_distance :
                        min_distance = distance_now
                        min_index = j
                if self.distance_all[i, 0] != min_index or self.distance_all[i, 1] > min_distance:
                    center_updated = True
                    self.distance_all[i, :] = min_index, min_distance
            if not center_updated:
                break
            # update center
            for i in range(self.k):
                index_all = self.distance_all[:, 0]
                value = np.nonzero(index_all == i)
                target_X = X[value[0]]
                self.centroids[i, :] = np.mean(target_X, axis=0)
        self.labels = self.distance_all[:, 0]

    def membership(self, X):
        # 输入特征，给出分类
        X_number = np.shape(X)[0]
        preds = np.empty((X_number,))
        for i in range(X_number):
            min_distance = np.inf
            for j in range(self.k):
                distance_now = distance(self.centroids[j, :], X[i, :])
                if distance_now < min_distance:
                    min_distance = distance_now
                    preds[i] = j
        return preds

    def demo(self):
        # 一个演示
        # 加载数据
        X = generate_data()
        # 开始训练
        self.clustering(X)
        # 得到中心点
        centers = self.centroid()
        print('centroid:\n',centers)
        # 得到聚类结果，只输出前10个数据点的结果
        Y = self.membership(X)
        print('class of first 10 data point:\n',Y[0:10])
        # 可视化
        import matplotlib.pyplot as plt
        colors = ['y', 'm', 'c', 'b', 'g', 'r', 'k']
        for i in range(self.k):
            # 找出所有同一类别的数据点
            index = np.nonzero(self.labels == i)[0]
            x0 = X[index, 0]
            x1 = X[index, 1]
            label_i = i
            # 画出属于这个类别的所有数据点
            for j in range(len(x0)):
                plt.text(x0[j], x1[j], str(label_i), color=colors[i], fontdict={'weight': 'bold', 'size': 6})
            # 画出中心点
            plt.scatter(centers[i, 0], centers[i, 1], marker='o', color=colors[i%len(colors)], linewidths=7)
        plt.title("K-Means: k ={}".format(self.k))
        min_x0 = min(X[:, 0])-1
        max_x0 = max(X[:, 0])+1
        min_x1= min(X[:,1])-1
        max_x1 = max(X[:, 1])+1

        plt.axis([min_x0, max_x0, min_x1, max_x1])
        plt.show()
        plt.close()


def test_kmeans():
    # init classifier
    k = 4
    kmeans = SuperKMeans(k)
    # run the demo
    kmeans.demo()


if __name__ == "__main__":
    test_kmeans()