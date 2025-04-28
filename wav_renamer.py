import os
import re
import whisper
import tkinter as tk
from tkinter import filedialog, simpledialog

# Load Whisper model once
model = whisper.load_model("small")

def transcribe_first_words(file_path, num_words=6):
    result = model.transcribe(file_path, fp16=False)
    text = result["text"].strip()
    words = text.split()
    selected_words = words[:num_words]
    title = "_".join(selected_words)
    title = re.sub(r'[^a-zA-Z0-9_]', '', title)  # clean title
    return title

def pick_folder_and_rename():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    folder_selected = filedialog.askdirectory(title="Select Folder with WAV files")
    if not folder_selected:
        print("No folder selected.")
        return

    # Ask if files should be marked as Final or Draft
    choice = simpledialog.askstring(
        "Naming Style",
        "Type 'final' or 'draft' to mark the files:",
    )

    if not choice or choice.lower() not in ["final", "draft"]:
        print("Invalid choice. Exiting.")
        return

    suffix = f"_{choice.lower()}"

    for filename in os.listdir(folder_selected):
        if filename.lower().endswith(".wav"):
            file_path = os.path.join(folder_selected, filename)
            print(f"Processing {filename}...")
            try:
                new_name = transcribe_first_words(file_path)
                new_filename = new_name + suffix + ".wav"
                new_path = os.path.join(folder_selected, new_filename)
                os.rename(file_path, new_path)
                print(f"Renamed to {new_filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    pick_folder_and_rename()
