from bokeh.plotting import figure, output_file, show
import bokeh.plotting  as bp
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.layouts import column
import pandas as pd
import os
import csv
import datetime
import json 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_to_csv_file(report_list):
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
                    
                    
                    
def get_from_csv_file():
            report_list = []
            file_name = 'scrapped_data.csv' 
            file_name = os.path.join(BASE_DIR,  file_name)
            with open(file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                  report_list.append(row)                  
            return report_list
           
           
def get_json_by_csv():
            df  = pd.read_csv("scrapped_data.csv")
            # df.drop(df.columns[0], inplace = True)
            print(df.columns)
            df["Numeric Views"] = df["Views"].apply(views_to_numeric)
            
            print(df.head())
            dic = {} 
            
            for column in df.columns:
                dic[column] = list(df[column])        
            
            dic["fetch time"] =  datetime.datetime.now().isoformat()
        
            
            return dic
                                

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
                                <p><strong style="color:red;">Published Time:</strong> @{Published Time}</p>
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
            
 
if __name__ == "__main__": 
        df = pd.read_csv("scrapped_data.csv")
    
        try:       
                   p = create_bokeh_plot(df)  
              
        except:
                   p = create_bokeh_plot(df , False)              

        output_file("static/bokeh_plot_with_hover_and_image.html")
        show(p)

                   