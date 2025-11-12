# Protocolo SRP (Secure Remote Password)

Este projeto implementa o protocolo **SRP (Secure Remote Password)** — um método de autenticação segura entre cliente e servidor, onde a senha **nunca é transmitida** pela rede.  
A comunicação é feita por **sockets TCP** locais (`127.0.0.1`) simulando o fluxo de autenticação distribuída.

---

## 📘 Descrição

O SRP (Secure Remote Password) é um protocolo de autenticação baseado em **prova de conhecimento zero (zero-knowledge proof)**.  
Ele permite que cliente e servidor autentiquem um ao outro sem nunca trocar ou expor a senha real.

---

## ⚙️ Estrutura do Projeto

```
SRP-Protocolo/
├── constants.py        # Parâmetros N, g e funções de hash
├── utils.py            # Funções auxiliares e derivação de chaves
├── register_user.py    # Registro de usuário e geração de salt/verificador
├── server.py           # Servidor SRP (autenticação)
├── client.py           # Cliente SRP (autenticação)
├── users.json          # Gerado automaticamente após o registro
├── .gitignore
└── .editorconfig
```

---

## 🚀 Como Executar

### 1. Ativar o ambiente virtual
```powershell
. .\.venv\Scripts\Activate.ps1
```

### 2. Registrar um usuário
```powershell
python register_user.py
```
Informe o `Username` e `Password` de teste.  
Isso cria o arquivo `users.json` com o salt e o verificador.

### 3. Iniciar o servidor
```powershell
python server.py
```
Deixe o servidor rodando neste terminal.

### 4. Em outro terminal, executar o cliente
```powershell
python client.py
```
Use as mesmas credenciais registradas.  
Se a autenticação for bem-sucedida, será exibido:
```
Autenticação SRP concluída com sucesso.
K (hex): 4f5e...
```

---

## 🧠 Conceito

Durante a execução, o cliente e o servidor derivam a **mesma chave de sessão (K)** usando operações modulares e hashing seguro.  
A senha nunca é enviada pela rede — o servidor armazena apenas um **verificador** derivado da senha.

---

## ✅ Resultado Esperado

- Cliente e servidor autenticam mutuamente.  
- Chave de sessão idêntica (`K`) é derivada em ambos os lados.  
- Nenhuma senha trafega pela rede.  
- Execução local via **sockets TCP**.

---

## 🧩 Tecnologias

- Python 3.12+  
- Sockets TCP  
- Hash SHA-256  

---

## 💬 Exemplo de Saída

Servidor:
```
Servidor SRP ativo em 127.0.0.1:5000
[OK] Sessão autenticada: thales
```

Cliente:
```
Username: thales
Password: ******
Autenticação SRP concluída com sucesso.
K (hex): 4f5e...
```
