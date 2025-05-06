import os
import sys

def get_phoneme_vocab(file_list_paths):
    """Calculates the unique phonemes from training/validation file lists."""
    phonemes = set()
    # --- Add known special tokens used by StyleTTS 2 ---
    # Check StyleTTS 2's text processing code/defaults for these. Common ones include:
    # '_' for padding, '^' for BOS (beginning), '$' for EOS (end), ' ' for space/word boundary
    special_tokens = ['_', '^', '$', ' '] # ASSUMED DEFAULTS - VERIFY!
    phonemes.update(special_tokens)
    # ---------------------------------------------------

    print("Calculating phoneme vocabulary...")
    for file_path in file_list_paths:
        if not os.path.exists(file_path):
            print(f"Warning: File list not found: {file_path}")
            continue
        print(f"Reading phonemes from: {file_path}")
        line_count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_count += 1
                try:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        # Split space-separated phonemes and add to set
                        current_phonemes = parts[1].split()
                        if not current_phonemes: # Handle empty phoneme strings if any
                             print(f"Warning: Empty phoneme string found in {file_path}, line {line_count}")
                        phonemes.update(current_phonemes)
                    else:
                        print(f"Warning: Malformed line in {file_path}, line {line_count}: {line.strip()}")
                except Exception as e:
                    print(f"Error processing line {line_count} in {file_path}: {line.strip()} - {e}")

    print(f"Found {len(phonemes)} unique phonemes/symbols (including assumed special tokens).")
    # Optional: Print the vocabulary to check
    # print("Vocabulary:", sorted(list(phonemes)))
    return phonemes

# Paths to your generated file lists
train_list = "train_list.txt"
val_list = "val_list.txt"

if not os.path.exists(train_list) or not os.path.exists(val_list):
     print("\nERROR: train_list.txt or val_list.txt not found. Please generate them first.", file=sys.stderr)
     n_symbols = "ERROR_FILE_LISTS_MISSING"
else:
    # Calculate vocabulary size
    vocab = get_phoneme_vocab([train_list, val_list])
    n_symbols = len(vocab)
    print(f"\n>>> Set 'n_token' in your config.yml to: {n_symbols}")

# Optional: Save the vocab to a file if needed by the training script (e.g., for token mapping)
# if isinstance(n_symbols, int):
#    vocab_file = "phoneme_vocab.txt"
#    try:
#        with open(vocab_file, "w", encoding="utf-8") as f:
#            for p in sorted(list(vocab)):
#                f.write(p + "\n")
#        print(f"Vocabulary saved to {vocab_file}")
#    except Exception as e:
#        print(f"Error saving vocabulary file: {e}")