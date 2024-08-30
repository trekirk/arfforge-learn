El mié, 28 ago 2024 a las 11:10, JUAN JOSE GAMBOA MONTERO (<jgamboa@ing.uc3m.es>) escribió:

    Una cosa,

    Lo de df_reentreno no se entiende nada, explícamelo mejor, por favor 

    Saludos,

    Juanjo

Claro. En la fase de validación que hicimos en el laboratorio ayer se generan 2 datasets. Uno de ellos contiene todos los datos predecidos por el modelo (lo adjunto en este correo porque a lo mejor también te hacen falta) ese dataset se llama df_real_test_Baseline o df_real_test_Test. Por otro lado se genera el dataset df_reentreno que contiene los datos que, durante la validación, el modelo ha predicho con una confianza superior al umbral y, por lo tanto, ha ido utilizando para su reentrenamiento.

Lo que yo estaba haciendo hasta ahora es utilizar los datasets generados df_reentreno para entrenar un modelo supervisado y predecir un número de etiquetas aleatorias (200 o 500).

Dime si me he explicado mejor.

