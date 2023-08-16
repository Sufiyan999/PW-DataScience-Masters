# # Import the necessary library
# import nbformat

# # Create a new Jupyter Notebook
# notebook = nbformat.v4.new_notebook()

# print("ENTER nO OF Ans : ")


# # Write numbers from 1 to 10 in separate cells
# for num in range(1, 11):
#     cell = nbformat.v4.new_code_cell(source=str(num))
#     notebook.cells.append(cell)

# # Save the notebook to a file
# file_path = 'number_cells.ipynb'
# with open(file_path, 'w') as f:
#     nbformat.write(notebook, f)

# print(f"Jupyter Notebook '{file_path}' created with number cells.")

import nbformat
def remove_space(input_string,space = " "):
    
    temp = input_string

    while space == input_string[0]:
        input_string = input_string[1:]
        
    while space == input_string[-1]:
        input_string = input_string[:-1] 
       
    if temp == input_string:   
             return input_string 
               
    print(f"trimed ({space}) : {temp} --> {input_string}")         
    return input_string    

def get_file_name():
        name = input("Enter name of the file :  ")
        name = remove_space(name)
        name = name + " assign.ipynb"  
        return name 


def main():
    
        file_path = get_file_name()
        # Create a new Jupyter Notebook
        notebook = nbformat.v4.new_notebook()

        k = int(input("ENTER No of Ans : ")) 
        
        # Define a function to add markdown cells
        def add_markdown_cell(notebook, content):
            cell = nbformat.v4.new_markdown_cell(content)
            notebook.cells.append(cell)

        # Add markdown cells with numbers 1 to 10 and empty code cells in between
        for num in range(1, k+1):
            
            ans =  f"<a id=\"{num}\"></a> \n # <p style=\"padding:10px;background-color: #00004d ;margin:10;color: white ;font-family:newtimeroman;font-size:100%;text-align:center;border-radius: 10px 10px ;overflow:hidden;font-weight:50\">Ans {str(num)} </p> "           
         
            # add_markdown_cell(notebook, f"## Ans {str(num)}")
            
            add_markdown_cell(notebook, ans)
            # add_markdown_cell(notebook, '')
            notebook.cells.append(nbformat.v4.new_code_cell(''))

        # Save the notebook to a fil
        
        with open(file_path, 'w') as f:
            nbformat.write(notebook, f)

        print(f"Jupyter Notebook '{file_path}' created with markdown and empty code cells.")


main()