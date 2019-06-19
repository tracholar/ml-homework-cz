namespace java com.zwt.thrift.api

struct FileData
{
    1:required string   name,                   // 文件名字
    2:required binary   buff,                   // 文件数据
}

service HelloWorldServer
{
    string ls(1: string path)
    string cat(1: string path,
               2: i16 mode)
    bool upload(1: FileData filedata)
    void download(1: string path)
}