package com.zwt.server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class ServerApplication {
    private static HelloWorldServerThread rpcThriftServer;
    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(HelloWorldServerThread.class, args);
        try {
            rpcThriftServer = context.getBean(HelloWorldServerThread.class);
            rpcThriftServer.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

//package com.hansonwang99.server;
//
//import org.springframework.boot.SpringApplication;
//import org.springframework.boot.autoconfigure.SpringBootApplication;
//import org.springframework.context.ApplicationContext;
//
//@SpringBootApplication
//public class RPCThriftServerApplication {
//    private static RPCThriftServer rpcThriftServer;
//    public static void main(String[] args) {
//        ApplicationContext context = SpringApplication.run(RPCThriftServerApplication.class, args);
//        try {
//            rpcThriftServer = context.getBean(RPCThriftServer.class);
//            rpcThriftServer.start();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }
//}
