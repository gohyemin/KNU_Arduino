import cv2
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import serial
import time


model = load_model('keras_model.h5')
labels = [line.strip() for line in open('labels.txt', 'r', encoding='utf-8')]


arduino = serial.Serial('COM3', 9600)
time.sleep(2)  


cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

       
        image = cv2.resize(frame, (224, 224))
        image = Image.fromarray(image)
        image = ImageOps.fit(image, (224, 224), method=Image.Resampling.LANCZOS)
        image = np.asarray(image).astype(np.float32) / 127.5 - 1
        image = np.expand_dims(image, axis=0)

        # 예측
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = labels[index]
        confidence = prediction[0][index]

        print(f"Detected: {class_name} ({confidence:.2f})")  

        
        if class_name == "0 조명 끄기" and confidence > 0.9:
            arduino.write(b'0')
            print("Sent to Arduino: 0 (LED OFF)")
        elif class_name == "1 조명 키기" and confidence > 0.9:
            arduino.write(b'1')
            print("Sent to Arduino: 1 (LED ON)")
        else:
            print("Confidence too low or unrecognized gesture. No command sent.")

        
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n사용자에 의해 종료되었습니다.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
