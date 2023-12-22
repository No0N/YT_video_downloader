
# Отфильтровываем разрешения, удовлетворяющие критериям
    valid_resolutions = []
    target_codecs = ["mp4v.20.3", "avc1.42001E", "avc1.64001F", "avc1.640028", "vp9"]
    existing_resolutions = set()

    for stream in yt.streams:
        if stream.includes_video_track and stream.video_codec in target_codecs and "video" in stream.mime_type:
            if stream.video_codec == "vp9" and stream.resolution in existing_resolutions:
                continue  # Пропускаем разрешения для vp9.2, которые уже в списке
            valid_resolutions.append(stream.resolution)
            existing_resolutions.add(stream.resolution)

# Выводим отфильтрованные разрешения с нумерацией
    print("Доступные разрешения:")
    for i, resolution in enumerate(valid_resolutions, start=1):
        print(f"{i}. {resolution}")

# Пользователь выбирает разрешение
    while True:
        try:
            choice = int(input("Выберите номер разрешения: "))
            if 1 <= choice <= len(valid_resolutions):
                target_video_res = valid_resolutions[choice - 1]
                break
            else:
                print("Неверный выбор. Пожалуйста, введите корректный номер.")
        except ValueError:
            print("Введите число.")


    print(stream)
    input("Останов")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ДАЛЬШЕ ОШИБКА ВЫБОРА может быть video/mp4 а может быть video/webm

    # Ищем нужный поток
    target_video_mime_type = "video/mp4"
    selected_video_stream = None
    for stream in yt.streams:
        if stream.resolution == target_video_res and stream.mime_type == target_video_mime_type:
            selected_video_stream = stream
            break