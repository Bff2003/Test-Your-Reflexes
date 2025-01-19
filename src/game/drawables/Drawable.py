import cv2
import numpy as np


class Drawable:
    def __init__(self):
        pass
        
    @staticmethod
    def _draw_png(frame, image, image_size=None, start_location=None):
        """Draws a PNG image on the frame, preserving transparency."""
        if start_location is None:
            start_location = (0, 0)
        if image_size is None:
            image_size = image.shape[:2]
        
        # Certifica que a imagem tem canal alfa
        if image.shape[2] == 4:  # Se a imagem tem canal alfa
            # Separa os canais BGR e alfa
            bgr = image[:, :, :3]
            alpha = image[:, :, 3] / 255.0  # Normaliza para valores entre 0 e 1
            
            # Redimensiona se necessário
            if image.shape[:2] != image_size:
                bgr = cv2.resize(bgr, (image_size[1], image_size[0]))
                alpha = cv2.resize(alpha, (image_size[1], image_size[0]))
            
            if bgr.shape[:2][0] > frame.shape[0] or bgr.shape[:2][1] > frame.shape[1]:
                bgr = cv2.resize(bgr, (frame.shape[1], frame.shape[0]))
                alpha = cv2.resize(alpha, (frame.shape[1], frame.shape[0]))
            
            # Calcula as posições finais
            end_y = min(start_location[1] + bgr.shape[0], frame.shape[0])
            end_x = min(start_location[0] + bgr.shape[1], frame.shape[1])
            
            # Certifica que a posição inicial está dentro dos limites
            start_y = max(start_location[1], 0)
            start_x = max(start_location[0], 0)
            
            # Define a região de interesse no frame
            roi = frame[start_y:end_y, start_x:end_x]
            
            # Recorta a imagem e o alpha para corresponder ao ROI
            bgr_cropped = bgr[:roi.shape[0], :roi.shape[1]]
            alpha_cropped = alpha[:roi.shape[0], :roi.shape[1]]
            
            # Cria uma matriz 3D do alpha para multiplicação
            alpha_3d = np.stack([alpha_cropped] * 3, axis=2)
            
            # Combina a imagem com o frame usando o canal alfa
            frame[start_y:end_y, start_x:end_x] = (bgr_cropped * alpha_3d + roi * (1 - alpha_3d)).astype(np.uint8)
        
        return frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Carrega a imagem PNG com transparência
        image = cv2.imread("assets/images/traffic_light/green.png", cv2.IMREAD_UNCHANGED)
        
        # Aplica a imagem sobre o frame
        frame = Drawable._draw_png(
            frame, 
            image,
            (300, 250),
            (frame.shape[1] - 250 - 10, 50)
        )
        
        cv2.imshow('MediaPipe Object Detection', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()