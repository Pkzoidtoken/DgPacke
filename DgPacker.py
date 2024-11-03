import os

class Dg:
    def __init__(self):
        self.DIR : tuple = ()
        self.FILE : tuple = ()
                    
    def read_process(self, target_dir):
        if os.path.isdir(target_dir):
            for dir in os.listdir(target_dir):
                path = os.path.join(target_dir, dir)
                if os.path.isdir(path):
                    self.read_process(target_dir=path)
                    self.DIR += (path.strip(),)
                else:
                    self.FILE += (path.strip(),)
        else:
            self.FILE += (target_dir.strip(),)

    def content_process(self, name):
        with open(name, "rb") as file:
            return file.read()

    def write_process(self, output):
        with open(output, "wb") as pack:
            pack.write(b"PACK! CREATED BY PKZOID")
            for dir in self.DIR:
                pack.write(f"\n[DIR] {dir}".encode())
            for file in self.FILE:
                pack.write(f"\n[FILE] {file} \n[R {file}]\n".encode())
                pack.write(self.content_process(file))
                pack.write(f"\n[R {file}]".encode())

    def block_process(self,input,start_marker:str):
        with open(input, "rb") as file:
            block = bytearray()
            in_block = False
            while True:
                line = file.readline()
                if not line:
                    break

                if line.strip() == start_marker and not in_block:
                    in_block = True
                    continue

                elif line.strip() == start_marker and in_block:
                    break 

                if in_block:
                    block.extend(line)  # Add binary line to block

            return block

    def extractall_process(self, input, path):
        with open(input, "rb") as pack:
            for line in pack.readlines():
                content = line.split()
                if b"[DIR]" in content:
                    f_dir = content.index(b"[DIR]")
                    name_dir = content[f_dir+1].decode()
                    os.makedirs(rf"{path}\{name_dir}", exist_ok=True)
                elif b"[FILE]" in content:
                    f_file = content.index(b"[FILE]")
                    name_file = content[f_file+1].decode()
                    with open(rf"{path}\{name_file}", "wb") as output_file:
                        block_content = self.block_process(input, f"[R {name_file}]".encode())
                        output_file.write(block_content)
        
    def extract_process(self, input,target:str):
        with open(input, "rb") as pack:
            for line in pack.readlines():
                content = line.split()

                if b"[FILE]" in content:
                    t_target = content.index(b"[FILE]")
                    find = content[t_target+1].split(b"\\")
                    if target.encode() in find:
                        name_file = find[find.__len__()-1]
                        with open(name_file,"wb") as file:
                            block_content = self.block_process(input, f"[R {content[t_target+1].decode()}]".encode())
                            file.write(block_content)

    def printdir_processs(self,input):
        with open(input,"rb") as pack:
            for line in pack.readlines():
                content = line.split()
                if b"[DIR]" in content:
                    dir = content.index(b"[DIR]")
                    print(content[dir+1].decode())
                elif b"[FILE]" in content:
                    file = content.index(b"[FILE]")
                    print(content[file+1].decode())

_dg = Dg()

class DgFile:
    def __init__(self):
        self.__file : str
    
    def open(self,filename:str):
        self.__file = filename
    
    def write(self,path:str):
        _dg.read_process(path)
        _dg.write_process(self.__file)
    
    def extractall(self,output_path:str):
        _dg.extractall_process(self.__file,output_path)

    def extract(self,target:str):
        _dg.extract_process(self.__file,target)

    def printdir(self):
        _dg.printdir_processs(self.__file)
