import classe_grafo as cg
import os
from rich.console import Console

if __name__ == "__main__":
    
    # Resgata o diretório atual
    diretorio = os.getcwd()
    
    # Adiciona /Entrada/ ao diretório atual
    diretorio_entrada = diretorio + "/Entradas/"
    
    # Lista os arquivos do diretório para que o usuário possa escolher
    console = Console()
    console.print("[bold]Arquivos disponíveis:[/bold]\n")
    for i, arquivo in enumerate(os.listdir(diretorio_entrada)):
        console.print(f"{i+1} - [bold cyan]{arquivo}[/bold cyan]")
        
    # Pede para o usuário escolher um arquivo
    escolha = int(console.input("\n[bold]Escolha um arquivo: [/bold]"))
    
    # Adiciona o nome do arquivo escolhido
    arquivo = diretorio_entrada + os.listdir(diretorio_entrada)[escolha-1]
    
    # Apaga a tela
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Pergunta o tamanho da lista tabu e o número máximo de iterações
    console = Console()
    tabu_size = int(console.input("Defina o tamanho da [bold red]lista tabu[/bold red]: "))
    max_iter = int(console.input("Defina o número máximo de [bold red]iterações[/bold red]: "))
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Instancia a classe grafo
    g = cg.grafo(arquivo, os.listdir(diretorio_entrada)[escolha-1])
        
    # Leitura do arquivo
    g.leitura_arquivo()
    
    # Printa o grafo
    g.print_grafo()
    
    g.busca_tabu_tsp(tabu_size, max_iter)
    
    #g.gera_grafico_grafos()