import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.optim as optim
from mlp_model import MLPModel
from dataloader import DataLoader
import numpy as np
import itertools

def train(model, epoch, train_data, criterion, optimizer, device):
    for iter_num in range(epoch):
        #train
        model.train()
        for batch in train_data:
            x = batch['batched_previous_n_day_data'].to(device)
            y = batch['batched_predict_data'].to(device)
            pred_y = model(x)
            loss = criterion(pred_y, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print("iter_num {}  loss {}".format(iter_num,loss.item()))
    return model


def evaluate(model, test_data, device, steps=1):
    # test
    with torch.no_grad():
        model.eval()
        real_data = []
        predict_data = []
        for batch in test_data:
            step_real_data = []
            step_predict_data = []
            x = batch['batched_previous_n_day_data'].to(device)
            y = batch['batched_predict_data'].to(device)
            for step_num in range(steps):
                pred_y = model(x)        
                step_real_data.extend(list(itertools.chain.from_iterable(y.tolist())))
                step_predict_data.extend(list(itertools.chain.from_iterable(pred_y.tolist())))
                x = torch.cat((x,pred_y), 1)[:, 1:]
            real_data.append(step_real_data)
            predict_data.append(step_predict_data)
    real_data = np.array(real_data)[:,-1]
    predict_data = np.array(predict_data)
    real_data = real_data[steps-1:]
    predict_data = predict_data[:-steps+1]
    # print(real_data[0:20])
    # print(predict_data[0:20])
    return real_data, predict_data


def draw(real_data, predict_data):
    predict_data = predict_data[:, -1]

    # 测试集预测图
    plt.plot(list(range(0, len(real_data), 1)), real_data, color="red", label="real_data")
    plt.plot(list(range(0, len(predict_data), 1)), predict_data, color="blue", label="predict_data")
    plt.legend()
    plt.xlabel("date")
    plt.ylabel("close_price")
    plt.title("real data and predicted data")
    plt.show()

    for temp in range(0,900,20):
        plt.plot(list(range(0, 20, 1)), real_data[temp:temp+20], color="red", label="real_data")
        plt.plot(list(range(0, 20, 1)), predict_data[temp:temp+20], color="blue", label="predict_data")
        plt.legend()
        plt.xlabel("date")
        plt.ylabel("close_price")
        plt.title("real data and predicted data")
        plt.show()


def main():
    #  超参数的输入，这个地方可以改成参数输入形式 import argparse
    data_length = 3
    batch_size = 100
    epoch = 100
    lr = 0.02
    evaluate_steps = 3

    #  载入数据
    dl = DataLoader(data_length=data_length)
    train_data = dl.data_generation(data=dl.train_data, is_shuffle=True, batch_size=batch_size)
    test_data = dl.data_generation(data=dl.test_data, is_shuffle=False, batch_size=1)
    print('data loaded.')

    #  模型的基本参数和模型训练设置
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    mlp = MLPModel(input_size=data_length)
    mlp.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(mlp.parameters(), lr=lr)

    # 模型的训练与评估
    mlp = train(mlp, epoch, train_data, criterion, optimizer, device)
    real_data, pred_data = evaluate(mlp, test_data, device,steps=evaluate_steps)
    draw(real_data, pred_data)


if __name__ == '__main__':
    main()
