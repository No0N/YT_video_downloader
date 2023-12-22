from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import sys

def download_video_and_audio(video_url, output_path):

    yt = YouTube(video_url)

# Исходный список
    streams = yt.streams

# Разбивка yt.streams на 3 списка
    part1 = [stream for stream in streams if stream.is_progressive]
    target_vcodecs = ["mp4v.20.3", "avc1.42001E", "avc1.64001F", "avc1.640028", "vp9", "vp9.2"]
    target_acodecs = ["mp4a.40.2"]

    part1_resolutions = set(stream.resolution for stream in part1)
# Выборка part2 исключая значения, которые уже есть в part1 с тем же разрешением
    part2 = [stream for stream in streams if stream.video_codec in target_vcodecs and stream.mime_type == "video/webm" and stream not in part1 and stream.fps == 60 and stream.resolution not in part1_resolutions]
    if not part2:
        part2 = [stream for stream in streams if stream.video_codec in target_vcodecs and stream.mime_type == "video/webm" and stream not in part1 and stream.fps == 30 and stream.resolution not in part1_resolutions]
    if not part2:
        part2 = [stream for stream in streams if stream.video_codec in target_vcodecs and stream.mime_type == "video/mp4" and stream not in part1 and stream.fps == 30 and stream.resolution not in part1_resolutions]    
    if not part2:
        part2 = [stream for stream in streams if stream.video_codec in target_vcodecs and stream.mime_type == "video/webm" and stream not in part1 and stream.fps == 25 and stream.resolution not in part1_resolutions]
    if not part2:
        part2 = [stream for stream in streams if stream.video_codec in target_vcodecs and stream.mime_type == "video/mp4" and stream not in part1 and stream.fps == 25 and stream.resolution not in part1_resolutions]


    part3 = [stream for stream in streams if stream.audio_codec in target_acodecs and stream not in part1 and stream not in part2 and stream.type in "audio"]

# Выборка из полученных списков только значений res:itag если res==NONE заменяем на abr (bitrate)
    res_itag_part1 = [f"{stream.resolution}:{stream.itag}" if stream.resolution else f"{stream.abr}:{stream.itag}" for stream in part1]
    res_itag_part2 = [f"{stream.resolution}:{stream.itag}" if stream.resolution else f"{stream.abr}:{stream.itag}" for stream in part2]
    res_itag_part3 = [f"{stream.resolution}:{stream.itag}" if stream.resolution else f"{stream.abr}:{stream.itag}" for stream in part3]

# Выполним сортировку в полученных списках от меньшего к большему с учётом что значение может быть не только int
    def sorted_key_func(x):
        try:
            resolution = int(x.split(":")[0].replace("p", ""))
        except ValueError:
            resolution = float('inf')
        return (resolution, x)

    res_itag_part1 = sorted(res_itag_part1, key=sorted_key_func)
    res_itag_part2 = sorted(res_itag_part2, key=sorted_key_func)
    res_itag_part3 = sorted(res_itag_part3, key=sorted_key_func)
    
    #Блок для контроля присвоения номера индекса к качеству потока
    for i in res_itag_part1:
        print(i)
    print()    
    for i in res_itag_part2:
        print(i)    
    print()   
    for i in res_itag_part3:
        print(i)
        
    combined_res_itag_dict = {}
    for index, item in enumerate(res_itag_part1):
        combined_res_itag_dict[item.split(":")[1]] = item
    for index, item in enumerate(res_itag_part2, start=len(res_itag_part1)):
        combined_res_itag_dict[item.split(":")[1]] = item
    for index, (itag, stream_info) in enumerate(combined_res_itag_dict.items()):
        video_info = stream_info.split(":")[0]
        list_number = 1 if index < len(res_itag_part1) else 2
        print(f"{index + 1}. {video_info}")
       
    # Выводим доступные видео стримы пользователю    
    try:
        selected_index = int(input("Введите номер выбранного видео стрима: ")) - 1
    except ValueError:
        print("Ошибка: введено некорректное значение. Введите число.")
        # Можно в этом месте принять решение, как обработать ошибку (возможно, запросить ввод снова или завершить программу).
        sys.exit(1)  # Выход с кодом ошибки
        
    selected_itag = list(combined_res_itag_dict.keys())[selected_index]
    selected_stream = yt.streams.get_by_itag(selected_itag)


    # Получаем выбранный itag и сохраняем его в переменную chosen_itag
    chosen_itag = selected_stream.itag
    chosen_list = list_number

    print(chosen_itag)
    print(chosen_list)

    # СТОПОР для отладки функционала выборки стрима video и audio 
    input()

    # Скачиваем видео в выбранном разрешении без аудио
    video = yt.streams.get_by_itag(chosen_itag)
    video.download(output_path, filename="video")
    print("Video - DONE")

    # Если выбран видео стрим из списка 1, то пропускаем скачивание аудио
    if chosen_list == 1:
        print("Выбран видео стрим из списка 1. Пропускаем скачивание аудио.")
    else:
        # Если выбран видео стрим из списка 2, то скачиваем аудио
        audio = yt.streams.get_audio_only()
        audio.download(output_path, filename="audio")
        print("Audio - DONE")


def merge_video_and_audio(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

# Соединяем видео и аудио
    video_clip = video_clip.set_audio(audio_clip)

# Экспортируем результат
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("Слияние завершено.")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=T6E9_kF8j-U"
    output_path = f"download/{YouTube(video_url).title}"
    
    download_video_and_audio(video_url, output_path)

    video_path = os.path.join(output_path, "video")
    audio_path = os.path.join(output_path, "audio")
    output_video_path = os.path.join(output_path, "output.mp4")

    merge_video_and_audio(video_path, audio_path, output_video_path)