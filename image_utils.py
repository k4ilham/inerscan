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
