**********************************************************************************************************************************************
![image](https://github.com/user-attachments/assets/15c111f4-f631-4ad7-b977-c533f190b619)


(base) PS F:\ai-elementar-strategy-cardgame-main> python training_mit_simulationen.py
2024-12-28 20:50:26.839319: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2024-12-28 20:50:27.746538: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
Kodierung der Elemente:
   Element  Kodiert als
0   Blitz            0
1     Eis            1
2    Erde            2
3   Feuer            3
4    Luft            4
5   Magie            5
6  Wasser            6

Kodierung der Werte:
       Wert  Kodiert als
0        1            0
1       10            1
2        2            2
3        3            3
4        4            4
5        5            5
6        6            6
7        7            7
8        8            8
9        9            9
10     Ass           10
11    Bube           11
12    Dame           12
13  KÃ¶nig           13

One-Hot-Encoding für Wetter:
       Wetter    Feature-Spalte
0   Erdbeben   wetter_Erdbeben
1      Regen      wetter_Regen
2  Windsturm  wetter_Windsturm

One-Hot-Encoding für Helden (Spieler):
   Spieler_Held Feature-Spalte_Spieler
0       Drache    spieler_held_Drache
1     Zauberer  spieler_held_Zauberer

One-Hot-Encoding für Helden (Gegner):
   Gegner_Held Feature-Spalte_Gegner
0      Drache    gegner_held_Drache
1    Zauberer  gegner_held_Zauberer
2024-12-28 20:50:32.553862: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
Epoch 1/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9814 - loss: 0.0558 - val_accuracy: 0.9910 - val_loss: 0.0296 - learning_rate: 5.0000e-04
Epoch 2/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9818 - loss: 0.0540 - val_accuracy: 0.9915 - val_loss: 0.0281 - learning_rate: 5.0000e-04
Epoch 3/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9829 - loss: 0.0508 - val_accuracy: 0.9901 - val_loss: 0.0312 - learning_rate: 5.0000e-04
Epoch 4/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9831 - loss: 0.0507 - val_accuracy: 0.9902 - val_loss: 0.0312 - learning_rate: 5.0000e-04
Epoch 5/10
10864/10894 ━━━━━━━━━━━━━━━━━━━━ 0s 912us/step - accuracy: 0.9832 - loss: 0.0495
Epoch 5: ReduceLROnPlateau reducing learning rate to 0.0002500000118743628.
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9832 - loss: 0.0495 - val_accuracy: 0.9918 - val_loss: 0.0283 - learning_rate: 5.0000e-04
Epoch 6/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9864 - loss: 0.0418 - val_accuracy: 0.9920 - val_loss: 0.0264 - learning_rate: 2.5000e-04
Epoch 7/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9862 - loss: 0.0400 - val_accuracy: 0.9934 - val_loss: 0.0225 - learning_rate: 2.5000e-04
Epoch 8/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9867 - loss: 0.0400 - val_accuracy: 0.9937 - val_loss: 0.0218 - learning_rate: 2.5000e-04
Epoch 9/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9868 - loss: 0.0398 - val_accuracy: 0.9927 - val_loss: 0.0224 - learning_rate: 2.5000e-04
Epoch 10/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9871 - loss: 0.0382 - val_accuracy: 0.9927 - val_loss: 0.0216 - learning_rate: 2.5000e-04
Restoring model weights from the end of the best epoch: 10.
