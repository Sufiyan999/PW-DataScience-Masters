import os

folder_dict = {
    "a" : "Assignments" ,
    'q': "Questions" ,
    "r" : "Resources" 
}

def generate_github_link(local_path , folder_key = "a"):
    # Convert backslashes to forward slashes (for Windows paths)

    local_path = local_path.replace("\\", "$").replace("/", "$")

    # Split the local path to get parts
    path_parts = local_path.split("$")
    print("\nDecomposition -->>", path_parts)
    
    folder = folder_dict[folder_key]
    # Find the index of the 'Assignments' directory
    assignments_index = path_parts.index(folder)

    # Extract the relevant part of the path
    relevant_path = "/".join(path_parts[assignments_index:]).replace(' ' ,"%20")

    # Construct the GitHub link
    github_link = f"https://github.com/Sufiyan999/PW-DataScience-Masters/blob/master/{relevant_path}"

    return github_link

def main():
        ff = """   
        "a" --- "Assignments" ,
        'q' --- "Questions" ,
        "r" --- "Resources" 
        
        Enter the folder key    :
      
      """
    
        # local_path_assignments = r"D:\Data Science\Assignments\01.    JANUARY\29_jan_assign.ipynb"
        local_path = input(r"Enter the local path in D:\Data Science:  ")
        folder_key = input(ff).lower()
        
        local_path = local_path.strip('"').strip(" ")
        print("-"*50+f"\nyour entered local path -->  " , local_path)
        github_link_assignments = generate_github_link(local_path , folder_key)
        print(f"\n GitHub link -->>> {github_link_assignments}")
        
        if folder_key == "a" :
             print(f"\n[Answer]({github_link_assignments})")
        if folder_key == "q" :
             print(f"\n[Question Bank]({github_link_assignments})") 
                 
        return github_link_assignments


if __name__=="__main__":
        main()