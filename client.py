# -*- coding: utf-8 -*-
import threading
import socket

def main():
    # Cria um objeto de soquete para o usuario
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao servidor
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    # Solicita nome de usuário
    username = input('Usuário> ')
    # Envia nome de usuário ao servidor
    client.send(username.encode('utf-8'))
    print('\nConectado! Use /w <usuario> <mensagem> para enviar mensagem privada.\n')

    # Inicia threads para receber e enviar mensagens
    threading.Thread(target=receiveMessages, args=(client,)).start()
    threading.Thread(target=sendMessages, args=(client, username)).start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(f"\n{msg}")
        except:
            print('\nConexão encerrada pelo servidor!')
            client.close()
            break

def sendMessages(client, username):
    while True:
        try:
            msg = input()
            if msg.startswith('/w '):
                # Envia mensagem privada
                client.send(msg.encode('utf-8'))
            else:
                # Envia mensagem normal (broadcast)
                client.send(f"<{username}> {msg}".encode('utf-8'))
        except:
            print('Erro ao enviar mensagem.')
            client.close()
            break

if __name__ == "__main__":
    main()