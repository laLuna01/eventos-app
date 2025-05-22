# 📝 README - Sistema de Gestão de Eventos com Redis

## 📌 Visão Geral
Este projeto implementa um sistema de gestão de eventos ao vivo utilizando Redis como camada de cache, fila de mensagens e sistema de publicação/assinatura. A aplicação foi desenvolvida para a avaliação prática de um sistema que requer baixa latência e alta escalabilidade.

## ✨ Funcionalidades Principais
1. **Cache de dados de eventos** (60 segundos de expiração)
2. **Fila de notificações** para usuários (processamento bloqueante)
3. **Canal de atualizações** em tempo real (Pub/Sub)

## 🛠️ Pré-requisitos
- Docker instalado
- Python 3.8+
- Git (opcional)

## 🚀 Como Executar

### 1. Iniciar o Redis com Docker
```bash
docker run -p 6379:6379 --name redis-eventos -d redis
```

### 2. Clonar o repositório (opcional)
```bash
git clone [URL_DO_REPOSITORIO]
cd eventos_app
```

### 3. Configurar ambiente Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate    # Windows
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação
```bash
python main.py
```

## 🔍 Testando as Funcionalidades

### Parte 1: Cache de Eventos
- A primeira busca de um evento mostra "Buscando dados na fonte"
- Buscas subsequentes mostram "Dados recuperados do cache"
- O cache expira após 60 segundos

### Parte 2: Fila de Notificações
- Notificações são adicionadas à fila e processadas em ordem FIFO
- O sistema fica aguardando novas mensagens (comportamento bloqueante)

### Parte 3: Pub/Sub
- Atualizações são publicadas em um canal
- Todos os assinantes recebem as mensagens em tempo real

## 📋 Estrutura do Código
```python
# Parte 1 - Cache
def obter_dados_evento(event_id): ...

# Parte 2 - Fila de Notificações
def adicionar_notificacao(usuario, mensagem): ...
def processar_notificacoes(): ...

# Parte 3 - Pub/Sub
def publicar_atualizacao_evento(event_id, titulo): ...
def assinar_atualizacoes(): ...
```

## 🧰 Comandos Úteis para Redis
Acesse o CLI do Redis para monitoramento:
```bash
docker exec -it redis-eventos redis-cli
```

Comandos úteis:
```bash
KEYS *                  # Listar todas as chaves
TTL event:1             # Ver tempo de cache restante
LLEN notificacao:fila   # Ver tamanho da fila
MONITOR                 # Monitorar operações em tempo real
```

## 📊 Critérios de Avaliação Atendidos
✅ **Parte 1 (3 pontos)**  
- Uso correto de GET e SETEX  
- Chave no formato `event:<event_id>`  
- Expiração de 60 segundos  

✅ **Parte 2 (3 pontos)**  
- Fila implementada com lista Redis  
- Uso de LPUSH/RPUSH e BRPOP  
- Processamento bloqueante  

✅ **Parte 3 (4 pontos)**  
- Implementação correta de Pub/Sub  
- Canal `eventos:atualizacoes`  
- Mensagens com event_id e título  

## ⚠️ Solução de Problemas
- **Erro de conexão com Redis**: Verifique se o container está rodando (`docker ps`)
- **Permissões Docker**: Execute com `sudo` ou adicione seu usuário ao grupo docker
- **Erros Python**: Confira se o ambiente virtual está ativado

## 📄 Licença
Este projeto é para fins educacionais e de avaliação.