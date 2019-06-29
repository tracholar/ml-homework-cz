package com.tx.homework;

import junit.framework.TestCase;
import org.apache.thrift.TException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.nio.ByteBuffer;
import java.util.List;

public class HelloServerImlTest extends TestCase {

    private HelloServerIml demo;

    @Before
    public void setUp() throws Exception {
        super.setUp();
        demo = new HelloServerIml();
    }

    @After
    public void tearDown() throws Exception {

    }

    @Test
    public void testLs() {
        List<MyFile> myFiles = null;
        try {
            myFiles = demo.ls("/Users/xuetang/workspaces/");
        } catch (TException e) {
            e.printStackTrace();
        }
        myFiles.stream().forEach(System.out::println);
    }

    @Test
    public void testCat() {
        try {
            System.out.println(demo.cat("/Users/xuetang/Downloads/test.bin",ModeStatus.BINARY));
        } catch (TException e) {
            e.printStackTrace();
        }

    }

    @Test
    public void testUpload() {
        byte[] data = "System.out.println(demo.cat(\"/Users/xuetang/Downloads/test.bin\",ModeStatus.BINARY));".getBytes();
        ByteBuffer bs=ByteBuffer.wrap(data);
        try {
            demo.upload("/Users/xuetang/Downloads/test2.txt",bs);
        } catch (TException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testDownload() {
        ByteBuffer bb= null;
        try {
            bb = demo.download("/Users/xuetang/Downloads/test.bin");
        } catch (TException e) {
            e.printStackTrace();
        }
        System.out.println(new String(bb.array(), 0, bb.array().length));
    }
}