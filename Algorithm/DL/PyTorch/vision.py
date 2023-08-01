import os.path

import numpy as np
import torch.utils.data
import torchvision
import torchvision.transforms as transforms
from matplotlib import pyplot as plt

from basic import LeNet

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ]
)
train_set = torchvision.datasets.CIFAR10(root='./', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=32, shuffle=True, num_workers=0)
test_set = torchvision.datasets.CIFAR10(root='./', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=32, shuffle=True, num_workers=0)

classes = (
    'plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'
)


def imshow(img):
    img = img / 2 + 0.5  # denormalize
    np_img = img.numpy()
    plt.imshow(np.transpose(np_img, (1, 2, 0)))
    plt.show()


# data_iter = iter(train_loader)
# images, labels = data_iter.__next__()
# print(' '.join('%5s' % classes[labels[j]] for j in range(8)))
# print(' '.join('%5s' % classes[labels[j]] for j in range(8, 16)))
# print(' '.join('%5s' % classes[labels[j]] for j in range(16, 24)))
# print(' '.join('%5s' % classes[labels[j]] for j in range(24, 32)))
# imshow(torchvision.utils.make_grid(images))

le_net_cifar10 = LeNet()
if os.path.exists('le_net_cifar10.pth'):
    le_net_cifar10.load_state_dict(torch.load('le_net_cifar10.pth'))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
le_net_cifar10.to(device)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(le_net_cifar10.parameters(), lr=0.001, momentum=0.9)
for epoch in range(1):
    running_loss = 0.0
    for i, data in enumerate(train_loader, start=0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = le_net_cifar10(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if i % 10 == 9:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 10))
            running_loss = 0.0
torch.save(le_net_cifar10.state_dict(), 'le_net_cifar10.pth')
data_iter = iter(test_loader)
images, labels = data_iter.__next__()
images, labels = images.to(device), labels.to(device)
outputs = le_net_cifar10(images)
_, predicted = torch.max(outputs, 1)
print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(32)))

correct = 0
total = 0
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        outputs = le_net_cifar10(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))

class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        outputs = le_net_cifar10(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1
for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))
