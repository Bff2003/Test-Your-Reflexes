# “The White Canvas” 

## A proposta 
Este documento tem como objetivo apresentar a proposta para o projeto final da disciplina de Computação Visual. A ideia principal é a criação de um quadro branco que permitirá desenhar na tela através de gestos, sendo o projeto nomeado de "The White Canvas".

## Motivação 
A motivação por trás deste projeto surgiu da experiência pessoal com quadros brancos digitais para anotações e apresentações. Ao lembrar de uma aplicação semelhante, decidi que seria interessante desenvolver um projeto com funcionalidades similares, explorando novas formas de interação humano-computador. 

## Funcionalidades principais 
O projeto devera fazer uso do algoritmo MediaPipe e devera conter as seguintes funcionalidades principais: 
| Contexto                  | Evento                    | Funcionalidade                          | Algoritmo       | Prioridade |
| ------------------------- | ------------------------- | --------------------------------------- | --------------- | ---------- |
| Interação por gestos      | Gesto de escrita (1 dedo) | Desenhar na tela com pincel             | MediaPipe Hands | P1         |
| Interação de gestos       | Gesto de seleção          | Gesto para selecionar opções            | MediaPipe Hands | P1         |
| Interação por gestos      | Gesto de borracha         | Apagar traços ou pontos específicos     | MediaPipe Hands | P1         |
| Reconhecimento de Objetos | Reconhece objeto          | Subestitui por imagem                   | Yolo            | P1         |
| Seleção de ferramentas    | Gesto de mudança de cor   | Alterar a cor do pincel                 | MediaPipe Hands | P2         |
| Salvamento de desenhos    | Gesto de salvar           | Salvar o desenho em arquivo             | MediaPipe Hands | P4         |
| Carregamento de desenhos  | Gesto de carregar         | Carregar um desenho salvo anteriormente | MediaPipe Hands | P4         |
| Gravação de sessões       | Gesto de gravar sessão    | Gravar a sessão de desenho em vídeo     | MediaPipe Hands | P4         |
| Mascara                   | Gravar sessão             | Troca o rosto por uma mascara           | Media Pipe      | P1         |

Funcionalidades extras poderão ser desenvolvidas no decorrer do projeto, mas somente após todas as funcionalidades prioritárias (P1, P2) estarem implementadas e funcionando corretamente.

## Público alvo 
O “The White Canvas” tem como objetivo principal ser usado para entretenimento (diversão), contudo, tem o seguinte publico alvo: 
- Crianças; 
- Adultos que queiram fazer apresentações; 
- Professores; 
- Estudantes; 

## Cronograma 
| Dias | Tarefa                                                  | Milestone |
| ---- | ------------------------------------------------------- | --------- |
| 3    | Planejamento do projeto e escolha de algoritmos         |           |
| 3    | Implementação do gesto de escrita (pincel)              | P1        |
| 3    | Implementação do gesto de borracha                      | P1        |
| 3    | Desenvolvimento da seleção de cores                     | P2        |
| 2    | Adição de funcionalidades de salvar e carregar desenhos | P4        |
| 5    | Testes e melhorias gerais                               |           |