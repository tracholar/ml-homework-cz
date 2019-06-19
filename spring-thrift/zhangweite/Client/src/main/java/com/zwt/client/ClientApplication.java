package com.zwt.client;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;


@SpringBootApplication
public class ClientApplication {
	private static HelloWorldClient rpcThriftServer;
	public static void main(String[] args) {
		ApplicationContext context = SpringApplication.run(HelloWorldClient.class, args);
		try {
			rpcThriftServer = context.getBean(HelloWorldClient.class);
			rpcThriftServer.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}

