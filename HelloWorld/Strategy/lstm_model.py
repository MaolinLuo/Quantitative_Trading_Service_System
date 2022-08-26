import torch
import torch.nn as nn


class LSTMModel(nn.Module):

    def __init__(self, input_size=1, hidden_size=64, output_size=1, num_of_layers=20):
        super(LSTMModel, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_of_layers,  # 认真参考课时89
            batch_first=True
        )

        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        :param x: x.shape -> [batch_size, N (close_price)] y.shape -> [batch_size, 1 (predict_close_price)]
        """
        out, hidden = self.rnn(x)
        # out: [batch_size, seq_len=2, hidden_size]     hidden_prev: [batch_size, num_layers=20, hidden_size]

        out = self.linear(out)
        out = out.squeeze(dim=-1)
        out = out[:, -1]

        ###########################
        # hidden = self.linear(hidden)
        # hidden = hidden.squeeze(dim=-1)
        # last_hidden = hidden[0, :]
        # return out, last_hidden
        ###########################

        return out, hidden


# def main():
#     x = torch.tensor([[[12.0800],
#                        [12.3100]],
#                       [[17.1100],
#                        [17.1300]],
#                       [[26.9600],
#                        [27.0600]],
#                       [[11.8000],
#                        [11.8800]],
#                       [[19.0500],
#                        [19.2500]]])
#     gru_model = GRUModel(num_of_layers=2)
#     out, hidden = gru_model(x)
#     print(out.shape)
#     # print(out)
#     print(hidden.shape)
#     # print(hidden)


# if __name__ == '__main__':
#     main()
