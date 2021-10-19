package com.tracholar.demo.utils;

import org.junit.Test;

/**
 * @author zuoyuan
 * @date 2021/10/9 20:01
 */
public class MyUtilsTest {
    private MyUtils utils = new MyUtils();
    @Test
    public void testImgMatch(){
        String data = "<img src=\"http://xxx.xx\"/>";
        System.out.println(utils.extractHeadImg(data));
    }
}
