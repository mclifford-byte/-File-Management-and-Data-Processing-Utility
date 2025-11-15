import os
import sys
import shutil
from datetime import datetime

#constants 
FOLDER_NAME = "StudentFiles"
LOG_FILENAME = "activity_log.txt"

def log_message(folder_path, message):
    log_path = os.path.join(folder_path,LOG_FILENAME)
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    try :
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    except Exception as e:
        #if logging fails, print to stderr (do not crash)
        print(f"ERROR: could not write to log file: {e}", file=sys.stderr)

def ensure_student_folder():
    try:
        if not os.path.exists(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)
        abs_path = os.path.abspath(FOLDER_NAME)
        print(f"Student folder located at: {abs_path}")
        return abs_path
    except Exception as e :
        #log to stderr and exit gracefully
        print(f"Filed to create or access folder '{FOLDER_NAME}': {e}",file=sys.stderr)
        sys.exit(1)

def create_student_file(folder_path):
    date_str = datetime.now().date().isoformat() #yyyy-mm-dd
    filename = f"records_{date_str}.txt"
    filepath = os.path.join(folder_path,filename)

    try:
        print("Please enter five student names")
        names = []
        for i in range(1,6):
            name = input(f"Student {i}:").strip()
            # allow blank but still write promp five names
            names.append(name)

        with open(filepath, "w", encoding="utf-8") as f:
            for n in names:
                f.write(n +"\n")
        
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_msg = f"{filename} created at {creation_time}"
        print(success_msg)
        log_message(folder_path, f"{filename} created successfully.")
        return filename,filepath
    
    except Exception as e:
        err = f"Error creating file '{filename}':{e}"
        print( err,file=sys.stderr)
        log_message(folder_path,err)
        sys.exit(1)

def read_and_info(filepath):
    try:
        print("\n--- File contents ---")
        with open(filepath, "r", encoding="utf-8") as f:
            contents = f.read()
        print(contents.rstrip("\n"))
    except Exception as e:
        raise RuntimeError(f"Failed to read file: {e}")
    
    try:
        size = os.path.getsize(filepath)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        print(f"File size : {size} bytes")
        print(f"Last modified:{mtime.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        raise RuntimeError(f"Failde to get file info: {e}")

def backup_and_archive(folder_path,filename,filepath):
    date_str = datetime.now().date().isoformat()
    backup_name = f"backup_{filename}"
    backup_path = os.path.join(folder_path, backup_name)
    archive_folder = os.path.join(folder_path,"Archive")

    try:
        #copyye
        shutil.copy(filepath, backup_path)
        print(f"Backup created : {backup_name}")
    except Exception as e:
        err = f"Failed to create backup: {e}"
        print(err ,file=sys.stderr)
        log_message(folder_path,err)
        return None
    
    try: 
        if not os.path.exists(archive_folder):
            os.mkdir(archive_folder)
        moved_path = shutil.move(backup_path, archive_folder)
        print(f"Backup moved to Archived: {moved_path}")
    except Exception as e:
        err = f"Failed to move backup to Archive: {e}"
        print(err,file=sys.stderr)
        log_message(folder_path, err)
        return None
    
    # list files in archive

    try:
        files = os.listdir(archive_folder)
        print("\nFiles in archive folder:")
        for f in files:
            print("-", f )
        return files
    except Exception as e:
        err = f"Failed to list A rchive folder: {e}"
        print(err,file=sys.stderr)
        log_message(folder_path, err)
        return None
    
def ask_and_delete(folder_path):
    try:
        resp = input("\nwould you like to delete a file from students files folder?(Yes/No):").strip()
    except KeyboardInterrupt:
        print("\nInput cancelled by user.")
        return
    if resp.lower() =="yes":
        file_to_delete = input("Enter the exact file name to delete:").strip()
        target_path = os.path.join(folder_path, file_to_delete)
        if not os.path.exists(target_path):
            msg = f"Deletion failed: file '{file_to_delete}' not found."
            print(msg)
            log_message(folder_path, msg)
            return
        
        try:
            os.remove(target_path)
            msg = f"{file_to_delete} deleted successfully."
            print(msg)
            log_message(folder_path,msg)
        except Exception as e:
            err = f"Failed to delete '{file_to_delete}':{e}"
            print(err, file=sys.stderr)
        else:
            print("No deletion requested")
        

        #display remainig files in your folder
        try: 
            remaining = os.listdir(folder_path)
            print("\nRemaining files in StudentsFiles:")
            for item in remaining:
                print("-", item)
        except Exception as e:
            err = f"Failed to list StudentFiles: {e}"
            print(err,file=sys.stderr)
            log_message(folder_path,err)

def main():
    #task 1
    student_folder_path = ensure_student_folder()

    #task 2  
    filename,filepath = create_student_file(student_folder_path)

    #task 3
    try:
        read_and_info(filepath)
    except Exception as e:
        err = str(e)
        print(err, file=sys.stderr)
        log_message(student_folder_path,err)
    
    #task 4
    archive_files = backup_and_archive(student_folder_path,filename,filepath)
    if archive_files is not None:
        log_message(student_folder_path,f"{filename}created and archived successfully.")

    #task 6
    ask_and_delete(student_folder_path)

if __name__ =="__main__":
    main()