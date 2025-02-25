import numpy as np
import torch
import lightning.pytorch as pl
import torchmetrics
from torchinfo import summary


class MultiClassModule(pl.LightningModule):
    def __init__(self,
                 output_size,
                 **kwargs):
        super().__init__(**kwargs)
        self.mc_acc = torchmetrics.classification.Accuracy(task='multiclass',
                                                           num_classes=output_size)
        self.cce_loss = torch.nn.CrossEntropyLoss()

    def predict(self, x):
        return torch.softmax(self(x),-1)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        return optimizer

    def training_step(self, train_batch, batch_idx):
        x, y_true = train_batch
        y_pred = self(x)
        perm = (0,-1) + tuple(range(y_pred.ndim))[1:-1]
        acc = self.mc_acc(y_pred.permute(*perm),y_true)
        loss = self.cce_loss(y_pred.permute(*perm),y_true)
        self.log('train_acc', acc, on_step=False, on_epoch=True)
        self.log('train_loss', loss, on_step=False, on_epoch=True)
        return loss
    
    def validation_step(self, val_batch, batch_idx):
        x, y_true = val_batch
        y_pred = self(x)
        perm = (0,-1) + tuple(range(y_pred.ndim))[1:-1]
        acc = self.mc_acc(y_pred.permute(*perm),y_true)
        loss = self.cce_loss(y_pred.permute(*perm),y_true)
        self.log('val_acc', acc, on_step=False, on_epoch=True)
        self.log('val_loss', loss, on_step=False, on_epoch=True)
        return loss

    def test_step(self, test_batch, batch_idx):
        x, y_true = test_batch
        y_pred = self(x)
        perm = (0,-1) + tuple(range(y_pred.ndim))[1:-1]
        acc = self.mc_acc(y_pred.permute(*perm),y_true)
        loss = self.cce_loss(y_pred.permute(*perm),y_true)
        self.log('test_acc', acc, on_step=False, on_epoch=True)
        self.log('test_loss', loss, on_step=False, on_epoch=True)
        return loss
        
class MultiClassNetwork(MultiClassModule):
    def __init__(self,
                 num_tokens,
                 output_size,
                 hidden_size = 128,
                 **kwargs):
        super().__init__(output_size=output_size,
                         **kwargs)
        self.embedding = torch.nn.Embedding(num_tokens,
                                            hidden_size)
        self.rnn_layer = torch.nn.RNN(hidden_size,
                                      hidden_size)
        self.output_layer = torch.nn.Linear(hidden_size,
                                            output_size)

    def forward(self, x):
        y = x
        y = self.embedding(y)
        y = self.rnn_layer(y.permute(1,0,2))
        y = self.output_layer(y[0][-1,:])
        return y

rng = np.random.default_rng(seed=0)
X = rng.integers(0,2,size=(200,50))
Y = np.cumsum(X,1) % 2

split_point = int(X.shape[0]*0.8)
n_timesteps = 50
batch_size = 32

x_train = torch.Tensor(X[:split_point,:n_timesteps]).long()
y_train = torch.Tensor(Y[:split_point,n_timesteps-1]).long()
x_val = torch.Tensor(X[split_point:,:n_timesteps]).long()
y_val = torch.Tensor(Y[split_point:,n_timesteps-1]).long()

xy_train = torch.utils.data.DataLoader(list(zip(x_train,
                                                y_train)),
                                       shuffle=True, batch_size=batch_size,
                                       num_workers=4)
xy_val = torch.utils.data.DataLoader(list(zip(x_val,
                                              y_val)),
                                     shuffle=False, batch_size=batch_size,
                                     num_workers=4)

logger = pl.loggers.CSVLogger("logs",name="rnn_Mto1_Results",)
model = MultiClassNetwork(num_tokens=len(x_train.unique()),
                          output_size=len(torch.unique(y_train)))

trainer = pl.Trainer(max_epochs=300, logger=logger)
trainer.fit(model, xy_train, xy_val)

print(model)
summary(model,input_data=x_train[0:1])