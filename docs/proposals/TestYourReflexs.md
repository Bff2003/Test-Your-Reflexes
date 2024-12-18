# TestYourReflexs

## A proposta 
Este documento apresenta a proposta do projeto final da disciplina de Computação Visual. A ideia principal é desenvolver um jogo chamado "Test Your Reflexs", que visa testar e melhorar os reflexos do utilizador de uma forma interativa e divertida.

O conceito central do jogo envolve um semáforo que muda de cor (vermelho, amarelo e verde) em intervalos de tempo aleatórios. Quando a cor muda para o verde, o utilizador deve realizar o gesto, pose ou interação indicada na tela o mais rapidamente possível. Ao final de cada sessão, o tempo de reação do utilizador será apresentado, incentivando a competição e a melhoria contínua.

## Motivação 
A ideia para este projeto surgiu do desejo de criar um jogo inovador, interativo e acessível que possa:
- Ser controlado apenas com gestos, poses ou objetos físicos, promovendo uma experiência única.
- Oferecer desafios aos reflexos e coordenação motora dos utilizadores.
- Ser inclusivo, com potencial para alcançar diferentes públicos, desde gamers até idosos que queiram treinar os reflexos.

## Funcionalidades principais 
O projeto utilizará o MediaPipe para reconhecimento de gestos, poses e objetos, além de outras bibliotecas complementares conforme necessário. Abaixo, detalhamos as funcionalidades e suas especificações:

### 1. Funcionalidades Essenciais
Incluem as principais funcionalidades do jogo, como detecção de gestos, reconhecimento de objetos e poses, cálculo de desempenho e apresentação das classificações.
| Contexto                  | Evento                  | Resposta                                 | Algoritmo       | Prioridade | Obs                   |
| ------------------------- | ----------------------- | ---------------------------------------- | --------------- | ---------- | --------------------- |
| Detecção de Gestos        | Gesto indicado na tela  | Validação do gesto e registo do tempo    | MediaPipe Hands | P1         | Detalhado na seção 4. |
| Reconheicmento de Objetos | Objeto indicado na tela | Apresentar objeto o mais rapido possivel | MediaPipe       | P1         | Detalhado na seção 3. |
| Reconheicmento de Poses   | Pose indicado na tela   | Apresentar objeto o mais rapido possivel | MediaPipe       | P1         | Detalhado na seção 2. |
| Cálculo de desempenho     | Finalização de sessão   | Exibição do tempo total da sessão        | MediaPipe Hands | P1         |                       |
| Sistema de classificações | Melhores tempos         | Apresentação das pontuações mais rápidas | MediaPipe Hands | P4         |                       |
| Mascara                   | Finalizar Jogo          | Subestituição do rosto por macara        | MediaPipe       | P2         |                       |


### 2. Reconhecimento de Poses <!-- 5 Poses -->
As poses são movimentos do corpo que o utilizador deve executar conforme instruções na tela.
| Pose                   | Evento                | Resposta                             | Algoritmo | Prioridade |
| ---------------------- | --------------------- | ------------------------------------ | --------- | ---------- |
| Mão em cima da cabeça  | Pose indicada na tela | Validação da Pose e registo do tempo | MediaPipe | P1         |
| Levantar 2 braços      | Pose indicada na tela | Validação da Pose e registo do tempo | MediaPipe | P1         |
| Braços em forma de "T" | Pose indicada na tela | Validação da Pose e registo do tempo | MediaPipe | P1         |
| Girar a cabeça         | Pose indicada na tela | Validação da Pose e registo do tempo | MediaPipe | P1         |
| Inclinar a cabeça      | Pose indicada na tela | Validação da Pose e registo do tempo | MediaPipe | P1         |

### 3. Reconhecimento de Objetos <!-- 5 Objetos -->
O utilizador deve apresentar o objeto indicado na tela, que será reconhecido pela câmera.
| Objeto             | Evento                  | Resposta                               | Algoritmo | Prioridade |
| ------------------ | ----------------------- | -------------------------------------- | --------- | ---------- |
| Telefone           | Objeto indicado na tela | Validação do Objeto e registo do tempo | MediaPipe | P1         |
| Copo               | Objeto indicado na tela | Validação do Objeto e registo do tempo | MediaPipe | P1         |
| Garrafa de água    | Objeto indicado na tela | Validação do Objeto e registo do tempo | MediaPipe | P1         |
| Mochila            | Objeto indicado na tela | Validação do Objeto e registo do tempo | MediaPipe | P1         |
| Comando ou Relogio | Objeto indicado na tela | Validação do Objeto e registo do tempo | MediaPipe | P1         |


### 4. Reconhecimento de Gestos <!-- 5 Gestos -->
Os gestos são movimentos específicos realizados com as mãos.
| Gesto     | Evento                 | Resposta                              | Algoritmo | Prioridade |
| --------- | ---------------------- | ------------------------------------- | --------- | ---------- |
| "V"       | Gesto indicado na tela | Validação do gesto e registo do tempo | MediaPipe | P1         |
| Soco      | Gesto indicado na tela | Validação do gesto e registo do tempo | MediaPipe | P1         |
| "L"       | Gesto indicado na tela | Validação do gesto e registo do tempo | MediaPipe | P1         |
| "Liga-me" | Gesto indicado na tela | Validação do gesto e registo do tempo | MediaPipe | P1         |
| "Fixe"    | Gesto indicado na tela | Validação do gesto e registo do tempo | MediaPipe | P1         |

### 5. Reconhecimento de Rosto <!-- 1 Rosto -->
O rosto do utilizador será identificado e utilizado para substituir com uma máscara personalizada ao final do jogo.
| Contexto               | Evento         | Resposta         | Algoritmo | Prioridade |
| ---------------------- | -------------- | ---------------- | --------- | ---------- |
| Subestituição de Rosto | Finalizar Jogo | Mascara no Rosto | MediaPipe | P2         |

### 6. Funcionalidades Extra
Funcionalidades adicionais que enriquecem a experiência, como gravação de sessões, efeitos sonoros e captura de fotos para os pódios ao final do jogo.
| Contexto         | Evento          | Resposta                                         | Prioridade |
| ---------------- | --------------- | ------------------------------------------------ | ---------- |
| Gravar Sessão    | Gravar Sessão   | Possibilidade de gravar a sessão                 | P3         |
| Sons de Fundo    | Algo Detetado   | Som de sucesso ou Falha                          | P3         |
| Foto para Podios | Jogo Finalizado | Tirar foto ao utilizador para colocar nos podios | P3         |

Funcionalidades extras poderão ser desenvolvidas no decorrer do projeto, mas somente após todas as funcionalidades acima estarem implementadas e funcionando corretamente.

## Público alvo 
O "Test Your Reflexs" destina-se a:
- Pessoas que buscam jogos interativos e desafiantes.
- Idosos interessados em treinar reflexos e coordenação motora.
- Desportistas que desejam melhorar o tempo de reação.

## Cronograma
| Dias | Tarefa                                          | Milestone |
| ---- | ----------------------------------------------- | --------- |
| 3    | Planejamento do projeto e escolha de algoritmos |           |
| 3    | Implementação do sistema de deteção de gestos   | P1        |
| 2    | Desenvolvimento do cálculo de tempos de reação  | P1        |
| 2    | Implementação de deteção de objetos             | P1        |
| 2    | Implementação de deteção de poses               | P1        |
| 3    | Adição do sistema de classificação              | P2        |
| 5    | Testes e ajustes finais                         |           |

Todas as funcionalidades designadas com a prioridade P1 devem ser concluídas no MVP (Minimum Viable Product).
