from unicodedata import name
from unittest import result
from statistics import mean
from flask import Flask, render_template, url_for, request
import googlemaps
import pprint
import requests
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('getapi2.html',)

@app.route('/search_index', methods=['GET', 'POST'])
def search_index():
    if request.method == 'POST':
        word = request.form["word"]
        key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM' #APIキー
        print(word)
        #eo_request_ur1 = 'https://get.geojs.io/v1/ip/geo.json'
        #data = requests.get(geo_request_ur1).json()
        client = googlemaps.Client(key) #インスタンス生成
        loc = {'lat': 33.9564096, 'lng': 131.2706817} # 軽度・緯度を取り出す
        place_results = client.places_nearby(location=loc, radius=10000, keyword={word} ,language='ja') #半径1000m以内のカフェ情報を取得
        #pprint.pprint(place_results)
        results = []
        photos = []
        p_values = []
        for place_result in place_results['results']:
            results.append(place_result)
            # 配列にphotosが存在しないとき、NO IMAGE画像を表示。
            if not 'photos' in place_result.keys():
                photo = 'https://hamaotoko.com/wp-content/uploads/2020/09/img_0961-scaled-e1599991033270.jpg'
                photos.append(photo)
                p_values.append(p_value)
            else:
                p_value = place_result['photos'][0]['photo_reference']
                p_values.append(p_value)
                photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,key)
                photos.append(photo)
        return render_template('index.html',results=results,photos=photos,p_values=p_values)
    else:
        return render_templates('index.html')

@app.route('/detail/<string:id>/<p_ref>')
def detail(id,p_ref):
    key = 'AIzaSyD_j3p1GZ9FWKt5Do_yRBdi_FvIFgNgqyQ' #APIキー
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}".format(id,key)
    photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_ref,key)

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return render_template('detail.html',details=response,photo=photo)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__=='__main__':
    app.run(debug=True)
