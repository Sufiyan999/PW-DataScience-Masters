from flask import Flask, render_template, request,jsonify,send_file
from flask_cors import CORS,cross_origin
import requests
import logging
import os
import re
import pandas as pd
import json 
from utils import  create_bokeh_plot , views_to_numeric , save_to_csv_file, get_from_csv_file , get_json_by_csv
from utils import figure, output_file, show
import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(BASE_DIR, "scrapper.log") , level=logging.INFO)

app = Flask(__name__)
query = None

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
            global query     
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
            print("min fethed videoes : " , min_video_count)
            
            for i in range(min_video_count):
                try:
                    temp = []
                    temp.append(i+1)
                    temp.append('https://www.youtube.com/watch?v=' + videoids[i].split('"')[-2])
                    temp.append(thumbnails[i].split('"')[-2])
                    temp.append(titles[i].split('"')[-2])
                    temp.append(views[i].split('"')[-2].split()[-2])
                    temp.append(published_time[i].split('"')[-2])
                    
                    report_list.append(temp)
                    
                except Exception as e:
                        print(e)
                        continue
                    
            # print(report_list)     
            save_to_csv_file(report_list)
            return render_template('result.html', report_list=report_list, channel=query)

        except UnicodeEncodeError as e:
                save_to_csv_file(report_list)
                return render_template('result.html', report_list=report_list, channel=query)
            
        except Exception as e:
            logging.info(e)
            query = request.form['content']
            return f'something is wrong with {query}' +'\n\n' + f'{str(e)}' 
        
    if request.method == 'GET':
        print('GET')
        
        report_list = get_from_csv_file()
        print(len(report_list) , len(report_list[0]))
        return render_template('result.html', report_list=report_list, channel=query)
    
    else:
        return render_template('index.html')




@app.route('/download')
@cross_origin()
def download_file():
    filename = 'scrapped_data.csv'

    csv_file = filename 
    df = pd.read_csv(csv_file)

    excel_file = 'scrapped_data.xlsx'  

    df["fetch time"]  =  (datetime.datetime.now().isoformat(),)*df.shape[0]
    df["Numeric Views"] = df["Views"].apply(views_to_numeric) 
    
    df.to_excel(excel_file, index=False)  
    
    return send_file( excel_file , as_attachment=True)


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
def show_videos():
    
    report_list = get_from_csv_file()[1:]
    video_urls = [] 
    if not bool(report_list):
        return "NO URLS WERE FOUND"
    for row in report_list:
        try: 
            video_urls.append(row[1].split("=")[-1])       
        except:            
           continue 
    
    return render_template('videos.html', video_urls=video_urls)
                   
                    
@app.route('/json',methods = ['POST' , 'GET'])
@cross_origin()
def json_renderer():
   
        dic = get_json_by_csv()
        return jsonify(dic)
         


@app.route('/JSON',methods = ['POST' , 'GET'])
@cross_origin()
def JSON_FILE():
    
     file_name = "scrapped_data.json"
    
     with open( file_name , "w") as fileobj:
         json.dump( get_json_by_csv(), fileobj ) 
         
     return send_file( file_name , as_attachment=True)

  
  

@app.route('/visualize')
def visualize():
    df  = pd.read_csv("scrapped_data.csv")
    p = create_bokeh_plot(df)
    output_file("static/bokeh_plot_with_hover_and_image.html")
    show(p)
    return render_template('bokeh.html', script=p)   
                    
                    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    #"D:\Softwares\Anaconda\Scripts\activate.bat"













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
"https://www.youtube.com/watch?v=b8u0bZpiA4I".split("=")[-1]
# %%

# %%
