import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """
    # TODO: Add your code here
    
    cobertura, redundancia, exposicion = problem.score_components(configuration)
    return cobertura - redundancia - exposicion
    # raise NotImplementedError("Punto 1: implemente configuration_score")


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Cada llamada a configuration_score(...) cuenta como una evaluación.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    # TODO: Add your code here
    """
    Version Inicial: 
    
    inicial = initial_configuration
    actual = inicial
    iteracion_actual = 0
    while iteracion_actual < max_iterations:
        vecinos = problem.neighbors(actual)
        vecino_elegido = vecinos[0]
        record = configuration_score(problem, vecinos[0])
        for vecino in vecinos:
            puntuacion_vecino = configuration_score(problem, vecino)
            if puntuacion_vecino > record:
                vecino_elegido = vecino
                record = puntuacion_vecino
        
        if configuration_score(problem, vecino) <= configuration_score(problem, actual):
            return actual
        actual = vecino_elegido
        iteracion_actual += 1
    return actual 
    
    El problema que tenía al momento de realizar esta implementación es que no sabía como retornar precisamente la respuesta como un OptimizationResult, por lo que estaba
    retornando solo la configuración respuesta pero esto no era suficiente para satisfacer el retorno esperado.
    
    Para este caso, el prompt utilizado en la IA ChatGPT Sonnet 5 fue "Mi función tiene que retornar un tipo de clase OptimizationResult, cómo puedo lograr esto?", junto con
    una imagen de la versión inicial y una imagen del código de OptimizationResult.
    
    La IA me realizó las siguientes correcciones: 
    - Retornar un OptimizationResult invocandolo como OptimizationResult(best_configuration, best_score, ...) dandole como argumentos los valores calculados en el algoritmo.
    - Guardar el historial de configuraciones y de puntuaciones, luego añadirlo al OptimizationResult al momento del return.
    - No estaba considerando las evaluaciones. Estas debían de considerarse al invocar configuration_score()
    - Debo de tener en cuenta la primera evaluación del nodo inicial y puedo ahorrarme una iteración si empiezo desde el segundo vecino en lugar de comparar el primero consigo mismo.
    
    """
    
    inicial = initial_configuration
    actual = inicial
    evaluaciones = 0
    
    puntaje_actual = configuration_score(problem, actual)
    evaluaciones += 1
    
    historial_conf = [actual]
    historial_punt = [puntaje_actual]
    
    iteracion_actual = 0
    while iteracion_actual < max_iterations:
        vecinos = problem.neighbors(actual)
        
        vecino_elegido = vecinos[0]
        record = configuration_score(problem, vecinos[0])
        evaluaciones += 1
        
        for vecino in vecinos[1:]:
            puntuacion_vecino = configuration_score(problem, vecino)
            evaluaciones += 1
            if puntuacion_vecino > record:
                vecino_elegido = vecino
                record = puntuacion_vecino
                
        if record <= puntaje_actual:
            return OptimizationResult(
                best_configuration = actual,
                best_score = puntaje_actual,
                evaluations = evaluaciones,
                iterations = iteracion_actual,
                history = historial_conf,
                score_history = historial_punt
            )
        
        actual = vecino_elegido
        puntaje_actual = record
        historial_conf.append(actual)
        historial_punt.append(puntaje_actual)
        iteracion_actual += 1
        
    return OptimizationResult(
        best_configuration = actual,
        best_score = puntaje_actual,
        evaluations = evaluaciones,
        iterations = iteracion_actual,
        history = historial_conf,
        score_history = historial_punt
    )
    # raise NotImplementedError("Punto 1: implemente hill_climbing")


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    # TODO: Add your code here
    # raise NotImplementedError("Punto 2: implemente cooling_schedule")


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9

    # TODO: Add your code here
    raise NotImplementedError("Punto 2: implemente simulated_annealing")


def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2

    corte_interior = rng.randint(1, len(parent1)-1)
    first_son = parent1[:corte_interior] + parent2[corte_interior:]
    second_son = parent2[:corte_interior] + parent1[corte_interior:]
    return (first_son, second_son)

   # raise NotImplementedError("Punto 3: implemente one_point_crossover")


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.

    Primera Version: 

    bits_activos = []
        bits_inactivos = []
    
        for i in range(len(individual)) :
            if (rng.random<mutation_probability):
                bits_activos.append (i)
            else:
                bits_inactivos.append (i)
        if (len(bits_inactivos) == 0 or len(bits_activos) == 0 ):
            return individual
        else:
    
            mayor_swap_es_ultimo = False
            i_activo = rng.choice(bits_activos)
            i_inactivo =  rng.choice(bits_inactivos)
    
            if (i_activo > i_inactivo):
                mayor_swap = i_activo
                menor_swap = i_inactivo
            else:
                mayor_swap = i_inactivo
                menor_swap = i_activo
            if (mayor_swap == len(individual)-1):
                mayor_swap_es_ultimo = True
            if (mayor_swap_es_ultimo == True):
                return  individual[:menor_swap] + individual[mayor_swap] + individual[menor_swap+1: mayor_swap] + individual[menor_swap]
            else:
                return individual[:menor_swap] + individual[mayor_swap] + individual[menor_swap+1:mayor_swap] + individual[menor_swap] + individual[mayor_swap+1:]
    
    La version actual fue corregida con IAG.
    La IAG me explico que la evaluacion probabilistica sobre si sucede o no la mutacion se realiza una vez y no bit por bit. 
    Ademas, me ayudo a simplificar la logica detras del slicing para retornar el individuo mutado.
    
    """

    if rng.random() >= mutation_probability:
        return individual

    bits_activos = [i for i, val in enumerate(individual) if val]
    bits_inactivos = [i for i, val in enumerate(individual) if not val]

    if not bits_activos or not bits_inactivos:
        return individual

    i_activo = rng.choice(bits_activos)
    i_inactivo = rng.choice(bits_inactivos)

    mutated = list(individual)
    
    #SWAP
    mutated[i_activo], mutated[i_inactivo] = mutated[i_inactivo], mutated[i_activo]

    return tuple(mutated)



def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
      
      Version Inicial:
      
      initial_population = problem.initial_population()
          best_record = []
          for j in range(generations):
              elite_one = None
              elite_two = None
              new_population = []
              best_record.append(problem.tournament_select())
              for i in range(1, len(initial_population)):
                  padre1 = problem.tournament_select()
                  padre2 = problem.tournament_select()
                  
                  if not elite_two and not elite_one:
                      elite_one = max(padre1, padre2)
                      elite_two = min(padre1,padre2)
      
                  else:
                      if padre1 > elite_one:
                          elite_two = elite_one
                          elite_one = padre1
                      elif padre1 > elite_two:
                          elite_two = padre1
                          
                      if padre2 > elite_one:
                          elite_two = elite_one
                          elite_one = padre2
                      elif padre2 > elite_two:
                          elite_two = padre2
      
                  hijo1, hijo2 = one_point_crossover(padre1, padre2, rng) #Tupla con 2 hijos
                  hijo1 = problem.repair_configuration(hijo1, rng)
                  hijo2 = problem.repair_configuration(hijo2, rng)
                  
                  hijo1 = swap_mutation(hijo1, mutation_probability)
                  hijo2 = swap_mutation(hijo2, mutation_probability)
                  new_population.append(hijo1)
                  new_population.append(hijo2)
                  
              new_population.append(elite_one)
              new_population.append(elite_two)
              best_record.append(elite_one)
              initial_population = new_population
              
          return max(best_record)
          
          
    Correcciones con IA:
    
    Los principales problemas que tenia en mi concepcion inicial fueron:
    1. ¿Como implementar elitismo?
    2. ¿Como determino la aptitud de un individuo?
    3. ¿Como mantengo la el numero de la poblacion entre genaraciones?
    4. ¿Que debo retornar?
    
    Al brindarle a la IAG diferentes partes del proyecto esta corrigio mi aproximacion frente al algoritmo genetico y me permitio entender mejor como funciona el algoritmo
    
    Por ejemplo algunas correcciones realizadas por la IAG fueron: 
    1. Utilizar la funcion configuration_score para determinar la utilidad de un individuo.
    2. Mantener un historial y numero de evaluaciones para cumplir con el formato de retorno.
    3. Añadir en primer lugar a los elites en la nueva generacion y posteriormente generar hijos iterativamente hasta alcanzar
    el tope de la genaracion.
    4. Satisfacer el formato de retorno del algoritmo.
    
    Considero que lo mas importante de haber iterado con IA fue comprender como se realizaba el proceso de trancision entre generaciones.
      
    """
    rng = rng or random.Random()
    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")
    
    
    rng = rng or random.Random()
    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")
    
    
    population = problem.initial_population(population_size, rng)

    best_overall_individual = None
    best_overall_score = float("-inf")
    history = []
    score_history = []
    evaluaciones = 0
    generaciones_ejecutadas = 0

    for gen in range(generations):
        scores = [configuration_score(problem, ind) for ind in population]
        evaluaciones += len(population)

        max_score = max(scores)
        best_idx = scores.index(max_score)
        if max_score > best_overall_score:
            best_overall_score = max_score
            best_overall_individual = population[best_idx]

        history.append(best_overall_individual)
        score_history.append(best_overall_score)
        generaciones_ejecutadas += 1

        sorted_indices = sorted(
            range(len(population)), key=lambda i: scores[i], reverse=True
        )
        elites = [population[i] for i in sorted_indices[:elite_size]]

        new_population = list(elites)

        while len(new_population) < population_size:
            padre1 = problem.tournament_select(population, scores, rng)
            padre2 = problem.tournament_select(population, scores, rng)

            hijo1, hijo2 = one_point_crossover(padre1, padre2, rng)

            hijo1 = problem.repair_configuration(hijo1, rng)
            hijo2 = problem.repair_configuration(hijo2, rng)

            hijo1 = swap_mutation(hijo1, mutation_probability, rng)
            hijo2 = swap_mutation(hijo2, mutation_probability, rng)

            new_population.append(hijo1)
            if len(new_population) < population_size:
                new_population.append(hijo2)

        population = new_population

    return OptimizationResult(
        best_configuration=best_overall_individual,
        best_score=best_overall_score,
        evaluations=evaluaciones,
        iterations=generaciones_ejecutadas,
        history=history,
        score_history=score_history,
    )
        
    
    

    

