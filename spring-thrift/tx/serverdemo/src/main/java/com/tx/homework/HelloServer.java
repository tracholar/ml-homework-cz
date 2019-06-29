package com.tx.homework;

import org.apache.thrift.TException;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.net.ServerSocket;

public class HelloServer {
    public static final int port=9122;
    public static void main(String[] args) throws Exception{

        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        HelloServerIml helloWorld = (HelloServerIml) context.getBean("helloWorld");
        System.out.println(helloWorld);

        ServerSocket socket=new ServerSocket(port);
        TServerSocket tsocket=new TServerSocket(socket);
        HelloWorld.Processor prococss=new HelloWorld.Processor(helloWorld);
        TServer tserver =new TSimpleServer(new TServer.Args(tsocket).processor(prococss) );

        System.out.println("starting server...");
        tserver.serve();
    }
}
