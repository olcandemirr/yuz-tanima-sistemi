
import cv2

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

    # FPS hesapla
    fps_counter += 1
    fps_end_time = cv2.getTickCount()
    fps = cv2.getTickFrequency() / (fps_end_time - fps_start_time)
    fps_start_time = fps_end_time

    # FPS değerini ekrana yazdır
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Arkaplan aydınlatma ve kontrast bilgilerini ekrana yazdır
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = int(gray_frame.mean())
    contrast = int(frame.std())
    cv2.putText(frame, f'Brightness: {brightness}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Contrast: {contrast}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Kameradan alınan kareyi göster
    cv2.imshow('Kamera Görüntüsü', frame)

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