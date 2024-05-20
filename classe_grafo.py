import networkx as nx
import matplotlib.pyplot as plt
import random
import heapq
from rich.console import Console
from rich.table import Table
import time

class grafo():
    
    def __init__(self, caminho, nome_arquivo):
        
        # Define o nome do arquivo que está a entrada
        self.nome = nome_arquivo
        
        # Define o caminho do arquivo
        self.caminho = caminho
           
    def leitura_arquivo(self):
        
        # Abre o arquivo e lê as linhas
        with open(self.caminho, 'r') as file:
            self.linhas = file.readlines()

        # Recebe o número de vértices do grafo
        self.num_vertices = int(self.linhas[0])
        
        # Cria o grafo usando networkx
        self.grafo = nx.Graph()
        
        # Adiciona os vértices no grafo
        self.grafo.add_nodes_from(range(1, self.num_vertices + 1))

        # Adiciona as arestas no grafo, todas as possiveis
        # Iterar sobre os vértices de um grafo. O loop externo percorre os vértices 
        # de 1 até o número total de vértices do grafo
        for i in range(1, self.num_vertices + 1):
            self.linha = self.linhas[i].split()
            
            # Percorre os vértices novamente. Se o valor na posição atual da 
            # linha não for zero, é adicionada uma aresta ao grafo, ligando os 
            # vértices i e j, com um peso igual ao valor na posição atual da linha
            for j in range(1, self.num_vertices + 1):
                if int(self.linha[j-1]) != 0:
                    self.grafo.add_edge(i, j, weight=int(self.linha[j-1]))
                    
    def custo_aresta(self, vertice1, vertice2):
        
        # Retorna o peso da aresta entre os vértices (vertice1 e vertice2)
        return self.grafo[vertice1][vertice2]['weight']
   
    def custo_distancia_total(self, caminho):
        
        #  -> Percorre o caminho dado para a função e calcula o custo total com
        #     base nos pesos já estabelecidos no grafo
        
        custo = 0
        for i in range(len(caminho) - 1):
            
            # Recebe os vértices do caminho i -> j
            vertice1, vertice2 = caminho[i], caminho[i+1]
            
            # Se a aresta entre os vértices existir, adiciona o custo da aresta
            if self.grafo.has_edge(vertice1, vertice2):
                custo += self.custo_aresta(vertice1, vertice2)
            else:
                raise ValueError(f"A aresta entre {vertice1} e {vertice2} não existe no grafo.")
                
        return custo
              
    def solucao_inicial_busca_tabu(self):
        
        # Randomiza o vértice inicial
        initial_vertex = 1
            
        # Cria uma lista de tuplas, onde cada tupla contém o caminho
        F = [(self.grafo,[initial_vertex])]
            
        # Número de vértices no grafo
        n = self.grafo.number_of_nodes()
            
        # Enquanto a lista F não estiver vazia, percorre a lista
        while F:
                
            # Extrai de F a tupla (grafo, caminho)
            graph,path = F.pop()
                
            # Configuração de caminhos
            confs = []
                
            # Itera sobre os vizinhos do último vértice do caminho
            for node in graph.neighbors(path[-1]):
                    
                # A variável conf_p é uma cópia da lista path com o último nó
                # adicionado. A variável conf_g é uma cópia do grafo graph com 
                # o último nó removido.
                conf_p = path[:]
                conf_p.append(node)
                conf_g = nx.Graph(graph)
                conf_g.remove_node(path[-1])
                confs.append((conf_g,conf_p))
                    
            # Se o caminho tiver o mesmo número de vértices que o grafo, verifica
            # se o último vértice do caminho é adjacente ao vértice inicial
            for g,p in confs:
                if len(p)==n:
                    if initial_vertex in list(self.grafo.neighbors(p[-1])):
                        p.append(initial_vertex)
                        return p
                    
                else:
                    F.append((g,p))
                    
        # Se a função chegar a este ponto, nenhum ciclo foi encontrado.
        # Então, chama a função novamente para tentar encontrar um ciclo.
        return self.solucao_inicial_busca_tabu()
         
    def encontra_vizinhos(self, caminho):
        
        # -> Função para encontrar os vizinhos de um caminho dado
        
        # Cria uma lista de vizinhos, serão armazenados todos os vizinhos
        # possiveis para o caminho dado
        vizinhos = []
        
        # Randomiza um índice i, no caso será um vertice do caminho que será
        # trocado com outro vertice
        i = random.randint(0, len(caminho) - 1)
        
        # Itera sobre o caminho, substituindo o vértice i pelo vértice j
        # e assim criando um novo caminho, não necessariamente válido
        # mas trocando todas as posições possíveis para a busca tabu
        for j in range(len(caminho)):
            
            # Apenas verifica se i é diferente de j para fazer a troca
            if i != j:
                vizinho = caminho.copy()
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                vizinhos.append(vizinho)
                
        return vizinhos
    
    def verifica_vizinhos_validos(self, vizinhos):
        
        # -> Função para verificar se os vizinhos são válidos, ou seja, se 
        #    todos os vértices / arestas do caminho existem no grafo e são
        #    válidos para a busca tabu
        
        # Cria uma lista de vizinhos válidos
        vizinhos_validos = []
        
        # Verifica se cada caminho é válido, se for valido, adiciona na lista
        # que retornará os vizinhos válidos, retirando os impossiveis
        for caminho in vizinhos:
            valido = all(self.grafo.has_edge(caminho[i], caminho[i+1]) for i in range(len(caminho) - 1))
            
            if valido and caminho[0] == caminho[-1]:
                vizinhos_validos.append(caminho)
                
        return vizinhos_validos
        
    def busca_tabu_tsp(self, tabu_size, max_iter):
        
        # Marca o tempo de início
        start = time.time()
        
        # Marca o tempo para achar a solução inicial
        start_solucao_inicial = time.time()
        
        self.solucao_inicial = self.solucao_inicial_busca_tabu()

        # Calcula o custo do caminho
        self.custo_solucao_inicial = self.custo_distancia_total(self.solucao_inicial)
        
        # Marca o tempo de término
        end_solucao_inicial = time.time()
        
        # Inicializa o melhor caminho encontrado e o melhor custo
        melhor_caminho = self.solucao_inicial
        melhor_custo = self.custo_solucao_inicial

        # Salva o melhor caminho e o melhor custo encontrado durante a busca,
        # mesmo que esse caminho não seja o melhor caminho no final da busca
        melhor_caminho_encontrado = melhor_caminho
        melhor_custo_encontrado = melhor_custo

        # Variaveis para salvar o pior caminho e o pior custo encontrado durante a busca
        pior_caminho = melhor_caminho
        pior_custo = melhor_custo

        # Inicializa a lista tabu
        tabu = []
        
        # Inicializa o contador de iterações
        iteracao = 0
        
        # Enquanto o número de iterações for menor que o máximo
        while iteracao < max_iter:
            
            # Gerar uma lista de vizinhos do melhor caminho encontrado
            vizinhos = self.encontra_vizinhos(melhor_caminho)
            
            # Ordena os vizinhos por custo
            heapq.heapify(vizinhos)
            
            # Verifica os vizinhos validos
            vizinhos_validos = self.verifica_vizinhos_validos(vizinhos)
            
            # Enquanto houver vizinhos válidos
            while vizinhos_validos:
                
                # Seleciona o melhor vizinho com menor custo, alem de garantir
                # que este vizinho não voltara a ser lido dentro deste while
                vizinho = heapq.heappop(vizinhos_validos)
                
                # Verifica o custo do vizinho que esta sendo processado
                custo_vizinho = self.custo_distancia_total(vizinho)
                            
                # Se o vizinho não estiver na lista tabu ou se o custo do vizinho 
                # for menor que o melhor custo
                if vizinho not in tabu or custo_vizinho < melhor_custo:
                    
                    # Atualiza o melhor caminho e o melhor custo
                    melhor_caminho = vizinho
                    melhor_custo = custo_vizinho
                    
                    # Adiciona o melhor caminho independente encontrado em
                    # toda a busca tabu
                    if melhor_custo < melhor_custo_encontrado:
                        melhor_caminho_encontrado = melhor_caminho
                        melhor_custo_encontrado = melhor_custo
                    
                    # Atualiza o pior caminho e o pior custo
                    if melhor_custo > pior_custo:
                        pior_caminho = melhor_caminho
                        pior_custo = melhor_custo
                    
                    # Adiciona o vizinho na lista tabu
                    tabu.append(vizinho)
                    
                    # Se o tamanho da lista tabu for maior que o tamanho da lista tabu
                    if len(tabu) > tabu_size:
                            
                        # Remove o primeiro elemento da lista tabu
                        tabu.pop(0)

            # Enquanto houver vizinhos
            iteracao += 1
            
            # Se o número de iterações exceder o máximo permitido, interrompe o loop
            if iteracao >= max_iter:
                break
        
        # Marca o tempo de término
        end = time.time()
        
        # Calcula o tempo de execução
        tempo_execucao = end - start

        console = Console()
        
        console.print(f"\n\nArquivo: [bold green]{self.nome}[/bold green]")
        
        console.print(f"Lista tabu com tamanho [bold green]{tabu_size}[/bold green] feito com [bold green]{max_iter}[/bold green] iterações")
        
        console.print(f"Tempo de Execução: [bold green]{tempo_execucao:.4f}[/bold green] segundos")
        
        console.print(f"Tempo para achar a solução inicial: [bold green]{end_solucao_inicial - start_solucao_inicial:.4f}[/bold green] segundos\n")
        
        console.print(f"\n\nCaminho Inicial: [bold yellow]{self.solucao_inicial}[/bold yellow], com custo [bold yellow]{self.custo_solucao_inicial}[/bold yellow]\n")
        
        console.print(f"Caminho final encontrado: [bold purple]{melhor_caminho}[/bold purple], com custo [bold purple]{melhor_custo}[bold purple]\n")
        
        console.print(f"Melhor Caminho Encontrado: [bold cyan]{melhor_caminho_encontrado}[/bold cyan], com custo [bold cyan]{melhor_custo_encontrado}[bold cyan]\n")
                  
        console.print(f"Pior Caminho Encontrado: [bold red]{pior_caminho}[/bold red], com custo [bold red]{pior_custo}[/bold red]\n\n")          
        
    def print_grafo(self):
          
        # Cria a tabela
        table = Table(title="Grafo")
        
        # Adiciona as colunas
        table.add_column("Vertices", justify="center", style="cyan", no_wrap=True)
        table.add_column("Arestas", justify="", style="magenta", no_wrap=True)
        
        # Adiciona as linhas (Vertices, Arestas)
        for i in range(1, self.num_vertices + 1):
            
            arestas = self.grafo.edges(i)
            table.add_row(str(i), str(arestas))
        
        # Printa a tabela
        console = Console()
        console.print(table)
    
    def gera_grafico_grafos(self):
        
        # Gera o gráfico
        nx.draw(self.grafo, with_labels=True)
        plt.show()