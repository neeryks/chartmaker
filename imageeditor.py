from PIL import Image, ImageDraw, ImageFont

import random
import time


def clean_crop(path,coords,filename):
    img = Image.open(f"{path}/{filename}")
    cropped_img = img.crop(coords)
    cropped_img.save(f"cropped-image/{filename}")

def random_crop(image, target_width, target_height):
    # Ensure the background image is larger than the target size
    bg_width, bg_height = image.size
    if bg_width < target_width or bg_height < target_height:
        raise ValueError("Background image is smaller than the target size")

    # Calculate random crop position
    left = random.randint(0, bg_width - target_width)
    top = random.randint(0, bg_height - target_height)
    
    # Crop the image
    return image.crop((left, top, left + target_width, top + target_height))

def add_chart_background(image_input, image_output, background_image=None):
    # Open the original image
    original_image = Image.open(image_input).convert("RGBA")
    
    # Get the size of the original image
    width, height = original_image.size
    
    # Open the background image if provided, otherwise create a default one
    
    if background_image:
        background = Image.open(background_image).convert("RGBA")
        background = background.resize((width, height))

    else:
        background = Image.new("RGBA", (width, height), (0, 0, 0, 255))  # Create a solid black image
    
    # Combine the images
    combined_image = Image.new('RGBA', (width, height))
    combined_image.paste(background, (0, 0))
    combined_image.paste(original_image, (0, 0), mask=original_image)
    
    # Create a circular mask to ensure the outside of the circle is transparent
    final_mask = Image.new('L', (width, height), 0)  # 0 means black, fully transparent
    draw = ImageDraw.Draw(final_mask)
    draw.ellipse((0, 0, width, width), fill=255)  # 255 means white, fully opaque
    
    # Apply the final mask to the combined image
    final_image = Image.new('RGBA', (width, height))
    final_image.paste(combined_image, (0, 0), mask=final_mask)
    
    # Save the result
    final_image.save(image_output)
    time.sleep(1)

from PIL import Image
import time

def merge(poster_image_path, cropped_underlayed_path, output_path, resize, position, background_image_path=None):
    toberesized = Image.open(cropped_underlayed_path)
    resized = toberesized.resize(resize)
    resized.save(cropped_underlayed_path)

    poster_image = Image.open(poster_image_path)
    cropped_underlayed = Image.open(cropped_underlayed_path)

    # Check if a background image is provided
    if background_image_path:
        background_image = Image.open(background_image_path)
        background_image = background_image.resize(poster_image.size)
    else:
        background_image = Image.new("RGBA", poster_image.size, (255, 255, 255, 0))

    # Paste the cropped underlayed image on the background
    background_image.paste(cropped_underlayed, position, cropped_underlayed)
    
    # Paste the poster image on top
    background_image.paste(poster_image, (0, 0), poster_image)
    
    # Save the final merged image
    background_image.save(output_path, format="PNG")
    time.sleep(1)


def text_write(image_path, line_coord, place, title_text, date,time, font_color, output_path,size):
    # Open the existing image
    image = Image.open(image_path)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Set the font sizes and types
    title_font_size = 50
    regular_font_size = 16
    if size == "A3" or "DG" or "A4":
        title_font_size = 220
        regular_font_size = 100
    

    title_font = ImageFont.truetype("media/ananda.ttf", title_font_size)
    regular_font = ImageFont.truetype("media/montlight.ttf", regular_font_size)
    
    # Calculate x-coordinates for centering
    title_text_x = (image.width - draw.textlength(title_text, font=title_font)) // 2
    place_text_x = (image.width - draw.textlength(f"STARS ABOVE {place.upper()}", font=regular_font)) // 2
    date_text_x = (image.width - draw.textlength(date, font=regular_font)) // 2
    time_text_x = (image.width - draw.textlength(time[0:-3], font=regular_font)) // 2
    
    # Write the text to the image with the specified font color
    draw.text((title_text_x, line_coord[0]), title_text, font=title_font, fill=font_color)
    draw.text((place_text_x, line_coord[1]), f"STARS ABOVE {place.upper()}", font=regular_font, fill=font_color)
    draw.text((date_text_x, line_coord[2]), "-".join(date.split("-")[::-1]), font=regular_font, fill=font_color)
    draw.text((time_text_x, line_coord[3]), time[0:-3], font=regular_font, fill=font_color)
    
    # Save the final image
    image.save(output_path)



