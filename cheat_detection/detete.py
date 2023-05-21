import os

def delete_shifted_files(folder_path):
    for filename in os.listdir(folder_path):
        if "shifted" in filename:
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Deleted: {filename}")

# Example usage
folder_path = "/Users/nptlinh/Desktop/LfB-Institute-Project/cheat_detection/dataset/Working"
delete_shifted_files(folder_path)
