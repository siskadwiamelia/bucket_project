from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://siskadwiamelia:06092002@ac-pf1qu7v-shard-00-00.h8mgzk5.mongodb.net:27017,ac-pf1qu7v-shard-00-01.h8mgzk5.mongodb.net:27017,ac-pf1qu7v-shard-00-02.h8mgzk5.mongodb.net:27017/?ssl=true&replicaSet=atlas-fnbeyo-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']     # Mengekstrak beberapa form informasi dari sisi client
    count = db.bucket.count_documents({})            # identifikasi unik untuk setiap item bucket list
    num = count + 1                                  # Menyambungkan num pada setiap dokumen baru
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = int(request.form['num_give'])
    db.bucket.delete_one(
        {'num': (num_receive)},
    )
    return jsonify({'msg': 'Item deleted!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)