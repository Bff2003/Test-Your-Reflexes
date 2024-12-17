# TestYourReflexs

## A proposta 
Esta documento tem como objetivo apresentar a proposta para o projeto final da disciplina de computação visual. A ideia principal é a criação de um jogo que tem como objetivo testar os reflexos do utilizador, sendo o projeto nomeado de "Test Your Reflexs".
O projeto consiste em um semaforo que muda com tempos inconstantes, entre vermelho, amarelo e verde, o utilizador devera fazer o gesto indicado no ecra o mais rapidamente possivel. No final sera apresentado o tempo que o utilizador fez.


## Motivação 
A motivação para a criação deste projeto surgiu pela vontade de desenvolver um jogo interativo que pudesse ajudar e ser jogado utilizando apenas gestos, promovendo diversão e um desafio aos reflexos dos utilizadores.

## Funcionalidades principais 
O projeto fará uso do algoritmo MediaPipe (para reconhecimento da posição dos dedos) ou OpenPose (para reconhecimento de gestos específicos já pré-treinados) e oferecerá as seguintes funcionalidades principais e especificações:
| Contexto                  | Evento                    | Resposta                                 | Algoritmo       | Prioridade |
| ------------------------- | ------------------------- | ---------------------------------------- | --------------- | ---------- |
| Detecção de gestos        | Gesto indicado na tela    | Validação do gesto e registo do tempo    | MediaPipe Hands | P1         |
| Cálculo de desempenho     | Finalização de sessão     | Exibição do tempo total do gesto         | MediaPipe Hands | P1         |
| Sistema de classificações | Tabela de melhores tempos | Apresentação das pontuações mais rápidas | MediaPipe Hands | P4         |
| Reconheicmento de Objetos | Objeto detetado           | Apresentar objeto o mais rapido possivel | Yolo            | P1         |
| Mascara                   | Mascara                   | Foto com mascara para leadermarks        | MediaPipe       | P1         |
| Gravar Sessão             | Gravar Sessão             | Possibelidade de gravar a sessão         | NO              | P3         |
Funcionalidades extras poderão ser desenvolvidas no decorrer do projeto, mas somente após todas as funcionalidades prioritárias (P1) estarem implementadas e funcionando corretamente.

## Público alvo 
O "Test Your Reflexs" tem como objetivo principal proporcionar entretenimento enquanto ajuda a desenvolver os reflexos dos utilizadores. O público-alvo inclui:
- Pessoas que gostam de jogos.
- Idosos que queiram melhorar os seus reflexos.
- Desportistas que necessitem de melhorar os seus reflexos

## Cronograma
| Dias | Tarefa                                          | Milestone |
| ---- | ----------------------------------------------- | --------- |
| 3    | Planejamento do projeto e escolha de algoritmos |           |
| 3    | Implementação do sistema de detecção de gestos  | P1        |
| 2    | Desenvolvimento do cálculo de tempos de reação  | P1        |
| 2    | Implementação de Mascaras                       | P1        |
| 2    | Implementação de Objetos                        | P1        |
| 2    | Adição da tabela de classificações              | P4        |
| 5    | Testes e ajustes gerais                         |           |
