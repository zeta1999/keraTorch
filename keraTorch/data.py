# AUTOGENERATED! DO NOT EDIT! File to edit: data.ipynb (unless otherwise specified).

__all__ = ['Data', 'TestData', 'TrainData', 'create_db']

# Cell
import torch
from torch.utils.data import Dataset, DataLoader
from fastai.data_block import DataBunch, DatasetType

from sklearn.model_selection import train_test_split

# import warnings

# torch.Tensor.ndim = property(lambda x: x.dim())
# tt = torch.Tensor

# Cell
class Data(Dataset):
    """
    Load raw x,y data
    """
    def __init__(self, *args):
        super().__init__()
        self.data = args

    def __len__(self):
        return len(self.data[0])

    def __getitem__(self, i):
        return {f'arg_{i}': torch.Tensor([x[i]])
                for i, x in enumerate(self.data)}

# Cell
class TestData(Dataset):
    """
    Load raw x,y data
    """
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.x_type = self.__get_type__(x.dtype.name)

    def __get_type__(self, type):
        if 'float' in type:
            return torch.float32
        if 'int' in type:
            return torch.long

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return torch.tensor(self.x[i], dtype=torch.float32)

class TrainData(TestData):
    """
    Load raw x,y data
    """
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
        self.y_type = self.__get_type__(y.dtype.name)

    def __getitem__(self, i):
        return torch.tensor(self.x[i], dtype=torch.float32), \
                torch.tensor(self.y[i], dtype=self.y_type)

# Cell
def create_db(x, y, train_size=0.8, bs=96, random_state=42):
    """
    Take dataframe and convert to Fastai databunch
    """
    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=train_size)

    train_ds = TrainData(X_train, y_train)
    val_ds = TrainData(X_test, y_test)

    bs = min(bs, len(train_ds))
    val_bs = min(bs, len(val_ds))

    train_dl = DataLoader(train_ds, bs)
    val_dl = DataLoader(val_ds, val_bs)

    return DataBunch(train_dl, val_dl)