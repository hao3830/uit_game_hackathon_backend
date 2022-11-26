import os
import random
import string
import zipfile
import uuid
import shutil
import glob


def is_float(N):
    try:
        float(N)
        return True
    except:
        return False


def gen_id(N):
    id = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))
    return id


def gen_uuid():
    return str(uuid.uuid4())


def gen_token(N):
    token = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))
    return token


def unzip(inpath, outpath):
    with zipfile.ZipFile(inpath, "r") as zip_ref:
        zip_ref.extractall(outpath)


def zipdir(inpath, outpath):
    zipf = zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(inpath):
        for file in files:
            ## zip with parent folder
            # zipf.write(
            #     os.path.join(root, file),
            #     os.path.relpath(os.path.join(root, file), os.path.join(inpath, "..")),
            # )

            # zip only file
            zipf.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(inpath, ".")),
            )
    zipf.close()


def zip_person_data(inpath, outpath):
    zipf = zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(inpath):
        for file in files:
            zipf.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(inpath, ".")),
            )
    zipf.close()


def clear_dir(dirpath):
    shutil.rmtree(dirpath)


def recreate_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    else:
        shutil.rmtree(dirpath)
        os.mkdir(dirpath)


def copy_file_with_ext(source_dir, dest_dir, ext):
    files = glob.iglob(os.path.join(source_dir, "*%s" % ext))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, dest_dir)


def copy_file_with_ext_and_str(source_dir, dest_dir, ext, str):
    files = glob.iglob(os.path.join(source_dir, "*%s" % ext))
    for file in files:
        if str in file:
            if os.path.isfile(file):
                shutil.copy2(file, dest_dir)


def copy_file_with_ext_without_str(source_dir, dest_dir, ext, str):
    files = glob.iglob(os.path.join(source_dir, "*%s" % ext))
    for file in files:
        if str in file:
            continue
        if os.path.isfile(file):
            shutil.copy2(file, dest_dir)


def recursive_file_permissions(path, mode):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mode)
        for file in files:
            os.chown(os.path.join(root, file), mode)


def recursive_chown(path, owner):
    for dirpath, dirnames, filenames in os.walk(path):
        shutil.chown(dirpath, owner)
        for filename in filenames:
            shutil.chown(os.path.join(dirpath, filename), owner)
