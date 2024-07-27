import cv2
import dlib
import os

# Yüz tespiti için dlib'in eğitilmiş modelini yükle
detector = dlib.get_frontal_face_detector()

# Kaydedilen fotoğrafların bulunduğu dizini al
image_dir = 'C:\\Users\\olcan\\PycharmProjects\\yapay zeka dersi projem\\images'

# Kaydedilen fotoğraflardan isim ve soyisim bilgilerini al ve bir sözlük oluştur
name_surname_dict = {}
for image_file in os.listdir(image_dir):
    name, surname = os.path.splitext(image_file)[0].split('_')
    name_surname_dict[(name.capitalize(), surname.capitalize())] = cv2.imread(os.path.join(image_dir, image_file))

# Kamera nesnesini oluştur
cap = cv2.VideoCapture(0)  # 0, yerleşik kamerayı temsil eder. Eğer harici bir kamera kullanıyorsanız, cihaz numarasını değiştirin.

# Görüntü kaydetme için ayarlar
frame_width = int(cap.get(3))  # Görüntü genişliği
frame_height = int(cap.get(4))  # Görüntü yüksekliği
out = cv2.VideoWriter('kayit.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

# FPS hesaplamak için kullanılan değişkenler
fps_start_time = cv2.getTickCount()
fps_counter = 0

# Kayıt durumu kontrolü
recording = False

while cap.isOpened():
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Kameradan gelen çerçeve başarılı bir şekilde okundu mu?
    if not ret:
        print("Kamera okuma hatası!")
        break

    # Gri tonlamalı çerçeve elde et
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = detector(gray)

    # Yüz tespiti yapıldıysa isim ve soyisimi yaz
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Her bir kişinin adını ve soyadını kontrol et
        for (name, surname), known_image in name_surname_dict.items():
            # Bilinen kişinin fotoğrafını gri tona dönüştür
            known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)

            # Yüzleri tespit et
            known_faces = detector(known_gray)

            # Eğer bilinen yüzler arasında bulunursa ad ve soyadı ekrana yaz
            for known_face in known_faces:
                if dlib.rectangle.contains(known_face, x, y) and dlib.rectangle.contains(known_face, x + w, y + h):
                    cv2.putText(frame, f'{name} {surname}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # FPS hesapla
    fps_counter += 1
    fps_end_time = cv2.getTickCount()
    fps = cv2.getTickFrequency() / (fps_end_time - fps_start_time)
    fps_start_time = fps_end_time

    # FPS değerini ekrana yazdır
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Arkaplan aydınlatma ve kontrast bilgilerini ekrana yazdır
    brightness = int(gray.mean())
    contrast = int(frame.std())
    cv2.putText(frame, f'Brightness: {brightness}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Contrast: {contrast}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Kameradan alınan kareyi göster
    cv2.imshow('Yüz Tanıma ve İsim Yazma', frame)

    # Kayıt durumunu kontrol et
    if recording:
        out.write(frame)

    # "q" tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # "r" tuşuna basıldığında kaydı başlat/durdur
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        recording = not recording
        if recording:
            print("Kayıt başlatıldı.")
        else:
            print("Kayıt durduruldu.")

    # "s" tuşuna basıldığında görüntüyü kaydet
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'frame_{fps_counter}.png', frame)
        print(f'Frame {fps_counter} kaydedildi.')

# Kaynakları serbest bırak
cap.release()
out.release()

# Penceleri kapat
cv2.destroyAllWindows()