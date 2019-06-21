struct FileStruct {
    1: string name,
    2: string path,
    3: string MIME,
    4: i64 size,
    5: i32 mode
}

enum CatMode {
    TXT = 1,
    BIN = 2
}

service FTPServer {
    list<FileStruct> ls(1: string path),
    string cat(1: FileStruct file, 2: optional CatMode mode),
    bool upload(1: string name, 2: binary data),
    binary downlaod(1: string path)
}
