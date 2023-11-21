from bokeh.plotting import figure, output_file, show
import bokeh.plotting  as bp
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.layouts import column
import pandas as pd
import os
import csv
import datetime
import json 
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_to_file(report_list ,query , time  =  None):
            file_name = os.path.join(BASE_DIR,  'scrapped_data.csv')
            with open(file_name, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                for i, row in enumerate(report_list):
                    try:
                        if i > 0 : 
                                row[3] = row[3].encode('utf-8')
                                
                        csvwriter.writerow(row)
                    except:                                         # UnicodeEncodeError ,because of these 🔥🔥 in the title row[3]     
                        row[3] = row[3].encode('utf-8') 
                        csvwriter.writerow(row)
                        continue
                            
            df  = pd.read_csv(file_name)
            # df.drop(df.columns[0], inplace = True)
            print(df.columns)
            df["Numeric Views"] = df["Views"].apply(views_to_numeric)
            
            print(df.head())
            
            dic = {} 
            
            for column in df.columns:
                dic[column] = list(df[column])        
            
            dic["Fetch Time"] =  time
            dic["Query"] =  query

            with open("scrapped_data.json" , "w") as fileobj:
                        json.dump( dic, fileobj )
            
                
                    
                    
                    
                    
def get_from_csv_file():
            report_list = []
            file_name = 'scrapped_data.csv' 
            file_name = os.path.join(BASE_DIR,  file_name)
            with open(file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                  report_list.append(row)                  
            return report_list
           
           
def get_json():
      file_name = os.path.join(BASE_DIR,  "scrapped_data.json")
      
      dic = {}
      
      with open( file_name  , "r") as fileobj:
            dic = json.load(fileobj)
            
      return dic


def refine_list(lst):
    for row in lst:
         temp = row[5]
         row[5] = row[6]
         row[6] =temp
            
    return lst                            

# Convert views to numeric
def views_to_numeric(views_str):
    try:
        
        if isinstance(views_str, int) or isinstance(views_str, float):
            return float(views_str)
        
        
        views_str = views_str.replace(',', '')  # Remove commas if present
        if 'K' in views_str:
            views_str = views_str.replace('K', '')
            return float(views_str) * 1000
        elif 'M' in views_str:
            views_str = views_str.replace('M', '')
            return float(views_str) * 1000000
        elif 'B' in views_str:
            views_str = views_str.replace('B', '')
            return float(views_str) * 1000000000
        else:
            return float(views_str)   
         
    except  Exception as e:
        print(f"ERROR: {e}")
        print( views_str , type(views_str))    

def create_bokeh_plot(df , hover_data = True): 
            data = {}

            for column in df.columns:
                try:
                    print(column , end = "--")
                    data[column] = df[column]
                except:
                    continue
            

            df["Numeric Views"] = df["Views"].apply(views_to_numeric)
            
            
            sno = list(range(1, len(df) + 1))

            # Create a Bokeh ColumnDataSource to supply data to the plot
            source = ColumnDataSource(df)

            # Create a Bokeh plot
            p = figure(
                title="YouTube Video Views vs. Serial Number",
                x_axis_label="Serial Number (latest videos has least sr. no.)",
                y_axis_label="Views",
                tools="hover,pan,box_zoom,reset"
            )

            # Add circular markers connected by lines
            p.line(x="index", y="Numeric Views", source=source, line_width=2, line_color="blue", legend_label="Line")
            circle = p.circle(x="index", y="Numeric Views", source=source, size=8, color="red", alpha=0.7, legend_label="Dots")



            if hover_data:
                        # Create a custom HTML div for the hover tooltip with an image
                        hover_html = """
                            <div style="color:blue;">
                                <img src="@{Thumbnail}" style="max-height: 100px;">
                                <a href="@{ Video url}" > </a>
                                <p><strong style="color:red;" >Title:</strong> @{Title}</p>
                                <p><strong style="color:red;">Published Time:</strong> @{Upload Time}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  @{Published Time}</p>
                                <p><strong style="color:red;">Views:</strong> @{Views}</p>
                            </div>
                        """

                        # Add a HoverTool with a custom tooltip
                        hover = HoverTool(renderers=[circle], tooltips=hover_html)
                        p.add_tools(hover)

            # Add a legend
            p.legend.title = "Legend"
            
            p.legend.label_text_font_size = "12pt"
            p.legend.click_policy="hide"
            
            return p
 
 
 
def refine_name(name):
   
    name = name.replace("b" ,"").replace("'","").replace('"' ,"").replace("-" ,"_" )   
    if "\\" in name:
        for prob in ["\\u", "\\\\u", "\\x", "\\\\x" ,"\\" ,"|"]:
                if prob in name:
                        name = name.replace(prob ,"")
                        
    import re                     
    import codecs

    # Sample text with Unicode escape sequences
    text = name

    # Decode Unicode escape sequences
    decoded_text = codecs.decode(text, 'unicode_escape')

    # Remove non-alphanumeric characters (excluding spaces)
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]+', '', decoded_text)

    # print(cleaned_text)
    return   cleaned_text   
      
      
        
def zip_images():
        import zipfile
        
        dic = get_json()
        # List of image URLs to download
        image_urls = dic["Thumbnail"]
        image_names = dic["Title"]	
        Upload_Time = dic["Upload Time"]
        # Relative_Time   = dic["Relative Time"]
        # Create a directory to store downloaded images
        download_dir = os.path.join(BASE_DIR, 'downloaded_images')
        os.makedirs(download_dir, exist_ok=True)

        # Download images and save them to the directory
        for  url , name ,i in zip(image_urls , image_names, range(len(image_urls))):
            response = requests.get(url)
            if response.status_code == 200:
                # filename = os.path.join(download_dir, os.path.basename(url))
                name = refine_name(name)
                st = "D+"+Upload_Time[i].replace( "-" ," ").replace(":" ,"_").replace("T" ," T+")
                filename = os.path.join(download_dir, name +f"  { st } "  +".jpg")
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f'Downloaded: {filename}')

        # Create a zip file containing the downloaded images
        zip_filename = os.path.join(BASE_DIR, 'images.zip') 
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(download_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), download_dir))

        # Send the zip file to the recipient using your preferred method (e.g., email, file sharing service, etc.)
        # You can use libraries like smtplib to send the email with the attachment.

        # Clean up the downloaded images and directory if needed
        for root, _, files in os.walk(download_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(download_dir)

        print(f'Zip file created: {zip_filename}')
        return zip_filename
       
            
 
if __name__ == "__main__": 
        # df = pd.read_csv("scrapped_data.csv")
    
        # try:       
        #            p = create_bokeh_plot(df)  
              
        # except:
        #            p = create_bokeh_plot(df , False)              

        # output_file("static/bokeh_plot_with_hover_and_image.html")
        # show(p)
        zip_images()


                   