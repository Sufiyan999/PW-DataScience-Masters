import nbformat
from nbformat.v4 import new_markdown_cell
import os

def append_markdown_cell_at_end(file_path, content):

    with open(file_path, 'r', encoding='utf-8') as notebook_file:
        notebook = nbformat.read(notebook_file, as_version=4)
    markdown_cell = new_markdown_cell(source=content)
    notebook['cells'].append(markdown_cell)
    with open(file_path, 'w', encoding='utf-8') as modified_file:
        nbformat.write(notebook, modified_file)
        
        
def insert_markdown_cell_at_index(file_path, content , index = 0):

    with open(file_path, 'r', encoding='utf-8') as notebook_file:
        notebook = nbformat.read(notebook_file, as_version=4)
    markdown_cell = new_markdown_cell(source=content)
    notebook['cells'].insert(index , markdown_cell)
    with open(file_path, 'w', encoding='utf-8') as modified_file:
        nbformat.write(notebook, modified_file)        


path_list = [path for path in os.listdir(os.getcwd()) if path.endswith("ipynb")]
for i , path in enumerate(path_list):
    print(f"\t{i}  --  {path}")
    
index = int(input("\n Enter  ^   Notebook Path index :  " ) )
notebook_path = path_list[index]

print(f"Chosen Notebook's path ---> {notebook_path}")

string_to_append = input("\n Enter the string to be appended in the notebook : ")


ff = """
  Enter The Place 
  u  --  At The First
  d  --   At The End   
  c  -- Custiom Index
  :   """

place = input(ff).lower()

if place == 'u':
            insert_markdown_cell_at_index(notebook_path, string_to_append , index = 0)
            
elif place == "d":
            append_markdown_cell_at_end(notebook_path, string_to_append)
 
elif place == 'c':
            
            with open(notebook_path , 'r', encoding='utf-8') as notebook_file:
                        notebook = nbformat.read(notebook_file, as_version=4)
                        
            no_of_cells = len(notebook['cells'])  
            print(f"Enter the custom index in {no_of_cells}:")          
            custom_index = int(input())            
            
            insert_markdown_cell_at_index(notebook_path, string_to_append , index = custom_index)
                
            
            

