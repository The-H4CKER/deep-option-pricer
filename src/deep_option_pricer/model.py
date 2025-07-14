# src/deep_option_pricer/model.py

import torch.nn as nn


class OptionPricer(nn.Module):
    def __init__(self, input_size):
        super(OptionPricer, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),  # Output layer
        )

    def forward(self, x):
        return self.layers(x)
