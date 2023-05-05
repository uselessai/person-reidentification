import torch
import torch.nn as nn
from torch.nn import init
from torchvision import models
from torch.autograd import Variable
import pretrainedmodels
import timm
from utils import load_state_dict_mute
######################################################################
#The code is a Python script that defines a neural network model based on ResNet50 architecture for image classification. 
#It also defines helper functions for initializing weights and dropout, and a class for a custom classification layer. 
#The script imports various modules including PyTorch, torchvision, pretrainedmodels, and timm. 
#The load_state_dict_mute function is also imported from a user-defined module named utils. 
#The weights_init_kaiming function initializes the weights of convolutional and linear layers using the He Kaiming initialization scheme.
#The weights_init_classifier function initializes the weights of the last linear layer in the classification layer using a normal distribution with a small standard deviation. 
#The activate_drop function sets the dropout rate to 0.1 for all dropout layers in the model. 
#The ClassBlock class defines a custom classification layer that consists of a fully connected layer with 512 units, batch normalization, ReLU activation, and dropout. 
#It also defines another fully connected layer that outputs the classification scores. 
#The forward method of this class applies the layers in sequence on the input tensor and returns either the classification scores or a list containing the scores and the feature tensor.
#The ft_net class defines the ResNet50-based model with a custom classification layer.
#It first loads the ResNet50 model pretrained on ImageNet and replaces the average pooling layer with an adaptive average pooling layer.
#It then defines a ClassBlock instance with the specified parameters and assigns it to the classifier attribute of the model. 
#The forward method of this class applies the ResNet50 layers and the custom classification layers on the input tensor and returns the classification scores. 
#The script also includes a simple main function that creates an instance of the ft_net class, removes the custom classification layer, and passes a random input tensor through the model to check its output shape. 
#The code is intended to be used for training and evaluating image classification models on large-scale datasets such as Market-1501 and DukeMTMC-reID.
######################################################################
def weights_init_kaiming(m):
    classname = m.__class__.__name__
    # print(classname)
    if classname.find('Conv') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_in') # For old pytorch, you may use kaiming_normal.
    elif classname.find('Linear') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_out')
    elif classname.find('BatchNorm1d') != -1:
        init.normal_(m.weight.data, 1.0, 0.02)
    if hasattr(m, 'bias') and m.bias is not None:
        init.constant_(m.bias.data, 0.0)

def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.normal_(m.weight.data, std=0.001)
        init.constant_(m.bias.data, 0.0)


def activate_drop(m):
    classname = m.__class__.__name__
    if classname.find('Drop') != -1:
        m.p = 0.1
        m.inplace = True

# Defines the new fc layer and classification layer
# |--Linear--|--bn--|--relu--|--Linear--|
class ClassBlock(nn.Module):
    def __init__(self, input_dim, class_num, droprate, relu=False, bnorm=True, linear=512, return_f = False):
        super(ClassBlock, self).__init__()
        self.return_f = return_f
        add_block = []

        # bloque 512
        add_block += [nn.Linear(input_dim, 512)]
        # dropout
        add_block += [nn.BatchNorm1d(linear)]
        add_block += [nn.ReLU()]
        add_block += [nn.Dropout(p=droprate)]
       
        add_block = nn.Sequential(*add_block)
        add_block.apply(weights_init_kaiming)

        classifier = []
        classifier += [nn.Linear(linear, class_num)]
        classifier = nn.Sequential(*classifier)
        classifier.apply(weights_init_classifier)

        self.add_block = add_block
        self.classifier = classifier
    def forward(self, x):
        x = self.add_block(x)
        if self.return_f:
            f = x
            x = self.classifier(x)
            return [x,f]
        else:
            x = self.classifier(x)
            return x

# Define the ResNet50-based Model
class ft_net(nn.Module):

    def __init__(self, class_num=751, droprate=0.5, stride=2, circle=False, ibn=False, linear_num=512):
        super(ft_net, self).__init__()
        model_ft = models.resnet50(pretrained=True)
        # avg pooling to global pooling
        if stride == 1:
            model_ft.layer4[0].downsample[0].stride = (1,1)
            model_ft.layer4[0].conv2.stride = (1,1)
        model_ft.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.model = model_ft
        self.classifier = ClassBlock(2048, class_num, droprate, linear=linear_num, return_f = circle)

    def forward(self, x):
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)
        x = self.model.avgpool(x)
        x = x.view(x.size(0), x.size(1))
        x = self.classifier(x)
        return x


'''
# debug model structure
# Run this code with:
python model.py
'''
if __name__ == '__main__':
# Here I left a simple forward function.
# Test the model, before you train it. 
    net = ft_net(751)
    #net = ft_net_swin(751, stride=1)
    net.classifier = nn.Sequential()
    print(net)
    input = Variable(torch.FloatTensor(8, 3, 224, 224))
    output = net(input)
    print('net output size:')
    print(output.shape)
