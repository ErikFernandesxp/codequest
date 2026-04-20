# 🎮 CodeQuest

> Aprenda programação jogando — do zero até resolver problemas reais.

---

## 🧠 Sobre o Projeto

O **CodeQuest** é uma plataforma educacional gamificada desenvolvida para ensinar programação de forma prática, interativa e progressiva.

A proposta é simples:
o usuário aprende **fazendo**, enfrentando desafios reais organizados em fases, com feedback imediato e evolução contínua.

---

## ✨ Principais Diferenciais

* 🎯 Aprendizado baseado em desafios práticos
* 🧑‍🏫 Sistema de feedback estilo “professor”
* 📈 Progressão por níveis (gamificação)
* 🌐 Aplicação web leve e acessível
* 🧩 Estrutura escalável para múltiplas linguagens

---

## 🚀 Tecnologias Utilizadas

| Camada    | Tecnologia |
| --------- | ---------- |
| Frontend  | Streamlit  |
| Backend   | Supabase   |
| Linguagem | Python     |
| Dados     | JSON       |

---

## 🎮 Como Funciona

1. O usuário realiza login
2. Escolhe uma linguagem de programação
3. Inicia uma trilha de aprendizado
4. Resolve desafios em forma de código
5. Recebe feedback automático
6. Avança conforme seu desempenho

---

## 🧩 Estrutura do Projeto

```id="u3p1ru"
codequest/
│
├── app.py                  # Aplicação principal
│
├── pages/                 # Páginas do Streamlit
│   ├── login.py
│   ├── dashboard.py
│   ├── linguagem.py
│   ├── fase.py
│
├── backend/               # Lógica de negócio
│   ├── supabase_client.py
│   ├── crud.py
│   ├── validator.py
│
├── data/                  # Conteúdo educacional
│   ├── fases.json
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Executando o Projeto

### 1. Clone o repositório

```id="frbl0f"
git clone https://github.com/SEU_USUARIO/codequest.git
cd codequest
```

---

### 2. Crie um ambiente virtual

```id="q0sp31"
python -m venv venv
```

Ativação:

Windows:

```id="43slcw"
venv\Scripts\activate
```

Linux/Mac:

```id="rr5n7t"
source venv/bin/activate
```

---

### 3. Instale as dependências

```id="0zjyhh"
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env`:

```id="of8f3u"
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

---

### 5. Execute o projeto

```id="8dwn1r"
streamlit run app.py
```

---

## 🌐 Deploy

O projeto pode ser publicado facilmente utilizando:

* Streamlit Cloud
* Render
* Railway

---

## 📸 Demonstração

> *(Adicione aqui prints ou GIF do sistema rodando)*

---

## 🧠 Arquitetura

* Aplicação baseada em componentes leves
* Separação entre interface, lógica e dados
* Persistência de progresso via Supabase
* Sistema de validação modular (extensível)

---

## 🔒 Segurança

* Não execução direta de código do usuário
* Uso de variáveis de ambiente (.env)
* Backend desacoplado da interface

---

## 📈 Possíveis Evoluções

* Sistema de XP e ranking
* Execução real de código em sandbox
* Integração com IA para feedback avançado
* Interface gamificada (estilo jogo real)
* Suporte a novas linguagens

---

## 👨‍💻 Autor

**Erik Fernandes Santos da Cruz**

* GitHub: https://github.com/erikfernandesxp

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
