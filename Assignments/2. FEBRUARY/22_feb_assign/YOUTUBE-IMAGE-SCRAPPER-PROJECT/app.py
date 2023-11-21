from flask import Flask, render_template, request,jsonify,send_file , redirect 
from flask_cors import CORS,cross_origin
import requests
import logging
import os
import re
import pandas as pd
import json 
from utils import  create_bokeh_plot , views_to_numeric , save_to_file, get_from_csv_file , get_json ,zip_images ,refine_list
from utils import figure, output_file, show
import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(BASE_DIR, "scrapper.log") , level=logging.INFO)

app = Flask(__name__)
query = None 
CSV_FILE_PATH = 'scrapped_data.csv'

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
            fetch_time = datetime.datetime.now().isoformat()
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
            relative_time = re.findall('"publishedTimeText":{"simpleText":".*?"', res)
            
           
            
            report_list = [
                ['S No', 'Video Url', 'Thumbnail', 'Title', 'Views', 'Published Time' , "Upload Time"]
            ]
            
            min_video_count = min(len(videoids) , len(thumbnails) , len(relative_time) , len(titles) , len(views))
            print("min fethed videos : " , min_video_count)
            
            urls =[]
            for i in range(min_video_count):
                try:
                    temp = []
                    temp.append(i+1)
                    temp.append('https://www.youtube.com/watch?v='  + videoids[i].split('"')[-2])
                    urls.append(temp[1])
                    temp.append(thumbnails[i].split('"')[-2])
                    temp.append(titles[i].split('"')[-2])
                    temp.append(views[i].split('"')[-2].split()[-2])
                    temp.append(relative_time[i].split('"')[-2])
                    
                    report_list.append(temp)
                    
                except Exception as e:
                        print(e)
                        continue
                    
            num_rows = min_video_count    
            # print(report_list) 
            
             
            # for url in urls:
            
            #     session = HTMLSession() 
            #     response = session.get(url)  

            #     if response.status_code != 200: 
            #         print("error")
            #         views.append("Error! Response = " + str(response.status_code))
            #     else:
            #         soup = bs(response.content, "html.parser")  
            #         view =  soup.find("meta", itemprop="interactionCount")["content"]
            #         views.append(view)
                    
            # print(views)
            
            times = []
            session = HTMLSession() 
            for url in urls:
   
                response = session.get(url)  

                if response.status_code != 200: 
                    times.append("Error! Response = " + str(response.status_code))
                else:
                    soup = bs(response.content, "html.parser")  
                    time = soup.find("meta", itemprop="uploadDate")["content"]
                    times.append(time)
              
            print(times  , len(times))  
            
            for time , row in zip(times , report_list[1:]):
                                          row.append(time) 
                                          
            report_list = refine_list(report_list)                                 
                       
            save_to_file(report_list , time = fetch_time ,query = query)
            
            return render_template('result.html', report_list=report_list, channel=query , num_rows = num_rows , fetch_time = fetch_time )
              
        except Exception as e:
            logging.info(e)
            query = request.form['content']
            return f'something is wrong with {query}' +'\n\n' + f'{str(e)}' 
        
    if request.method == 'GET':
        print('GET')
        try:
               report_list = get_from_csv_file()
        except:         
               return render_template("index.html")         
         
        if len(report_list) > 2:                         
                    print(report_list[-2][0] , len(report_list[0]))
                    try:
                            num_rows =  int(report_list[-1][0])
                    except:
                            num_rows =  int(report_list[-2][0]) 
                            
        else : 
             num_rows = 1                         
                
        dic = get_json()
        fetch_time =  dic["Fetch Time"]
        
        if query is None:
            query  = dic["Query"]
          
        return render_template('result.html', report_list=report_list, channel=query , num_rows = num_rows, fetch_time = fetch_time )
    
    else:
        return render_template('index.html')




@app.route('/download')
@cross_origin()
def download_file():
    EXCEL_FILE_PATH = 'scrapped_data.xlsx'  
 
    df = pd.read_csv(CSV_FILE_PATH)
    
    dic = get_json()
    
    df["Fetch Time"]  =  pd.Series(  ( dic["Fetch Time"] , )*df.shape[0]  )
    df["Numeric Views"] = pd.Series(dic["Numeric Views"]) 
    
    df.to_excel( EXCEL_FILE_PATH , index=False)  
    
    return send_file( EXCEL_FILE_PATH , as_attachment=True)


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
   
        dic = get_json()
        return jsonify(dic)
         

@app.route('/JSON',methods = ['POST' , 'GET'])
@cross_origin()
def JSON_FILE():
    
     JSON_FILE_PATH = "scrapped_data.json"
     return send_file( JSON_FILE_PATH , as_attachment=True)


@app.route('/ZIP',methods = ['POST' , 'GET'])
@cross_origin()
def ZIP_FILE():  
     ZIP_FILE_PATH = zip_images()  
     return send_file( ZIP_FILE_PATH , as_attachment=True)
  
  

@app.route('/visualize')
def Visualize():
    OUTPUT_FILE_NAME = "static/bokeh_plot_with_hover_and_image.html"
    
    df  = pd.read_csv(CSV_FILE_PATH)
    p = create_bokeh_plot(df)
    output_file(OUTPUT_FILE_NAME)
    show(p)
    return redirect(OUTPUT_FILE_NAME)
    # return render_template('bokeh.html', script=p)   
                    
                 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    files = [ "scrapped_data.csv" , "scrapped_data.json" , "scrapped_data.xlsx" , "static/bokeh_plot_with_hover_and_image.html" ,"images.zip"]
    # for file in files:
    #     os.remove(files)
        


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
