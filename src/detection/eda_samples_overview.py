import os
import pandas as pd

import imageio
from PIL import Image, ImageOps, ImageDraw, ImageFont
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from joblib import Parallel, delayed

BBOX_COLOR = "magenta"
OVERWRITE = True
N_JOBS = 4


def draw_bboxes_on_image(img_path, bboxes, bbox_format='xywh', font_size=60, bbox_color=BBOX_COLOR, bbox_thickness=12,
                         square_size=None):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(font_size)

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

        label = f'{cat_name}'

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline=bbox_color, width=bbox_thickness)

        # Draw text
        space = (font_size * 1.25)
        text_x, text_y = x1, y1 - space
        draw.text((text_x, text_y), label, fill=bbox_color, font=font, width=bbox_thickness)

    if square_size:
        img = ImageOps.pad(img, size=(square_size, square_size), color="black", centering=(0.5, 0.5))

    return img


def generate_sample_images_plot(df, cat_type, cat_name, output_path, max_images=25, n_cols=3, square_size=900,
                                verbose=False, overwrite=OVERWRITE):
    if cat_type not in ['cat_name', 'supercategory']:
        raise ValueError(f"cat_type must be 'cat_name' or 'supercategory'")
    if cat_name not in df[cat_type].unique():
        raise ValueError(f"cat_name must be one of {df[cat_type].unique()}")

    groups = df.query(f"{cat_type} == '{cat_name}'").groupby("path")
    groups = list(groups)[:max_images]

    # add n images to the filename
    output_path = output_path.replace('.png', f' ({len(groups)} examples).png')

    if os.path.exists(output_path) and not overwrite:
        print(f"File {output_path} already exists. Skipping.") if verbose else None
        return output_path

    n_rows = np.ceil(len(groups) / n_cols).astype(int)
    s = 6
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(s * n_cols, s * n_rows))
    axes = axes.flatten()

    print("> Plotting images...") if verbose else None
    for i, (image_path, group_df) in enumerate(tqdm(groups, disable=not verbose)):
        bboxes = group_df[["cat_name", "x", "y", "width", "height"]].values
        img = draw_bboxes_on_image(image_path, bboxes, square_size=square_size, bbox_format='xywh')

        axes[i].imshow(img)
        axes[i].set_title(
            f"{os.path.basename(os.path.dirname(image_path))}/{os.path.basename(image_path)} ({cat_name} - {len(bboxes)} bboxes)")
        axes[i].axis('off')

    fig.tight_layout()

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    fig.savefig(output_path, dpi=300)
    print(f"> Saved figure to {output_path}") if verbose else None
    plt.close(fig)

    return output_path


def create_gif(df, output_path, fps=2, square_size=None, verbose=False, overwrite=OVERWRITE):
    """
    Create a gif from a dataframe of images and bounding boxes.

    Args:
        df (DataFrame): Dataframe containing image paths and bounding boxes.
        output_path (str): Output path for the gif.
        fps (int): Frames per second for the gif.
        square_size (int): Size to make images square.
        verbose (bool): Whether to print out messages.
        bbox_format (str): Format of the bounding boxes. 'xyxy', 'xywh' or 'cxcywh'
    """
    images = []

    if os.path.exists(output_path) and not overwrite:
        print(f"File {output_path} already exists. Skipping.") if verbose else None
        return output_path

    for image_path, group_df in tqdm(df.groupby("path"), desc="Creating GIF", disable=not verbose):
        bboxes = group_df[["cat_name", "x", "y", "width", "height"]].values
        img = draw_bboxes_on_image(image_path, bboxes, square_size=square_size, bbox_format='xywh')
        images.append(img)

    try:
        imageio.mimsave(output_path, images, loop=0, fps=fps)
    except Exception as e:
        if verbose:
            print(f"Error while creating gif: {e}")
        return None
    else:
        if verbose:
            print(f"Successfully created gif at {output_path} with {len(images)} images")
        return output_path


def parallel_create_gif(meta_df, category, category_type, max_images, output_dir, fps, square_size):
    # Sélectionner des images pour la catégorie courante
    selected_images_examples = meta_df[meta_df[category_type] == category]
    if len(selected_images_examples) > max_images:
        selected_images_examples = selected_images_examples.sample(max_images)

    output_path = os.path.join(output_dir, f"{category}.gif")
    create_gif(selected_images_examples, output_path, fps=fps, square_size=square_size)


def generate_all_gifs_from_meta_df(meta_df, category_type, max_images, output_dir, fps=4, square_size=900):
    categories = meta_df[category_type].unique().tolist()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    Parallel(n_jobs=N_JOBS)(
        delayed(parallel_create_gif)(meta_df, category, category_type, max_images, output_dir, fps, square_size) for
        category in tqdm(categories, desc=f"Generating GIFs ({category_type})"))


def main_gif():
    # Example usage
    TACO_DATASET_ROOT_PATH = r"N:\My Drive\KESKIA Drive Mlamali\datasets\taco-2gb"
    taco_meta_df = pd.read_csv(os.path.join(TACO_DATASET_ROOT_PATH, "meta_df.csv"))
    taco_meta_df["path"] = taco_meta_df["img_file"].apply(lambda x: os.path.join(TACO_DATASET_ROOT_PATH, "data", x))

    for cat_type in ['cat_name', 'supercategory']:
        generate_all_gifs_from_meta_df(taco_meta_df, cat_type, max_images=50,
                                       output_dir=f'results/eda/samples-overview/taco-base-gif/{cat_type}',
                                       square_size=900)


def parallel_generate_sample_images_plot(taco_meta_df, cat_type, cat_name, root_path, max_images, n_cols, square_size):
    output_path = os.path.join(root_path, f'{cat_type}/{cat_name}.png')
    generate_sample_images_plot(taco_meta_df, cat_type, cat_name, output_path, max_images=max_images, n_cols=n_cols,
                                square_size=square_size)


def main_plot():
    TACO_DATASET_ROOT_PATH = r"N:\My Drive\KESKIA Drive Mlamali\datasets\taco-2gb"
    taco_meta_df = pd.read_csv(os.path.join(TACO_DATASET_ROOT_PATH, "meta_df.csv"))
    taco_meta_df["path"] = taco_meta_df["img_file"].apply(lambda x: os.path.join(TACO_DATASET_ROOT_PATH, "data", x))

    output_root_path = '../../results/eda/samples-overview/taco-base-plot'

    for cat_type, max_images in [('cat_name', 36), ('supercategory', 48)]:
        cat_names = taco_meta_df[cat_type].unique().tolist()
        Parallel(n_jobs=N_JOBS)(
            delayed(parallel_generate_sample_images_plot)(taco_meta_df, cat_type, cat_name, output_root_path,
                                                          max_images, n_cols=4, square_size=900) for cat_name in
            tqdm(cat_names, desc=f"Generating plots ({cat_type})"))


if __name__ == "__main__":
    main_gif()
    main_plot()
