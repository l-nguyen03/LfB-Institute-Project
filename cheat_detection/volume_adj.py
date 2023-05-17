import os
from pydub import AudioSegment
import shutil


def reduce_volume(input_dir, backup_dir, reduction_db):
    # Ensure the backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Go through each file in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a .wav file
        if filename.endswith('.wav'):
            # Backup the original file
            shutil.copy(os.path.join(input_dir, filename), backup_dir)
            # Load the .wav file
            audio = AudioSegment.from_wav(os.path.join(input_dir, filename))
            
            # Reduce the volume
            reduced_volume_audio = audio - reduction_db
            
            # Save the reduced volume audio to the backup directory
            reduced_volume_audio.export(os.path.join(input_dir, filename), format='wav')
            print(f"Processed file: {filename}")

# Usage
input_dir = '/Users/nptlinh/Desktop/LfB-Institute-Project/cheat_detection/dataset/Speech'
backup_dir = '/Users/nptlinh/Desktop/backup_dataset/Speech'
reduction_db = 5
reduce_volume(input_dir, backup_dir, reduction_db)
