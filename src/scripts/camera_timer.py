import cv2
import time

# Inicializa a câmara.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmara.")
    exit()

while True:
    # Lê o frame atual da câmara.
    success, frame = cap.read()
    if not success:
        print("A ignorar frame vazio da câmara.")
        continue

    # Mostra o feed da câmara.
    cv2.imshow('Captura de Imagem', frame)

    # Verifica se o utilizador pressionou uma tecla.
    key = cv2.waitKey(1) & 0xFF

    # Pressionar 'Esc' para sair.
    if key == 27:
        break

    # Pressionar 'Espaço' para iniciar o cronómetro e tirar uma foto.
    if key == ord(' '):
        start_time = time.time()
        while time.time() - start_time < 5:
            # Lê e exibe continuamente o feed enquanto o cronómetro corre.
            success, frame = cap.read()
            if not success:
                continue

            elapsed_time = int(time.time() - start_time)
            # Mostra o cronómetro no feed.
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Cronómetro: {5 - elapsed_time} seg", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Captura de Imagem', display_frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Permitir sair durante o cronómetro.
                break

        # Tira a foto ao final do cronómetro.
        filename = f"captura_{time.strftime('%Y%m%d-%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Foto tirada e guardada como {filename}.")

# Liberta os recursos.
cap.release()
cv2.destroyAllWindows()
