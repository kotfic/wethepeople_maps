import pandas as pd
from pyzipcode import ZipCodeDatabase
from api import api
import json

JSON_FILE = "data/{}_sigs.json"

pro_petitions = ["50cb6501c988d49b7800000b",
                 "50cb6d2ba9a0b1c52e000017",
                 "50cb7200adfd95590e000001",
                 "50cb73680aa04d993b000015",
                 "50cb7488eab72abb7e000001",
                 "50cb75e32bcfa3ee40000003",
                 "50cb7dafc988d40545000000",
                 "50cb80550aa04dd55e000003",
                 "50cd07126ce61ce80700001f",
                 "50cd2fd8704301943a000007",
                 "50cf5d0d0aa04d4b28000007",
                 "50cf9dc42f2c88eb71000001"]

anti_petitions = ["50cb7553704301d569000011",
                  "50cb96be2bcfa31354000014",
                  "50cba05ceab72a4c1f000018",
                  "50cbb7dfb15a7a740d000007",
                  "50cbc221cde5b8d309000003",
                  "50cbcf8700e579d95e000015",
                  "50cbd3b90aa04d6369000016",
                  "50cbe2196ce61ceb0c000011",
                  "50cc6206b15a7a9849000008",
                  "50cd2a1f7043013e2000000b",
                  "50cddd112bcfa39404000008",
                  "50ce2ea36889384429000017",
                  "50ce9674eab72ab102000000",
                  "50ceb247ee140fe937000010",
                  "50ced0ed6ce61c0a65000016",
                  "50cf53c4b15a7a3f27000012",
                  "50cf71e1adfd95a103000028",
                  "50cfb654b15a7aaf75000001",
                  "50cfeb21688938874a00000f",
                  "50d212bca9a0b17b2b00001f",
                  "50d47d37b15a7af10b000009"]

petition_ids = pro_petitions + anti_petitions

zcdb = ZipCodeDatabase()


def get_zip(code):
    try:
        return (zcdb[code].latitude, zcdb[code].longitude)
    except:
        return (None, None)


def geocode_zips(file_id):
    df = pd.read_json(JSON_FILE.format(file_id))
    df['lat'], df['lon'] = zip(*df['zip'].map(get_zip))
    df.dropna(subset=['lat']).to_csv("data/lat_lon_{}.csv".format(file_id),
                                     index=False)


if __name__ == "__main__":
    #    "530b81dd7043017077000009" - Baseball petition

    for pid in petition_ids:
        with open("data/{}.json".format(pid), "w") as h:
            h.write(json.dumps(api.get_petition(pid)))

        sigs = api.get_signature_collection(pid)
        with open(JSON_FILE.format(pid), "w") as h:
            h.write(json.dumps(sigs))

        geocode_zips(pid)
