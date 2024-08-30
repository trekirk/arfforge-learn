Hola Juanjo,

Estoy entrenando el modelo directamente.

Te adjunto los datasets mejor porque si hago ahora un push al GIT lo llenaría de archivos que no son útiles pero que ahora necesito para las pruebas que estoy haciendo para ver si consigo mejores resultados.

Te explico que contiene cada dataset:

Estos archivos corresponden con los datos que ha utilizado el sistema en su reentrenamiento en cada caso en la fase de validación:

- df_reentreno_Baseline: Contiene el conjunto de datos que va a utilizar en el sistema de referencia para entrenar en la fase de testeo.
- df_reentreno_Test: Igual que el anterior pero para el sistema.

Para la fase de test estoy utilizando estos datasets:

- reduced_sound_labels_200: 200 datos etiquetados seleccionados aleatoriamente del dataset grande original para el testeo.
- reduced_sound_labels_500: Igual pero con 500
- reduced_sound_labels_200_unlabeled: Los 200 datos sin etiquetar (para publicar con el publisher de gestures)
- reduced_sound_labels_500_unlabeled: Igual pero con 500.

Gracias por la ayuda.
