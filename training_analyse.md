**********************************************************************************************************************************************
![image](https://github.com/user-attachments/assets/15c111f4-f631-4ad7-b977-c533f190b619)


![image](https://github.com/user-attachments/assets/73780f25-9813-43c2-a001-5c3ffd7d48d0)



(base) PS F:\ai-elementar-strategy-cardgame-main> python training_mit_simulationen.py
2024-12-29 07:13:47.478159: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2024-12-29 07:13:49.307963: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.


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

2024-12-29 07:13:57.153121: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.

Epoch 1/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 15s 1ms/step - accuracy: 0.9872 - loss: 0.0388 - val_accuracy: 0.9936 - val_loss: 0.0205 - learning_rate: 2.5000e-04
Epoch 2/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9875 - loss: 0.0373 - val_accuracy: 0.9940 - val_loss: 0.0205 - learning_rate: 2.5000e-04
Epoch 3/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9874 - loss: 0.0380 - val_accuracy: 0.9939 - val_loss: 0.0191 - learning_rate: 2.5000e-04
Epoch 4/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9879 - loss: 0.0363 - val_accuracy: 0.9945 - val_loss: 0.0197 - learning_rate: 2.5000e-04
Epoch 5/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9879 - loss: 0.0357 - val_accuracy: 0.9948 - val_loss: 0.0179 - learning_rate: 2.5000e-04
Epoch 6/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9880 - loss: 0.0355 - val_accuracy: 0.9936 - val_loss: 0.0196 - learning_rate: 2.5000e-04
Epoch 7/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9882 - loss: 0.0352 - val_accuracy: 0.9948 - val_loss: 0.0183 - learning_rate: 2.5000e-04
Epoch 8/10
10852/10894 ━━━━━━━━━━━━━━━━━━━━ 0s 967us/step - accuracy: 0.9886 - loss: 0.0346

Epoch 8: ReduceLROnPlateau reducing learning rate to 0.0001250000059371814.

10894/10894 ━━━━━━━━━━━━━━━━━━━━ 13s 1ms/step - accuracy: 0.9886 - loss: 0.0346 - val_accuracy: 0.9945 - val_loss: 0.0180 - learning_rate: 2.5000e-04
Epoch 9/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9895 - loss: 0.0314 - val_accuracy: 0.9954 - val_loss: 0.0161 - learning_rate: 1.2500e-04
Epoch 10/10
10894/10894 ━━━━━━━━━━━━━━━━━━━━ 12s 1ms/step - accuracy: 0.9895 - loss: 0.0315 - val_accuracy: 0.9952 - val_loss: 0.0156 - learning_rate: 1.2500e-04

Restoring model weights from the end of the best epoch: 10.

Testgenauigkeit: 0.9952

2724/2724 ━━━━━━━━━━━━━━━━━━━━ 1s 533us/step

Klassifikationsbericht:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     40766
           1       1.00      1.00      1.00     41138
           2       0.98      0.94      0.96      5242

    accuracy                           1.00     87146
   macro avg       0.99      0.98      0.99     87146
weighted avg       1.00      1.00      1.00     87146
