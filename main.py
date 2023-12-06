import time
import cv2 as cv
import requests

# Função para obter o fluxo de vídeo da câmera IP
def getVideoCapture():
    # URL da câmera IP
    url = "http://user:user1!@ghelfer.no-ip.org:8040/videostream.cgi"
    # Inicializa o objeto VideoCapture
    cap = cv.VideoCapture(url)
    # Verifica se a câmera está aberta corretamente
    if not cap.isOpened():
        print("Falha na conexão com câmera...")
        exit()

    return cap

# Função para processar um frame de imagem
def processFrame(imagem):
    # Verifica se a imagem é válida
    if imagem is None:
        print("Erro, imagem não disponível.")
        exit()

    # Salva a imagem original
    imagemOriginal = imagem
    # Converte a imagem para escala de cinza
    imagemCinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    # Parâmetros para cálculo da altura da água
    x, y = 340, 115
    height, cm = 42, 5.20
    tu, td = 50, 150

    # Aplica o detector de bordas Canny
    edges = cv.Canny(imagemCinza, tu, td)
    px = 0

    # Encontra a posição da borda na imagem
    for i in range(y, 157, 1):
        if edges[i, x] == 255:
            break
        px += 1

    # Calcula a altura com base na posição da borda
    altura = (height - px) * cm

    return altura, imagemOriginal

# Função para enviar mensagens para o Telegram
def sendMessageTelegram(mensagem):
    # URL da API do Telegram para enviar mensagens
    url = 'https://api.telegram.org/bot6727165822:AAH_nhaYpI4w-itj4DI1XFEBtieCHI7qq2w/sendMessage'
    # Parâmetros da mensagem
    myobj = {'chat_id': '782862208', 'text': mensagem}

    try:
        # Envia a requisição POST para enviar a mensagem
        requests.post(url, json=myobj)
    except:
        print('Erro na requisição de enviar mensagem!')

# Ponto de entrada do programa
if __name__ == '__main__':
    # Obtém o fluxo de vídeo da câmera
    cap = getVideoCapture()

    # Loop infinito para processar frames continuamente
    while True:
        # Lê um frame do fluxo de vídeo
        ret, imagem = cap.read()

        # Verifica se o frame foi recebido corretamente
        if not ret:
            print("Frame da imagem não recebido!")
            break

        # Processa o frame para obter a altura da água
        altura, processed_frame = processFrame(imagem)

        # Exibe a imagem processada em uma janela
        cv.imshow("Galeria Rua Sao Jose", processed_frame)

        # Envia mensagens para o Telegram com base na altura calculada
        if altura <= 0:
            sendMessageTelegram('Análise da imagem impossibilitada, possivelmente está à noite!')
            time.sleep(300)

        if 1 <= altura <= 100:
            sendMessageTelegram("|Altura da água normal| -> A altura atual da Galeria é: " + str(220 - altura) + " cm")
            time.sleep(200)

        if 100 < altura < 200:
            sendMessageTelegram(
                "|Altura da água está mediana| -> A altura atual da Galeria é: " + str(220 - altura) + " cm")
            time.sleep(100)

        if 200 <= altura < 220:
            sendMessageTelegram(
                "|Altura da água está Alto| -> A altura atual da Galeria é: " + str(220 - altura) + " cm")

        # Aguarda a tecla "e" ser pressionada para sair do programa
        k = cv.waitKey(10)
        if k == ord("e"):
            exit()
