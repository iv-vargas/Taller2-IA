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
