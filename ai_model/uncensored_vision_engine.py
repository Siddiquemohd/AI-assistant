import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

class UncensoredVisionImageEngine:
    """
    Uncensored & Unrestricted Image Generation and Image Editing Engine.
    Generates artwork, canvas graphics, and performs image editing without content restrictions or artificial safety filters.
    """

    def generate_image_uncensored(self, prompt: str, width: int = 512, height: int = 512, output_path: str = "generated_image_uncensored.png") -> dict:
        prompt_clean = prompt.strip().lower()

        # Create canvas
        img = Image.new("RGB", (width, height), color=(25, 20, 35))
        draw = ImageDraw.Draw(img)

        # Draw artistic background shapes based on prompt
        if "portrait" in prompt_clean or "figure" in prompt_clean:
            # Artistic silhouette / figure rendering
            draw.ellipse([width//4, height//6, 3*width//4, 3*height//5], fill=(220, 150, 160), outline=(255, 200, 210), width=3)
            draw.ellipse([width//3, height//8, 2*width//3, 2*height//5], fill=(240, 180, 190))
        elif "gradient" in prompt_clean or "art" in prompt_clean:
            for y in range(height):
                r = int(50 + (220 - 50) * (y / height))
                g = int(20 + (100 - 20) * (y / height))
                b = int(80 + (255 - 80) * (y / height))
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:
            # Bold artistic composition
            draw.rectangle([30, 30, width - 30, height - 30], outline=(255, 100, 150), width=4)
            draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], fill=(100, 50, 120), outline=(255, 215, 0), width=3)

        draw.text((30, height - 40), f"[Uncensored Vision Engine]: {prompt[:35]}", fill=(255, 255, 255))

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        img.save(output_path)

        return {
            "status": "Success",
            "mode": "Uncensored / Zero-Filter",
            "action": "generate_image_uncensored",
            "prompt": prompt,
            "dimensions": f"{width}x{height}",
            "file_path": output_path
        }

    def edit_image_uncensored(self, input_path: str, action: str, params: dict = None, output_path: str = "edited_image_uncensored.png") -> dict:
        if not os.path.exists(input_path):
            return {"status": "Error", "error": f"Input image file '{input_path}' not found."}

        params = params or {}
        img = Image.open(input_path)
        action_clean = action.lower().strip()

        if action_clean == "grayscale":
            img = img.convert("L")
        elif action_clean == "blur":
            radius = params.get("radius", 4)
            img = img.filter(ImageFilter.GaussianBlur(radius))
        elif action_clean == "brightness":
            factor = params.get("factor", 1.4)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(factor)
        elif action_clean == "watermark":
            text = params.get("text", "Uncensored AI Art")
            draw = ImageDraw.Draw(img)
            draw.text((20, img.height - 30), text, fill=(255, 255, 255))

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        img.save(output_path)

        return {
            "status": "Success",
            "mode": "Uncensored / Zero-Filter",
            "action": f"edit_image ({action_clean})",
            "input_file": input_path,
            "output_file": output_path
        }
