package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.core.classloader.annotations.SuppressStaticInitializationFor;
import org.powermock.modules.junit4.PowerMockRunner;
import org.powermock.reflect.Whitebox;

import java.util.logging.Logger;

/**
 * Created by zuoyuan on 2019/7/23.
 */
public class TestStaticFieldTest {
    @Test
    public void test1(){
        //TODO 测试下面的方法调用
        StaticFieldTest test = new StaticFieldTest();
        test.doSomething();
    }
}
