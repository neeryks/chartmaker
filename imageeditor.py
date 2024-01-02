from PIL import Image, ImageDraw, ImageFont
from preset import presets,presets_size,presets_merge
import random
import time


def clean_crop(path,size,filename):
    img = Image.open(f"{path}{filename}")
    cropped_img = img.crop(presets_size(size)['crop_coords'])
    cropped_img.save(f"chartmaker/cropped-image/{filename}")

def add_chart_background(image_input, chartbg_color, image_output):
    # Open the original image
    original_image = Image.open(image_input)

    # Get the size of the original image
    width, height = original_image.size

    # Create a new image with the same size as the original image
    new_image = Image.new("RGB", (width, height))

    # Set the background color based on the chartbg_color parameter
    if chartbg_color.lower() == "white":
        background_color = (255, 255, 255)  # RGB for white
    elif chartbg_color.lower() == "black":
        background_color = (0, 0, 0)  # RGB for black
    elif chartbg_color.lower() == "complex":
        # For complex, add an image as the background
        background_image_path = "chartmaker/media/underlay.jpg"  # Replace with the actual path
        background_image = Image.open(background_image_path)

        # Get a random crop from the background image
        background_image = random_crop(background_image, width, height)

        # Paste the underlay image on top of the new image
        background_image.paste(original_image, (0, 0))
        background_image.save(image_output)
        time.sleep(1)
        return

    # Fill the new image with the selected background color
    new_image.paste(background_color, [0, 0, width, height])

    # Paste the original image on top of the background
    new_image.paste(original_image, (0, 0), original_image)

    # Save the final image
    new_image.save(image_output)
    time.sleep(1)

def random_crop(image, crop_width, crop_height):

    # Get the size of the original image
    width, height = image.size

    # Calculate random coordinates for the crop
    left = random.randint(0, max(0, width - crop_width))
    top = random.randint(0, max(0, height - crop_height))
    right = min(left + crop_width, width)
    bottom = min(top + crop_height, height)

    return image.crop((left, top, right, bottom))

def merge(poster_image_path, cropped_underlayed_path, output_path, position, poster_type):

    toberesized = Image.open(cropped_underlayed_path)
    resized = toberesized.resize(presets_merge(f"{poster_type}")['resize'])
    resized.save(cropped_underlayed_path)
    poster_image = Image.open(poster_image_path)
    cropped_underlayed = Image.open(cropped_underlayed_path)
    merged_image = Image.new("RGBA", poster_image.size, (255, 255, 255, 20))
    merged_image.paste(cropped_underlayed, position)
    merged_image.paste(poster_image, (0, 0), poster_image)
    
    merged_image.paste(poster_image, (0, 0), poster_image)
    merged_image.save(output_path, format="PNG")
    time.sleep(1)

def text_write(image_path, line_coord, place, title_text, datetime, font_color, output_path,size):
    # Open the existing image
    image = Image.open(image_path)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Set the font sizes and types
    title_font_size = 50
    regular_font_size = 16
    if size == "A3" or "DG":
        title_font_size = 70
        regular_font_size = 24
    

    title_font = ImageFont.truetype("chartmaker/media/ananda.ttf", title_font_size)
    regular_font = ImageFont.truetype("chartmaker/media/montlight.ttf", regular_font_size)
    
    # Calculate x-coordinates for centering
    title_text_x = (image.width - draw.textlength(title_text, font=title_font)) // 2
    place_text_x = (image.width - draw.textlength(f"STARS ABOVE {place.upper()}", font=regular_font)) // 2
    datetime_text_x = (image.width - draw.textlength(datetime, font=regular_font)) // 2
    
    # Write the text to the image with the specified font color
    draw.text((title_text_x, line_coord[0]), title_text, font=title_font, fill=font_color)
    draw.text((place_text_x, line_coord[1]), f"STARS ABOVE {place.upper()}", font=regular_font, fill=font_color)
    draw.text((datetime_text_x, line_coord[2]), datetime, font=regular_font, fill=font_color)
    
    # Save the final image
    image.save(output_path)



