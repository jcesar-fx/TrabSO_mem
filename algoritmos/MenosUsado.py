import time as t

class MenosRecente():
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador # carrega todas variveis passada na inicialização
        self.processos = gerenciador.processos # instancializa os processos
        self.processosProntos = [] # inicia uma lista vazia de processos prontos
        self.generalSleepTime = 0.003 # apenas uma formalização na hora de usar a função sleep
    
    # inicia o algoritmo
    def iniciar(self):
        self._alternanciaCirc()
    
    def _alternanciaCirc(self):
        tamanhoInicial = len(self.processos)    # tamanho inicial da lista de processos
        processosExecutaveis = []               # inicializa a lista que nos ajuda a separar os processos iniciados dos demais
        clockTick = 0                           # clockTick é usado para saber quando rodamos uma fração de clocks de cpu (definida na entrada)
        
        # enquanto o tamanho de processos pronto for menor que o tamanho da lista inicial "só acaba quando todos os processos ficarem prontos"
        while len(self.processosProntos) < tamanhoInicial:
            print("Tick..", clockTick, "Tack..")
            self.gerenciador.clock += 1 # contador global de clock (diferente do clockS =/= clock)

            # se o tick do clock for igual ao clockS(que é a fração de CPU)
            if clockTick == self.gerenciador.clocks:

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
            
            # para cada i entre a qnt até 0 (decrescente)
            for i in reversed(range(len(self.processos))):
                # se o processo "i" está na lista de execução,
                # remova da lista de processos
                if self.processos[i] in processosExecutaveis:
                    self.processos.pop(i)

            # se há processos na lista de processosExecutaveis
            if processosExecutaveis:
                # diminui o tempo de execução restante do primeiro processo da lista
                processosExecutaveis[0].execTime -= 1
                
                # se o tempo de execução chegou a zero
                if processosExecutaveis[0].execTime == 0:
                    print(f"\u2705 Processo {processosExecutaveis[0].PiD} terminou\n")
                    t.sleep(self.generalSleepTime)

                    self.processosProntos.append(processosExecutaveis[0])   # adiciona o processo a lista de processos prontos
                    processosExecutaveis.pop(0)                             # e remove o processo da lista de executaveis

            clockTick += 1 # avança o tick do clock