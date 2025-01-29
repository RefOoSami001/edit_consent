import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image
import numpy as np
from io import BytesIO
import random
import os
from datetime import datetime, timedelta

def generate_random_past_and_future_dates():
    """
    Generates a random past date (within the last year) and a random future date (within the next year).
    
    :return: A tuple containing (past_date, future_date) in the format dd-mm-yyyy.
    """
    # Get the current date
    current_date = datetime.now()

    # Generate a random future date within the next year
    future_date = current_date + timedelta(days=random.randint(1, 365))  # Random days between 1 and 365
    future_date_formatted = future_date.strftime("%d-%m-%Y")

    return future_date_formatted

def generate_random_arabic_date():
    """
    Generates a random date in the past one or one and a half years and returns the day and date in Arabic.
    
    :return: A tuple containing (day_in_arabic, date_in_format_dd_mm_yyyy).
    """
    # Define Arabic days of the week
    arabic_days = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

    # Get the current date
    current_date = datetime.now()

    # Calculate the range for the past one or one and a half years
    one_year_ago = current_date - timedelta(days=365)
    one_and_half_years_ago = current_date - timedelta(days=547)  # 1.5 years ≈ 547 days

    # Generate a random date within the range
    random_days = random.randint(0, 547)  # Random days between 0 and 547
    random_date = current_date - timedelta(days=random_days)

    # Format the date as dd-mm-yyyy
    formatted_date = random_date.strftime("%d-%m-%Y")

    # Get the day of the week in Arabic
    day_of_week = random_date.weekday()  # Monday is 0, Sunday is 6
    day_in_arabic = arabic_days[day_of_week]

    return day_in_arabic, formatted_date

def add_arabic_text_to_image(ax, text, x, y, font_path, font_size, text_color, letter_spacing=None, alpha=1.0, noise=False):
    """
    Adds Arabic text to an image at specified coordinates with optional letter spacing and noise effect.
    """
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    font_prop = font_manager.FontProperties(fname=font_path, size=font_size)

    if noise:
        for _ in range(10):
            noise_alpha = alpha * np.random.uniform(0.3, 0.6)
            noise_x_offset = x + np.random.uniform(-1, 1)
            noise_y_offset = y + np.random.uniform(-1, 1)
            ax.text(
                x=noise_x_offset, y=noise_y_offset, s=bidi_text,
                fontproperties=font_prop, color=text_color,
                alpha=noise_alpha, zorder=-1,
            )

    if letter_spacing is not None:
        x_offset = x
        for char in bidi_text:
            ax.text(
                x=x_offset, y=y, s=char,
                fontproperties=font_prop, color=text_color,
                alpha=alpha,
            )
            x_offset += letter_spacing
    else:
        ax.text(
            x=x, y=y, s=bidi_text,
            fontproperties=font_prop, color=text_color,
            alpha=alpha,
        )

    return ax

def overlay_image(base_image, overlay_image_path, position, size):
    """
    Overlays an image on top of the base image at the specified position and size.
    """
    overlay_image = Image.open(overlay_image_path).convert("RGBA")
    overlay_image = overlay_image.resize(size)
    base_image = base_image.copy().convert("RGBA")
    base_image.paste(overlay_image, position, overlay_image)
    return base_image

def generate_image_1(base_image_path, serial, owner, sales_name, nationality, idNo, phone, landline, central, quota, price, payment_frequency, date):
    """
    Generates the first image with Arabic text overlaid.
    """
    # Format the date
    day, month, year = date.split("-")
    formatted_date = f"{day}    {int(month)}    {year}"

    # Generate the first image
    text_elements = [
        {"text": serial, "x": 740, "y": 390, "font_path": "Arimo-VariableFont_wght.ttf", 
         "font_size": 6, "text_color": "#740022", "alpha": 1, "noise": True},
        {"text": owner, "x": 550, "y": 550, "font_path": "Dima Font.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": owner, "x": 325, "y": 700, "font_path": "Dima Font.ttf", 
         "font_size": 4, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": owner, "x": 340, "y": 760, "font_path": "alfont_com_Digi-Maryam-Regular.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": sales_name, "x": 150, "y": 700, "font_path": "Dima Font.ttf", 
         "font_size": 4, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": sales_name, "x": 140, "y": 755, "font_path": "alfont_com_Digi-Maryam-Regular.ttf", 
         "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": nationality, "x": 790, "y": 590, "font_path": "Dima Font.ttf", 
         "font_size": 5.5, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": idNo, "x": 630, "y": 748, "font_path": "Molhim.ttf", 
         "font_size": 5.9, "text_color": "#140a72", "alpha": 1, "noise": True, "letter_spacing": 21},
        {"text": phone, "x": 550, "y": 960, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": phone, "x": 680, "y": 1400, "font_path": "Molhim.ttf", 
         "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": landline, "x": 870, "y": 975, "font_path": "Molhim.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": landline, "x": 160, "y": 390, "font_path": "Molhim.ttf", 
         "font_size": 8.5, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": landline, "x": 680, "y": 1220, "font_path": "Molhim.ttf", 
         "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": central, "x": 720, "y": 1350, "font_path": "Dima Font.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": quota, "x": 420, "y": 560, "font_path": "Caveat-Regular.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": price, "x": 320, "y": 560, "font_path": "Caveat-Regular.ttf", 
         "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": formatted_date, "x": 375, "y": 800, "font_path": "Molhim.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": True},
        {"text": formatted_date, "x": 155, "y": 795, "font_path": "Molhim.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": True},
    ]

    # Add '/' based on payment frequency selection
    if payment_frequency == "month":
        text_elements.append({"text": "/", "x": 400, "y": 610, "font_path": "Dima Font.ttf","font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True})
    elif payment_frequency == "6_months":
        text_elements.append({"text": "/", "x": 335, "y": 610, "font_path": "Dima Font.ttf", "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True})
    elif payment_frequency == "12_months":
        text_elements.append({"text": "/", "x": 250, "y": 610, "font_path": "Dima Font.ttf", "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": True})

    image = Image.open(base_image_path)

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.imshow(image)

    # Add all text elements to the image
    for element in text_elements:
        ax = add_arabic_text_to_image(ax, **element)

    # Hide axes
    ax.axis("off")

    # Save the image to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg', bbox_inches="tight", pad_inches=0, dpi=300)
    img_buffer.seek(0)
    plt.close('all')  # Close all figures to free up memory

    return img_buffer

# The image generation function remains mostly the same but with changes for handling buffers
def generate_image_2(base_image_path, stamp_image_path, front_id_buffer, back_id_buffer, owner, central, date, landline):
    """
    Generates the second image with overlays and text.
    """
    # Open the base image
    base_image = Image.open(base_image_path).convert("RGBA")

    # Overlay stamp image
    base_image = overlay_image(base_image, stamp_image_path, (1900, 2100), (600, 290))

    # Overlay front ID image (from BytesIO buffer)
    base_image = overlay_image(base_image, front_id_buffer, (250, 2500), (1000, 700))

    # Overlay back ID image (from BytesIO buffer)
    base_image = overlay_image(base_image, back_id_buffer, (1400, 2500), (1000, 700))

    # Format the date: single-digit month and two spaces between day, month, and year
    day, month, year = date.split("-")
    formatted_date = f"{day}    {int(month)}    {year}"  # Convert month to int to remove leading zero

    # Define text elements
    text_elements = [
        {"text": formatted_date, "x": 1970, "y": 900, "font_path": "Molhim.ttf", "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": owner, "x": 1430, "y": 1360, "font_path": "Dima Font.ttf", "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": central, "x": 1520, "y": 1510, "font_path": "Dima Font.ttf", "font_size": 6.2, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": landline, "x": 300, "y": 1370, "font_path": "Molhim.ttf", "font_size": 8.5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": landline, "x": 1020, "y": 2160, "font_path": "Molhim.ttf", "font_size": 10, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": owner, "x": 170, "y": 2180, "font_path": "alfont_com_Digi-Maryam-Regular.ttf", "font_size": 9, "text_color": "#140a72", "alpha": 1, "noise": False},
    ]

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.imshow(base_image)

    # Add all text elements to the image
    for element in text_elements:
        ax = add_arabic_text_to_image(ax, **element)

    # Hide axes
    ax.axis("off")

    # Save the image to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg', bbox_inches="tight", pad_inches=0, dpi=300)
    img_buffer.seek(0)
    plt.close('all')  # Close all figures to free up memory

    # Convert the BytesIO object to a PIL image
    final_image = Image.open(img_buffer)

    # Save the final image to a new BytesIO object
    final_buffer = BytesIO()
    final_image.save(final_buffer, format='JPEG')
    final_buffer.seek(0)

    return final_buffer

def generate_image_3(base_image_path, owner, renter_name):
    """
    Generates the third image with Arabic text overlaid.
    """
    day, date = generate_random_arabic_date()
    day_, month, year = date.split("-")
    
    future_date = generate_random_past_and_future_dates()
    future_day, future_month, future_year = future_date.split('-')

    # Generate the first image
    text_elements = [
        {"text": day, "x": 480, "y": 142, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": day_, "x": 375, "y": 142, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": month, "x": 320, "y": 142, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": year, "x": 230, "y": 142, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": renter_name, "x": 440, "y": 172, "font_path": "Dima Font.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": renter_name, "x": 1130, "y": 495, "font_path": "Dima Font.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": renter_name, "x": 1130, "y": 455, "font_path": "Molhim.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": owner, "x": 840, "y": 455, "font_path": "Molhim.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": owner, "x": 840, "y": 495, "font_path": "Dima Font.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": owner, "x": 440, "y": 225, "font_path": "Dima Font.ttf", 
         "font_size": 5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "جمهورية مصر العربية", "x": 180, "y": 172, "font_path": "Dima Font.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "جمهورية مصر العربية", "x": 160, "y": 229, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": day_, "x": 345, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": month, "x": 310, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": year, "x": 260, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": day_, "x": 170, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": month, "x": 130, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": str(int(future_year)+1), "x": 80, "y": 366, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "1000", "x": 260, "y": 450, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "ألف", "x": 140, "y": 452, "font_path": "Molhim.ttf", 
         "font_size": 6, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "هذا العقد ساري وعلي مسئوليتي", "x": 420, "y": 40, "font_path": "Dima Font.ttf", 
         "font_size": 5.5, "text_color": "#140a72", "alpha": 1, "noise": False},
        {"text": "هذا العقد ساري وعلي مسئوليتي", "x": 1000, "y": 700, "font_path": "Molhim.ttf", 
         "font_size": 7, "text_color": "#140a72", "alpha": 1, "noise": False},
    ]

    image = Image.open(base_image_path)

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.imshow(image)

    # Add all text elements to the image
    for element in text_elements:
        ax = add_arabic_text_to_image(ax, **element)

    # Hide axes
    ax.axis("off")

    # Save the image to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg', bbox_inches="tight", pad_inches=0, dpi=300)
    img_buffer.seek(0)
    plt.close('all')  # Close all figures to free up memory

    return img_buffer
