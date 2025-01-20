import cv2
import numpy as np

def overlay_image(frame, image_path, location=(0, 0), size=None, verbose=False): # size=(width, height), location=(x, y)
    if verbose: print("Inside overlay_image")
    # Carregar a imagem PNG com canal alpha
    if type(image_path) == str:
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    else:
        image = image_path
    
    if image.shape[2] == 3:
        image = add_alpha_channel(image)

    # Verificar se a imagem foi carregada corretamente
    if image is None:
        raise ValueError("A imagem não pôde ser carregada. Verifique o caminho.")

    # Redimensionar a imagem para o tamanho desejado    
    if size is not None:
        if verbose: print("\tResizing image")
        image = cv2.resize(image, size)

    x, y = location

    # size of the image is larger than the frame
    if x + image.shape[1] > frame.shape[1] or y + image.shape[0] > frame.shape[0]:
        if verbose: print("\tA imagem é maior que o frame")
        image = cv2.resize(image, (frame.shape[1] - x, frame.shape[0] - y))

    if verbose: print("\tSplitting image")
    # Separar os canais da imagem (B, G, R, A)
    b, g, r, a = cv2.split(image)

    if verbose: print("\tCreating alpha mask")
    # Criar uma máscara a partir do canal alpha
    alpha_mask = a / 255.0

    if verbose: print("\tGetting ROI")
    # Obter a região do frame onde a imagem será sobreposta
    h, w = image.shape[:2]
    roi = frame[y:y+h, x:x+w]

    if verbose: print("\tApplying mask")
    # Aplicar a máscara na região de interesse
    for c in range(0, 3):  # Para os canais B, G, R
        roi[:, :, c] = roi[:, :, c] * (1 - alpha_mask) + image[:, :, c] * alpha_mask
    
    if verbose: print("\tPutting ROI back in frame")
    # Colocar a região modificada de volta no frame
    frame[y:y+h, x:x+w] = roi

    if verbose: print("\tReturning frame")

    return frame

def add_alpha_channel(image):
    if image.shape[2] == 3:
        b, g, r = cv2.split(image)
        a = np.ones(b.shape, dtype=b.dtype) * 255
        return cv2.merge((b, g, r, a))
    else:
        return image

def remove_alpha_channel(image):
    b, g, r, a = cv2.split(image)
    return cv2.merge((b, g, r))

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # set size of the frame
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    image_path = 'assets/smile.png'
    x, y = 50, 50
    size = (300, 300)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    while True:
        # Capturar frame da câmera
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível capturar o frame da câmera.")
            break
        
        print("(Y, X, A) ")
        print("Frame shape: ", frame.shape)
        print("Image shape: ", image.shape)
        print("Resizing: ", (frame.shape[0], frame.shape[1]))

        # Chamar a função para sobrepor a imagem
        result_frame = overlay_image(frame, image, 50, 0)

        # Mostrar o resultado
        cv2.imshow('Resultado', result_frame)

        # Sair do loop se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar a captura e fechar as janelas
    cap.release()
    cv2.destroyAllWindows()