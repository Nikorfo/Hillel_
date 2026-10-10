
import random
import threading
import time

files = ["photo.jpg", "document.pdf", "video.mp4", "archive.zip", "music.mp3"]

def download_file(file_name):
    print(f"Початок завантаження {file_name}...")
    time.sleep(random.randint(1, 4))
    print(f"Завершено: {file_name}")

print("--- Послідовне завантаження ---")
start = time.perf_counter()

for file in files:
    download_file(file)

sequential_time = time.perf_counter() - start
print(f"Загальний час (послідовно): {sequential_time} ")

print("--- Паралельне завантаження ---")
start = time.perf_counter()

threads = []
for file in files:
    thread = threading.Thread(target=download_file, args=(file,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

parallel_time = time.perf_counter() - start
print(f"Загальний час (паралельно): {parallel_time} ")

difference = sequential_time - parallel_time
print(f"Різниця: {difference} ")
print(f"Паралельне виконання швидше у {sequential_time / parallel_time} раза")