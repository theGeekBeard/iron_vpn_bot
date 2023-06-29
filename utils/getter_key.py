import os, random

from loader import db


async def get_key(tariff):
    tariff = await db.get_tariff(tariff)
    tariff_id = tariff[0]["id"]
    tariff_name = tariff[0]["name"]
    path = f"data/vpns/{tariff_name}/"
    config_path = path + "config/"
    qr_code_path = path + "qr_code/"

    try:
        listdir = os.listdir(config_path)

        if not listdir:
            return False

        filename = listdir[0]
        image_name = filename.split(".")[0] + ".jpg"

        file_path = config_path + filename
        image_path = qr_code_path + image_name

        result = {"file_path": file_path, "image_path": image_path}
        if tariff_id == 4:
            if len(listdir) <= 1:
                return False

            filename2 = listdir[1]
            image_name2 = filename2.split(".")[0] + ".jpg"

            file_path2 = config_path + filename2
            image_path2 = qr_code_path + image_name2

            result2 = {"file_path2": file_path2, "image_path2": image_path2}
            result.update(result2)
        return result
    except:
        return False
