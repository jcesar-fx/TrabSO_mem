import time as t

class AlternanciaCirc():
                    def __init__(self,gerenciador):
                        self.gerenciador = gerenciador
                        self.processos = gerenciador.processos
                        self.processosProntos = gerenciador.processoPronto
                        self.generalSleepTime = 0.003   

                    def iniciar(self):
                        self._alternanciaCirc()
                    
                    def _alternanciaCirc(self):
                        tamanhoInicial = len(self.processos)
                        processosExecutaveis = []
                        clockTick = 0
                        while len(self.processosProntos) < tamanhoInicial: # enquanto tenha processos a executar...
                            print("Tick..", clockTick, "Tack..")
                            self.gerenciador.clock += 1
                            if clockTick == self.gerenciador.clocks:
                                print(f"\u274C Processo {processosExecutaveis[0].PiD} saiu da CPU...\n")
                                t.sleep(self.generalSleepTime)
                                processosExecutaveis.append(processosExecutaveis[0])
                                processosExecutaveis.pop(0)
                                clockTick = 0
                            for i in range(0, len(self.processos)):
                                if self.processos[i].startTime <= self.gerenciador.clock:
                                    print("Processo: ",self.processos[i].PiD," iniciado...\n")
                                    processosExecutaveis.append(self.processos[i])
                            
                            for i in reversed(range(len(self.processos))):
                                if self.processos[i] in processosExecutaveis:
                                    self.processos.pop(i)
                            
                            if processosExecutaveis:
                                
                                processosExecutaveis[0].execTime -= 1
                                
                                if processosExecutaveis[0].execTime == 0:
                                    clockTick = -1
                                    print(f"\u2705 Processo {processosExecutaveis[0].PiD} terminou\n")
                                    t.sleep(self.generalSleepTime)
                                    self.processosProntos.append(processosExecutaveis[0])
                                    processosExecutaveis.pop(0)
                            clockTick += 1