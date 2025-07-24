import copy, time as t
#from algoritmos.FIFO import FIFO
from algoritmos.MenosUsado import MenosRecente
#from algoritmos.NaoUsadoFreq import NaoUsadoFreq
from algoritmos.Otimo import Otimo


class Processo:
    def __init__(self, startTime, PiD, execTime, priority, qntMem, listaSqAcesso):
        self.startTime = startTime # momento do clock que o processo deve inicializar
        self.PiD = PiD # identificador unico do processo
        self.execTime = execTime # quantos clocks o processo deve executar para finalizar
        self.priority = priority # prioridade/ticket do processo (nao utilizado devido ao uso do algoritmo de alternancia)
        self.qntMem = qntMem #qnt de memoria que um processo deve ter
        self.listaSqAcesso = listaSqAcesso # lista de sequencia de paginas que o processo vai acessar por clock

class Memoria():
    def __init__(self, sizeMem, sizeMold):
        self.sizeMem = sizeMem
        self.sizeMold = sizeMold
        self.moldurasTotais = self.sizeMem//self.sizeMold       

class GerenciadorDeMemoria():
    def __init__(self, nome):
        self.arquivo = nome + ".txt"
        self.algoritmo = None
        self.processos = []
        self.fracaoCPU = None # parcela de clock que um processo deve executar
        self.processoPronto = []
        self.clock = 0 #contador globar do clock
        self.politicaMem = None
        self.listaResultados = [] # lista com o numero de trocas de cada algoritmo de substituição
        self.memoria = None
        self.percent = 0

    def iniciar(self): #função responsavel por chamar todas as funções necessarias pro programa funcionar
        self._le_arquivo()
        if self._validacaoBasica():
            self._exec_algoritmo()
            self._finalizacao()
        else:
            print("há algo de errado na entrada....")

    def _le_arquivo(self): #função que lê o arquivo e preenche as variaveis
        with open(self.arquivo, 'r') as starter:
            linhasLimpas = []
            for line in starter.readlines():
                linhasLimpas.append(line.strip())#cria lista contendo conteudo do arquivo

            self.algoritmo = (linhasLimpas[0].split('|')[0]).lower()
            self.fracaoCPU = int(linhasLimpas[0].split('|')[1])
            self.politicaMem = (linhasLimpas[0].split('|')[2])
            self.sizeMem = int(linhasLimpas[0].split('|')[3])
            self.sizeMold = int(linhasLimpas[0].split('|')[4])
            self.percent = int(linhasLimpas[0].split('|')[5])/100

            self.memoria = Memoria(self.sizeMem, self.sizeMold)

            for linha in linhasLimpas[1:]:#for responsavel por obter os dados de cada processo e cria-los
                partes = linha.split('|')

                startTime = int(partes[0])
                PiD = partes[1]
                execTime = int(partes[2])
                priority = int(partes[3])
                qntMem = int(partes[4])
                sqAcesso = partes[5]
                listaSqAcesso = list(map(int, sqAcesso.split(' ')))

                self.processos.append(Processo(startTime, PiD, execTime, priority, qntMem, listaSqAcesso))

    def _validacaoBasica(self):
        usedMem = 0
        uniquePiDs = []
        leiFracao = []
        for i in range(0, len(self.processos)):
            usedMem += self.processos[i].qntMem
            if self.processos[i].PiD not in uniquePiDs:
                uniquePiDs.append(self.processos[i].PiD)
            if len(self.processos[i].listaSqAcesso) == self.processos[i].execTime:
                leiFracao.append(1)
        if self.sizeMem > self.sizeMold and self.sizeMem > usedMem and (self.politicaMem == 'local' or self.politicaMem == 'global') and len(self.processos) == len(uniquePiDs) and len(self.processos) == len(leiFracao):
            return True
        else:
            return False

    def _exec_algoritmo(self):#função responsavel por conectar o main aos demais scripts
        sleeptime = 0.003
        print(f"\u2699 Iniciando gerenciador com os algoritmos...\n")
        t.sleep(sleeptime)

        MRUself = copy.deepcopy(self)
        OTIMOself = copy.deepcopy(self)

        #self.listaResultados.append( FIFO(self).iniciar() )
        self.listaResultados.append( MenosRecente(MRUself).iniciar() )
        #self.listaResultados.append( NaoUsadoFreq(self).inciar() )
        self.listaResultados.append( Otimo(OTIMOself).iniciar() )

    def _finalizacao(self):
        print(self.listaResultados)
                
GerenciadorDeMemoria("test").iniciar()           