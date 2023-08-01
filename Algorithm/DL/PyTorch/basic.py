# This is a sample Python script.
import numpy as np
import torch


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def num_flat_features(x):
    size = x.size()[1:]
    num_features = 1
    for s in size:
        num_features *= s
    return num_features


class LeNet(torch.nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=8, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(in_channels=8, out_channels=16, kernel_size=5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 32)
        self.fc2 = torch.nn.Linear(32, 16)
        self.fc3 = torch.nn.Linear(16, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, (2, 2))
        x = self.conv2(x)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, 2)
        x = x.view(-1, num_flat_features(x))
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def play_op():
    with torch.no_grad():
        try:
            a = torch.Tensor(2, 3).cuda()
            b = torch.Tensor(2, 3).cuda()
            c = torch.Tensor(2, 3).cuda()
            torch.add(a, b, out=c)
            a.requires_grad = True
            b.requires_grad = True
            d = a - b
            e = d[1, :]
            d[0, 0].backward()
            h = a.grad.clone()
            d.backward(a)
            f = a.grad.clone()
            if e.is_cuda:
                e = e.cpu()
            if e.grad_fn is not None:
                e = e.detach()
            e = e.numpy()
            g = torch.from_numpy(np.random.randn(2, 3)).mean()
            return c, d, e, f, g, h
        except Exception as e:
            print(repr(e))
            return ['Done']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # res = play_op()
    # for r in res:
    #     print(r)
    net = LeNet()
    input_tensor = torch.randn(1, 1, 32, 32)
    target_tensor = torch.randn(1, 32)
    criterion = torch.nn.MSELoss()
    learning_rate = 0.1
    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)
    optimizer.zero_grad()

    output_tensor = net(input_tensor)
    loss = criterion(output_tensor, target_tensor)
    print(net.conv1.bias.grad)
    # 更新梯度
    loss.backward()
    print(net.conv1.bias.grad)
    print(net.conv1.bias)
    # 更新权重
    optimizer.step()
    print(net.conv1.bias)

    # for f in net.parameters():
    #     f.data.sub_(f.grad.data * learning_rate)
    # print('Done')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
