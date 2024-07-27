import cv2

# Kamera nesnesini oluştur
cap = cv2.VideoCapture(0)

# Kaç kişi kaydedileceğini belirt
num_people = int(input("Kaç kişi kaydetmek istiyorsunuz? "))

# Kişilerin fotoğraflarını çek ve kaydet
for i in range(num_people):
    name = input(f"{i+1}. kişinin adı: ")
    surname = input(f"{i+1}. kişinin soyadı: ")

    # Kameradan bir kare al
    ret, frame = cap.read()

    # Kameradan gelen çerçeve başarılı bir şekilde okundu mu?
    if not ret:
        print("Kamera okuma hatası!")
        break
    else:
        # Resmi kaydet
        file_name = (f'C:\\Users\\olcan\\PycharmProjects\\yapay zeka dersi projem\\images\\'
                     f'{name}_{surname}.jpg')
        cv2.imwrite(file_name, frame)
        print(f"{name} {surname} adlı kişinin fotoğrafı başarıyla kaydedildi.")

# Kaynakları serbest bırak
cap.release()
