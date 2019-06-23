package com.zwt.client;

import com.zwt.thrift.api.FileData;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.protocol.TProtocol;
import com.zwt.thrift.api.HelloWorldServer;
import org.apache.thrift.protocol.TBinaryProtocol;


import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.nio.ByteBuffer;

public class HelloWorldClient {
    public void start() throws Exception{
        TTransport transport = new TSocket("localhost",  9120);
        transport.open();

        TProtocol protocol = new TBinaryProtocol(transport);
        HelloWorldServer.Client client = new HelloWorldServer.Client(protocol);
        System.out.println(client.ls("/Users/zhangweite/Documents"));
        System.out.println(client.cat("/Users/zhangweite/Documents/test.txt",(short)1));

        String filePath = "/Users/zhangweite/Documents/test.txt";
        byte[] bytes = toByteArray(filePath);
        FileData fileData = new FileData();
        fileData.name = filePath;
        fileData.buff = ByteBuffer.wrap(bytes);
        client.upload(new FileData(fileData));


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