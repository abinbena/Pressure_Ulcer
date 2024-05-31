# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UaeNrzivDqgv3db7BKeuYm2foxaHQPpg
"""

import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import picamera
import keyboard

# Load the TFLite model
interpreter = tflite.Interpreter(model_path="efficientnet_b0.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define a function to capture and process an image
def capture_and_process_image():
    # Initialize the Raspberry Pi camera
    camera = picamera.PiCamera()
    # Set camera resolution (optional)
    camera.resolution = (224, 224)
    # Capture an image from the camera
    camera.capture("input_image.jpg")
    # Close the camera
    camera.close()

    # Load and preprocess the input image
    input_image = Image.open("input_image.jpg").resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
    input_data = np.expand_dims(input_image, axis=0)
    input_data = input_data / 255.0  # Normalize the input

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Decode the prediction (assuming ImageNet labels)
    # You may need to modify this depending on the model's output format
    with open("imagenet_labels.txt", "r") as f:
        labels = f.read().splitlines()

    predicted_class_index = np.argmax(output_data)
    predicted_label = labels[predicted_class_index]
    print("Predicted class:", predicted_label)

# Register the callback function for key press event
def on_key_press(event):
    if event.name == 'h':
        print("Taking picture...")
        capture_and_process_image()
        print("Picture taken and processed successfully!")

# Register the callback function for key press event
keyboard.on_press(on_key_press)

# Keep the script running
keyboard.wait('esc')