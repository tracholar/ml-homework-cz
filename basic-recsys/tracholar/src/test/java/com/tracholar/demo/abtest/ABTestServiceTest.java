package com.tracholar.demo.abtest;

import org.junit.Test;

/**
 * @author zuoyuan
 * @date 2021/10/2 16:02
 */
public class ABTestServiceTest {
   @Test
   public void test(){
       ABTestService service = new ABTestService();
       System.out.println(service.getABTestInfo("0"));
   }
}
