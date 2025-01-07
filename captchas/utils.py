# import random
# from PIL import Image, ImageDraw, ImageFont
# import io
# import base64

# def generate_math_captcha():
#     # Generate two random numbers between 0 and 9
#     num1 = random.randint(0, 9)
#     num2 = random.randint(0, 9)
    
#     # Calculate the sum (this will be the correct answer)
#     answer = str(num1 + num2)
    
#     # Create the question text
#     question = f"{num1} + {num2} = ?"
    
#     # Create image with the math problem
#     img = Image.new('RGB', (95, 70), color='white')
#     d = ImageDraw.Draw(img)
    
#     # Add text to image
#     d.text((35, 35), question, fill='black')
    
#     # Convert image to base64
#     buffer = io.BytesIO()
#     img.save(buffer, format='PNG')
#     image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
#     return answer, image_base64


# import random
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO
# import base64

# def generate_captcha_text():
#     """Generate random CAPTCHA text."""
#     return str(random.randint(1000, 9999))

# def generate_captcha_image(text):
#     """Create CAPTCHA image from text."""
#     # Create image with white background
#     image = Image.new('RGB', (100, 40), color='white')
#     draw = ImageDraw.Draw(image)
    
#     # Add noise (random dots)
#     for _ in range(20):
#         x = random.randint(0, 100)
#         y = random.randint(0, 40)
#         draw.point((x, y), fill='black')
    
#     # Add text
#     draw.text((25, 10), text, fill='black')
    
#     # Convert to base64
#     buffer = BytesIO()
#     image.save(buffer, format='PNG')
#     return base64.b64encode(buffer.getvalue()).decode()


# utils.py
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

def generate_captcha():
    # Generate random string of 4 characters
    chars = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choices(chars, k=5))
    
    # Create image
    image = Image.new('RGB', (130, 50), color='white')
    draw = ImageDraw.Draw(image)
    
    # Add noise
    for _ in range(500):
        x = random.randint(0, 120)
        y = random.randint(0, 40)
        draw.point((x, y), fill='black')
    
    # Add text
    draw.text((40, 15), captcha_text, fill='black', font_size=21)
    
    # Convert to base64
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return captcha_text, image_base64


