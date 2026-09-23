import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

class VisionImageEngine:
    """
    Image Generation & Editing Engine.
    Generates canvas artwork, diagrams, text graphics, and performs image editing operations.
    """

    def generate_image(self, prompt: str, width: int = 512, height: int = 512, output_path: str = "generated_image.png") -> dict:
        prompt_clean = prompt.strip().lower()

        # Create canvas
        img = Image.new("RGB", (width, height), color=(30, 30, 45))
        draw = ImageDraw.Draw(img)

        # Draw artistic background shapes based on prompt
        if "gradient" in prompt_clean or "abstract" in prompt_clean:
            for y in range(height):
                r = int(30 + (220 - 30) * (y / height))
                g = int(50 + (100 - 50) * (y / height))
                b = int(120 + (255 - 120) * (y / height))
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        elif "diagram" in prompt_clean or "flowchart" in prompt_clean:
            draw.rectangle([50, 50, 200, 120], outline=(0, 255, 200), width=3)
            draw.text((70, 75), "Input / Data", fill=(255, 255, 255))

            draw.line([(200, 85), (300, 85)], fill=(255, 255, 255), width=2)

            draw.rectangle([300, 50, 450, 120], outline=(255, 100, 200), width=3)
            draw.text((320, 75), "AI Processing", fill=(255, 255, 255))

        else:
            # Default elegant banner
            draw.rectangle([20, 20, width - 20, height - 20], outline=(0, 180, 255), width=4)
            draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], outline=(255, 215, 0), width=3)

        # Overlay text label
        draw.text((40, height - 50), f"ISAI Custom Engine: {prompt[:30]}", fill=(240, 240, 240))

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        img.save(output_path)

        return {
            "status": "Success",
            "action": "generate_image",
            "prompt": prompt,
            "dimensions": f"{width}x{height}",
            "file_path": output_path
        }

    def edit_image(self, input_path: str, action: str, params: dict = None, output_path: str = "edited_image.png") -> dict:
        if not os.path.exists(input_path):
            return {"status": "Error", "error": f"Input image file '{input_path}' not found."}

        params = params or {}
        img = Image.open(input_path)

        action_clean = action.lower().strip()

        if action_clean == "grayscale":
            img = img.convert("L")

        elif action_clean == "blur":
            radius = params.get("radius", 3)
            img = img.filter(ImageFilter.GaussianBlur(radius))

        elif action_clean == "resize":
            w = params.get("width", img.width // 2)
            h = params.get("height", img.height // 2)
            img = img.resize((w, h))

        elif action_clean == "rotate":
            angle = params.get("angle", 90)
            img = img.rotate(angle, expand=True)

        elif action_clean == "brightness":
            factor = params.get("factor", 1.5)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(factor)

        elif action_clean == "contrast":
            factor = params.get("factor", 1.5)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(factor)

        elif action_clean == "watermark":
            text = params.get("text", "ISAI Personal AI")
            draw = ImageDraw.Draw(img)
            draw.text((20, img.height - 40), text, fill=(255, 255, 255))

        else:
            return {"status": "Error", "error": f"Unsupported edit action '{action}'."}

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        img.save(output_path)

        return {
            "status": "Success",
            "action": f"edit_image ({action_clean})",
            "input_file": input_path,
            "output_file": output_path
        }
