#!/usr/bin/env python3

import base64
import io
import json
import logging
import boto3
from PIL import Image
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ImageError(Exception):
    """Custom exception for errors returned by Amazon Nova"""
    def __init__(self, message):
        self.message = message

def generate_image_with_nova_omni(prompt, width=3072, height=1024):
    """Generate an image using Amazon Nova 2 Omni model (Preview)."""
    logger.info("Attempting to generate image with Amazon Nova 2 Omni model")
    
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        config=Config(read_timeout=600)
    )
    
    model_id = "us.amazon.nova-2-omni-v1:0"
    
    # Try with explicit dimension prompt
    try:
        logger.info("Generating with Nova 2 Omni...")
        
        dimension_prompt = f"""IMPORTANT: Generate an image with EXACTLY {width} pixels width and EXACTLY {height} pixels height. The aspect ratio must be exactly 3:1 (three times wider than tall). Resolution: {width}x{height} pixels.

Image content: {prompt}

Remember: The output MUST be {width}x{height} pixels, no other size."""
        
        conversation = [
            {
                "role": "user",
                "content": [{"text": dimension_prompt}]
            }
        ]
        
        response = bedrock.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 4096}
        )
        
        content = response['output']['message']['content']
        for block in content:
            if 'image' in block:
                image_data = block['image']['source']['bytes']
                img = Image.open(io.BytesIO(image_data))
                actual_width, actual_height = img.size
                logger.info(f"Generated image size: {actual_width}x{actual_height}")
                return image_data
        
    except Exception as e:
        logger.error(f"Nova 2 Omni failed: {str(e)}")
        raise ImageError(f"Nova 2 Omni failed: {str(e)}")

def smart_resize_to_3_1(image_bytes, target_width=3072, target_height=1024):
    """
    Resize to 3:1 ratio by stretching width only (no cropping).
    Maintains full vertical content, stretches horizontal to achieve 3:1 ratio.
    """
    img = Image.open(io.BytesIO(image_bytes))
    original_width, original_height = img.size
    original_ratio = original_width / original_height
    target_ratio = target_width / target_height
    
    logger.info(f"Original: {original_width}x{original_height} (ratio: {original_ratio:.2f}:1)")
    logger.info(f"Target: {target_width}x{target_height} (ratio: {target_ratio:.2f}:1)")
    
    # If already correct ratio, just resize
    if abs(original_ratio - target_ratio) < 0.01:
        logger.info("Ratio already correct, simple high-quality resize")
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img_resized.save(output, format='PNG', quality=100)
        return output.getvalue()
    
    # Strategy: Stretch width to achieve 3:1 ratio (no cropping)
    # This preserves all vertical content
    
    logger.info(f"Stretching width from {original_width} to {target_width} (keeping height at {target_height})")
    logger.info(f"Width stretch factor: {target_width / original_width:.2f}x")
    logger.info(f"Height resize factor: {target_height / original_height:.2f}x")
    
    # Direct resize to target dimensions (stretches width more than height)
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    img_resized.save(output, format='PNG', quality=100)
    
    logger.info("✓ Width-stretched resize complete (no cropping, full vertical content preserved)")
    return output.getvalue()

def save_image(image_bytes, filename=None):
    """Save image bytes to a file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
    
    image = Image.open(io.BytesIO(image_bytes))
    image.save(filename, quality=100)
    logger.info(f"Image saved as {filename}")
    
    # Verify final size
    final_size = image.size
    aspect_ratio = final_size[0] / final_size[1]
    logger.info(f"Final image size: {final_size[0]}x{final_size[1]} (aspect ratio: {aspect_ratio:.2f}:1)")
    
    return filename

def main():
    # Full prompt for Nova 2 Omni
    full_prompt = """Ultra-wide cinematic cityscape at dusk, viewed from a high rooftop, 3:1 banner composition. In the foreground, several diverse characters in futuristic streetwear are leaning on the railing, silhouetted against the glowing city: one character holding a holographic tablet displaying neon UI panels, another with a cybernetic arm and a long coat blowing in the wind, and a third character sitting on a crate with headphones, looking toward the horizon. The midground is a dense cluster of skyscrapers with reflective glass, animated billboards, floating drones, and suspended sky-bridges filled with tiny crowds of people. Flying cars and hovercrafts leave long light trails, curving across the sky from left to right, emphasizing the panoramic width of the scene. In the background, a massive ring-shaped structure floats above the city, partially obscured by volumetric fog and clouds. The setting sun is low on the horizon, casting golden and magenta light, creating strong rim lighting on the characters and buildings. Highly detailed, sharp focus, complex lighting, global illumination, soft atmospheric haze, subtle depth of field, cinematic color grading, rich reflections on glass and metal surfaces, hyperrealistic textures on buildings and clothing, high dynamic range, 8k concept art, perfect composition for a hero banner with plenty of negative space near the top and bottom for text overlay."""
    
    width = 3072
    height = 1024
    
    try:
        logger.info("Starting image generation...")
        logger.info(f"Resolution: {width}x{height}")
        logger.info(f"Aspect Ratio: 3:1")
        logger.info("Model: Amazon Nova 2 Omni")
        
        # Generate with Nova 2 Omni
        logger.info("Generating with Nova 2 Omni...")
        image_bytes = generate_image_with_nova_omni(full_prompt, width, height)
        
        # Check dimensions and apply smart resize if needed
        img = Image.open(io.BytesIO(image_bytes))
        actual_width, actual_height = img.size
        
        if actual_width == width and actual_height == height:
            filename = save_image(image_bytes, "cityscape_banner_3x1_nova_omni.png")
            logger.info("✓ Successfully generated with native 3:1 ratio!")
        else:
            logger.info(f"Nova 2 Omni generated {actual_width}x{actual_height}, applying smart resize...")
            
            # Save original 2:1 image first
            original_filename = save_image(image_bytes, "cityscape_banner_2x1_nova_omni_original.png")
            logger.info(f"✓ Original 2:1 image saved: {original_filename}")
            
            # Then create and save 3:1 resized version
            smart_resized_bytes = smart_resize_to_3_1(image_bytes, width, height)
            filename = save_image(smart_resized_bytes, "cityscape_banner_3x1_nova_omni.png")
            logger.info("✓ Successfully generated with smart high-quality resize to 3:1!")
        
        logger.info("Image generation completed successfully!")
        logger.info(f"Output files: {original_filename if actual_width != width else ''} {filename}")
        
    except ImageError as e:
        logger.error(f"Image generation failed: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
