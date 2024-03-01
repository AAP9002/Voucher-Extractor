from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

make_images_2_col = True

def get_image_file_names(directory):
    image_file_names = []
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is an image file
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_file_names.append(filename)
    else:
        print(f"Directory '{directory}' does not exist.")
    
    return image_file_names

def create_stacked_images_pdf(image_paths, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)

    x_offset = 30  # Starting x-coordinate for the images
    y_offset = 770  # Starting y-coordinate for the images

    left = True
    for image_path in image_paths:
        img = Image.open(image_path)
        width, height = img.size
        aspect_ratio = width / height

        # Adjust width and height to fit within a 400x400 box
        if width > 400 or height > 400:
            if aspect_ratio > 1:
                width = 400
                height = int(width / aspect_ratio)
            else:
                height = 400
                width = int(height * aspect_ratio)

        # Draw image on canvas
        c.drawImage(image_path, x_offset, y_offset - height, width=width, height=height)
        y_offset -= (height + 20)  # Adjust y-coordinate for the next image

        # Add a new page if there's not enough space for the next image
        if y_offset <= 50:
            y_offset = 770
            if left and make_images_2_col:
                x_offset = 300
                left = False
            else:
                x_offset = 30
                left = True
                c.showPage()

    c.save()

if __name__ == "__main__":
    # Paths to the images
    directory = 'bin/image_temp'
    image_paths = [directory+"/"+x for x in get_image_file_names(directory)]
    # image_paths = ["bin/image_temp/0.png", "bin/image_temp/1.png", "bin/image_temp/2.png", "bin/image_temp/3.png", "bin/image_temp/4.png", "bin/image_temp/5.png"]  # Add your image paths here

    # Output PDF file
    output_pdf = "stacked_images.pdf"

    create_stacked_images_pdf(image_paths, output_pdf)
