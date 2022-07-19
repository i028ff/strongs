from unittest import result
from statistics import mean
from flask import Flask, render_template
import googlemaps
import pprint
import requests

app = Flask(__name__)

@app.route('/')
def index():
    key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM' # 上記で作成したAPIキーを入れる
    client = googlemaps.Client(key) #インスタンス生成
    loc = {'lat': 33.9563797, 'lng': 131.2725447} # 軽度・緯度を取り出す
    place_results = client.places_nearby(location=loc, radius=10000, keyword='麺',language='ja') #半径1000m以内のカフェ情報を取得
    #pprint.pprint(place_results)
    results = []
    photos = []
    for place_result in place_results['results']:
        results.append(place_result)
        # 配列にphotosが存在しないとき、NO IMAGE画像を表示。
        if not 'photos' in place_result.keys():
            photo = 'https://hamaotoko.com/wp-content/uploads/2020/09/img_0961-scaled-e1599991033270.jpg'
            photos.append(photo)
        else:
            #p_value = results['photos'][0]
            #photos_photo_reference = p_value['photo_reference']
            #print.pprint(photos_photo_reference)
            #photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(photos_photo_reference,str(app.config['AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM']))
            #配列に追加 
            #photos.append(photo)
            
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM')
            photos.append(photo)
    #pprint.pprint(results)
    #pprint.pprint(photos)
    #print(results)
    return render_template('index.html',results=results,photos=photos)

@app.route('/detail/<string:id>')
def detail(id):
    key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM' #APIキー
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+id+"&fields=name%2Crating%2Cformatted_phone_number%2Cformatted_address&key="+key
    #url = "https://maps.googleapis.com/maps/api/place/detailes/xml?key="+key+"&"+id
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return render_template('detail.html',detail=response)
if __name__=='__main__':
    app.run(debug=True)
