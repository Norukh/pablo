import copy
import csv
import json
from os import listdir
from os.path import isfile, join

def get_paintings(artist_name):
    artist_path = "../static/images/original/" + artist_name
    return ["/static/images/resized/" + f.title() for f in listdir(artist_path) if isfile(join(artist_path, f))]


def csv_to_json():
    jsonArray = []

    with open('artists.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            row["paintings"] = get_paintings(row["name"].replace(" ", "_"))
            row["genre"] = row["genre"].split(",")

            jsonArray.append(row)

    with open('artists.json', 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


def artist_json_to_model():
    with open('artists.json') as dataf, open('output.json', 'w') as out:
        data = json.load(dataf)
        newdata = []
        for i, block in enumerate(data):
            new = dict(model="pablo_app.Artist", pk=block["id"])
            new["fields"] = dict(
                name=block["name"],
                years=block["years"],
                nationality=block["nationality"],
                bio=block["bio"],
                wikipedia=block["wikipedia"],
                genre=",".join(block["genre"]),
            )

            newdata.append(copy.deepcopy(new))
        json.dump(newdata, out, indent=2)


def painting_json_to_model():
    with open('artists.json') as dataf, open('output-paintings.json', 'w') as out:
        data = json.load(dataf)
        newdata = []
        for i, block in enumerate(data):
            for painting in block["paintings"]:
                new = dict(model="pablo_app.Painting")
                new["fields"] = dict(
                    path=painting,
                    artist=int(block["id"])
                )

                newdata.append(copy.deepcopy(new))
        json.dump(newdata, out, indent=2)


if __name__ == "__main__":
    painting_json_to_model()