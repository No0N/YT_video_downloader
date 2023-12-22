from pytube import YouTube

video_url = "https://youtu.be/SJs4x8pNZ4g?si=X0ZZInQ6RvccN1fY"
# video_url = "https://youtu.be/7PIji8OubXU?si=qSSiGYBCOb5GtJJ7"
# video_url = "https://youtu.be/T6E9_kF8j-U?si=HqFWGyph95EPnhE7"
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


for i in res_itag_part1:
    print(i)
print()    
for i in res_itag_part2:
    print(i)    
print()   
for i in res_itag_part3:
    print(i)
    
for i in streams:
    print(i)