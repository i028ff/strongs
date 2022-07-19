from unittest import result
from flask import Flask, render_template
import googlemaps
import pprint

app = Flask(__name__)

@app.route('/')

def getapi():
    key = 'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM' # 上記で作成したAPIキーを入れる
    client = googlemaps.Client(key) #インスタンス生成
    loc = {'lat': 33.9563797, 'lng': 131.2725447} # 軽度・緯度を取り出す
    place_results = client.places_nearby(location=loc, radius=100000, keyword='カフェ',language='ja') #半径10000m以内のカフェ情報を取得
    #pprint.pprint(place_results)
    results = []
    photos = []
    for place_result in place_results['results']:
        if 'photos' in place_result.keys():
            results.append(place_result)
        
            #p_value = results['photos'][0]
            #photos_photo_reference = p_value['photo_reference']
            #print.pprint(photos_photo_reference)
            #photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(photos_photo_reference,str(app.config['AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM']))
            #配列に追加 
            #photos.append(photo)
            
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,'AIzaSyCqmC20D0M_x4rrJyAMgdvJaY7-4cXYNBM')
            photos.append(photo)

    pprint.pprint(photos)
    #print(results)
    return render_template('getapi2.html',result=results,photos=photos)

if __name__=='__main__':
    app.run(debug=True)
