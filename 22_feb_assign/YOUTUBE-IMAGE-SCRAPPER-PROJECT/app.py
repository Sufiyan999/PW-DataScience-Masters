from flask import Flask, render_template, request,jsonify,send_file
from flask_cors import CORS,cross_origin
import requests
from urllib.request import urlopen as uReq
import logging
import pymongo
import os
import shutil
import re
import csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(BASE_DIR, "scrapper.log") , level=logging.INFO)

app = Flask(__name__)

print("Youtube Scrap")
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
                      
            query = request.form['content'].replace(" ","")
            
            # fake user agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

            # fetch the search results page
            response = requests.get(f"https://www.youtube.com/@{query}/videos", headers=headers)
            res = response.text

            # Video
            videoids = re.findall('"videoRenderer":{"videoId":".*?"', res)
            # thumbnail
            thumbnails = re.findall('"thumbnail":{"thumbnails":\[{"url":".*?"', res)
            # Title
            titles = re.findall('"title":{"runs":\[{"text":".*?"', res)
            # Views
            views = re.findall('"shortViewCountText":{"accessibility":{"accessibilityData":{"label":".*?"', res)
            # Published Time
            published_time = re.findall('"publishedTimeText":{"simpleText":".*?"', res)
            
            print(views)
            
            report_list = [
                ['S No', 'Video url', 'Thumbnail', 'Title', 'Views', 'Published Time']
            ]
            
            print(videoids)
            # if len(videoids) > 0:
            for i in range(20):
                try:
                    temp = []
                    temp.append(i+1)
                    temp.append('https://www.youtube.com/watch?v=' + videoids[i].split('"')[-2])
                    temp.append(thumbnails[i].split('"')[-2])
                    temp.append(titles[i].split('"')[-2])
                    temp.append(views[i].split('"')[-2])
                    temp.append(published_time[i].split('"')[-2])
                    
                    report_list.append(temp)
                    
                except Exception as e:
                        print(e)
                        continue
                    
            print(report_list)     
            save_to_csv_file(report_list)
            return render_template('result.html', report_list=report_list, channel=query)

        except UnicodeEncodeError as e:
                save_to_csv_file(report_list)
                return render_template('result.html', report_list=report_list, channel=query)
            
        except Exception as e:
            print(e.__class__)
            print(type(e))
            logging.info(e)
            query = request.form['content']
            return f'something is wrong with {query}' +'\n\n' f'{str(e)}' 
    else:
        return render_template('index.html')


@app.route('/download')
def download_file():
    filename = 'temp.csv'
    return send_file(filename, as_attachment=True)


def save_to_csv_file(report_list):
            file_name = os.path.join(BASE_DIR,  'scrapped_data.csv')
            with open(file_name, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in report_list:
                    try:
                        csvwriter.writerow(row)
                    except:                # UnicodeEncodeError ,because of these 🔥🔥 in the title row[3]    
                        # print(row[3])  
                        row[3] = row[3].encode('utf-8')
                        # print(row[3])  
                        csvwriter.writerow(row)
                        continue

def get_from_csv_file():
            temp = []
            file_name = 'scrapped_data.csv' 
            file_name = os.path.join(BASE_DIR,  file_name)
            with open(file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                  temp.append(row)                  
            return temp     

@app.route('/Thumbnail',methods = ['POST' , 'GET'])
def show_thumbs():
    temp = get_from_csv_file()[1:]
    if not bool(temp):
        return "NO IMAGES WERE FOUND"
    
    img_urls = [] 
    for row in temp:
       try: 
             img_urls.append(row[2]) 
       except:
           continue 
    print(img_urls)    
    return render_template('imgs.html', img_urls=img_urls)

@app.route('/Video url',methods = ['POST' , 'GET'])
def show_urls():
    temp = get_from_csv_file()[1:]
    video_urls = [] 
    if not bool(temp):
        return "NO URLS WERE FOUND"
    for row in temp:
        video_urls.append(row[1])       
        
    print(video_urls)    
    return jsonify({"urls": video_urls})
                    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)




























# temp =get_from_csv_file()
#             return render_template('result.html', report_list=temp, channel=query)