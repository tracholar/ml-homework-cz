#namespace java com.cimon.SimpleFileSystem


enum Mode{
  TXT=1,
  BIN=2
}

struct ThriftFile{
1:string path,
2:string name,
3:string mime,
4:string size,
5:string filemode,
}

service FileSystem{
   list<ThriftFile> ls(1:string param),
   string cat(1:string param,2:Mode op),
   bool uploadFile(1:string filename,2:binary data),
   binary downFile(1:string path)
}