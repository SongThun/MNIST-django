import torch


class custom_softMax( torch.autograd.Function):
    @staticmethod
    def forward( ctx, Z, X, y):

        """_summary_
        X : logits
        """
        y_hat = torch.exp(Z) / torch.sum( torch.exp(Z), dim = 1).view(-1,1)
        ctx.save_for_backward(Z,y_hat, y , X)
        return y_hat
    @staticmethod
    def backward ( ctx, gradient_output):
        logits, y_hat, y, X = ctx.saved_tensors
        grad_present = torch.mm(X.t(), (y_hat - y))
        return grad_present * gradient_output

class LeNet5(torch.nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.in_channel = 1
        self.num_classes = num_classes
        self.features = torch.nn.Sequential(
            # layer 1
            torch.nn.Conv2d(in_channels= self.in_channel, out_channels= 6, kernel_size= 5),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2),
            #layer 2
            torch.nn.Conv2d(6,16,kernel_size=5),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2)
        )
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(16 * 5 * 5, 120),
            torch.nn.Sigmoid(),
            torch.nn.Linear(120,84),
            torch.nn.Sigmoid(),
            torch.nn.Linear(84,num_classes)
        )
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1) # from NCWH -> NM, where M = C * W * H
        logits = self.classifier(x)
        A_probas = torch.nn.functional.softmax(logits, dim = 1)
        return logits, A_probas