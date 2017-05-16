Se ha preprocesado el dataset utilizando python (ver en /tools/29-3f_multiple.ipynb)
Se han eliminado la data de índices 20, 21 y 22 porque no se calculo correctamente el dato, es decir, presentaba solo unos o solo ceros y no era posible normalizar.
Tambien se eliminaron data de índices 30,34 y 35 ya que el svm-scale mostraba una advertencia indicando que no encontraba data de esos indices en otros archivos.

Para calcular las medidas de performance entrar a cada directorio. Ejemplo:

cd data/process3/ALE_L23

y ejecutar:

python easy-one-class.py

En el archivo easy-one-class.py
comentar y descomentar las siguientes lineas:
mean_sd_rates()
  #para calcular Accuracy
#mean_sd_numbers() #para calcular NTP (Numero de True Positivos), NFP (Numero de Falsos Positivos), etc.
