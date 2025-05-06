import soundfile as sf
import os
from tqdm import tqdm
import librosa # Can use librosa too, might give different errors

def check_audio_file(file_path):
    """Tries to load an audio file and returns True if successful, False otherwise."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    try:
        # Option 1: Use soundfile directly (closer to the error source)
        data, samplerate = sf.read(file_path)
        # Check if data is empty (might indicate corrupt header but no data)
        if data is None or (hasattr(data, 'shape') and data.shape[0] == 0):
             print(f"Warning: File loaded but contains no data (empty): {file_path}")
             return False # Treat as bad file
        # Option 2: Use librosa (might catch different issues)
        # y, sr = librosa.load(file_path, sr=None)
        return True
    except sf.LibsndfileError as e:
        # Try to get a better error message if possible
        try:
             detailed_error = str(e)
        except:
             detailed_error = "<Could not get detailed error string>"
        print(f"LibsndfileError loading {file_path}: {detailed_error}")
        return False
    except Exception as e:
        print(f"Other error loading {file_path}: {type(e).__name__} - {e}")
        return False

# Paths to your file lists and root audio directory
train_list = "Data/train_list.txt"
val_list = "Data/val_list.txt"
root_path = "/Users/ronan/LSVSC-1000_24k"


bad_files = []
checked_files = 0

print("--- Checking Training Files ---")
if os.path.exists(train_list):
    with open(train_list, 'r', encoding='utf-8') as f:
        train_files = [line.strip().split('|')[0] for line in f if line.strip()]
    for rel_path in tqdm(train_files, desc="Checking train audio"):
        checked_files += 1
        abs_path = os.path.join(root_path, rel_path)
        if not check_audio_file(abs_path):
            bad_files.append(rel_path) # Store relative path
else:
    print(f"Train list not found at {train_list}")

print("\n--- Checking Validation Files ---")
if os.path.exists(val_list):
     with open(val_list, 'r', encoding='utf-8') as f:
        val_files = [line.strip().split('|')[0] for line in f if line.strip()]
     for rel_path in tqdm(val_files, desc="Checking val audio"):
        checked_files += 1
        abs_path = os.path.join(root_path, rel_path)
        if not check_audio_file(abs_path):
            bad_files.append(rel_path) # Store relative path
else:
     print(f"Validation list not found at {val_list}")


print(f"\nChecked {checked_files} files.")
if bad_files:
    print("\n--- Found Potentially Problematic Files ---")
    # Create sets for unique paths
    unique_bad_files = set(bad_files)
    print(f"Found {len(unique_bad_files)} unique problematic file paths:")
    for bf_rel in unique_bad_files:
        print(os.path.join(root_path, bf_rel)) # Print absolute path for easier inspection

    print("\nNext Steps:")
    print("1. Inspect these files: Check their size (are they 0 bytes?). Try downloading and playing them.")
    print("2. Remove corresponding lines: Edit train_list.txt and val_list.txt to remove the lines pointing to these bad relative paths.")
    print("3. (Optional) Try re-running the resampling/processing step for just the bad files if the original exists.")
else:
    print("\n--- All audio files in lists checked successfully ---")
    print("If the error persists, it might be related to the dataloader interacting with accelerate or a system library issue.")