import os
import shutil

def copy_source_to_dest(source, destination):
    if os.path.exists(source):
        pass
        print(f"source path: {source} exists")
    else:
        raise FileNotFoundError (f"source path {source} does not exist")

    if os.path.exists(destination):
        pass
        print(f"destination path: {destination} exists")
    else:
        raise FileNotFoundError (f"destination path {destination} does not exist")

    paths = os.listdir(path=destination)
    # print (paths)
    for path in paths:
        dest_path = os.path.join(destination, path)
        if os.path.isfile(dest_path):
            print(f"removing file: {dest_path}")
            os.remove(dest_path)
        if os.path.isdir(dest_path):
            print(f"removing directory: {dest_path}")
            shutil.rmtree(dest_path)
    copy_objects(source, destination)


def copy_objects(source, destination):
    objects_to_copy = os.listdir(path=source)
    for obj in objects_to_copy:
        source_path = os.path.join(source, obj)
        dest_path = os.path.join(destination, obj)
        if os.path.isfile(source_path):
            print(f"copying object: {source_path} to {destination}")
            shutil.copy(source_path, destination)
        if os.path.isdir(source_path):
            print(f"creating directory: {dest_path} in {destination}")
            os.mkdir(dest_path)
            copy_objects(source_path, dest_path)
