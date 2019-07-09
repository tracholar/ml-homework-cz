package com.zwt.server;

import org.apache.thrift.TException;

import com.zwt.thrift.api.HelloWorldServer;
import com.zwt.thrift.api.FileData;

import java.io.*;
import java.nio.ByteBuffer;
import java.util.Scanner;

import java.nio.channels.FileChannel;

import java.net.FileNameMap;
import java.net.URLConnection;

public class HelloWorldServerImpl implements HelloWorldServer.Iface {
    @Override
    public String ls(String path) throws TException{
        File file = new File(path);
        File[] tempList = file.listFiles();
        String[] file_list=file.list();
        String[] res = new String[file_list.length];
        FileNameMap fileNameMap = URLConnection.getFileNameMap();
        for(int i=0;i<res.length;i++){
            res[i] = "";
            res[i] = res[i] + tempList[i].getParent() + " ";
            res[i] = res[i] + tempList[i].getName() + " ";
            res[i] = res[i] + tempList[i].canRead() + " ";
            res[i] = res[i] + tempList[i].canWrite() + " ";
            String type = fileNameMap.getContentTypeFor(path+"/"+file_list[i]);
            res[i] = res[i] + type + " ";
            res[i] = res[i] + tempList[i].length();
        }
        String list = "";
        for(String r:res){
            list = list + r + "\n";
        }
        return list;
    }
    @Override
    public String cat(String path, short mode) {
        try {
            String res = "";
            Scanner sc = new Scanner(new File(path));
            while (sc.hasNextLine()) {
                res = res + " " + sc.nextLine() + '\n';
            }
            return res;
        } catch(Exception e) {
            System.out.println("文件不存在");
        };
        return "";
    }
    @Override
    public boolean upload(FileData data){
        String filePath = "/Users/zhangweite/Documents/test2.txt";
        try
        {
            File file = new java.io.File(filePath);
            FileOutputStream fos = new FileOutputStream(file);
            FileChannel channel = fos.getChannel();
            channel.write(data.buff);
            channel.close();
        }
        catch (Exception x)
        {
            x.printStackTrace();
            return false;
        }
        return true;
    }
    @Override
    public FileData download(String data){
        String filePath = "/Users/zhangweite/Documents/test3.txt";
        byte[] bytes = toByteArray(filePath);
        FileData fileData = new FileData();
        fileData.name = filePath;
        fileData.buff = ByteBuffer.wrap(bytes);
        return fileData;
    }
    private static byte[] toByteArray(String filePath){
        byte[] buffer = null;
        try {
            File file = new File(filePath);
            FileInputStream fis = new FileInputStream(file);
            ByteArrayOutputStream bos = new ByteArrayOutputStream(1000);
            byte[] b = new byte[1000];
            int n;
            while ((n = fis.read(b)) != -1) {
                bos.write(b, 0, n);
            }
            fis.close();
            bos.close();
            buffer = bos.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return buffer;
    }

}