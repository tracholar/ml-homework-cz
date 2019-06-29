package com.tx.homework;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.springframework.context.support.ClassPathXmlApplicationContext;


import java.nio.ByteBuffer;
import java.util.List;

public class HelloClient {
    public static void main(String[] args){
        //1. 直接调用
//        TTransport transport=new TSocket("localhost",9122);
//        try {
//            transport.open();
//        } catch (TTransportException e) {
//            e.printStackTrace();
//        }
//
//        TProtocol protocal =new TBinaryProtocol(transport);
//        HelloWorld.Client client=new HelloWorld.Client(protocal);

        //2. 使用spring
        ClassPathXmlApplicationContext cx=new ClassPathXmlApplicationContext("beans.xml");
        TTransport transport= (TSocket) cx.getBean("tsocket");
        try {
            transport.open();
        } catch (TTransportException e) {
            e.printStackTrace();
        }

        HelloWorld.Client client=(HelloWorld.Client)cx.getBean("client");

        try {
            List<MyFile> myFiles = client.ls("/Users/xuetang/workspaces/");
            myFiles.stream().forEach(System.out::println);

            System.out.println(client.cat("/Users/xuetang/Downloads/test.bin",ModeStatus.BINARY));
//
            byte[] bytes="hhhhhhh天气很好yyyfasdfadfasdfasdfasdf".getBytes();
            ByteBuffer bs=ByteBuffer.wrap(bytes);
            client.upload("/Users/xuetang/Downloads/test2.txt",bs);

            ByteBuffer bb = client.download("/Users/xuetang/workspaces/tx-homework/docs/data.dat");
            System.out.println(new String (bb.array(),0, bb.array().length));
        } catch (TException e) {
            e.printStackTrace();
        }


    }
}
