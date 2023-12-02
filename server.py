from flask import Flask, request, make_response
from simplexml import dumps 
from flask_restful import Api, Resource
from config import conn

# fungsi query database
def get_query(limit=100):
    cursor = conn.cursor()
    cursor.execute(f'select row_to_json(row) from (select mahasiswa.id, mahasiswa.nama, mahasiswa.nim, mahasiswa.fakultas, mahasiswa.prodi from mahasiswa) row limit {limit};')
    data = cursor.fetchall()
    return [x[0] for x in data]

# fungsi membuat output reponse bentuk XML dari API
def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response' : data}), code)
    resp.headers.extend(headers or {})
    return resp

# fungsi membuat output response bentuk JSON dari API
def output_json(data, code, headers=None):
    resp = make_response({'response' : data}, code)
    resp.headers.extend(headers or {})
    return resp

# konfigutasi FLASK API
app = Flask(__name__)
api = Api(app, default_mediatype='application/xml')

# baca request header Accept xml/json
api.representations['application/xml'] = output_xml
api.representations['application/json'] = output_json

# class Mahasiswa
class Mahasiswa(Resource):
    def get(self):
        limit = request.args.get('limit')
        data = get_query(limit)
        return { 'data': data }

# baca endpoint /mahasiswa
api.add_resource(Mahasiswa, '/mahasiswa')

# jalankan server
if __name__ == '__main__':
    app.run(port=3000, debug=False)
