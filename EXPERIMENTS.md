### Experiment 1: Baseline Model
* **Date:** 2025-07-14
* **Description:** Initial baseline model with original features.
* **Parameters:** `epochs=1000`, `lr=0.001`, 3 hidden layers (128, 64, 32).
* **Result:** Final Test RMSE = **$5.17**
* **Conclusion:** Establishes the initial performance benchmark.

---
### Experiment 2: Increased Training Epochs
* **Date:** 2025-07-14
* **Description:** Doubled training epochs to check for convergence.
* **Parameters:** `epochs=2000`, `lr=0.001`.
* **Result:** Final Test RMSE = **$5.01**
* **Conclusion:** Longer training provided a marginal improvement. The model is limited by its features/architecture.

---
### Experiment 3 & 4: Added 'Moneyness' Feature
* **Date:** 2025-07-14
* **Description:** Added `moneyness` as a new input feature.
* **Result:** Initially worse performance (RMSE ~$5.09), indicating the new feature caused the simple model to overfit faster.
* **Conclusion:** The new feature is powerful but requires a better model architecture and regularization to be effective.

---
### Experiment 5 & 6: New Architecture + Regularization
* **Date:** 2025-07-14
* **Description:** Implemented a deeper/wider architecture with `BatchNorm`, `Dropout`, and an LR Scheduler.
* **Result:** Minimum Test RMSE of **$4.97** was achieved.
* **Conclusion:** Regularization techniques helped find the optimal training point for the new architecture, achieving the best predictive accuracy so far.

---
### Experiment 7-9: Log-Transform & Hyperparameter Tuning
* **Date:** 2025-07-14
* **Description:** Changed model to predict `log(price)` and tuned `lr` and `weight_decay`.
* **Result:** Minimum Test RMSE of **$11.74** was achieved.
* **Conclusion:** The log-transform stabilized training but required significant hyperparameter tuning. The model is stable but less accurate than the non-log model when `implied_volatility` is included.

---
### Experiment 10: Final Model (No Implied Volatility)
* **Date:** 2025-07-14
* **Description:** Removed the `implied_volatility` feature to test the model's ability to price options from fundamental inputs alone.
* **Parameters:** `epochs=2000`, `lr=0.0001`, `weight_decay=1e-5`, Advanced Architecture, Log-Transform.
* **Result:** Minimum Test RMSE of **$9.97** was achieved at epoch 1000.
* **Conclusion:** The model successfully learned the pricing function without the "cheat" of implied volatility, demonstrating a strong understanding of the underlying problem.
