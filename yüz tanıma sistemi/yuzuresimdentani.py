import cv2
import dlib
import os

# Yüz tespiti için dlib'in eğitilmiş modelini yükle
detector = dlib.get_frontal_face_detector()

# Proje klasöründeki tüm resim dosyalarını al
image_files = os.listdir('C:\\Users\\olcan\\PycharmProjects\\yapay zeka dersi projem\\images')

for image_file in image_files:
    # Resmi yükle
    image_path = os.path.join('C:\\Users\\olcan\\PycharmProjects\\yapay zeka dersi projem\\images', image_file)
    known_image = cv2.imread(image_path)

    # Resmi gri tona dönüştür
    known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = detector(known_gray)

    # Yüz tespiti yapıldıysa isim ve soyisimi yaz
    if len(faces) > 0:
        # İsim ve soyisim dosya adından al
        name, surname = os.path.splitext(image_file)[0].split('_')
        name = name.capitalize()  # İlk harfi büyük yap
        surname = surname.capitalize()

        # Her yüz için isim ve soyisimi çiz
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.putText(known_image, f'{name} {surname}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Tanımlı resmi ekranda göster
        cv2.imshow('Yüz Tanıma ve İsim Yazma', known_image)
        cv2.waitKey(1000)  # Her bir kişi için bir saniye göster
        cv2.destroyAllWindows()
