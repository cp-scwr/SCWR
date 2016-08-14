import json

para = "gmail:aitrinh2312@yahoo.com"
gmail = para[6:]
with open("editor.json", "r+") as jsonFile:
    data = json.load(jsonFile)

    tmp = data["gmail"]
    data["min_motion_frames"] = 2

    jsonFile.seek(0)  # rewind
    jsonFile.write(json.dumps(data))
    jsonFile.truncate()
