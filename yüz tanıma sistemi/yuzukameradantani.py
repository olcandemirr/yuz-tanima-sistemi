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
cap = cv2.VideoCapture(0)

while True:
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

    # Kameradan alınan kareyi göster
    cv2.imshow('Yüz Tanıma ve İsim Yazma', frame)

    # "q" tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
