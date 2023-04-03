import cv2
import numpy as np
import time
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from pydub import AudioSegment

# задаем параметры звуковой дорожки
sample_rate = 44100  # частота дискретизации
duration = 10  # длительность в секундах

# создаем синусоидальный сигнал
frequency = 440  # частота сигнала в герцах
amplitude = 10000  # амплитуда сигнала
time_array = np.arange(0, duration, 1/sample_rate)
signal = (amplitude * np.sin(2*np.pi*frequency*time_array)).astype(np.int16)

# экспортируем сигнал в файл
audio = AudioSegment(signal.tobytes(), frame_rate=sample_rate, sample_width=signal.dtype.itemsize, channels=1)
audio.export("sound.wav", format="wav")

# задаем параметры анимации
animation_length = 10  # длительность анимации в секундах
fps = 60  # количество кадров в секунду
circle_radius = 128+64  # радиус круга
circle_center = (0, int(2160/2))  # координаты центра круга
circle_speed = 3840/animation_length  # скорость движения круга в пикселях в секунду

# создаем видеоврайтер для сохранения видео в файл
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter("animation.mp4", fourcc, fps, (3840, 2160))

# создаем звуковую дорожку
audio_clip = AudioFileClip("sound.wav")

# создаем цикл анимации
frame_count = int(animation_length * fps)
start_time = time.time() # время начала анимации
for i in range(frame_count):
    # вычисляем новые координаты круга
    t = i / fps
    circle_x = int(circle_center[0] + t * circle_speed)
    circle_y = circle_center[1]

    # создаем новый кадр анимации
    frame = np.zeros((2160, 3840, 3), dtype=np.uint8) + 255  # белый фон
    cv2.circle(frame, (circle_x, circle_y), circle_radius, (0, 0, 255), -1)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)  # сглаживание круга

    # записываем кадр в видео
    video_writer.write(frame)
    
    # выводим прогресс выполнения в консоль
    progress = (i + 1) / frame_count * 100
    elapsed_time = time.time() - start_time
    remaining_time = elapsed_time / progress * (100 - progress)
    print(f"Прогрресс: {progress:.2f}%, Осталось времени: {remaining_time:.2f} секунд")
video_writer.release()
video_clip = VideoFileClip("animation.mp4")
final_clip = video_clip.set_audio(CompositeAudioClip([audio_clip]))
final_clip.write_videofile("animation_with_sound.mp4")

# os.remove("sound.wav")

print("Готово!")