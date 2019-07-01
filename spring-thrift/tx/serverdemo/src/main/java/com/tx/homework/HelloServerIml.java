package com.tx.homework;

import org.apache.thrift.TException;
import sun.security.util.BitArray;

import java.io.*;
import java.net.URLConnection;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.List;



public class HelloServerIml implements HelloWorld.Iface{
    @Override
    public List<MyFile> ls(String path) throws TException{
        File directory=new File(path);
        String[] files=directory.list();
        List<MyFile> myFileList = new ArrayList<>();

        for(String filepath:files){
            File file=new File(filepath);
            String filename=file.getName();
            String fileAbsolutePath=directory.getAbsolutePath()+"/"+filepath;
            String mimeType = URLConnection.guessContentTypeFromName(file.getName());
            Long filesize = file.length();
            ModeStatus ms = null;
            if (mimeType != null && file.isFile()) {
                System.out.println(mimeType);
                if(mimeType.contains("text")){
                    ms=ModeStatus.TEXT;
                } else {
                    ms = ModeStatus.BINARY;
                }
            }


            MyFile myFile=new MyFile(fileAbsolutePath,filename,mimeType,filesize,ms);
            myFileList.add(myFile);
        }

        return myFileList;
    }

    @Override
    public String cat(String path, ModeStatus mode) throws TException{
        StringBuilder sb=new StringBuilder();

        if(mode != null){
            if(mode == ModeStatus.TEXT){
                try {
                    String line;
                    BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(new File(path)),StandardCharsets.UTF_8));
                    while((line=br.readLine())!=null){
                        sb.append(line);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            else{
                int len;
                try {
                    InputStream is=new FileInputStream(new File(path));
                    byte[] bb=new byte[1024];
                    while((len=is.read(bb))!=-1){
                        String hexstr=toHexString(bb,len);
                        sb.append(hexstr);
                    }
                } catch (java.io.IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return sb.toString();
    }

    @Override
    public void upload(String name, java.nio.ByteBuffer data) throws TException{
        try {
            FileOutputStream os=new FileOutputStream(new File(name));
            byte[] bytes=new byte[data.remaining()];    // limit -position
            data.get(bytes);
            os.write(bytes);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public java.nio.ByteBuffer download(String path) throws TException{
        File file=new File(path);
        try {
            InputStream is=new FileInputStream(file);
            if(file.length()>Integer.MAX_VALUE)
                return ByteBuffer.allocate(0);
            ByteBuffer bb=ByteBuffer.allocate((int)file.length());
            int i;
            while((i=is.read())!=-1){
                bb.put((byte)i);
            }
            bb.flip();
            is.close();
            return bb;
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
        }
        return ByteBuffer.allocate(0);
    }

    private final static char[] digits = {
            '0' , '1' , '2' , '3' , '4' , '5' ,
            '6' , '7' , '8' , '9' , 'a' , 'b' ,
            'c' , 'd' , 'e' , 'f'
    };

    private static String toHexString(byte[] bytes,int len){
        char[] res=new char[len*2];
        int a;
        int charPos=0;
        for (int i = 0; i <len ; i++) {
            byte b=bytes[i];
            if(b<0)
                a= b & 0xff;
            else
                a=b;

            res[charPos++]=digits[a/16];
            res[charPos++]=digits[a%16];

        }
        return new String(res);   //res.toString();

    }

    public static void main(String[] args){
        HelloServerIml demo = new HelloServerIml();
        try {
            List<MyFile> myFiles = demo.ls("/Users/xuetang/workspaces/");
            myFiles.stream().forEach(System.out::println);
//            int i = Integer.parseInt("10",10);
//            System.out.println(i);
//            System.out.println((byte)i);
//            byte[] bs=new byte[1];
//            bs[0]=(byte)i;
//            String res=toHexString(bs);
//            System.out.println(res);
            System.out.println(demo.cat("/Users/xuetang/Downloads/test.bin",ModeStatus.BINARY));

            byte[] data = "System.out.println(demo.cat(\"/Users/xuetang/Downloads/test.bin\",ModeStatus.BINARY));".getBytes();
            ByteBuffer bs=ByteBuffer.wrap(data);
            demo.upload("/Users/xuetang/Downloads/test2.txt",bs);

            ByteBuffer bb=demo.download("/Users/xuetang/workspaces/tx-homework/docs/data.dat");
            System.out.println(new String(bb.array(), 0, bb.array().length));

        } catch (TException e) {
            e.printStackTrace();
        }
    }


}
