import subprocess
import os
import time

# record start time
start = time.time()

# Paths
source_path = os.getcwd()
compressed_path = os.path.join(source_path, "compressed")
files_path = os.path.join(source_path, "silesia")

# Full path to 7z.exe (غيره إذا 7-Zip عندك في مكان آخر)
seven_zip = r"C:\Program Files\7-Zip\7z.exe"

# Create compressed directory if it doesn't exist
os.makedirs(compressed_path, exist_ok=True)

# Check if files_path exists
if not os.path.exists(files_path):
    print(f"❌ Error: Source folder not found: {files_path}")
    exit(1)

# List files
dir_list = [f for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, f))]

print("Number of files to compress:", len(dir_list))
print("Files in:", files_path)
print(dir_list)

success_count = 0
error_count = 0

for sourceFile in dir_list:
    input_file = os.path.join(files_path, sourceFile)
    output_file = os.path.join(compressed_path, f"{sourceFile}_Compressed.7z")

    print("Compressing the file:", sourceFile)

    try:
        result = subprocess.run(
            [seven_zip, "a", "-bt", output_file, input_file, "-m0=LZMA"],
            capture_output=True, text=True, check=True
        )

        print(f"✓ Successfully compressed: {sourceFile}")
        success_count += 1

    except subprocess.CalledProcessError as e:
        print(f"✗ Process error compressing: {sourceFile}")
        print(f"Error: {e.stderr}")
        error_count += 1
    except FileNotFoundError:
        print(f"✗ Error: 7z.exe not found at {seven_zip}")
        break
    except Exception as e:
        print(f"✗ Unexpected error compressing: {sourceFile}")
        print(f"Error: {e}")
        error_count += 1

# record end time
end = time.time()
execution_time_ms = (end - start) * 1000
execution_time_sec = (end - start)

print("\n=== Compression Summary ===")
print(f"Successfully compressed: {success_count} files")
print(f"Errors: {error_count} files")
print(f"Total execution time: {execution_time_sec:.2f} seconds ({execution_time_ms:.2f} ms)")
