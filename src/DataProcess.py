import os
import random
import shutil

#data clean
def clean_data(basedir = '/webshellBoW'):
    num = 0
    files = os.listdir(basedir)
    for file in files:
        filepath = os.path.join(basedir, file)
        file_content = open(filepath, 'r').read().strip()
        
        if file_content != '' and file_content != 'PhpParser\\Node\\Stmt\\InlineHTML':
            os.rename(filepath, os.path.join(basedir, str(num)+".BoW"))
            num += 1
        else:
            os.remove(filepath)

#data split
def split_data(basedir = './webshellBoW'):
    files = os.listdir(basedir)

    train_data_path = os.path.join(basedir, 'train')
    test_data_path = os.path.join(basedir, 'test')

    if not os.path.exists(train_data_path):
        os.mkdir(train_data_path)

    if not os.path.exists(test_data_path):
        os.mkdir(test_data_path)

    train_data_vol = 0
    while train_data_vol < len(files)//2:
        file = random.choice(files)
        files.remove(file)
        filepath = os.path.join(basedir,file)

        shutil.move(filepath, train_data_path)
        train_data_vol += 1

    for file in files:
        filepath = os.path.join(basedir,file)
        shutil.move(filepath, test_data_path)

#undo split operation
def no_split(basedir = './webshellBoW'):
    subdirs = os.listdir(basedir)
    for subdir in subdirs:
        subdirpath = os.path.join(basedir, subdir)
        if not os.path.isdir(subdirpath):
            continue
        files = os.listdir(subdirpath)
        for file in files:
            filepath = os.path.join(subdirpath, file)
            shutil.move(filepath, basedir)
        print(f'remove {subdirpath}')
        os.rmdir(subdirpath)

if __name__ == '__main__':
    clean_data('./whitecodeBoW')
    clean_data('./webshellBoW')
    # split_data('./whitecodeBoW')
    # split_data('./webshellBoW')
    # no_split('./webshellBoW')
    # no_split('./whitecodeBoW')
