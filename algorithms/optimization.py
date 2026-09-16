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
    raise NotImplementedError("Punto 1: implemente hill_climbing")


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    # TODO: Add your code here
    temperatura = initial_temperature * cooling_rate**iteration
    return temperatura
    #raise NotImplementedError("Punto 2: implemente cooling_schedule")


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
    
    """
    VERSION INICIAL
    
    
    inicial = initial_configuration
    actual = inicial
    evaluaciones = 0 
    
    puntaje_actual = configuration_score(problem, actual)
    evaluaciones += 1
    
    mejor_estado = inicial
    puntaje_mejor = puntaje_actual
    
    historial_conf = [actual]
    historial_punt = [puntaje_actual]
    
    iteracion_actual = 0
    
    while iteracion_actual < max_iterations:
        
        temperatura_actual = cooling_schedule(initial_temperature, cooling_rate, iteracion_actual)
        
        if temperatura_actual < minimum_temperature:
            break
        
        candidato = rng.choice(problem.neighbors(actual))
        
        puntaje_candidato = configuration_score(problem, candidato)
        evaluaciones += 1
        
        delta_E = puntaje_candidato - puntaje_actual 
        if delta_E > 0:
            actual = candidato
            puntaje_actual = puntaje_candidato
            
            historial_conf.append(actual)
            historial_punt.append(puntaje_actual)
            
            if puntaje_actual > puntaje_mejor:
                mejor_estado = actual
                puntaje_mejor = puntaje_actual
                
        else:
            probabilidad = math.exp(delta_E / temperatura_actual)
            num_random = random.random()
            if num_random < probabilidad:
                actual = candidato
                puntaje_actual = puntaje_candidato
                
                historial_conf.append(actual)
                historial_punt.append(puntaje_actual)
            else:
                break
            
        iteracion_actual += 1
        
    return OptimizationResult(mejor_estado, puntaje_mejor, evaluaciones, iteracion_actual, historial_conf, historial_punt)
    
    
    El problema en este caso es que el algoritmo estaba haciendo un break al momento de rechazar un estado teniendo en cuenta la probabilidad de elegirlo. Esto hacia que el resultado no
    fuera correcto al finalizar el ciclo cuando en realidad según el pseudocódigo de la guia de clase debería de seguir a la siguiente iteración pero conservando el estado actual sin cambios.
    
    Para este caso, el prompt utilizado en la IA Claude Sonnet 5 fue "Tengo un problema en el que mi implementación del Recocido Simulado / Simulated Annealing se detiene muy temprano asemejandose
    a un Ascenso de Colina / Hill Climbing. Qué parte de mi implementación podría estar causando esta falla?" junto a una imagen del codigo inicial y el pseudocódigo de la guia de clase.
    
    La IA realizó las siguientes correciones: 
    - Eliminar el break que descarta a un estado por probabilidad.
    - Realizar un el append a los historiales y la comparación de mejor estado al final.
    
    Lo aprendido en este caso es tener cuidado a la hora de implementar el pseudocódigo y asegurarse de no incluir elementos que no estén explícitos o estar seguros de que no afecta a la estructura
    del pseudocódigo ya existente. 
    
    """
    
    inicial = initial_configuration
    actual = inicial
    evaluaciones = 0 
    
    puntaje_actual = configuration_score(problem, actual)
    evaluaciones += 1
    
    mejor_estado = inicial
    puntaje_mejor = puntaje_actual
    
    historial_conf = [actual]
    historial_punt = [puntaje_actual]
    
    iteracion_actual = 0
    
    while iteracion_actual < max_iterations:
        
        temperatura_actual = cooling_schedule(initial_temperature, cooling_rate, iteracion_actual)
        
        if temperatura_actual < minimum_temperature:
            break
        
        candidato = rng.choice(problem.neighbors(actual))
        
        puntaje_candidato = configuration_score(problem, candidato)
        evaluaciones += 1
        
        delta_E = puntaje_candidato - puntaje_actual 
        if delta_E > 0:
            actual = candidato
            puntaje_actual = puntaje_candidato
            
            if puntaje_actual > puntaje_mejor:
                mejor_estado = actual
                puntaje_mejor = puntaje_actual
                
        else:
            probabilidad = math.exp(delta_E / temperatura_actual)
            num_random = rng.random()
            if num_random < probabilidad:
                actual = candidato
                puntaje_actual = puntaje_candidato
                
        historial_conf.append(actual)
        historial_punt.append(puntaje_actual)
        
        if puntaje_actual > puntaje_mejor:
            mejor_estado = actual
            puntaje_mejor = puntaje_actual
            
        iteracion_actual += 1
        
    return OptimizationResult(mejor_estado, puntaje_mejor, evaluaciones, iteracion_actual, historial_conf, historial_punt)
    
    # raise NotImplementedError("Punto 2: implemente simulated_annealing")


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

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente one_point_crossover")


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
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente swap_mutation")


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

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente genetic_algorithm")
