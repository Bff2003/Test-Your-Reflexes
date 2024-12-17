# Speak With Libras

## A proposta 
Este documento pretende apresentar a proposta para o projeto final da disciplina de Computação Visual. A ideia principal é a criação de uma aplicação que permite traduzir gestos de Libras (neste caso o abecedário) e convertê-los para áudio, sendo o projeto nomeado de "Speak With Libras".

## Motivação 
A motivação por trás deste projeto foi a vontade de querer criar algo que pudesse de alguma forma ajudar as pessoas utilizando tecnologia. Assim, surgiu a ideia de desenvolver uma solução que convertesse gestos de Libras em áudio. 

## Funcionalidades principais 
O projeto fará uso do algoritmo MediaPipe (caso se opte por detecção direta da posição dos dedos) ou OpenPose (caso se utilize reconhecimento de imagem com modelos pré-treinados). As funcionalidades principais e suas especificações são:
| Contexto                 | Evento                           | Resposta                               | Algoritmo       | Prioridade |
| ------------------------ | -------------------------------- | -------------------------------------- | --------------- | ---------- |
| Reconhecimento de gestos | Detecção do abecedário em Libras | Transcrever o gesto para texto         | MediaPipe Hands | P1         |
| Reconhecimento de gestos | Gesto de "espaço"                | Inserir um espaço entre palavras       | MediaPipe Hands | P1         |
| Reconhecimento de gestos | Gesto de "podes ler!"            | Ativar o TTS para ler a frase completa | MediaPipe Hands | P1         |
| 

Funcionalidades extras poderão ser desenvolvidas no decorrer do projeto, mas somente após todas as funcionalidades prioritárias (P1) estarem implementadas e funcionando corretamente.

## Público alvo 
O "Speak With Libras" tem como objetivo principal ser uma ferramenta de utilidade pública destinada ao seguinte público-alvo:
- Pessoas com deficiência verbal ou auditiva (Surdos ou Mudos).

## Cronograma de Desenvolvimento
| Dias | Tarefa                                              | Milestone |
| ---- | --------------------------------------------------- | --------- |
| 3    | Planejamento do projeto, escolha de algoritmos      |           |
| 7    | Implementação da detecção do abecedário             | P1        |
| 2    | Implementação dos gestos "espaço" e "podes ler!"    | P1        |
| 2    | Desenvolvimento da integração com TTS               | P1        |
| 5    | Testes e ajustes das funcionalidades principais     | P1        |
| ?    | Adição de funcionalidades extras e melhorias gerais |           |