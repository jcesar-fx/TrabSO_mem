import time as t

class processMemGerenciador():
    def __init__(self, pe):
        self.PiD = pe.PiD # identificador do processo
        self.listaSqAcesso = pe.listaSqAcesso # lista de sequencia do processo
        self.localMem = [] # lista da memoria local do processo
        self.maxLocalMem = pe.qntMem # tamanho max que a mem. local do processo pode ter
        self.contador = 0 # contador usado para saber qual pagina ele deve ler
        self.MRU = [] # lista dos menos recentemente usados
        self.numTrocas = 0
        self.politicaMem = None

        
    def mainCall (self):
        if self.politicaMem == 'local':
            if self.listaSqAcesso[self.contador] in self.localMem: # se esta na memoria
                #le a pagina
                self.MRU.remove(self.listaSqAcesso[self.contador]) # atualiza mru
                self.MRU.append(self.listaSqAcesso[self.contador])
                self.contador += 1 # incrementa contador
            else: # se nao esta na memoria
                if len(self.localMem) >= self.maxLocalMem: # se memoria cheia
                    self.localMem.remove(self.MRU[0]) # remove o menos usado
                    self.MRU.pop(0) # remove da lista de menos usado
                    self.localMem.append(self.listaSqAcesso[self.contador]) # adiciona o valor na memoria local
                    self.MRU.append(self.listaSqAcesso[self.contador]) # adiciona o valor a lista de menos usados
                    self.numTrocas += 1
                    self.contador += 1 # incrementa contador
                else: # se memoria nao cheia
                    self.localMem.append(self.listaSqAcesso[self.contador]) # adiciona o valor na memoria local
                    self.MRU.append(self.listaSqAcesso[self.contador]) # adiciona o valor a lista de menos usados
                    self.contador += 1 # incrementa contador


class MenosRecente():
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador # carrega todas variveis passada na inicialização
        self.processos = gerenciador.processos # instancializa os processos
        self.processosProntos = [] # inicia uma lista vazia de processos prontos
        self.generalSleepTime = 0.003 # apenas uma formalização na hora de usar a função sleep
        self.dictProcessMem = {}
    # inicia o algoritmo
    def iniciar(self):
        print("MRU start")
        self._alternanciaCirc()
        # prints de log
        print("MRU end")
        totalTrocas = sum(i.numTrocas for i in self.dictProcessMem.values())
        return totalTrocas
    
    def _alternanciaCirc(self):
        tamanhoInicial = len(self.processos)    # tamanho inicial da lista de processos
        processosExecutaveis = []               # inicializa a lista que nos ajuda a separar os processos iniciados dos demais
        clockTick = 0                           # clockTick é usado para saber quando rodamos uma fração de fracaoCPU de cpu (definida na entrada)
        
        # enquanto o tamanho de processos pronto for menor que o tamanho da lista inicial "só acaba quando todos os processos ficarem prontos"
        while len(self.processosProntos) < tamanhoInicial:
            print("Tick..", clockTick, "Tack..")
            self.gerenciador.clock += 1 # contador global de clock (diferente do fracaoCPU =/= clock)

            # se o tick do clock for igual ao fracaoCPU(que é a fração de CPU)
            if clockTick == self.gerenciador.fracaoCPU:

                print(f"\u274C Processo {processosExecutaveis[0].PiD} saiu da CPU...\n")
                t.sleep(self.generalSleepTime)
                processosExecutaveis.append(processosExecutaveis[0])
                processosExecutaveis.pop(0)
                clockTick = 0

            for i in range(0, len(self.processos)): # para cada i entre 0 e a qnt de processos
                # se o processo "i" tem o tempo de inicialização igual ou menor ao clock,
                # adiciona a lista de processo executaveis
                if self.processos[i].startTime <= self.gerenciador.clock:
                    print("Processo: ",self.processos[i].PiD," iniciado...\n")
                    processosExecutaveis.append(self.processos[i])
                    pid = self.processos[i].PiD
                    if pid not in self.dictProcessMem:
                        processoMem = processMemGerenciador(self.processos[i])
                        processoMem.politicaMem = self.gerenciador.politicaMem
                        processoMem.maxLocalMem = int((processoMem.maxLocalMem//self.gerenciador.memoria.sizeMold)*self.gerenciador.percent)  # adiciona o tamanho de página
                        self.dictProcessMem[pid] = processoMem

            # para cada i entre a qnt até 0 (decrescente)
            for i in reversed(range(len(self.processos))):
                # se o processo "i" está na lista de execução,
                # remova da lista de processos
                if self.processos[i] in processosExecutaveis:
                    self.processos.pop(i)

            # se há processos na lista de processosExecutaveis
            if processosExecutaveis:
                # diminui o tempo de execução restante do primeiro processo da lista
                ################################################################
                                    # area de "execução"
                ################################################################
                processosExecutaveis[0].execTime -= 1
                
                self.dictProcessMem[processosExecutaveis[0].PiD].mainCall()


                ################################################################
                                    # fim de "execução"
                ################################################################
                # se o tempo de execução chegou a zero
                if processosExecutaveis[0].execTime == 0:
                    print(f"\u2705 Processo {processosExecutaveis[0].PiD} terminou\n")
                    t.sleep(self.generalSleepTime)

                    self.processosProntos.append(processosExecutaveis[0])   # adiciona o processo a lista de processos prontos
                    processosExecutaveis.pop(0)                             # e remove o processo da lista de executaveis

            clockTick += 1 # avança o tick do clock