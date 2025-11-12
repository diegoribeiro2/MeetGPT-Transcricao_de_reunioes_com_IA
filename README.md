# MeetGPT – Transcrição Inteligente de Reuniões

Bem-vindo ao repositório do **MeetGPT**, um projeto prático e robusto que desenvolvi para transformar a maneira como documentamos e analisamos reuniões corporativas.
Acesse a aplicação :

[Acesse a aplicação aqui](https://transcricao-de-reunioes-diego.streamlit.app/)

---

## 🎯 O Problema: A Perda de Informação em Reuniões

Quantas vezes você saiu de uma reunião com a sensação de que algum detalhe importante foi esquecido ou mal anotado?  
Decisões cruciais, *action items* e discussões técnicas muitas vezes se perdem em anotações manuais ou na memória dos participantes.  
O MeetGPT foi criado para resolver exatamente esse problema.

---

## 💡 A Solução: MeetGPT

O **MeetGPT** é um Web App desenvolvido em Python que automatiza e inteligibiliza o registro de reuniões. Suas funções principais são:

- Capturar o áudio da reunião em tempo real, diretamente pelo microfone do navegador.
- Transcrever automaticamente o áudio falado para texto preciso.
- Gerar resumos inteligentes dos pontos mais importantes e das decisões tomadas.

O resultado é uma ferramenta valiosa que assegura a documentação fiel de todos os detalhes, economizando tempo e aumentando a produtividade da equipe.

---

## 🚀 Para Além da Transcrição: Aplicações do Projeto

Embora a transcrição seja o coração do projeto, a aplicação vai muito além e serve como base para diversas inovações:

- **Base para Assistentes Virtuais**: O texto transcrito pode alimentar um agente de IA para responder perguntas específicas sobre o que foi discutido.
- **Apoio a Deficientes Auditivos**: Funciona como um sistema de legenda em tempo real, garantindo acessibilidade.
- **Análise de Sentimento**: Pode ser extendido para identificar o tom e a satisfação dos participantes.
- **Sistema de Busca Semântica**: Permite encontrar trechos de reuniões passadas usando conceitos e ideias, não apenas palavras-chave.

---

## 🛠️ Tecnologias e Habilidades Aplicadas

Este projeto foi uma imersão prática em algumas das tecnologias mais demandadas do mercado. Aqui está o que utilizei e aprendi:

### Linguagem e API
- **Python**: Utilizado para toda a lógica de backend, desde a captura do áudio até a interação com APIs externas.
- **OpenAI API (Whisper & GPT)**: O coração da inteligência do projeto.
  - **Whisper**: Modelo de reconhecimento de fala que realiza a transcrição de áudio para texto com alta precisão.
  - **GPT (ex: GPT-3.5-Turbo ou GPT-4)**: Modelo de linguagem responsável por analisar a transcrição e gerar resumos concisos e contextuais.

### Framework Web e Interface
- **Streamlit**: Para construir a interface do usuário de forma rápida e eficiente, permitindo:
  - Gravação de áudio diretamente do navegador.
  - Exibição do status da gravação e processamento.
  - Apresentação organizada da transcrição e do resumo gerado.

### Funcionalidades Técnicas Implementadas
- **Interação com APIs**: Chamadas robustas para a API da OpenAI, tratando respostas e erros.
- **Processamento de Fluxos de Áudio**: Captura de áudio do frontend
-  e envio para o backend em formato adequado.
- **Lógica de Negócio**: Orquestração do fluxo completo:
  áudio -> transcrição (Whisper) -> análise e resumo (GPT) -> apresentação para o usuário.

---

### Gerenciamento de Dados
Criei um sistema simples, mas eficaz, para armazenar e recuperar o histórico de reuniões, permitindo que o usuário acesse transcrições e resumos passados facilmente.

---

## 📈 O Resultado Final

Ao final do desenvolvimento, tenho em mãos um projeto robusto e altamente aplicável.  
O **MeetGPT** é mais do que um simples transcritor; é uma prova de conceito que exemplifica a poderosa integração entre:

- **Desenvolvimento Web com Python (Streamlit)**
- **APIs de Inteligência Artificial de ponta (OpenAI)**
- **Processamento de Linguagem Natural (NLP)**

Este projeto não apenas resolve um problema real, mas também demonstra um fluxo de trabalho moderno para a criação de aplicações inteligentes, abrindo portas para diversas outras possibilidades no universo da IA.
