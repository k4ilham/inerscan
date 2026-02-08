from PIL import Image, ImageDraw, ImageFont

def create_default_icon():
    # Create a 256x256 image
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: Rounded Square (Blue)
    # Draw blue circle/rect
    blue = "#3B82F6"
    draw.rounded_rectangle([(10, 10), (246, 246)], radius=60, fill=blue)

    # Document Outline (White)
    draw.rectangle([(60, 50), (196, 206)], fill="white")
    
    # Text Lines (Gray)
    for y in range(80, 180, 20):
        draw.line([(80, y), (176, y)], fill="#E5E7EB", width=4)

    # Scanner Beam (Cyan/Green gradient simulation)
    # Simple line for now
    draw.line([(50, 120), (206, 120)], fill="#EF4444", width=8) # Red scan line
    
    # Save
    img.save("app_icon.png")
    img.save("app_icon.ico", format='ICO')
    print("Icon created: app_icon.png")

if __name__ == "__main__":
    create_default_icon()
