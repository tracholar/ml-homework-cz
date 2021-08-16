namespace java com.cjf.thrift.generate

struct ThriftFile
{
    1:required string   name,
    2:required binary   buff,
}

service CjfService
{
    string ls(1: string path)
    string cat(1: string path,
               2: i16 mode)
    bool upload(1: ThriftFile file)
    ThriftFile download(1: string file)
}