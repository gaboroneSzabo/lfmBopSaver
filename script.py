import requests
import json

LFM_BOP_URL = "https://api2.lowfuelmotorsport.com/api/hotlaps/getBopPrediction"

def main():
    tracks = load_tracks()

    pretty_names = list(map(lambda x: ("track id: %s" % x["track_id"], x["track_name"]), tracks))
    track_id = int(input("choose a track id: %s" % (pretty_names)))
    
    for current in tracks:
        if (current['track_id'] == track_id):
            track = current['track_name_id']

    data = download_track_data(track_id)
    bop = create_bop(data, track)

    write_bop_file(bop)
    
        
def write_bop_file(bop):
    with open("bop.json", "w") as json_file:
        json.dump(bop, json_file)

def load_tracks():
    with open('tracks.json', 'r') as f:
        return json.load(f)
    
def load_dummydata():
    with open('dummy.json', 'r') as f:
        return json.load(f)  

def create_bop_entrie(raw_data, track):
    result = []
    for bop_data in raw_data:
        row = {}
        row['track'] = track
        row['carModel'] = bop_data['car_id']
        row['ballastKg'] = int(bop_data['bop'])
        row['restrictor'] = 0
        result.append(row)
    return result

def create_bop(data, track):
    relevant = create_bop_entrie(data['laps_relevant'], track)
    other = create_bop_entrie(data['laps_others'], track)
    
    bop = {'entries' : []}

    for current in relevant:
        bop['entries'].append(current)

    for current in other:
        bop['entries'].append(current)
    return bop

def download_track_data(track_id):
    url = LFM_BOP_URL + "?track=%d" % track_id
    return download_json(url)

def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Error: Unable to fetch data from URL")
        return None


if __name__ == "__main__":
    main()