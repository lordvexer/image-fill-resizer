import cv2
import numpy as np
import os
from tkinter import Tk, filedialog

def proportional_resize(image, target_width, target_height):
    original_height, original_width = image.shape[:2]
    aspect_ratio_original = original_width / original_height
    aspect_ratio_target = target_width / target_height
    
    if aspect_ratio_original > aspect_ratio_target:
        new_width = target_width
        new_height = int(target_width / aspect_ratio_original)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio_original)
    
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image

def resize_with_padding(image, target_width, target_height, padding_color=(0, 0, 0)):
    original_height, original_width = image.shape[:2]
    aspect_ratio_original = original_width / original_height
    aspect_ratio_target = target_width / target_height
    
    if aspect_ratio_original > aspect_ratio_target:
        new_width = target_width
        new_height = int(target_width / aspect_ratio_original)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio_original)
    
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    padded_image = np.full((target_height, target_width, 3), padding_color, dtype=np.uint8)
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    
    padded_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image
    return padded_image

def process_images_in_folder(input_folder, output_folder, target_width, target_height, compression_percent, method='padding', padding_color=(0, 0, 0)):
    os.makedirs(output_folder, exist_ok=True)
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            image = cv2.imread(input_path)
            
            if method == 'resize':
                processed_image = proportional_resize(image, target_width, target_height)
            elif method == 'padding':
                processed_image = resize_with_padding(image, target_width, target_height, padding_color)
            else:
                raise ValueError("Method must be either 'resize' or 'padding'")
            
            # Handle compression based on image format
            if filename.lower().endswith(('.jpg', '.jpeg')):
                compression_params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_percent)]
            elif filename.lower().endswith('.png'):
                compression_params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_percent / 10)]
            else:
                compression_params = []  # WebP and others can be handled similarly if needed
            
            cv2.imwrite(output_path, processed_image, compression_params)
            print(f"Processed and saved: {output_path} with {compression_percent}% compression")

def select_folder(title):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=title)
    root.destroy()
    return folder_selected

def get_size_input(prompt):
    while True:
        try:
            size = int(input(prompt))
            if size > 0:
                return size
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def get_compression_input(prompt):
    while True:
        try:
            compression = int(input(prompt))
            if 0 < compression <= 100:
                return compression
            else:
                print("Please enter an integer between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 100.")

# Get input and output folders from the user
input_folder = select_folder("Select the input folder containing images")
output_folder = select_folder("Select the output folder to save processed images")

# Get the target width, height, and compression percentage from the user
target_width = get_size_input("Enter the target width: ")
target_height = get_size_input("Enter the target height: ")
compression_percent = get_compression_input("Enter the compression percentage (1-100): ")

# Define method and padding color
method = 'padding'  # Choose 'resize' for proportional resize, 'padding' for resize with padding
padding_color = (255, 255, 255)  # White padding for 'padding' method

# Process all images in the selected input folder
process_images_in_folder(input_folder, output_folder, target_width, target_height, compression_percent, method, padding_color)
