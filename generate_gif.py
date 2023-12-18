import os
import pandas as pd
from tqdm import tqdm
import numpy as np

import imageio
from PIL import Image, ImageOps, ImageDraw, ImageFont
from tqdm import tqdm


def create_gif(df, output_path, fps=2, square_size=None, verbose=False, bbox_format: str = 'xywh'):
    """
    Create a gif from a list of images.

    Args:
        image_paths (list): List of image paths.
        output_path (str): Output path for the gif.
        fps (int): Frames per second for the gif.
        square_size (int): Size to make images square.
        verbose (bool): Whether to print out messages.
        images_bboxes (dict): Dictionary of image paths and bounding boxes.
        bbox_format (str): Format of the bounding boxes. 'xyxy', 'xywh' or 'cxcywh'
    """
    images = []
    for image_path, group_df in df.groupby("path"):
        img = Image.open(image_path)

        bboxes = group_df[["cat_name", "x", "y", "width", "height"]].values

        # Draw rectangles if bounding boxes are provided
        if len(bboxes) > 0:
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default(10)  # Default font, you can customize it

            for box in bboxes:
                if bbox_format == 'xyxy':
                    cat_name, x1, y1, x2, y2 = box
                elif bbox_format == 'xywh':
                    cat_name, x1, y1, w, h = box
                    x2, y2 = x1 + w, y1 + h
                elif bbox_format == 'cxcywh':
                    cat_name, cx, cy, w, h = box
                    x1, y1 = cx - w / 2, cy - h / 2
                    x2, y2 = cx + w / 2, cy + h / 2
                else:
                    raise ValueError(f'Unknown bbox format {bbox_format}')

                label = f'{cat_name}'  # Assuming cls is a string. If it's an index, convert it to a label string.

                # Define box and text properties
                color = (25, 255, 25)  # Green color
                thickness = 15
                # text_size = draw.textsize(label, font=font)
                text_x, text_y = x2, y2

                # Draw rectangle and text background
                draw.rectangle([x1, y1, x2, y2], outline=color, width=thickness)
                # draw.rectangle([text_x, text_y, text_x + text_size[0], text_y + text_size[1]], fill=color)

                # Draw text
                draw.text((text_x, text_y), label, fill=color, font=font)

        # Make image square if needed
        if square_size:
            img = ImageOps.pad(img, size=(square_size, square_size), color="black", centering=(0.5, 0.5))

        images.append(img)

        # Create gif
    try:
        imageio.mimsave(output_path, images, loop=0, fps=fps)
    except Exception as e:
        if verbose:
            print(f"Error while creating gif: {e}")
        return False
    else:
        if verbose:
            print(f"Successfully created gif at {output_path} with {len(images)} images")
        return True


def generate_gifs(meta_df, category_type, max_images, output_dir, fps=4, square_size=600):
    """
    Generate GIFs for each unique category in the dataset.

    Args:
        taco_meta_df (DataFrame): Dataframe containing image and category data.
        category_type (str): Column name to categorize by ('cat_name' or 'supercategory').
        max_images (int): Maximum number of images per GIF.
        output_dir (str): Directory to save the GIFs.
        fps (int): Frames per second for the GIF.
        square_size (int): Size to make images square.
    """

    categories = meta_df[category_type].unique().tolist()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create GIFs for each category ('Plastic', 'Metal', etc.)
    for category in tqdm(categories, desc=f"Generating GIFs ({category_type})"):
        # Select images for the current category
        selected_images_examples = meta_df[meta_df[category_type] == category]
        if len(selected_images_examples) > max_images:
            selected_images_examples = selected_images_examples.sample(max_images)

        output_path = os.path.join(output_dir, f"{category}.gif")
        create_gif(selected_images_examples, output_path, fps=fps, verbose=0, square_size=square_size)




def main():
    # Example usage
    TACO_DATASET_ROOT_PATH = r"N:\My Drive\KESKIA Drive Mlamali\datasets\taco-2gb"
    taco_meta_df = pd.read_csv(os.path.join(TACO_DATASET_ROOT_PATH, "meta_df.csv"))
    # column require : path, cat_name, x, y, width, height
    taco_meta_df["path"] = taco_meta_df["img_file"].apply(lambda x: os.path.join(TACO_DATASET_ROOT_PATH, "data", x))

    for cat_type in ['cat_name', 'supercategory']:
        generate_gifs(taco_meta_df, cat_type, max_images=50,output_dir=f'outputs/animated-overview/taco/gif {cat_type}')


if __name__ == "__main__":
    main()