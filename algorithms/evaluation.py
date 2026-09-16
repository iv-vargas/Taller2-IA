import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    
    Codigo antes de la ayuda de la IA:
    
    Se plantea la funcion de utilidad:
    f(estado) = score_estado + cercania_terminal - terminales_pendientes. Pues un mayor numero de terminales pendientes
    indica que el estado aleja a MAX de revisar las terminales
    
    Se usa la distancia propuesta por el esqueleto en el layout para medir que tan lejos está MAX de su terminal más cercana.
    Como para MAX es mejor tener una distancia menor a las terminales, se hace 100.0/1.0+masCercano para que a menor distancia crezca el valor.
    el valor de las terminales pendientes se multiplica por 10 como un peso asignado al numero de terminales que faltan por visitar
    al final del calculo total se verifica que no salga de las cotas establecidas, en caso de hacerlo se reduce una unidad o se aumenta una unidad.
    
    if state.is_win() or state.is_lose():
            return base_evaluation_function(state)
    
        score = state.get_score()
        if state.pending_terminals:
          masCercano = float("inf")
          for terminal in state.pending_terminals:
            distance = state.layout.distance(state.defender_position,terminal)
            if distance <masCercano:
              masCercano = distance
          valor_terminal = 0.0
          if masCercano!= float("inf"):
            valor_terminal = 100.0/1.0+masCercano
          
          valor_pendientes = -10.0*len(state.pending_terminals)
          
          utilidad = score+valor_terminal+valor_pendientes
          
          if utilidad >=1000:
            utilidad = 999.0
          elif utilidad <=-1000:
            utilidad = -999.0
            
        return utilidad
    
    
    
    """
    
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    score = state.get_score()
    if state.pending_terminals:
      masCercano = float("inf")
      for terminal in state.pending_terminals:
        distance = state.layout.distance(state.defender_position,terminal)
        if distance <masCercano:
          masCercano = distance
      
      seguridad = 0.0
      valor_intruso = state.layout.distance(state.defender_position,state.intruder_position)
      #Con ayuda de la IA añadimos el parametro distancia al intruso, a mayor distancia del defensor al intruso,
      #más seguros podemos estar de que no se van a cruzar y MAX perderá.
      #en este caso, mayor distancia es directamente mejor, por lo que no hace falta tocar el calculo.
      if valor_intruso != float("inf"):
        seguridad = valor_intruso #Se hace un check para evitar que las distancias sean infinitas y dañen la utilidad.
      valor_terminal = 0.0
      if masCercano!= float("inf"):
        valor_terminal = 100.0/1.0+masCercano
      
      valor_pendientes = 10.0*len(state.pending_terminals)
      
      utilidad = score+seguridad+valor_terminal-valor_pendientes #Se le suma a la evaluación el componente de "seguridad" (distancia al intruso)
      
      if utilidad >=1000:
        utilidad = 999.0
      elif utilidad <=-1000:
        utilidad = -999.0
        
    return utilidad
