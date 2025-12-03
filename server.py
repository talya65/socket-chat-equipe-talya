# -*- coding: utf-8 -*-
import threading
import socket

# Dicionário de clientes: username -> socket
clients = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client):
    try:
        # Recebe o nome de usuário do cliente
        username = client.recv(2048).decode('utf-8')
        clients[username] = client
        
    except:
        client.close()
        return

    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if msg.startswith("/w "):
                # Mensagem privada
                try:
                    _, destinatario, mensagem = msg.split(' ', 2)
                    if destinatario in clients:
                        clients[destinatario].send(f"(Privado) {mensagem}".encode('utf-8'))
                    else:
                        client.send(f"Usuário {destinatario} não encontrado.".encode('utf-8'))
                except ValueError:
                    client.send("Formato incorreto! Use: /w <destinatario> <mensagem>".encode('utf-8'))
            else:
                # Broadcast normal
                broadcast(msg.encode('utf-8'), client)
        except:
            remove_client(username)
            break

# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
    for user, client in clients.items():
        if client != sender:
            try:
                client.send(msg)
            except:
                remove_client(user)

# Função para remover um cliente
def remove_client(username):
    if username in clients:
        clients[username].close()
        del clients[username]
        broadcast(f"{username} saiu do chat.".encode('utf-8'), None)
        

# Função principal
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Servidor de bate-papo iniciado")

    try:
        server.bind(("localhost", 7777))
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        print(f'Cliente conectado: {addr}')
        print("Usuários conectados:", list(clients.keys()))


        # Inicia uma thread para cada cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Executa o programa
main()