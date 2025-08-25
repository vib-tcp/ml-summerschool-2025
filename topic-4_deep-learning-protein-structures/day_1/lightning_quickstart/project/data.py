import torch
from pathlib import Path
import pandas as pd
from lightning.pytorch import LightningDataModule
from torch.utils.data import DataLoader


class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data, save_dir, transform=None, target_transform=None):
        self.data = data
        self.save_dir = save_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # these need to be saved in the prepare_data function
        filepath = Path(self.save_dir) / self.data.iloc[idx, 0]
        data = torch.load(filepath)
        label = self.data.iloc[idx, 1]
        if self.transform:
            data = self.transform(data)
        if self.target_transform:
            label = self.target_transform(label)
        return {"features": data, "label": label}


class MyDataModule(LightningDataModule):
    def __init__(
        self,
        root: Path,
        filename: str,
        batch_size=2,
        num_workers=8,
    ):
        super().__init__()
        self.root = Path(root)
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.root.mkdir(parents=True, exist_ok=True)
        self.data_dir = self.root / "raw"
        self.data = pd.read_csv(self.root / filename)

    def prepare_data(self) -> None:
        for split in ["train", "val"]:
            # do preprocessing stuff here and save to files
            pass

    def setup(self, stage: str | None = None):
        # Split data into train and val here
        if stage == "fit" or stage is None:
            self.train_dataset = MyDataset(
                self.data[self.data["split"] == "train"],
                self.data_dir,
            )
            self.val_dataset = MyDataset(
                self.data[self.data["split"] == "val"],
                self.data_dir,
            )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
            drop_last=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )
