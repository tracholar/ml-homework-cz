package com.cjf.main;

import com.cjf.thrift.generate.CjfService;
import com.cjf.thrift.generate.ThriftFile;
import org.apache.thrift.TException;

import java.io.*;
import java.net.FileNameMap;
import java.net.URLConnection;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CjfServiceImpl implements CjfService.Iface{

    @Override
    public String ls(String path) throws TException {
        File file = new File(path);
        File[] tList = file.listFiles();
        String[] f_list = file.list();
        String[] out = new String[f_list.length];
        FileNameMap fileMap = URLConnection.getFileNameMap();
        for (int i = 0; i < out.length; i++) {
            out[i] = tList[i].getParent() + " " + tList[i].getName() + " " + tList[i].canRead() + " " + tList[i].canWrite() + " ";
        }
        String res = "";
        for (String i: out) {
            res += res + i + "\n";
        }
        return res;
    }

    @Override
    public String cat(String path, short mode) throws TException {
        try {
            String res = "";
            Scanner sc = new Scanner(new File(path));
            while (sc.hasNextLine()) {
                res += " " + sc.nextLine() + "\n";
            }
            return res;
        } catch (Exception e) {
            System.out.println("File not found!");
            return "";
        }
    }

    @Override
    public boolean upload(ThriftFile file) throws TException {
        String path = "/Users/chengjiafeng/Desktop/test/test1.txt";
        try {
            File myfile = new File(path);
            FileOutputStream fileOuputStream = new FileOutputStream(myfile);
            FileChannel channel = fileOuputStream.getChannel();
            channel.write(file.buff);
            channel.close();
            return true;
        } catch (Exception e){
            System.out.println("Can not upload file!");
            return false;
        }
    }

    @Override
    public ThriftFile download(String file) throws TException {
        String path = "/Users/chengjiafeng/Desktop/test/test2.txt";
        byte[] bytes = toByteArray(path);
        ThriftFile myfile = new ThriftFile();
        myfile.name = path;
        myfile.buff = ByteBuffer.wrap(bytes);
        return myfile;
    }

    private static byte[] toByteArray(String filePath){
        byte[] buffer = null;
        try {
            File myfile = new File(filePath);
            FileInputStream fileInputStream = new FileInputStream(myfile);
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(1000);
            byte[] b = new byte[1000];
            int n;
            while ((n = fileInputStream.read(b)) != -1) {
                byteArrayOutputStream.write(b, 0, n);
            }
            fileInputStream.close();
            byteArrayOutputStream.close();
            buffer = byteArrayOutputStream.toByteArray();
        } catch (Exception e) {
            System.out.println("Can not toByteArray");
        }
        return buffer;
    }

}

