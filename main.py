import pygame  # Importa a biblioteca pygame para criar o jogo

# Inicializa o pygame
pygame.init() 

# Definindo o tamanho da janela do jogo e o título da janela
window = pygame.display.set_mode([1280, 720])  # Cria uma janela de 1280x720 pixels
pygame.display.set_caption("Pong - Kessler e Erick")  # Define o título da janela

# Inicializando o estado do jogo
score = [0, 0]  # Inicializa o placar dos jogadores
score_imgs = [pygame.image.load("assets/score/0.png"), pygame.image.load("assets/score/0.png")]  # Carrega as imagens para o placar

# Definindo os jogadores e suas propriedades
players = {
    "player1": {"image": pygame.image.load("assets/player1.png"), "y": 310, "moveup": False, "movedown": False},
    "player2": {"image": pygame.image.load("assets/player2.png"), "y": 310, "moveup": False, "movedown": False}
}

# Carrega imagens para o campo, menu e bola
field = pygame.image.load("assets/field.png")
menu_img = pygame.image.load("assets/menu.png")
ball = pygame.image.load("assets/ball.png")

# Inicializa as variáveis da bola
ball_x, ball_y = 617, 337  # Posição inicial da bola
ball_dir, ball_dir_y = -6, 1  # Direção inicial da bola
ball_speed = 1  # Velocidade inicial da bola

clock = pygame.time.Clock()  # Cria um objeto Clock para controlar a taxa de quadros
play_button_img = pygame.image.load("assets/play_button.png")  # Carrega a imagem do botão "Play"

# Função para desenhar o menu na tela
def draw_menu():
    window.blit(menu_img, (0, 0))  # Desenha a imagem do menu no canto superior esquerdo
    window.blit(play_button_img, (button_x, button_y))  # Desenha o botão "Play" no centro da tela
    pygame.display.update()  # Atualiza a tela para mostrar as mudanças

# Calcula a posição do botão "Play" para centralizá-lo na tela
button_x = (1280 - play_button_img.get_width()) // 2
button_y = (720 - play_button_img.get_height()) // 2
in_menu = True  # Variável para controlar se o jogo está no menu ou em execução

# Função para desenhar o campo de jogo, jogadores, bola e placar na tela
def draw_game():
    window.blit(field, (0, 0))  # Desenha o campo de jogo
    window.blit(players["player1"]["image"], (50, players["player1"]["y"]))  # Desenha o Jogador 1
    window.blit(players["player2"]["image"], (1150, players["player2"]["y"]))  # Desenha o Jogador 2
    window.blit(ball, (ball_x, ball_y))  # Desenha a bola
    window.blit(score_imgs[0], (500, 50))  # Desenha a pontuação do Jogador 1
    window.blit(score_imgs[1], (710, 50))  # Desenha a pontuação do Jogador 2
    pygame.display.update()  # Atualiza a tela para mostrar as mudanças

# Função para mover os jogadores de acordo com as teclas pressionadas
def move_player():
    for player in players.values():
        if player["moveup"] and player["y"] > 0:
            player["y"] -= 7  # Move o jogador para cima
        if player["movedown"] and player["y"] < 575:
            player["y"] += 7  # Move o jogador para baixo

# Função para verificar a vitória
def check_victory():
    global in_menu, score
    if score[0] == 10:
        show_victory_message("Player 1 Wins!")  # Exibe mensagem de vitória para Jogador 1
        reset_game()  # Reinicia o jogo
        in_menu = True  # Volta para o menu   
    elif score[1] == 10:
        show_victory_message("Player 2 Wins!")  # Exibe mensagem de vitória para Jogador 2
        reset_game()  # Reinicia o jogo
        in_menu = True  # Volta para o menu

# Função para mostrar a mensagem de vitória na tela
def show_victory_message(message):
    font = pygame.font.Font(None, 74)  # Define a fonte e o tamanho do texto
    text = font.render(message, True, (0, 0, 0))  # Renderiza o texto em preto
    text_rect = text.get_rect(center=(1280//2, 720//2))  # Centraliza o texto na tela
    window.blit(text, text_rect)  # Desenha o texto na tela
    pygame.display.update()  # Atualiza a tela para mostrar a mensagem
    pygame.time.wait(3000)  # Aguarda 3 segundos antes de continuar

# Função para mover a bola e detectar colisões
def move_ball():
    global ball_x, ball_y, ball_dir_y, ball_dir, score, score_imgs, start_time, ball_speed
    ball_x += ball_dir * ball_speed  # Move a bola horizontalmente
    ball_y += ball_dir_y * ball_speed  # Move a bola verticalmente

    # Detecção de colisão com as raquetes
    if ball_x < 120 and players["player1"]["y"] < ball_y + 23 < players["player1"]["y"] + 146:
        collision_y = ball_y - (players["player1"]["y"] + 73)
        ball_dir_y = collision_y / 73 * 3
        ball_dir *= -1  # Inverte a direção horizontal da bola

    if ball_x > 1100 and players["player2"]["y"] < ball_y + 23 < players["player2"]["y"] + 146:
        collision_y = ball_y - (players["player2"]["y"] + 73)
        ball_dir_y = collision_y / 73 * 3
        ball_dir *= -1  # Inverte a direção horizontal da bola

    if ball_y >= 680 or ball_y <= 0:
        ball_dir_y *= -1  # Inverte a direção vertical da bola

    if ball_x < 45:
        score[1] += 1  # Incrementa a pontuação do Jogador 2
        score_imgs[1] = pygame.image.load(f"assets/score/{score[1]}.png")  # Atualiza a imagem da pontuação
        check_victory()  # Verifica se houve vitória
        reset_round()  # Reinicia a posição da bola e dos jogadores
        start_time = pygame.time.get_ticks()  # Reseta o cronômetro após marcar um ponto
    elif ball_x > 1190:
        score[0] += 1  # Incrementa a pontuação do Jogador 1
        score_imgs[0] = pygame.image.load(f"assets/score/{score[0]}.png")  # Atualiza a imagem da pontuação
        check_victory()  # Verifica se houve vitória
        reset_round()  # Reinicia a posição da bola e dos jogadores
        start_time = pygame.time.get_ticks()  # Reseta o cronômetro após marcar um ponto

    # Verifica se é hora de aumentar a velocidade da bola
    current_time = pygame.time.get_ticks()  # Obtém o tempo atual em milissegundos
    if current_time - start_time >= 10000:  # Se passaram 10 segundos desde o último aumento
        ball_speed += 0.25  # Aumenta a velocidade da bola em 0.25
        start_time = current_time  # Reseta o cronômetro para os próximos 10 segundos

# Função para reiniciar a pontuação dos jogadores 
def reset_game():
    global score_imgs, score
    score = [0, 0]
    score_imgs[0] = pygame.image.load(f"assets/score/{score[0]}.png") 
    score_imgs[1] = pygame.image.load(f"assets/score/{score[1]}.png")  

# Função para reiniciar a posição da bola e dos jogadores
def reset_round():
    global ball_x, ball_y, ball_dir, ball_dir_y, ball_speed
    ball_x, ball_y = 617, 337  # Reinicia a posição da bola
    ball_dir *= -1  # Inverte a direção horizontal da bola
    ball_dir_y = 1  # Reseta a direção vertical da bola
    ball_speed = 1  # Reseta a velocidade da bola
    players["player1"]["y"] = 310  # Reinicia a posição do Jogador 1
    players["player2"]["y"] = 310  # Reinicia a posição do Jogador 2 




# Inicializa o temporizador para o aumento de velocidade
start_time = pygame.time.get_ticks()  # Configura o tempo inicial do jogo

# Loop principal do jogo
loop = True
while loop:
    for events in pygame.event.get():  # Loop para processar eventos
        if events.type == pygame.QUIT:
            loop = False  # Encerra o loop se a janela for fechada

        if in_menu:
            if events.type == pygame.MOUSEBUTTONDOWN:  # Verifica clique do mouse
                mouse_x, mouse_y = events.pos
                if button_x <= mouse_x <= button_x + play_button_img.get_width() and \
                   button_y <= mouse_y <= button_y + play_button_img.get_height():
                    in_menu = False  # Sai do menu e entra no jogo
                    reset_game()
                    reset_round()
        else:
            if events.type == pygame.KEYDOWN:  # Verifica teclas pressionadas
                if events.key == pygame.K_w:
                    players["player1"]["moveup"] = True
                if events.key == pygame.K_s:
                    players["player1"]["movedown"] = True
                if events.key == pygame.K_UP:
                    players["player2"]["moveup"] = True
                if events.key == pygame.K_DOWN:
                    players["player2"]["movedown"] = True
            if events.type == pygame.KEYUP:  # Verifica teclas soltas
                if events.key == pygame.K_w:
                    players["player1"]["moveup"] = False
                if events.key == pygame.K_s:
                    players["player1"]["movedown"] = False
                if events.key == pygame.K_UP:
                    players["player2"]["moveup"] = False
                if events.key == pygame.K_DOWN:
                    players["player2"]["movedown"] = False

    if in_menu:
        draw_menu()  # Desenha o menu se estiver no menu
    else:
        draw_game()  # Desenha o campo de jogo, jogadores, bola e placar
        move_ball()  # Move a bola
        move_player()  # Move os jogadores

    clock.tick(75)  # Controla a taxa de quadros do jogo

pygame.quit()  # Encerra o módulo pygame