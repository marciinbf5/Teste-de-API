# Busca de Operadoras de Saúde

Aplicação web para pesquisa de operadoras de saúde utilizando **Vue.js** no frontend e **Python (Flask)** no backend. A aplicação carrega dados de um arquivo CSV e permite buscar operadoras por razão social, CNPJ, cidade ou UF, retornando resultados relevantes e formatados.

---

## Índice

- [Descrição](#descrição)  
- [Tecnologias](#tecnologias)  
- [Funcionalidades](#funcionalidades)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Instalação e Configuração](#instalação-e-configuração)  
  - [Backend](#backend)  
  - [Frontend](#frontend)  
- [Uso](#uso)  
- [API](#api)  
  - [Buscar Operadoras](#buscar-operadoras)  
  - [Health Check](#health-check)  
- [Contribuições](#contribuições)  
- [Licença](#licença)  

---

## Descrição

Este projeto consiste em um sistema de busca que oferece uma interface intuitiva para localizar operadoras de saúde. O backend é responsável por carregar e filtrar dados a partir de um arquivo CSV, enquanto o frontend provê a interface para o usuário realizar buscas e visualizar os resultados em tempo real.

---

## Tecnologias

- **Frontend:**  
  - Vue.js 2.x  
  - HTML5 / CSS3  
  - JavaScript (Fetch API)  

- **Backend:**  
  - Python 3.x  
  - Flask (micro-framework web)  
  - Pandas (manipulação de dados CSV)  
  - Flask-CORS (liberação de requisições cross-origin)

---

## Funcionalidades

- Pesquisa por múltiplos critérios (razão social, nome fantasia, CNPJ, cidade, UF).  
- Limitação de resultados para performance (20 resultados por busca).  
- Tratamento de erros robusto para leitura do CSV e requisições HTTP.  
- Indicadores visuais de carregamento, erro e ausência de resultados no frontend.  
- Formatação automática do CNPJ para melhor leitura.  
- API REST simples e eficiente para integração.

---

## Estrutura do Projeto
├── backend/
│ ├── server.py # Backend Flask que serve a API
│ ├── operadoras.csv # Arquivo CSV com dados das operadoras
│ └── requirements.txt # Dependências Python
├── frontend/
│ ├── App.vue # Componente Vue.js principal da interface
│ ├── package.json # Configuração do frontend (npm)
│ └── ... # Outros arquivos do Vue.js
├── README.md # Este arquivo

## Instalação e Configuração

### Backend

1. Clone o repositório e navegue até a pasta backend:

```bash
git clone https://github.com/marciinbf5/Teste-de-API.git
cd Teste-de-API/backend

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install flask pandas flask-cors


python server.py

Navegue até o diretório frontend:

bash
Copiar
Editar
cd ../frontend
npm install
npm run serve
