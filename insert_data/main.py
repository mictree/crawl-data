#%%
import pandas as pd

#%% read xlsx file

# get list of filename in data folder
import os

# get list of file in data folder
list_file = os.listdir("./data")

for index, file in enumerate(list_file):
    print(f"{index+1}. {file}")
    print(f"{index+1}/{file}")
    print("--------------------------------------------------")

    FILE_NAME = file.split(".")[0]
    df = pd.read_excel(f"./data/{FILE_NAME}.xlsx", "Sheet1")
    
    # %% clean data
    # change collumn name
    df = df.rename(columns={"post_id": "id", "post_text": "content"})

    # drop row that have shared_text is not null
    df = df[df["shared_text"].isnull()]


    # create a dataframe with some collumn
    df = df[["id", "content","image_lowquality",
            "images_lowquality", "images_lowquality_description",
            "image", "images","images_description" , "video", "timestamp", "username"]]


    #%% transform to json

    # for each row in dataframe will transform to custom object
    def transform(row):
        # create a dict
        data = {}
        # add key and value to dict
        
        data["content"] = row["content"]
        # merge image, image_lowquality, images and images_lowquality to one column
        # if row["image_lowquality"] is not None:
        #     data["image"] = row["image_lowquality"]
        # elif row["images_lowquality"] is not None:
        #     data["image"] = row["images_lowquality"]
        # elif row["image"] is not None:
        #     data["image"] = row["image"]
        # elif row["images"] is not None:
        #     data["image"] = row["images"]
        # else:
        #     data["image"] = None

        data["image"] = row["image"]
        data["image_lowquality"] = row["image_lowquality"]
        data["images"] = row["images"]
        data["images_lowquality"] = row["images_lowquality"]
        data["images_description"] = row["images_description"]
        data["video"] = row["video"]
        data["username"] = row["username"]


        # merge image with video to one column 
        # as attach_file with additonal attribute type
        # if row["image"] is not None:
        #     # if image is array
        #     if isinstance(row["image"], list) is False:
        #         data["files.url[0]"] = row["image"]
        #     elif row["image"] is not None and row["image"].length > 0:
        #         for index, image in row["images"]:
        #             data[f"files.url[{index}]"] = image

        #     data["files.type"] = "image"
        # elif row["video"] is not None:
        #     data["files.url[0]"] = row["video"]
        #     data["files.type"] = "video"

        data["author"] = "64a4e00235de73389c5bfcb8"

        data["images_description"] = row["images_description"]
        data["video"] = row["video"]

        # transform timestamp to datetime
        data["created_at"] = pd.to_datetime(row["timestamp"], unit="s")
        # return dict
        return data

    # apply transform function to each row return dict
    df = df.apply(transform, axis=1, result_type="expand")

    df.to_json(f"./json/{FILE_NAME}.json", orient="records", lines=True)

    # %% save csv file
    df.to_csv(f"./csv/{FILE_NAME}.csv", index=False)
    print(f"Save {FILE_NAME}.csv success")
