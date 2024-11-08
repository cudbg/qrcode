
from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode

def generate_qr_code(url, file_path="qr_code.png"):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # version can be adjusted to control the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image
    img.save(file_path)
    print(f"QR code saved to {file_path}")

def create_card(name, email, description, comp, qr_code_path=None, output_path="card.png"):
    qr_code_path = qr_code_path or f"qr-{email.split('@')[0]}.png"
    generate_qr_code(f"mailto:{email}", qr_code_path)


    # Define card dimensions and background color
    card_width, card_height = 650, 325  # 4x6 inches at 150 DPI
    card = Image.new("RGB", (card_width, card_height), "white")
    
    # Load font (Pillow does not include fonts, so make sure you have one)
    try:
        font_large = ImageFont.truetype("Avenir.ttc", 36)  # Adjust font size and path if needed
        font_small = ImageFont.truetype("Avenir.ttc", 24)
    except IOError:
        print("Font not found. Make sure you have arial.ttf or adjust to an available font.")
        return
    
    draw = ImageDraw.Draw(card)
    
    # Draw the name, email, and description on the card
    margin = 20
    current_height = margin
    
    draw.text((margin, current_height), name, font=font_large, fill="black")
    current_height += font_large.getbbox(name)[3] - font_large.getbbox(name)[1] + margin

    draw.text((margin, current_height), email, font=font_small, fill="black")
    current_height += font_small.getbbox(name)[3] - font_large.getbbox(name)[1] + margin

    nchar = 30
    description_wrapped = "\n".join(textwrap.wrap(description, width=nchar)) + f"\n\n{comp}"
    draw.text((margin, current_height), description_wrapped, font=font_small, fill="black")
    # Calculate the height of multiline text by summing the height of each line
    line_height = font_small.getbbox("A")[3] - font_small.getbbox("A")[1]  # approximate line height
    lines = description_wrapped.splitlines()  # split the text into lines

    # Update current_height by adding the height of each line with margins
    current_height += len(lines) * line_height + (len(lines) - 1) * margin



    # Load and paste the QR code onto the card
    qr_code = Image.open(qr_code_path).resize((275, 275))  # Resize to fit on the card
    qr_x = card_width - qr_code.width - margin
    qr_y = card_height - qr_code.height - margin
    card.paste(qr_code, (qr_x, qr_y))
    
    # Save the card
    card.save(output_path)
    print(f"Card saved to {output_path}")

if __name__ == "__main__":
  # Example usage
  create_card(
      name="John Doe",
      email="AZ9999@columbia.edu",
      description="This is a sample project description with some details of the goals and requirements for the student.",
      comp="Paid or For Credit",
      qr_code_path="example_qr_code.png",
      output_path="printed_card.png"
  )