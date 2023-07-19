import random
import string
import os
import csv
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

captcha_length = 6
image_width = 200
image_height = 70
font_size = 40
font_folder = "fonts"
text_file = "new.txt"
output_folder = "images"
csv_file = "data/captchas.csv"

# Metin dosyasından captcha metinlerini okuma
def read_captcha_text_from_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]

# Büyük harf ve küçük harf kombinasyonlarıyla captcha metnini oluşturma
def generate_captcha_text(text):
    captcha_text = ""
    for char in text:
        if char.isalpha():
            if random.choice([True, False]):
                captcha_text += char.upper()
            else:
                captcha_text += char.lower()
        else:
            captcha_text += char
    return captcha_text

# Captcha resmini oluşturma
def generate_captcha_image(text, width, height, font_size, font):
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Her harfi belirli bir açıda, yükseklikte ve derinlikte konumlandırma
    rotation_angles = [random.randint(-15, 15) for _ in range(len(text))]
    y_offsets = [random.randint(-10, 10) for _ in range(len(text))]
    depths = [random.uniform(-0.1, 0.1) for _ in range(len(text))]
    for char, angle, y_offset, depth in zip(text, rotation_angles, y_offsets, depths):
        char_width, char_height = draw.textsize(char, font=font)
        char_image = Image.new('RGBA', (char_width, char_height), color=(255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((0, 0), char, font=font, fill=(0, 0, 0))
        char_image = char_image.rotate(angle, expand=True)

        # Metin boyutuna, derinliğe ve yüksekliğe göre konumlandırma ayarları
        char_x = x + int(char_width * depth)
        char_y = y + y_offset - int(char_height * depth)

        image.paste(char_image, (char_x, char_y), char_image)

        x += char_width

    return image

# Rastgele bir font dosyası seçme
def get_random_font():
    fonts = [os.path.join(font_folder, filename) for filename in os.listdir(font_folder) if filename.endswith('.ttf')]
    return random.choice(fonts)

# Captcha metni ve resmini kaydetme
def save_captcha_data(text, image):
    # Resmi kaydet
    filename = os.path.join(output_folder, f"{text}.png")
    image.save(filename)

    # Metni küçük harfe dönüştür
    lowercase_text = text.lower()

    # Verileri CSV dosyasına kaydet
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([filename, lowercase_text])

# Captcha oluşturma ve kaydetme
def generate_and_save_captcha():
    captcha_texts = read_captcha_text_from_file(text_file)
    captcha_text = random.choice(captcha_texts)

    captcha_text = generate_captcha_text(captcha_text)  # Büyük/küçük harf kombinasyonlarını oluştur

    font_path = get_random_font()
    font_size = 40  # Font boyutunu başlangıç değeri olarak belirle
    font = ImageFont.truetype(font_path, font_size)

    font_height = font.getsize('A')[1]
    text_width = font.getsize(captcha_text)[0]
    text_height = font_height + random.randint(0, 10)  # Yükseklik için rastgele bir değer ekle

    scale = min(image_width / text_width, image_height / text_height)  # Metni resim boyutuna sığdırmak için ölçek faktörü hesapla
    font_size = int(font_size * scale)  # Font boyutunu ölçeğe göre ayarla
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = font.getsize(captcha_text)  # Güncellenmiş metin boyutunu al

    image = generate_captcha_image(captcha_text, image_width, image_height, font_size, font)
    save_captcha_data(captcha_text, image)

# Örnek olarak 10 adet captcha oluşturup kaydediyoruz
for _ in tqdm(range(1000)):
    generate_and_save_captcha()
