package com.cimon.SimpleFileSystem;
import org.apache.thrift.TException;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.nio.ByteBuffer;

public class FileSystemHandler implements FileSystem.Iface {

    @Override
    public List<ThriftFile> ls(String path) throws TException {
        List<ThriftFile> lt=new ArrayList<>();
        File file =new File(path);
        if(!file.exists())
            return null;
        else if( file.isFile()){
             lt.add(tools.getFileInfo(file));

        }else{

               File[] filelist=file.listFiles();

               if(filelist.length<=0)
                   return null;
               else{
                   for(File tmp : filelist){

                       //System.out.println(tmp.isFile());
                        if(tmp.isFile()){// 只处理 文件, 忽略目录

                            ThriftFile t=tools.getFileInfo(tmp);

                            lt.add(t);
                        }
                   }
                   //System.out.println(lt.size());
                   return lt;
               }

        }
        return  lt;
    }

    @Override
    public String cat(String path,Mode mode){
       byte[] bytes= tools.toByteArray(path);
         if(mode==Mode.TXT){
            return new String(bytes);
         }
         else if(mode==Mode.BIN){
             return tools.byte2HexString(bytes);
         }
        return null;
    }

    @Override
    public boolean uploadFile(String filename,ByteBuffer data){
        /* 不想写的太复杂了，随便给路径吧*/
        String filePath = "/Users/bing/Desktop/IDEAP/thrift-start-learning/Src/com/cimon/SimpleFileSystem/StorageFile";

        return tools.writeByteBuffer(filePath+"/"+filename,data);
    }

    @Override
    public ByteBuffer downFile(String path){
        byte[] bytes=tools.toByteArray(path);
        return ByteBuffer.wrap(bytes);
    }
}
