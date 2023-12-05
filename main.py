import cv2 as cv
import requests

# Trabalho realizado por Henyo Nunes, Lucas Rodrigues e Lucas Zatt
# Utilizamos um bot do telegram para fazer envio das informações em tempo real, podendo ser ajustado para minutos/horas.
# Foi utilizado o método de análise de imagem

def getVideoCapture():
    url = "http://user:user1!@ghelfer.no-ip.org:8040/videostream.cgi"
    cap = cv.VideoCapture(url)
    if not cap.isOpened():
        print("Falha na conexão com câmera...")
        exit()
    return cap


def processFrame(imagem):
    if imagem is None:
        print("Erro, imagem não disponível.")
        exit()

    imagemOriginal = imagem
    imagemCinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    x, y = 340, 115
    height, cm = 42, 5.20
    tu, td = 50, 150

    edges = cv.Canny(imagemCinza, tu, td)
    px = 0

    for i in range(y, 157, 1):
        if edges[i, x] == 255:
            break
        px += 1

    altura = (height - px) * cm

    if altura <= 0:
        print('Análise da imagem imposibilitada, possivelmente está à noite!')
        sendMessageTelegram('Análise da imagem imposibilitada, possivelmente está à noite!')
    else:
        print("A altura atual da Galeria é: " + str(220 - altura) + " cm")
        sendMessageTelegram(
            "A altura atual da Galeria é: " + str(220 - altura) + " cm")  # Envio de mensagem do telegram

    return imagemOriginal

def sendMessageTelegram(mensagem):
    url = 'https://api.telegram.org/bot6727165822:AAH_nhaYpI4w-itj4DI1XFEBtieCHI7qq2w/sendMessage'
    myobj = {'chat_id': '782862208', 'text': mensagem}

    try:
        requests.post(url, json=myobj)
    except:
        print('Erro na requisição de enviar mensagem!')

if __name__ == '__main__':
    cap = getVideoCapture()

    while True:
        ret, imagem = cap.read()

        if not ret:
            print("Frame da imagem não recebido!")
            break

        processed_frame = processFrame(imagem)

        cv.imshow("Galeria Rua Sao Jose", processed_frame)
        k = cv.waitKey(10)
        if k == ord("e"):
            exit()
