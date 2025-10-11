import subprocess
import os
import time
import threading

# Record start time
start = time.time()

# -------------------------------
# 🔧 Set the number of threads manually here
threads_num = 4  # ← change this number to use more or fewer threads
# -------------------------------

threads_list = []
seven_zip = r"C:\Program Files\7-Zip\7z.exe"  # Full path to 7z.exe

def thread_function(name, start_index, files_to_process, dir_list, compressed_path):
    print(f"Thread {name} starting compression...")
    for xi in range(start_index, start_index + files_to_process):
        x = dir_list[xi]
        input_file = os.path.join(source_path, "silesia", x)
        output_file = os.path.join(compressed_path, f"{x}.7z")

        print(f"Thread {name} compress => {x}")
        result = subprocess.run(
            [seven_zip, "a", "-bt", output_file, input_file, "-m0=LZMA"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error compressing {x}: {result.stderr}")
    print(f"Thread {name} finished compression.")

# Paths
source_path = os.getcwd()
compressed_path = os.path.join(source_path, "compressed")
os.makedirs(compressed_path, exist_ok=True)

# Get list of files in /silesia
dir_list = os.listdir(os.path.join(source_path, "silesia"))
list_len = len(dir_list)

# Ensure not more threads than files
threads_num = min(threads_num, list_len)
files_per_thread = max(1, list_len // threads_num)

print(f"Using {threads_num} threads")
print("list_len =", list_len, "files_per_thread =", files_per_thread)
print("Files:", dir_list)

# Create and start threads
for i in range(threads_num):
    start_index = i * files_per_thread
    if i == threads_num - 1:
        files_to_process = list_len - start_index  # last thread takes the rest
    else:
        files_to_process = files_per_thread

    thread = threading.Thread(
        target=thread_function,
        args=(i, start_index, files_to_process, dir_list, compressed_path)
    )
    threads_list.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads_list:
    thread.join()

# Print execution time
end = time.time()
print("Execution time:", round(end - start, 2), "seconds")
