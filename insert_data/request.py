import requests

# get all file in csv folder
import os
import pandas as pd

# get list of file in data folder
list_file = os.listdir("./csv")

for index, file in enumerate(list_file):

    FILE_NAME = file.split(".")[0]
    # delete the String "Machine_learing" in file name
    FILE_NAME = FILE_NAME.replace("Machine_learing", "")
    print(f"{index+1}. {FILE_NAME}")

    # read csv file

    df = pd.read_csv(f"./csv/Machine_learing{FILE_NAME}.csv")

    # # register with POST

    # register_url = "http://localhost:5000/api/v1/auth/register"

    # # random birthday from 1990 to 2001
    # import random
    # import datetime

    # start_date = datetime.date(1990, 1, 1)
    # end_date = datetime.date(2001, 1, 1)

    # time_between_dates = end_date - start_date
    # days_between_dates = time_between_dates.days
    # random_number_of_days = random.randrange(days_between_dates)
    # random_date = start_date + datetime.timedelta(days=random_number_of_days)
    # birthday = random_date.strftime("%Y-%m-%d")

    # payload = {
    # "email": f"{FILE_NAME}@gmail.com",
    # "password": "12345678",
    # "fullname": "Đen Vâu",
    # "birthday": birthday,
    # "username": FILE_NAME,
    # }

    # register_response = requests.post(register_url, json=payload)
    # print(register_response.json())

    
    # login to the http://localhost:5000/api/v1/auth/login with POST and get the token in cookie

    # get the token from cookie with POST
    url = "http://localhost:5000/api/v1/auth/login"
    payload = {"username": FILE_NAME, "password": "12345678"}

    response = requests.post(url, json=payload)

    print(response.status_code)

    token = response.json()["token"]

    # POST /post/create create post with json

    post_url = "http://localhost:5000/api/v1//post/create-link"

    # create a dict
    data = {
        "content": "Hello world",
        "link": {
            "url": ["https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Hawaiian_Banana.jpg/330px-Hawaiian_Banana.jpg"],
            "type":"image"
        }
    }

    header  = {"Authorization": f"Bearer {token}"}

    def createPost():
        response = requests.post(post_url, json=data, headers=header)
        return response.json()


    # Read data from csv file
    def checkLink(link):
    # check if link have domain like this: "https://m.facebook.com" return False
        if "https://m.facebook.com" in link:
            return False
        else:
            return True

    import ast
    count = 0
    # # each row create request
    for index, row in df.iterrows():
        try:            
            data_url = []
            type_data = "image"

            # put the images and images_lowquality first in if else
            if row["images"] is not None:
                # convert string to list
                images_link = ast.literal_eval(row["images"])
                # check if link have domain like this: "https://m.facebook.com"
                if checkLink(str(images_link)):
                    data_url = images_link

            elif row["images_lowquality"] is not None:
                data_url = ast.literal_eval(row["images_lowquality"])
            elif row["image"] is not None and checkLink(str(row["image"])):
                data_url = [row["image"]]
            elif row["image_lowquality"] is not None:
                data_url = [row["image_lowquality"]]
            if row["video"] is not None and data_url == []:
                data_url = [row["video"]]
                type_data = "video"

            data = {
                "content": row["content"],
                "created_at": row["created_at"],
                "link": {
                    "url": data_url,
                    "type":type_data
                }
            }
            response = requests.post(post_url, json=data, headers=header)
            print(response.json())

            count += 1
            print(f"Request {count}/{df.shape[0]} ")
        except:
            pass
        
