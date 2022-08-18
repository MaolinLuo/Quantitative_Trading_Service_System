import torch
import torch.nn as nn

class MLPModel(nn.Module):

    def __init__(self, input_size, hidden_size_1 = 50, hidden_size_2 = 100, hidden_size_3 = 50, output_size = 1):
        super(MLPModel, self).__init__()
        self.input_size = input_size
        self.hidden_size_1 = hidden_size_1
        self.hidden_size_2 = hidden_size_2
        self.hidden_size_3 = hidden_size_3
        self.output_size = output_size
        self.mlp = nn.Sequential(nn.Linear(self.input_size, self.hidden_size_1),
                        nn.ReLU(),
                        nn.Linear(self.hidden_size_1, self.hidden_size_2),
                        nn.ReLU(),
                        nn.Linear(self.hidden_size_2, self.hidden_size_3),
                        nn.ReLU(),
                        nn.Linear(self.hidden_size_3, self.output_size))

    
    def forward(self, x):
        '''
        :param x: x.shape -> [batch_size, N (close_price)] y.shape -> [batch_size, 1 (predict_close_price)]
        '''
        out = self.mlp(x)
        return out

def main():
    x = torch.tensor([[12.0800,12.3100],
                      [17.1100,17.1300],
                      [26.9600,27.0600],
                      [11.8000,11.8800],
                      [19.0500,19.2500]])
    mlp_model = MLPModel(input_size=2)
    out = mlp_model(x)
    print(out)

if __name__ == '__main__':
    main()