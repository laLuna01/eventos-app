import redis
import time
import json

# Conexão com o Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Fonte simulada de dados de eventos
eventos_fonte = {
    "1": {"id": "1", "titulo": "Show da Taylor Swift", "descricao": "Show internacional", "data": "2023-11-15"},
    "2": {"id": "2", "titulo": "Tech Conference", "descricao": "Conferência de tecnologia", "data": "2023-11-20"},
    "3": {"id": "3", "titulo": "Festival de Gastronomia", "descricao": "Evento gastronômico", "data": "2023-12-05"}
}

def obter_dados_evento(event_id):
    # Verifica se os dados estão no cache
    chave = f"event:{event_id}"
    dados_cache = r.get(chave)
    
    if dados_cache:
        print(f"Dados do evento {event_id} recuperados do cache")
        return json.loads(dados_cache)
    else:
        print(f"Buscando dados do evento {event_id} na fonte")
        # Simula um delay de acesso à fonte principal
        time.sleep(2)
        
        dados = eventos_fonte.get(event_id)
        if dados:
            # Armazena no Redis com expiração de 60 segundos
            r.setex(chave, 60, json.dumps(dados))
            return dados
        else:
            return None

def adicionar_notificacao(usuario, mensagem):
    notificacao = {
        "usuario": usuario,
        "mensagem": mensagem,
        "timestamp": time.time()
    }
    # Adiciona no início da fila
    r.lpush("notificacao:fila", json.dumps(notificacao))
    print(f"Notificação adicionada para {usuario}")

def processar_notificacoes():
    print("Iniciando processamento de notificações...")
    while True:
        # BRPOP é bloqueante - espera até que haja uma notificação
        _, notificacao_json = r.brpop("notificacao:fila")
        notificacao = json.loads(notificacao_json)
        
        print(f"\nNova notificação:")
        print(f"Usuário: {notificacao['usuario']}")
        print(f"Mensagem: {notificacao['mensagem']}")
        print(f"Timestamp: {time.ctime(notificacao['timestamp'])}")


def publicar_atualizacao_evento(event_id, titulo):
    mensagem = {
        "event_id": event_id,
        "titulo": titulo,
        "timestamp": time.time()
    }
    r.publish("eventos:atualizacoes", json.dumps(mensagem))
    print(f"Atualização publicada para o evento {event_id}")

def assinar_atualizacoes():
    pubsub = r.pubsub()
    pubsub.subscribe("eventos:atualizacoes")
    print("Inscrito no canal de atualizações. Aguardando mensagens...")
    
    for mensagem in pubsub.listen():
        if mensagem['type'] == 'message':
            dados = json.loads(mensagem['data'])
            print(f"\nNova atualização recebida:")
            print(f"Evento ID: {dados['event_id']}")
            print(f"Título: {dados['titulo']}")
            print(f"Timestamp: {time.ctime(dados['timestamp'])}")


if __name__ == "__main__":
    import threading
    
    # Teste Parte 1 - Cache de Eventos
    print("=== Teste Parte 1 - Cache de Eventos ===")
    print(obter_dados_evento("1"))  # Busca na fonte
    print(obter_dados_evento("1"))  # Busca no cache
    print(obter_dados_evento("99"))  # Evento não existe
    
    # Teste Parte 2 - Fila de Notificações
    print("\n=== Teste Parte 2 - Fila de Notificações ===")
    # Inicia o processador em uma thread separada
    processor_thread = threading.Thread(target=processar_notificacoes)
    processor_thread.daemon = True
    processor_thread.start()
    
    # Adiciona algumas notificações
    adicionar_notificacao("joao", "Seu ingresso foi confirmado!")
    adicionar_notificacao("maria", "Evento atualizado: novo horário")
    time.sleep(1)  # Dá tempo para processar
    
    # Teste Parte 3 - Pub/Sub
    print("\n=== Teste Parte 3 - Pub/Sub ===")
    # Inicia o assinante em uma thread separada
    subscriber_thread = threading.Thread(target=assinar_atualizacoes)
    subscriber_thread.daemon = True
    subscriber_thread.start()
    
    # Publica algumas atualizações
    publicar_atualizacao_evento("1", "Show da Taylor Swift - LOCAL ALTERADO")
    publicar_atualizacao_evento("2", "Tech Conference - PALESTRANTE CONFIRMADO")
    
    # Mantém o programa rodando por um tempo para ver as mensagens
    time.sleep(5)