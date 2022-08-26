from asyncio.windows_events import NULL
from logging import NullHandler
import torch
import torch.nn as nn
import torch.optim as optim
from . import gru_model
from . import dataloader
import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.metrics import mean_squared_error



def train(model, epoch, train_data, criterion, optimizer, device):
    for iter_num in range(epoch):
        # train
        model.train()
        for batch in train_data:
            x = batch['batched_previous_n_day_data'].to(device)
            y = batch['batched_predict_data'].to(device)
            pred_y, _ = model(x)
            loss = criterion(pred_y, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print("iter_num {}  loss {}".format(iter_num,loss.item()))
    return model



def evaluator(model, test_data, device, steps=2):
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
                pred_y, _ = model(x)
                step_real_data.extend(y.tolist())
                step_predict_data.extend(pred_y.tolist())
                pred_y = pred_y.unsqueeze(0).unsqueeze(0)
                x = torch.cat((x,pred_y), 1)[:, 1:]
            real_data.append(step_real_data)
            predict_data.append(step_predict_data)
    real_data = np.array(real_data)[:,-1]
    predict_data = np.array(predict_data)
    real_data = real_data[steps-1:]
    predict_data = predict_data[:-steps+1]
    predict_data = predict_data[:, -1]
    print('MSE:',  mean_squared_error(real_data, predict_data))
    return real_data, predict_data



def draw(real_data, predict_data):
    # predict_data = predict_data[:, -1]

    plt.plot(list(range(0, len(real_data), 1)), real_data, color="red", label="real_data")
    plt.plot(list(range(0, len(predict_data), 1)), predict_data, color="blue", label="predict_data")
    plt.legend()
    plt.xlabel("date")
    plt.ylabel("close_price")
    plt.title("real data and predicted data")
    plt.show()

    plt.plot(list(range(0, 10, 1)), real_data[0:10], color="red", label="real_data")
    plt.plot(list(range(0, 10, 1)), predict_data[0:10], color="blue", label="predict_data")
    plt.legend()
    plt.xlabel("date")
    plt.ylabel("close_price")
    plt.title("real data and predicted data")
    plt.show()


def prepareModel(ts_code, start_date="20190101", end_date="20220811", train_test_rate = 0.8, epoch=100, steps=3):
    #  超参数的输入，这个地方可以改成参数输入形式 import argparse
    num_of_layers = 1
    data_length = 5
    batch_size = 100
    epoch = epoch
    lr = 0.01
    steps = steps

    #  载入数据
    dl = dataloader.DataLoader(data_length=data_length, ts_code=ts_code, start_date=start_date, end_date=end_date, train_test_rate=train_test_rate)
    train_data = dl.data_generation(data=dl.train_data, is_shuffle=True, batch_size=batch_size)
    test_data = dl.data_generation(data=dl.test_data, is_shuffle=False, batch_size=1)
    print('data loaded.')

    #  模型的基本参数和模型训练设置
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print(device)
    
    gru = gru_model.GRUModel(num_of_layers=num_of_layers)
    gru.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(gru.parameters(), lr=lr)

    # 模型的训练与评估
    gru = train(gru, epoch, train_data, criterion, optimizer, device)
    torch.save(gru, './gru.pt')
    real_data, pred_data = evaluator(gru, test_data, device, steps=steps)
    # draw(real_data, pred_data)


# if __name__ == '__main__':
#     prepareModel(ts_code="300750.SZ", start_date="20190101", end_date="20220811", train_test_rate=0.8)
