import requests
import json

if __name__ == '__main__':
    data = {
        'data': {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
        }
    }

    json_data = json.dumps(data,indent=4)
    r = requests.get("http://127.0.0.1:5000/api/get_duration", json=json_data)
    print(r.content)