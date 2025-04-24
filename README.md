# Acesso ao Ambiente da Aplicação com Docker

Este guia explica como iniciar o ambiente da aplicação utilizando Docker e acessar o banco de dados PostgreSQL via pgAdmin.

## ✅ Pré-requisitos

- Docker instalado e funcionando
- Git instalado

## 🚀 Passo a Passo

### 🧬 PASSO 0 - Clonar o repositório da aplicação

Clone o repositório do GitHub para sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

Substitua `seu-usuario` e `seu-repositorio` pelo caminho correto do seu repositório no GitHub.

---

### 📁 PASSO 1 - Entrar no diretório do projeto

Se ainda não estiver no diretório do projeto, navegue até ele:

```bash
cd /caminho/para/o/seu/projeto
```

---

### 🐳 PASSO 2 - Subir os containers com Docker

Execute o seguinte comando para subir os containers:

```bash
docker-compose up -d
```

```bash
docker-compose down
docker-compose up --build -d
```
with open("../init-db/02_script_dados_systock.sql", "w", encoding="utf-8-sig") as f:

Isso irá:

- Subir o container do **PostgreSQL** com as tabelas criadas automaticamente.
- Subir o container do **pgAdmin** para acessar o banco via navegador.

---

### 🌐 PASSO 3 - Acessar o pgAdmin

1. Abra o navegador e acesse: [http://localhost:8080]
2. Faça login com as credenciais configuradas:

   - **Email:** `admin@systock.com`  
   - **Senha:** `admin123`

3. Conecte-se ao servidor PostgreSQL com as seguintes informações:

#### Aba "Geral":

- **Nome da conexão:** `systock`

#### Aba "Conexões":

- **Host:** `db`  
- **Porta:** `5432`  
- **Database:** `postgres`  
- **Usuário:** `systonk`  
- **Senha:** `systock123`

---

### 📦 PASSO 4 - Verificar tabelas no banco

Após se conectar ao banco, verifique que as tabelas foram criadas automaticamente.

Você pode agora executar as consultas normalmente utilizando o pgAdmin ou qualquer client PostgreSQL de sua preferência.

---

## 📝 Observações

- As configurações de acesso e inicialização do banco estão no arquivo `docker-compose.yml`.
- Certifique-se de que nenhuma outra aplicação está utilizando as portas 5432 (PostgreSQL) ou 8080 (pgAdmin) em seu sistema.

---


pip freeze > requirements.txt# Case-tecnico
