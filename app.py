from flask import Flask, request, send_file
import pandas as pd
import os
import csv

app = Flask(__name__)

@app.route('/save_data', methods=['POST'])
def save_data():
    data = {
        'user_id': request.form['user_id'],
        'object_name': request.form['object_name'],
        'object_description': request.form['object_description'],
        'deadline': request.form['deadline'],
        'location': request.form['location'],
        'photo_path': request.form['photo_path']
    }
    # save data to csv file
    file_exists = os.path.isfile('data.csv')
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    return 'Data saved successfully!'

@app.route('/get_data', methods=['GET'])
def get_data():
    object_name = request.args.get("object_name")
    print(object_name)
    # search for rows with the specified object_name
    df = pd.read_csv('data.csv')
    print(df.columns)
    filtered_df = df.loc[df['object_name'] == object_name]

    # return rows as string
    return filtered_df.to_dict()

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    name = request.form['photo_path']
    # save photo to photos folder
    photo.save(os.path.join('photos', name))
    return name

@app.route('/get_photo', methods=['GET'])
def get_photo():
    filename = request.args.get('filename')
    return send_file(f'photos/{filename}', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)