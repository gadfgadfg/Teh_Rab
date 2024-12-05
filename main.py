import os
from PIL import Image, ImageDraw, ImageFont, ImageOps


def get_image_selection(image_folder, allowed_extensions):

    images = [f for f in os.listdir(image_folder) if f.lower().endswith(allowed_extensions)]

    if not images:
        print("Ошибка: В указанной папке нет изображений с выбранными расширениями.")
        return []

    print("Доступные изображения:")
    for i, image_name in enumerate(images):
        print(f"{i + 1}: {image_name}")

    selected_images = []
    while True:
        user_input = input(
            "Введите номера изображений, которые вы хотите выбрать (через запятую), или 'q' для завершения: ")
        if user_input.lower() == 'q':
            break
        try:
            indices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_images = [images[i] for i in indices if 0 <= i < len(images)]
            if selected_images:
                print("Выбранные изображения:", selected_images)
            else:
                print("Не выбрано ни одного изображения.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, попробуйте снова.")

    return selected_images


def generate_collage(image_folder, selected_images, collage_title, output_file, img_size=(200, 200), border=10):

    if not selected_images:
        print("Ошибка: Не выбрано ни одного изображения для коллажа.")
        return

    try:
        title_font = ImageFont.truetype("Arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()

    n_images = len(selected_images)
    grid_size = int(n_images ** 0.5) + 1
    collage_width = grid_size * (img_size[0] + border) - border
    collage_height = collage_width + 50

    collage = Image.new('RGB', (collage_width, collage_height), color=(220, 220, 220))

    x_offset = 0
    y_offset = 50

    for i, image_name in enumerate(selected_images):
        img_path = os.path.join(image_folder, image_name)
        img = Image.open(img_path)
        img = ImageOps.fit(img, img_size, method=Image.LANCZOS)

        collage.paste((0, 0, 0), (x_offset, y_offset, x_offset + img_size[0] + border, y_offset + img_size[1] + border))
        collage.paste(img, (x_offset + border // 2, y_offset + border // 2))

        x_offset += img_size[0] + border
        if (i + 1) % grid_size == 0:
            x_offset = 0
            y_offset += img_size[1] + border

    draw = ImageDraw.Draw(collage)
    title_bbox = draw.textbbox((0, 0), collage_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    draw.text(((collage_width - title_width) // 2, 10), collage_title, font=title_font, fill=(0, 0, 0))

    collage.save(output_file, 'JPEG')
    print(f"Коллаж сохранен как '{output_file}'")

image_folder_path = input("Введите путь к папке с изображениями: ")
allowed_extensions_input = input("Введите разрешенные расширения изображения (например, jpg, png), разделенные запятыми: ")
allowed_extensions = tuple('.' + ext.strip().lower() for ext in allowed_extensions_input.split(','))

collage_title_text = input("Введите заголовок для коллажа: ")
output_file_name = input("Введите путь для сохранения коллажа (например, C:\\Foto\\collage.jpg): ")

selected_images = get_image_selection(image_folder_path, allowed_extensions)

generate_collage(image_folder_path, selected_images, collage_title_text, output_file_name)