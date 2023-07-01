# This is a sample Python script.
import numpy as np
import torch


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Net(torch.nn.Module):
    def __int__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=8, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(in_channels=8, out_channels=16, kernel_size=5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, 32)

    def forward(self, x):
        x = self.conv1(x)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, (2, 2))
        x = self.conv2(x)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.max_pool2d(x, 2)
        x=x.view


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
    res = play_op()
    for r in res:
        print(r)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
