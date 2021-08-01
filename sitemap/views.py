from abc import abstractproperty
from django.db import close_old_connections
from django.db.models import constraints, indexes, lookups
from django.shortcuts import render
from django.http import HttpResponse, request 
import folium 
from .models import  cidade, rota 
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from django.views.generic.base import View
from folium import plugins # this line is needed for BeautifyIcon




var3 = { 0 : "joinville, -26.3631553, -48.8283163",
         1 : "araquari,  -26.3627797, -48.8254145",
         2 : "jaragua,   -26.3651089,-48.8139691",
         3 : "sfs,       -26.3638811, -48.8274835",
         4 : "barra ,    -26.3651089,-48.8139691",
         5 : "curitiba,  -26.3674473, -48.8310336",
         6 : "matinhos,  -26.3739262,-48.8385038",
         7 : "profipo,   -26.3495175,-48.8313656",
         8 : "itinga,    -26.3531123,-48.8121246",
         9 : "floresta,  -26.3651089,-48.8139691",
        10 : "aventureiro,  -26.3512483,-48.8032469",
        11 : "escolinha,    -26.3513485,-48.8071171",
        12 : "boa vista,    -26.3465655, -48.8272675",
        13 : "itaum,        -26.3513485,-48.8071171",
        14 : "quero quero,  -26.3638256,-48.8133629",
        15 : "pia pia,  -26.3497858,-48.8270138" ,
        16 : "jjjjj,  -26.3651089,-48.8139691" ,
    }



cidades = [] 
# Lista de cores utilizadas no sistema  
cores = ["Yellow","Green","Red"]

# Cor passado no parametro  
cor_max = ""


#Abaixo variáveis para definir as cores  
lista_vrp = [] 
cor_lista = []    
valores = [] 



class Index(View): 
    def get(self,request):
    
        # Mapa tela inicial 
        m = folium.Map( location = [-26.358612,-48.8356497], zoon_start=5 )
        
        main() # Chama a função de roteamento 

        # Abaixo a soma utilizada para marcar a sequencia de vista 
        soma = 0  
       
        # Abaixo tratar dados da função de roteamento
        texto = ''
        distancia = ""
        lista_mensagens = []   
        lista_cidades = []  
        valores.clear()     
        for index, item in enumerate(lista_vrp):
            lista_mensagens = item.split(':')  
            valores.append(lista_mensagens)
            for i in lista_mensagens:
                distancia = lista_mensagens[2] 
                lista_cidades.append(lista_mensagens[2]) 
         
        # Abaixo dados do Html  
        distancia_real = []
        total = []          
        for index, item in enumerate(lista_vrp): 
            texto = item.split('\n')    
            distancia_real.append(texto[2])
            total.append(texto[2])

        # Tratando dos dados para calcular total de km  
        soma = []
        soma_total = 0 
        for valor in total:
            total = valor.split(':')
            soma.append(total)

        # Total de Kilometragem
        for j in soma: 
            valor = (j[1])
            soma_total = soma_total + int(valor)
            print(soma_total)

                
        # Abaixo trata sequencia de visita e passar os valores de cor para mapa 
        cor_usada = ""

        for index, item  in enumerate (lista_vrp):
            texto = (item)
            lista_mensagem = texto.split('\n')    
            
            for index, item  in enumerate (lista_mensagem):
                if index ==1: 
                    sequencia = item        
                    busca(sequencia)
                    cor_usada = ""  
                    if "Yellow" not in cor_lista:
                        cor_usada = "Yellow"
                        cor_lista.append(cor_usada)
                    elif "Blue" not in cor_lista:
                        cor_usada = "Blue"    
                        cor_lista.append(cor_usada)
                    elif "Red" not in cor_lista:
                        cor_usada = "Red"    
                        cor_lista.append(cor_usada)    
                    elif "Orange" not in cor_lista:
                        cor_usada = "Orange"    
                        cor_lista.append(cor_usada)

                    # Abaixo preenche o ícone do mapa 
                    
                    soma = 0                
                    for j in cidades:
                        folium.Marker( location = [ j[1],j[2]],
                        popup = j[0],
                        icon=folium.plugins.BeautifyIcon(
                               border_color = cor_usada,
                               background_color= '#FFF',
                               text_color= cor_usada,
                               number= soma,
                               icon_shape='marker'),
                        tooltip=soma            
                        ).add_to(m)                   

                        ultimo  = j  
                        soma = soma + 1 
                        
                
                               

        # Tratar o ponto de origem no mapa    
        for j in ultimo:
            #print("ultimo:", ultimo[1])
            folium.Marker(
                location=[ ultimo[1], ultimo[2]],
                popup="Mt. Hood Meadows",
                icon=folium.Icon(icon="cloud"),
                ).add_to(m)
        

        cor_lista.clear() # Limpar dados por causa do refresh 
        lista_vrp.clear() # Limpar dados por causa do refresh 
        
        

        m = m._repr_html_()
        context = {
            'm': m,
            'distancia_real': distancia_real,
            'soma_total':soma_total  
        }            

        return render(request, 'map.html', context) 


def busca(sequencia):
    
    cidade = [] 
    sequencia = sequencia.split('->')
    for x in sequencia:      
        for i in var3:
            if int(x) == int(i):
                cidade.append(var3[i])

    cidades.clear()
    for i in cidade: 
        x = i.split(',') 
        cidades.append(x)

def cor(): 

    if "Yellow" not in cor_lista:
        cor_usada = "Yellow"
        cor_lista.append(cor_usada)
    elif "Blue" not in cor_lista:
        cor_usada = "Blue"    
        cor_lista.append(cor_usada)
    elif "Red" not in cor_lista:
         cor_usada = "Red"    
         cor_lista.append(cor_usada)    
    elif "Orange" not in cor_lista:
        cor_usada = "Orange"    
        cor_lista.append(cor_usada)  

    return(cor_usada) 

def create_data_model():

    '''
    data = {}
    data['distance_matrix'] = [
    ] 
    data['num_vehicles'] = 1
    data['depot'] = 0

     #Rota Selecionada 
    rota_selecioana = rota.objects.filter(nome_rota="sul")   

         # Separar as cidades que precisam ser visitadas 
    cidade_visitadas = [] 
    for i in rota_selecioana:        
            cidade_visitadas.append(i.cidade) 
    

        # Abaixo, buscar o ponto de origem 
    tamanho = len(cidade_visitadas)
    cidade1 = ['0']
    
    for i in rota_selecioana: 
        cidades = cidade.objects.filter(cidade_origem=i.cidade)       
        if (i.primeiro == True):
            primeiro1 = i.cidade
           
            for j in cidades:
                if j.cidade_destino in cidade_visitadas:
                    cidade1.append(j.distancia)
                    

        
         # Inserir o ponto de origem no começo da lista  
        cidade_visitadas = [] 
        for i in rota_selecioana: 
            cidades = cidade.objects.filter(cidade_origem=i.cidade)       
            if (i.primeiro == True):
                cidade_visitadas.append(i.cidade)          
    
        # Inserir os pontos de visitas  
        for i in rota_selecioana: 
            cidades = cidade.objects.filter(cidade_origem=i.cidade)       
            if (i.primeiro == False):
                cidade_visitadas.append(i.cidade)

        

        # Alimenta a tabela interna cidade destino 
        cidade_destino = []
        cidade_des = [] 
        for i in cidade_visitadas:   
            origem = i 
            if len(cidade_destino) != 0:
                cidade_des.append(cidade_destino) 
                cidade_destino = [] 
            for j in cidade_visitadas:
                cidades = cidade.objects.filter(cidade_origem=origem,cidade_destino=j)  
                for j in cidades:            
                    cidade_destino.append(j.distancia)                     
                      
        if len(cidade_destino) != 0:
            cidade_des.append(cidade_destino) 
            cidade_destino = [] 


        # Alimenta a matriz do algoritimo de roteiro 
        data['distance_matrix'].clear() 
        #resultado_final.clear()
        #valor_distancia.clear()
        for x in cidade_des:
            data['distance_matrix'].append(x)

        return data
'''
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [

        [
            0, 4.6, 9.8, 11, 9.6, 14
        ],
        [
            4.5, 0, 13.8, 13.8, 11.8, 16.6
        ],
        [
            9.6, 12.2, 0, 7,4, 14.6, 17
        ],
	[
            12.8, 17.4, 8.1, 0, 22.4, 9.9
        ],
        [
            9.8, 9.2 , 14.6, 20.1, 0, 22.9
        ],
	[
            13.5, 17.5 , 18.4, 10.6, 26.2, 0
        ],

    ]
    data['num_vehicles'] = 2
    data['depot'] = 0

    return data

    



def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    #print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = '{}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distancia: {}\n'.format(route_distance)  
       # print(plan_output)      
        lista_vrp.append(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    #print('Maximum of the route distances: {}m'.format(max_route_distance))



def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


if __name__ == '__main__':
    main()

  