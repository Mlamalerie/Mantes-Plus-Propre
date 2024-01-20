import requests
import json
import pandas as pd
import replicate
from IPython.display import Image
import os
# load env
from dotenv import load_dotenv
from tqdm import tqdm
from typing import List, Dict, Optional
from src.detection.category_utils import CATIDX_2_EN_CATNAME
from pydantic import BaseModel, Field
from datetime import datetime
import io

load_dotenv()


class DetectedDechet(BaseModel):
    photo: List[dict] = Field(..., description="List of photos.")
    cat_idxs: Optional[List[int]] = Field(None, description="List of classes names.")
    cat_idx_occurences: str = Field(..., description="Occurences of each class. Exemple: {58: 1, 4: 2, 22: 1}")
    longitude: str = Field(..., description="Longitude.")
    latitude: str = Field(..., description="Latitude.")
    status: int = Field(1266082, description="Status.")
    description: Optional[str] = Field(None, description="Description.")



class BaserowTable:
    def __init__(self, table_id: int):
        self.table_id = table_id

    def __make_req(self, url, method="GET", verbose=False, **kwargs):
        """
        Make a request
        """
        # check if headers are passed
        if "headers" not in kwargs:
            kwargs["headers"] = {
                "Authorization": f"Token {os.environ['BASEROW_DB_API_TOKEN']}"
            }
        else:
            kwargs["headers"]["Authorization"] = f"Token {os.environ['BASEROW_DB_API_TOKEN']}"
        r = requests.request(method, url, **kwargs)
        if r.status_code == 200:
            print("Success!") if verbose else None
        else:
            raise Exception("Error!", f"{r.status_code} {r.text}")

        return r.json()

    def get_fields(self):
        """
        Get all fields from the dechets table, like photo, names, classes_names, status, etc.
        """
        return self.__make_req(
            f"https://api.baserow.io/api/database/fields/table/{self.table_id}/?user_field_names=true")

    # list rows
    def get_list_rows(self, page: int = None, size: int = None, search: str = None):
        """
        To list rows in the table.

        Args:
            page (int, optional): Page number. Defaults to None.
            size (int, optional): Number of rows per page. Defaults to None.
            search (str, optional): Search string. Defaults to None.
        """
        url = f"https://api.baserow.io/api/database/rows/table/{self.table_id}/?user_field_names=true"
        if page is not None:
            url += f"?page={page}"
        if size is not None:
            url += f"&size={size}"
        if search is not None:
            url += f"&search={search}"

        return self.__make_req(url)["results"]

    # recursive function to get all rows
    def get_list_all_rows(self, search: str = None):
        """
        To list all rows in the table.

        Args:
            search (str, optional): Search string. Defaults to None.
        """

        r = self.__make_req(f"https://api.baserow.io/api/database/rows/table/{self.table_id}/?user_field_names=true")
        results = r["results"]
        while r["next"] is not None:
            r = self.__make_req(r["next"])
            results += r["results"]

        return results

    def get_row(self, row_id: int):
        url = f"https://api.baserow.io/api/database/rows/table/{self.table_id}/{row_id}/?user_field_names=true"
        return self.__make_req(url)

    # create row
    def create_row(self, data: dict):
        url = f"https://api.baserow.io/api/database/rows/table/{self.table_id}/?user_field_names=true"
        return self.__make_req(url, method="POST", json=data, headers={"Content-Type": "application/json"})

    def update_row(self, row_id: int, data: dict):
        pass

    def upload_file(self, file: tuple):

        url = "https://api.baserow.io/api/user-files/upload-file/"
        files = {
            "file": file
        }
        return self.__make_req(url, method="POST", files=files)

    def upload_file_from_path(self, file_path: str):
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} does not exist.")

        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1]
        return self.upload_file(file=(file_name, open(file_path, "rb"), f"image/{ext}"))


class DechetsTable(BaserowTable):
    def __init__(self, table_id: int = 244285):
        super().__init__(table_id=table_id)

        self.status_options_id_dict = {option["id"]: option["value"] for option in
                                       self.get_field_info_by_name("status")[
                                           "select_options"]}  # {1212366: 'Ramassé 😊', 1212367: 'Toujours là', 1213480: "Ceci n'est pas un déchets"}

    def get_field_info_by_name(self, name: str):
        for field in self.get_fields():
            if field["name"] == name:
                return field
        return None

    def generate_description_with_ai(self, image: str | bytes, cat_idx_occurences: Optional[Dict[int,int]] = None, verbose: bool = False):
        """
        Use AI to generate a description of the image.

        Args:
            image : Path to the image or file object. (image = open("mystery.jpg", "rb") or image = "https://example.com/mystery.jpg")
        """

        if not isinstance(image, str) and not isinstance(image, bytes):
            raise Exception("Image must be a path to the image or a file object.")

        if cat_idx_occurences is None:
            VIZ_MODEL_PROMPT = """what do you see in this picture? Generate a description of no more than 50 words. If you see garbage, please specify all the type of garbage you see. A simple but complete answer in French."""
        else:
            dechets_occurences_text : str = ", ".join([f"{occurence} {CATIDX_2_EN_CATNAME[cat_idx]}" for cat_idx, occurence in cat_idx_occurences.items()])
            VIZ_MODEL_PROMPT = f"""what do you see in this picture? I see {dechets_occurences_text} in this picture. Generate a description of no more than 50 words. If you see others garbage, please specify all the type of garbage you see. A simple but complete answer in French. """

        model_name: str = "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358"


        output_desc = replicate.run(
            model_name,
            input={
                "image": image,
                "top_p": 1,
                "prompt": VIZ_MODEL_PROMPT,
                "max_tokens": 120,
                "temperature": 0.2
            }
        )
        return " ".join(output_desc)

    def add_dechet_row(self, image: str | bytes, cat_idx_occurences: Dict[int,int], longitude: str, latitude: str,
                       description: str = None,
                       generate_description: bool = False, use_occurences_for_description: bool = False,
                       verbose: bool = False):
        if verbose:
            print(f">>>> Adding dechet row to Baserow DB ({self.table_id})...")
            print(f"> Uploading image to Baserow DB...")
        # 1. Upload file

        if isinstance(image, str):
            image_uploaded = self.upload_file_from_path(image)
        elif isinstance(image, bytes):
            image_uploaded = self.upload_file(file=("mystery.jpg", image, "image/jpeg"))
        else:
            raise Exception("Image must be a path to the image or a file object.")

        # 2. Generate description
        if description is None and generate_description:
            if verbose:
                print(f"> Generating description with AI...")
            description: str = self.generate_description_with_ai(image_uploaded["url"], cat_idx_occurences if use_occurences_for_description else None, verbose=verbose)

        detected_dechet: DetectedDechet = DetectedDechet(
            photo=[{"name": image_uploaded["name"]}],
            cat_idxs=[cat_idx + 1 for cat_idx in cat_idx_occurences.keys()],
            cat_idx_occurences=json.dumps(cat_idx_occurences),
            longitude=longitude,
            latitude=latitude,
            description=description,
        )
        if verbose:
            print(f"> Ok. Creating row in Baserow DB...")
        return super().create_row(data=detected_dechet.model_dump())


if __name__ == "__main__":
    DECHETS_TABLE_ID = 244285

    cat_table = BaserowTable(table_id=235215)

    table_manager = DechetsTable(table_id=DECHETS_TABLE_ID)
    # get all rows
    rows = table_manager.get_list_all_rows()

    # fields
    fields = table_manager.get_fields()

    file_path = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\egoblur_demo\mantes (18).jpg"
    # uploaded_result = table_manager.upload_file_from_path(file_path)

    # uploaded_result2 = table_manager.upload_file(file=("mantes (test).jpg", open(file_path, "rb").read(), "image/jpeg"))
    exit(0)
    # add row
    response = table_manager.add_dechet_row(image=file_path, cat_idx_occurences={58: 10, 4: 2, 22: 10}, longitude="1.234",
                                 latitude="2.345", generate_description=True, verbose=True)

    response
    print("end.")
