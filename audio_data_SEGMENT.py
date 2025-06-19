#!/bin/env/python3

import os
from pydub import AudioSegment

# Define paths
input_dir = "/kaggle/input/bc2-ttv/BC2_TTV"                  # Input the directory
output_dir = "/kaggle/working/segmented_BC2_TTV"             # Input the output directory

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Segmentation parameter
segment_duration_ms = 2000                                   # Segment duration in milliseconds (2 seconds) and can be varied

def fixed_time_segmentation(audio_path, output_path, segment_duration_ms):
    try:
        audio = AudioSegment.from_wav(audio_path)
        total_duration_ms = len(audio)
        num_segments = int(total_duration_ms / segment_duration_ms) + (1 if total_duration_ms % segment_duration_ms > 0 else 0)
        
        for i in range(num_segments):
            start_ms = i * segment_duration_ms
            end_ms = min(start_ms + segment_duration_ms, total_duration_ms)
            segment = audio[start_ms:end_ms]
            segment_file = f"{output_path}_segment_{i+1}.wav"
            segment.export(segment_file, format="wav")
            print(f"Saved segment: {segment_file}")
    except Exception as e:
        print(f"Error processing {audio_path}: {str(e)}")

def process_directory(input_root, output_root):
    for root, dirs, files in os.walk(input_root):
        relative_path = os.path.relpath(root, input_root)
        current_output_dir = os.path.join(output_root, relative_path)
        if not os.path.exists(current_output_dir):
            os.makedirs(current_output_dir)
        
        # Process each .wav file in the current directory
        for file_name in files:
            if file_name.endswith(".wav"):
                audio_path = os.path.join(root, file_name)
                base_name = os.path.splitext(file_name)[0]
                output_path = os.path.join(current_output_dir, base_name)
                fixed_time_segmentation(audio_path, output_path, segment_duration_ms)

process_directory(input_dir, output_dir)
print("Segmentation completed!")
