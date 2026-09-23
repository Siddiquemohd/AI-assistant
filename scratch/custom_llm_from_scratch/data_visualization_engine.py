import os
from PIL import Image, ImageDraw

class DataVisualizationEngine:
    """
    Data Visualization & Chart Plotting Engine.
    Generates bar charts, line graphs, and visual data graphics exported as PNG images.
    """

    def generate_bar_chart(self, labels: list[str], values: list[float], title: str = "Data Chart", output_path: str = "output_chart.png") -> dict:
        width, height = 600, 400
        img = Image.new("RGB", (width, height), color=(250, 250, 255))
        draw = ImageDraw.Draw(img)

        # Title
        draw.text((20, 20), title, fill=(20, 30, 80))
        draw.line([(20, 45), (width - 20, 45)], fill=(200, 200, 220), width=2)

        # Axes
        origin_x, origin_y = 60, height - 60
        max_val = max(values) if values else 1
        plot_height = height - 120

        draw.line([(origin_x, origin_y), (width - 40, origin_y)], fill=(50, 50, 50), width=2) # X Axis
        draw.line([(origin_x, origin_y), (origin_x, 60)], fill=(50, 50, 50), width=2)        # Y Axis

        # Plot Bars
        n_items = len(values)
        bar_width = (width - 120) // max(1, n_items)

        colors = [(0, 150, 255), (255, 100, 100), (0, 200, 120), (255, 180, 0), (150, 100, 255)]

        for i, (label, val) in enumerate(zip(labels, values)):
            x0 = origin_x + i * bar_width + 15
            x1 = x0 + bar_width - 30
            h = int((val / max_val) * plot_height)
            y0 = origin_y - h
            y1 = origin_y

            color = colors[i % len(colors)]
            draw.rectangle([x0, y0, x1, y1], fill=color)

            # Label & Value text
            draw.text((x0, y0 - 18), str(val), fill=(30, 30, 30))
            draw.text((x0, y1 + 10), label[:8], fill=(30, 30, 30))

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        img.save(output_path)

        return {
            "status": "Success",
            "action": "generate_bar_chart",
            "title": title,
            "data_points": len(values),
            "file_path": output_path
        }
