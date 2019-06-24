package com.cimon.SimpleFileSystem;


import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

public class SfsServer {
    public static void main(String args[]){
        try {

            /*
             * Your code to define processor ,etc..
             *
             * Start.Processor processor = new  Start.Processor(new StartHandler);
             *
             * */
            FileSystem.Processor processor = new FileSystem.Processor(new FileSystemHandler());

            TServerTransport serverTransport = new TServerSocket(9090);
            TServer server = new TSimpleServer(new TServer.Args(serverTransport).processor(processor));
            System.out.println("Starting the simple server...");
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
