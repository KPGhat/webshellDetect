import os
import string
import random
import subprocess

def gen_phpfile_bow(basedir = '../whitecode', bowpath = './whitecodeBoW'):
    
    files = os.listdir(basedir)

    for file in files:
        filepath = os.path.join(basedir, file)
        if os.path.isdir(filepath):
            gen_phpfile_bow(filepath)

        # 只处理php文件
        if file.split('.')[-1] != 'php':
            continue

        # 读取已经处理的文件名文件，减少重复处理
        with open('generated.txt', 'r', encoding='utf-8') as f:
            processed_files = f.read()
        if filepath in processed_files:
            continue

        print(f"[+]Get {file}'s BoW")

        # 生成随机的文件名且该文件名不存在
        bowname = os.path.join(bowpath, ''.join(random.choices(string.ascii_letters, k=15))+".BoW")
        while os.path.exists(bowname):
            bowname = os.path.join(bowpath, ''.join(random.choices(string.ascii_letters, k=15))+".BoW")
        subprocess.run(["php", "GenASTBoW.php", filepath], stdout=open(bowname, 'w'))

        with open('generated.txt', 'a+', encoding='utf-8') as f:
            f.write(filepath + '\n')

if __name__ == '__main__':
    gen_phpfile_bow('../webshell', './webshellBoW')
    gen_phpfile_bow('../whitecode', './whitecodeBoW')
    print('[+]Finish!!!')