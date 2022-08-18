import pandas as pd
import torch
import random


class DataLoader:
    """
        data_length: 使用前N个数字来完成预测，同时N也是MLP模型的层数
    """
    def __init__(self, data_length=5):
        data_file = pd.read_table('./orcl-1995-2014.txt', sep=',', index_col=0, parse_dates=['Date'])
        self.data_length = data_length
        self.close_price = data_file['Close'].values.astype(float).tolist()
        self.train_data, self.test_data = self._data_partition_()

    def _data_partition_(self):
        """
        划分数据为训练集和测试集，这一部分可以改写成按照比例的划分
        :return: 训练和测试数据
        """
        train_data = self.close_price[0:4000]
        test_data = self.close_price[4000:5000]
        return train_data, test_data

    def data_generation(self, data, is_shuffle=True, batch_size = 1):
        """
        生成用于训练和测试的数据集 close_price -> cp
        :param is_shuffle: 是否打乱数据
        :param data: 数据 [cp_1, cp_2, ..., cp_n]
        :return: 数据格式： x-> [x_1, x_2, ..., x_n-1], y-> [x_n]，数据用字典成组（batch）存储，
                 可以通过shuffle来打乱数据格式提高训练效果
        """
        # 生成用于训练和测试的数据的标准格式
        self.batch_size = batch_size
        data_4_batch = []
        for i in range(0, len(data) - self.data_length - 1):
            previous_n_day_data = [data[j] for j in range(i, i + self.data_length)]  # x
            predict_data = [data[i + self.data_length + 1]]  # y
            # ([x_1, x_2, ..., x_n-1], [x_n])
            data_4_batch.append({'previous_n_day_data': previous_n_day_data, 'predict_data': predict_data})
        # print(data_4_batch[0])  # data_length=5, batch_size=3
        # # {'batched_previous_n_day_data': tensor([[14.7500, 15.5000, 15.8750, 15.4400, 16.4200],
        # #                                         [17.7700, 18.4400, 18.0400, 19.1800, 19.0000],
        # #                                         [24.7600, 24.9500, 24.7000, 24.8800, 24.8700]]), 
        # # 'batched_predict_data': tensor([[14.3300],
        # #                                 [19.7700],
        # #                                 [25.0500]])}

        if is_shuffle:
            random.shuffle(data_4_batch)
        batched_data = [data_4_batch[i:i + self.batch_size] for i in range(0, len(data_4_batch), self.batch_size)]
        if self.batch_size != 1:
            batched_data = batched_data[0:-1]

        # 对batch进行处理，将x和y分别聚合成tensor格式，之所以现在做是为了前面的shuffle

        standard_batched_data = []
        for single_batch in batched_data:
            batched_previous_n_day_data = []
            batched_predict_data = []
            for single_data in single_batch:
                batched_previous_n_day_data.append(single_data['previous_n_day_data'])
                batched_predict_data.append(single_data['predict_data'])
            standard_batched_data.append({'batched_previous_n_day_data': torch.tensor(batched_previous_n_day_data),
                                          'batched_predict_data': torch.tensor(batched_predict_data)})
        return standard_batched_data

    def display(self):
        print(len(self.train_data))
        print(len(self.test_data))


def main():
    dl = DataLoader(data_length=5, batch_size=3)
    train_data = dl.data_generation(data=dl.train_data, is_shuffle=True)
    test_data = dl.data_generation(data=dl.test_data, is_shuffle=False)
    print(len(train_data))
    print(len(test_data))
    print(train_data[0])



if __name__ == '__main__':
    main()