namespace java com.tx.homework

service HelloWorld {
    list<MyFile> ls(1:string path);
    string cat(1:string path,2:ModeStatus mode);
    void upload(1:string name,2:binary data);
    binary download(1:string path)

}

struct MyFile {
    1:required string path;
    2:required string name;
    3:string mime;
    4:i64 size;
    5:ModeStatus mode
}

enum ModeStatus{
    TEXT,
    BINARY
}

