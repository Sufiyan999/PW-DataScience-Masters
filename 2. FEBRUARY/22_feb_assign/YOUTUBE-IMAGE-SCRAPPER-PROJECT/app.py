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
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            # return show_urls()       
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
            
           
            
            report_list = [
                ['S No', 'Video url', 'Thumbnail', 'Title', 'Views', 'Published Time']
            ]
            
            min_video_count = min(len(videoids) , len( thumbnails) , len(published_time) , len( titles) , len( views))
            print(min_video_count)
            for i in range(min_video_count):
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
            logging.info(e)
            query = request.form['content']
            return f'something is wrong with {query}' +'\n\n' + f'{str(e)}' 
    else:
        return render_template('index.html')




@app.route('/download')
@cross_origin()
def download_file():
    filename = 'scrapped_data.csv'
    return send_file(filename, as_attachment=True)


def save_to_csv_file(report_list):
            file_name = os.path.join(BASE_DIR,  'scrapped_data.csv')
            with open(file_name, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in report_list:
                    try:
                        csvwriter.writerow(row)
                    except:                                         # UnicodeEncodeError ,because of these 🔥🔥 in the title row[3]     
                        row[3] = row[3].encode('utf-8') 
                        csvwriter.writerow(row)
                        continue

def get_from_csv_file():
            report_list = []
            file_name = 'scrapped_data.csv' 
            file_name = os.path.join(BASE_DIR,  file_name)
            with open(file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                  report_list.append(row)                  
            return report_list    

@app.route('/Thumbnail',methods = ['POST' , 'GET'])
@cross_origin()
def show_thumbs():
    report_list = get_from_csv_file()[1:]
    if not bool(report_list):
        return "NO IMAGES WERE FOUND"
    
    img_urls = [] 
    for row in report_list:
       try: 
             img_urls.append(row[2]) 
       except:
           continue  
    return render_template('imgs.html', img_urls=img_urls)

@app.route('/Video url',methods = ['POST' , 'GET'])
@cross_origin()
def show_urls():
    report_list = get_from_csv_file()
    video_urls = [] 
    if not bool(report_list):
        return "NO URLS WERE FOUND"
    for row in report_list:
        try: 
            video_urls.append(row[1])       
        except:            
           continue  
#   binary_string = "b'Best Way To Start Class -9th English \xf0\x9f\x92\xa5 || Master Strategy Plan || Follow this \xe2\x9a\xa1\xe2\x9a\xa1'"
# normal_string = binary_string.encode('utf-8').decode('unicode-escape')
# print(normal_string)

    return jsonify({"urls": video_urls})
                    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)








#In[]:
binary_string = "b'Best Way To Start Class -9th English \xf0\x9f\x92\xa5 || Master Strategy Plan || Follow this \xe2\x9a\xa1\xe2\x9a\xa1'"
print(binary_string.encode('utf-8'))
# print(binary_string.decode('unicode-escape'))
normal_string = binary_string.encode('utf-8').decode('unicode-escape')
print(normal_string)

# %%
print(normal_string)
# %%
b'this' + 'class'
# %%

binary_string = "b'Best Way To Start Class -9th English \xf0\x9f\x92\xa5 || Master Strategy Plan || Follow this \xe2\x9a\xa1\xe2\x9a\xa1'"
print(binary_string.encode('utf-8'))
# print(binary_string.decode('unicode-escape'))
normal_string = binary_string.encode('utf-8').decode('unicode')
print(normal_string)

# %%
