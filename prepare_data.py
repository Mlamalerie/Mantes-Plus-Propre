from sklearn.model_selection import train_test_split
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import shutil
from tqdm import tqdm
from datetime import datetime
from joblib import Parallel, delayed
from concurrent.futures import ThreadPoolExecutor
from joblib import Parallel, delayed
from config import *



def split_dataset(df, val_size=0.1, test_size=0.2, random_state=123, stratify_by=None):
    """Split dataset into train, validation, and test sets.

    Args:
        df: Dataframe to split.
        val_size: Size of the validation set.
        test_size: Size of the test set.
        random_state: Random state for reproducibility.
        stratify_by: Stratify by column name.

    Returns:
        Tuple of train, validation, and test sets.
    """
    # Ensure stratify_by is a valid column
    if stratify_by not in df.columns:
        stratify_by = None

    # Adjust val_size to reflect the proportion of the remaining dataset after test split
    val_size_adjusted = val_size / (1 - test_size)

    # Splitting the dataset into training + validation and test sets
    train_val_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[stratify_by] if stratify_by else None
    )

    # Splitting the training + validation set into training and validation sets
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_size_adjusted,
        random_state=random_state,
        stratify=train_val_df[stratify_by] if stratify_by else None
    )

    return train_df, val_df, test_df


def process_image_group(object_group, new_dataset_path):
    orig_image_path = object_group[0]
    label_matrix = object_group[1][["cat_id", "x_center_norm", "y_center_norm", "width_norm", "height_norm"]].values
    image_name = object_group[1]["img_file"].values[0]

    # copy image
    new_image_path = os.path.join(new_dataset_path, "images", image_name)
    if not os.path.exists(os.path.dirname(new_image_path)):
        os.makedirs(os.path.dirname(new_image_path))
    shutil.copy(orig_image_path, new_image_path)

    # create label file (yolo format) .txt
    new_label_path = os.path.join(new_dataset_path, "labels", os.path.splitext(image_name)[0] + ".txt")
    if not os.path.exists(os.path.dirname(new_label_path)):
        os.makedirs(os.path.dirname(new_label_path))

    #print(" > new_label_path: ", new_label_path)
    with open(new_label_path, "w") as f:
        for label in label_matrix:
            f.write("{} {} {} {} {}\n".format(int(label[0]), float(label[1]), float(label[2]), float(label[3]), float(label[4])))

def process_images(df, new_dataset_path, df_name):
    object_groups = df.groupby("path")
    for object_group in tqdm(object_groups, desc=f"Processing {df_name} dataset"):
        process_image_group(object_group, os.path.join(new_dataset_path, df_name))

def process_images_parallel(df, new_dataset_path, df_name, n_jobs=-1):
    # create folders
    if not os.path.exists(os.path.join(new_dataset_path, df_name, "images")):
        os.makedirs(os.path.join(new_dataset_path, df_name, "images"))
    if not os.path.exists(os.path.join(new_dataset_path, df_name, "labels")):
        os.makedirs(os.path.join(new_dataset_path, df_name, "labels"))

    object_groups = df.groupby("path")
    Parallel(n_jobs=n_jobs)(delayed(process_image_group)(object_group, os.path.join(new_dataset_path, df_name)) for object_group in tqdm(object_groups, desc=f"Processing {df_name} dataset"))

def generate_data_yaml(new_dataset_path : str, classes : dict):
    # train
    with open(os.path.join(new_dataset_path, "data.yaml"), "w") as f:
        f.write("train: ../train/images\n")
        f.write("val: ../val/images\n")

        f.write("nc: {}\n".format(len(classes)))
        f.write("names:\n")
        for class_id, class_name in classes.items():
            f.write(f"  {class_id}: {class_name}\n")

    print(" > data.yaml generated")



def main_data_processing_yolo_format():
    TACO_DATASET_ROOT_PATH = r"N:\My Drive\KESKIA Drive Mlamali\datasets\taco-2gb"
    YYYYMMDDHH = datetime.now().strftime("%Y%m%d_%H")

    taco_meta_df = pd.read_csv(os.path.join(TACO_DATASET_ROOT_PATH, "meta_df.csv"))

    taco_meta_df["path"] = taco_meta_df["img_file"].apply(lambda x: os.path.join(TACO_DATASET_ROOT_PATH, "data", x))

    # add new img file path (replace '/' by '_')
    taco_meta_df["img_file"] = taco_meta_df["img_file"].apply(lambda x: x.replace("/", "_"))

    # Calcul et ajout des nouvelles colonnes normalisées
    taco_meta_df['x_center_norm'] = (taco_meta_df['x'] + taco_meta_df['width'] / 2) / taco_meta_df['img_width']
    taco_meta_df['y_center_norm'] = (taco_meta_df['y'] + taco_meta_df['height'] / 2) / taco_meta_df['img_height']
    taco_meta_df['width_norm'] = taco_meta_df['width'] / taco_meta_df['img_width']
    taco_meta_df['height_norm'] = taco_meta_df['height'] / taco_meta_df['img_height']

    # process cat_id
    taco_meta_df["cat_id"] = taco_meta_df["cat_name"].apply(lambda x: CATNAME_TO_IDX_MAP[x])
    # Example usage
    train_df, val_df = train_test_split(
        taco_meta_df,
        test_size=0.15,
        random_state=123,
        stratify=taco_meta_df["supercategory"] # we can't stratify by cat_name because : the least populated class in y has only 1 member, which is too few. The minimum number of groups for any class cannot be less than 2.
    )
    #train_df = train_df.head(50)
    #val_df = val_df.head(50)
    print(f"train_df: {len(train_df)} ({len(train_df) / len(taco_meta_df) * 100:.1f}%)")
    print(f"val_df: {len(val_df)} ({len(val_df) / len(taco_meta_df) * 100:.1f}%)")

    # Vos chemins de fichiers et autres configurations initiales restent inchangés
    # Sequential processing of the datasets
    print(" > Launching processing of the datasets")
    NEW_TACO_DATASET_PATH = f"{os.path.dirname(TACO_DATASET_ROOT_PATH)}/taco-yolo-format train-{len(train_df)}-val-{len(val_df)} {YYYYMMDDHH}"
    print(f" > New dataset path: {NEW_TACO_DATASET_PATH}")
    process_images_parallel(train_df, NEW_TACO_DATASET_PATH, "train")
    process_images_parallel(val_df, NEW_TACO_DATASET_PATH, "val")
    print(f" > Done. New dataset path: {NEW_TACO_DATASET_PATH}")
    generate_data_yaml(NEW_TACO_DATASET_PATH, classes=IDX_TO_CATNAME_MAP)

if __name__ == "__main__":
    main_data_processing_yolo_format()
