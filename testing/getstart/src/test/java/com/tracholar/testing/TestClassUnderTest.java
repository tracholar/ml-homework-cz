package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

import static org.powermock.api.mockito.PowerMockito.mockStatic;
import static org.powermock.api.mockito.PowerMockito.verifyStatic;
import static org.powermock.api.mockito.PowerMockito.when;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class TestClassUnderTest {
    @Test
    public void demoStaticMethodMocking() throws Exception {
        //TODO 测试下面的方法调用
        new ClassUnderTest().methodToTest();
    }
}
