from PIL import Image, ImageEnhance, ImageOps
import numpy as np

class ImageProcessor:
    @staticmethod
    def process_page(page_data):
        """
        Applies all edits from page_data to the original image.
        Returns the processed PIL Image.
        """
        img = page_data['original'].copy()

        # Preserve Alpha if present
        has_alpha = img.mode == 'RGBA'

        # 1. Rotation
        if page_data['rotation'] != 0:
            img = img.rotate(page_data['rotation'], expand=True)

        # 2. Flips
        if page_data['flip_h']:
            img = ImageOps.mirror(img)
        if page_data['flip_v']:
            img = ImageOps.flip(img)

        # 3. Grayscale
        if page_data['grayscale']:
            img = img.convert("L") # Auto drops alpha
            if has_alpha:
                 # If we want grayscale + alpha, we need a different approach, 
                 # but usually grayscale implies B&W document. 
                 # Let's keep it simple: Grayscale kills transparency or we convert back to simple RGB.
                 pass
            img = img.convert("RGB") 
        else:
            # Only convert to RGB if it's NOT RGBA (to preserve transparency)
            if img.mode != "RGB" and img.mode != "RGBA":
                img = img.convert("RGB")

        # 4. Brightness
        if page_data['brightness'] != 1.0:
            if img.mode == 'RGBA':
                # Split alpha, enhance RGB, merge back
                r, g, b, a = img.split()
                rgb_img = Image.merge('RGB', (r, g, b))
                enhancer = ImageEnhance.Brightness(rgb_img)
                rgb_img = enhancer.enhance(page_data['brightness'])
                r, g, b = rgb_img.split()
                img = Image.merge('RGBA', (r, g, b, a))
            else:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(page_data['brightness'])

        # 5. Contrast
        if page_data['contrast'] != 1.0:
            if img.mode == 'RGBA':
                r, g, b, a = img.split()
                rgb_img = Image.merge('RGB', (r, g, b))
                enhancer = ImageEnhance.Contrast(rgb_img)
                rgb_img = enhancer.enhance(page_data['contrast'])
                r, g, b = rgb_img.split()
                img = Image.merge('RGBA', (r, g, b, a))
            else:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(page_data['contrast'])
            
        return img

    @staticmethod
    def remove_white_background(pil_image, threshold=230):
        """
        Removes pixels brighter than threshold.
        Default threshold increased to 230 to avoid removing face highlights.
        """
        img = pil_image.convert("RGBA")
        data = np.array(img)
        
        # Transpose to get channels easily: (4, H, W)
        # data.T returns (width, height, 4) if data is (height, width, 4)? No.
        # Numpy layout is (H, W, C). T is (C, W, H).
        # Let's stick to standard indexing for clarity.
        
        red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
        
        # Mask: All channels > threshold
        white_areas = (red > threshold) & (green > threshold) & (blue > threshold)
        
        # Set alpha to 0 for white areas
        data[..., 3][white_areas] = 0
        
        return Image.fromarray(data)

    @staticmethod
    def perform_auto_crop(pil_image):
        """
        Crops the image to the bounding box of non-transparent pixels.
        Returns the cropped image.
        """
        if pil_image.mode != 'RGBA':
            return pil_image
            
        bbox = pil_image.getbbox()
        if bbox:
            return pil_image.crop(bbox)
        return pil_image # Return original if empty or no alpha

    @staticmethod
    def apply_background_color(pil_image, color_rgb):
        """
        Composites the image over a solid background color.
        pil_image must be RGBA (e.g. after removing bg).
        color_rgb is a tuple (r, g, b).
        """
        params = (int(color_rgb[0]), int(color_rgb[1]), int(color_rgb[2]), 255)
        background = Image.new("RGBA", pil_image.size, params)
        return Image.alpha_composite(background, pil_image).convert("RGB")

    @staticmethod
    def split_image_vertical(pil_image):
        """
        Splits the image vertically into Left and Right halves.
        Returns a tuple (left_img, right_img).
        """
        w, h = pil_image.size
        half_w = w // 2
        
        # Crop Left
        left_img = pil_image.crop((0, 0, half_w, h))
        
        # Crop Right
        right_img = pil_image.crop((half_w, 0, w, h))
        
        return left_img, right_img

    @staticmethod
    def create_photo_grid(images, grid_layout="2x2", spacing=10, bg_color=(255, 255, 255)):
        """
        Creates a photo grid/collage from multiple images.
        
        Args:
            images: List of PIL Images
            grid_layout: String like "2x2", "3x3", "1x2", "2x1", etc.
            spacing: Pixels between images
            bg_color: Background color (R, G, B)
        
        Returns:
            PIL Image of the grid
        """
        if not images:
            raise ValueError("No images provided")
        
        # Parse grid layout
        parts = grid_layout.lower().split('x')
        if len(parts) != 2:
            raise ValueError("Grid layout must be in format 'WxH' (e.g., '2x2')")
        
        cols = int(parts[0])
        rows = int(parts[1])
        total_slots = cols * rows
        
        # Extend or trim images list
        if len(images) < total_slots:
            # Fill remaining slots with blank white images
            blank = Image.new('RGB', images[0].size, bg_color)
            images = images + [blank] * (total_slots - len(images))
        elif len(images) > total_slots:
            images = images[:total_slots]
        
        # Convert all to RGB and find max dimensions
        rgb_images = []
        max_w, max_h = 0, 0
        for img in images:
            if img.mode == 'RGBA':
                # Composite over white background
                bg = Image.new('RGB', img.size, bg_color)
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            rgb_images.append(img)
            max_w = max(max_w, img.width)
            max_h = max(max_h, img.height)
        
        # Resize all images to same size (use average or max)
        cell_w = max_w
        cell_h = max_h
        
        resized = []
        for img in rgb_images:
            # Resize maintaining aspect ratio
            img_copy = img.copy()
            img_copy.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
            
            # Create cell with background color
            cell = Image.new('RGB', (cell_w, cell_h), bg_color)
            paste_x = (cell_w - img_copy.width) // 2
            paste_y = (cell_h - img_copy.height) // 2
            cell.paste(img_copy, (paste_x, paste_y))
            resized.append(cell)
        
        # Calculate final grid size
        grid_w = cols * cell_w + (cols - 1) * spacing
        grid_h = rows * cell_h + (rows - 1) * spacing
        
        # Create final grid
        grid = Image.new('RGB', (grid_w, grid_h), bg_color)
        
        # Place images
        idx = 0
        for row in range(rows):
            for col in range(cols):
                if idx < len(resized):
                    x = col * (cell_w + spacing)
                    y = row * (cell_h + spacing)
                    grid.paste(resized[idx], (x, y))
                    idx += 1
        
        return grid

    @staticmethod
    def deskew_image(pil_image):
        """
        Automatically detects and corrects the skew/tilt of an image.
        Uses contour detection and minimum area rectangle for high accuracy.
        
        Args:
            pil_image: PIL Image to deskew
            
        Returns:
            PIL Image that has been straightened
        """
        import cv2
        
        # Convert PIL to numpy array
        img_array = np.array(pil_image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive threshold for better edge detection
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            # Try regular Canny edge detection as fallback
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return pil_image
        
        # Find the largest contour (assuming it's the main object/document)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get minimum area rectangle
        rect = cv2.minAreaRect(largest_contour)
        angle = rect[2]
        
        # Normalize angle
        # minAreaRect returns angle in range [-90, 0)
        # We need to adjust it to get the correct rotation
        if angle < -45:
            angle = 90 + angle
        
        # Only apply correction if angle is significant (> 0.3 degrees)
        if abs(angle) < 0.3:
            return pil_image
        
        # Get image dimensions
        h, w = gray.shape
        
        # Calculate rotation matrix
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate new bounding dimensions
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # Adjust rotation matrix for new center
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # Rotate the image
        rotated = cv2.warpAffine(img_array, M, (new_w, new_h), 
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(255, 255, 255))
        
        # Convert back to PIL
        if len(img_array.shape) == 3:
            corrected = Image.fromarray(rotated)
        else:
            corrected = Image.fromarray(rotated).convert('L')
        
        return corrected

    @staticmethod
    def auto_straighten_simple(pil_image):
        """
        Simpler straightening method that works without OpenCV.
        Uses projection profile method to detect text orientation.
        
        Args:
            pil_image: PIL Image to straighten
            
        Returns:
            PIL Image rotated to the best angle
        """
        # Convert to grayscale
        if pil_image.mode == 'RGBA':
            # Convert RGBA to RGB first
            bg = Image.new('RGB', pil_image.size, 'white')
            bg.paste(pil_image, mask=pil_image.split()[3])
            img = bg.convert('L')
        elif pil_image.mode != 'L':
            img = pil_image.convert('L')
        else:
            img = pil_image
        
        # Try angles from -10 to +10 degrees
        best_angle = 0
        best_score = 0
        
        for angle in range(-10, 11, 1):
            # Rotate image
            rotated = img.rotate(angle, expand=False, fillcolor=255)
            img_array = np.array(rotated)
            
            # Calculate horizontal projection (sum of black pixels per row)
            projection = np.sum(255 - img_array, axis=1)
            
            # Score is variance of projection (higher = more aligned text)
            score = np.var(projection)
            
            if score > best_score:
                best_score = score
                best_angle = angle
        
        # Apply best rotation to original image
        if best_angle != 0:
            return pil_image.rotate(best_angle, expand=True, fillcolor='white')
        else:
            return pil_image

    @staticmethod
    def add_watermark(pil_image, text="COPY", position="center", 
                     opacity=128, rotation=-45, font_size=None, color=(255, 0, 0)):
        """
        Add a watermark/stamp to the image.
        
        Args:
            pil_image: PIL Image to add watermark to
            text: Watermark text (e.g., "COPY", "DRAFT", "CONFIDENTIAL")
            position: Position of watermark - "center", "top-right", "bottom-right", "diagonal"
            opacity: Transparency 0-255 (0=invisible, 255=opaque)
            rotation: Rotation angle in degrees (negative for counter-clockwise)
            font_size: Font size in pixels (auto-calculated if None)
            color: RGB color tuple
            
        Returns:
            PIL Image with watermark
        """
        from PIL import ImageDraw, ImageFont
        
        # Create a copy to avoid modifying original
        img = pil_image.copy()
        
        # Ensure RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate font size if not provided (proportional to image size)
        if font_size is None:
            font_size = int(min(img.size) * 0.15)  # 15% of smaller dimension
        
        # Create overlay layer
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Try to load a bold font, fallback to default
        try:
            # Try common Windows fonts
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default
                font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        if position == "center":
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
        elif position == "top-right":
            x = img.width - text_width - 50
            y = 50
        elif position == "bottom-right":
            x = img.width - text_width - 50
            y = img.height - text_height - 50
        elif position == "top-left":
            x = 50
            y = 50
        elif position == "bottom-left":
            x = 50
            y = img.height - text_height - 50
        else:  # diagonal (multiple watermarks)
            position = "center"
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
        
        # Create text with specified opacity
        text_color = (*color, opacity)
        
        # Draw text on overlay
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Rotate overlay if needed
        if rotation != 0:
            overlay = overlay.rotate(rotation, expand=False, fillcolor=(255, 255, 255, 0))
        
        # Convert base image to RGBA for compositing
        img_rgba = img.convert('RGBA')
        
        # Composite overlay onto image
        watermarked = Image.alpha_composite(img_rgba, overlay)
        
        # Convert back to RGB
        final = watermarked.convert('RGB')
        return final

    @staticmethod
    def add_text(pil_image, text, position=(50, 50), font_size=40, color=(0, 0, 0), opacity=255):
        """
        Add manual text to the image at specific coordinates.
        """
        from PIL import ImageDraw, ImageFont
        img = pil_image.copy().convert('RGBA')
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            
        draw.text(position, text, font=font, fill=(*color, opacity))
        combined = Image.alpha_composite(img, txt_layer)
        return combined.convert('RGB')
    @staticmethod
    def automatic_document_transform(pil_image):
        """
        Detects document corners and performs a perspective transform to flatten it.
        Uses OpenCV for contour detection and warping.
        """
        import cv2
        img = np.array(pil_image.convert('RGB'))
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        screen_cnt = None
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                screen_cnt = approx
                break

        if screen_cnt is None:
            return pil_image  # Could not find document

        # Perspective Transform
        pts = screen_cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[1] - br[1]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[1] - bl[1]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpAffine(img, M, (maxWidth, maxHeight)) # Fix: should be warpPerspective
        # Using warpPerspective instead of warpAffine
        warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

        return Image.fromarray(warped)

    @staticmethod
    def enhance_document_text(pil_image):
        """
        Cleans background and enhances text using adaptive thresholding.
        Returns a clean B&W document style image.
        """
        import cv2
        img = np.array(pil_image.convert('L'))
        enhanced = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(enhanced)

    @staticmethod
    def detect_blank_page(pil_image, threshold=0.005):
        """
        Returns True if the page is likely blank.
        Uses Laplacian variance or basic edge counting.
        """
        import cv2
        img = np.array(pil_image.convert('L'))
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        # High variance means lots of details (edges), low variance means blank/blurry.
        # Usually variance < 100 for blank pages
        return laplacian_var < 100

    @staticmethod
    def redact_faces(pil_image):
        """
        Automatically detects and blurs faces in the image.
        """
        import cv2
        img = np.array(pil_image.convert('RGB'))
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            sub_face = img[y:y+h, x:x+w]
            # Blur the face
            sub_face = cv2.GaussianBlur(sub_face, (99, 99), 30)
            img[y:y+h, x:x+w] = sub_face
            
        return Image.fromarray(img)
