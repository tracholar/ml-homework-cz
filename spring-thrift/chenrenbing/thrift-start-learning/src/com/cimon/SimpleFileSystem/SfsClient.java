package com.cimon.SimpleFileSystem;


import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;

import java.io.File;
import java.nio.ByteBuffer;

public class SfsClient {
    public static void main(String args[]){
        try {
            TTransport transport;

            transport = new TSocket("localhost", 9090);
            transport.open();
            TProtocol protocol = new TBinaryProtocol(transport);
            FileSystem.Client client = new FileSystem.Client(protocol);
             TestClient(client);
            transport.close();
        } catch (TException x) {
            x.printStackTrace();
        }

    }
    public static void TestClient(FileSystem.Client client) throws TException{

        String path="/Users/bing/Desktop/IDEAP/thrift-start-learning/Src/com/cimon/SimpleFileSystem";
        String filePath = "/Users/bing/Desktop/IDEAP/thrift-start-learning/Src/com/cimon/SimpleFileSystem/StorageFile";

        File f=new File(filePath+"/"+"FileSystem.thrift");
        tools.printThriftFile(tools.getFileInfo(f));
         // System.out.println(client.cat(path+"/"+"FileSystem.thrift",Mode.TXT));
        // System.out.println(client.cat(path+"/"+"FileSystem.thrift",Mode.BIN));

        client.uploadFile("test.txt",ByteBuffer.wrap(tools.toByteArray(path+"/"+"test.txt")));
        tools.writeByteBuffer(filePath+"/"+"/FromHelloWorld.txt",client.downFile(path+"/HelloWorld.txt"));

        //System.out.println(client.ls(path).size());

        for(ThriftFile tf : client.ls(path)){
            //System.out.println(" in  ");
            if(tf==null)
                break;
            else
                tools.printThriftFile(tf);
        }


    }
}
