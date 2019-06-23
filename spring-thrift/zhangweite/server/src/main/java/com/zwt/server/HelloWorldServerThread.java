package com.zwt.server;

import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.server.TServer;
import com.zwt.thrift.api.HelloWorldServer;
import org.apache.thrift.server.TSimpleServer;
import java.net.ServerSocket;


public class HelloWorldServerThread {
    public static final int port = 9120;
    public void start() throws Exception{
        ServerSocket socket = new ServerSocket(port);
        TServerSocket tsocket = new TServerSocket(socket);
        HelloWorldServer.Processor processor = new HelloWorldServer.Processor(new HelloWorldServerImpl());
        TServer server = new TSimpleServer(new TServer.Args(tsocket).processor(processor));
        System.out.println("Starting the simple server...");
        server.serve();
    }
}