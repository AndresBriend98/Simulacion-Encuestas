import time

# Definición de la estructura de la encuesta y respuestas
encuesta = {
    "¿Tuvo alguna dificultad para tragar durante su última comida?": "",
    "¿Tosió o sintió que se ahogaba al tragar?": "",
    "¿Su voz cambió después de comer o beber, como si estuviera más ronca?": "",
    "¿Tuvo que tragar varias veces para que la comida bajara?": "",
    "¿Usó alguna técnica especial para ayudar a tragar, como cambiar la postura de la cabeza o tomar sorbos pequeños?": "",
    "¿Le ayudaron estas técnicas a tragar mejor?": "",
    "¿Sintió dolor o malestar al tragar?": ""
}

# Función para generar números pseudoaleatorios usando el método del cuadrado medio de Von Neumann
def generar_pseudoaleatorios(n, semilla):
    numeros = [] #Almaceno los numeros pseudo aleatorios
    x = semilla
    for _ in range(n): #Generación de n números pseudoaleatorios mediante un bucle
        x = x ** 2
        x = int(str(x).zfill(8)[2:6])
        # Convierte x en una cadena de caracteres y le añade ceros a la izquierda si es necesario, para que tenga al menos 8 dígitos.
        #[2:6]: Toma los cuatro dígitos centrales del resultado.
        #int(...): Convierte los dígitos centrales de vuelta a un número entero.
        numeros.append(x / 10000)  # Normalizamos para obtener un número entre 0 y 1, Divide el valor de x por 10000, ya que x es un número de 4 dígitos, para obtener un número entre 0 y 1.
    return numeros

# Test de Chi-cuadrado para verificar la uniformidad de los números generados
def test_chi_cuadrado(numeros):
    frecuencias_esperadas = [len(numeros) / 2, len(numeros) / 2]  # Esperamos una distribución uniforme (50% para cada valor)
    frecuencias_observadas = [sum(1 for num in numeros if num < 0.5), sum(1 for num in numeros if num >= 0.5)] #Contamos cuántos números en la lista son menores de 0.5 y cuántos son mayores o iguales a 0.5.
    
    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo, fe in zip(frecuencias_observadas, frecuencias_esperadas)) #Fórmula de Chi-cuadrado 
    
    xEsperado = 3.841 # Valor esperado para alpha = 0.05 y 1 grado de libertad (tabla de distribución de Chi-cuadrado.)
    
    print(f"\nChi-cuadrado observado: {chi_cuadrado:.4f}") #.4 numero de digitos despues de la coma a mostrar
    print(f"X esperado: {xEsperado}")
    
    if chi_cuadrado < xEsperado:
        print("\nNo se rechaza la hipótesis nula: Los números generados siguen una distribución uniforme.")
    else:
        print("\nSe rechaza la hipótesis nula: Los números generados no siguen una distribución uniforme.")
    return chi_cuadrado < xEsperado

# Simulación del tiempo de respuesta y respuesta (Sí/No) de cada pregunta
def simular_respuestas(encuesta, numeros_aleatorios):
    """
    Simula el tiempo de respuesta y la respuesta (Sí/No) para cada pregunta en la encuesta.

    Args:
    - encuesta (dict): Diccionario con las preguntas de la encuesta.
    - numeros_aleatorios (list): Lista de números pseudoaleatorios generados.

    Returns:
    - float: Tiempo total estimado de la simulación.
    """
    tiempo_total = 0 #Variable para acumular el tiempo total
    
    for i, pregunta in enumerate(encuesta): #Itera sobre cada pregunta en el diccionario
        inicio_respuesta = time.time()  # Registra el momento de inicio de la respuesta
        respuesta = "Sí" if numeros_aleatorios[i] < 0.5 else "No"  
        # Determina la respuesta basándose en el número aleatorio correspondiente. Si el número es menor que 0.5, la respuesta es "Sí"; de lo contrario, es "No".
        tiempo_respuesta = 10 + 10 * numeros_aleatorios[i]
        #Calcula el tiempo de respuesta simulando entre 10 y 20 segundos. Multiplicando el número aleatorio por 10 se obtiene un valor entre 0 y 10, 
        # y sumándole 10 se asegura que el mínimo tiempo sea 10 segundos.
        
        print(f"\nRespondiendo pregunta: {pregunta}")
        time.sleep(tiempo_respuesta)  # Simulamos el tiempo que tarda el paciente en responder
        fin_respuesta = time.time()  # Momento de finalización de la respuesta
        tiempo_pregunta = fin_respuesta - inicio_respuesta  # Calculamos el tiempo que tardó en responder
        encuesta[pregunta] = f"Respuesta: {respuesta}, Tiempo de respuesta: {tiempo_pregunta:.2f} segundos"  # Guardamos la respuesta simulada
        print(f"Respuesta: {respuesta}")
        print(f"Tiempo de respuesta: {tiempo_pregunta:.2f} segundos")
        print("-" * 30)
        tiempo_total += tiempo_pregunta
    
    return tiempo_total

# Función principal para ejecutar todo el flujo
def main():
    # Generación de números pseudoaleatorios y test de Chi-cuadrado
    print("Generando números pseudoaleatorios usando el método del cuadrado medio de Von Neumann...")
    semilla = int(time.time() * 1000000) % 10000  # Semilla basada en el tiempo actual en microsegundos, limitada a 4 dígitos
    numeros_aleatorios = generar_pseudoaleatorios(len(encuesta), semilla)
    #Llama a la función generar_pseudoaleatorios con el número de preguntas en la encuesta y la semilla generada para obtener una lista de números pseudoaleatorios.
    
    print("\nRealizando el test de Chi-cuadrado para verificar la uniformidad de los números generados...")
    uniformidad = test_chi_cuadrado(numeros_aleatorios)
    #Llama a la función test_chi_cuadrado y pasa la lista de números pseudoaleatorios. 
    # Esta función devuelve True si los números pasan el test de uniformidad y False en caso contrario.
    
    if uniformidad: ##Simular las respuestas a la encuesta solo si los números pasan el test de uniformidad.
        # Simulación de respuestas
        print("\nIniciando simulación de respuestas a la encuesta...")
        inicio = time.time()
        tiempo_total = simular_respuestas(encuesta, numeros_aleatorios) #Llama a la función simular_respuestas, que utiliza los números pseudoaleatorios para generar respuestas y tiempos de respuesta.
        fin = time.time()
        print("Simulación completada.")
        
        # Mostrar resultados simulados y tiempo total
        print("\nResultados simulados de la encuesta:")
        for pregunta, respuesta in encuesta.items():
            print(f"- {pregunta}: \n   > {respuesta}")
        
        print(f"\nTiempo total de simulación: {tiempo_total:.2f} segundos")
    else:
        print("\nNo se puede iniciar la simulación debido a que los números generados no siguen una distribución uniforme.")

# Ejecución del programa principal
if __name__ == "__main__":
    main()
