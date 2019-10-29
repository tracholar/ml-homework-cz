package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

import static org.junit.Assert.assertEquals;
import static org.powermock.api.mockito.PowerMockito.spy;
import static org.powermock.api.mockito.PowerMockito.verifyPrivate;
import static org.powermock.api.mockito.PowerMockito.when;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class TestPrivatePartialMockingExample {
    @Test
    public void demoPrivateMethodMocking() throws Exception{
        final String expected = "TEST VALUE";
        final String nameOfMethodToMock = "methodToMock";
        final String input = "input";

        //TODO 测试下面的方法调用
        PrivatePartialMockingExample underTest = new PrivatePartialMockingExample();

        assertEquals(expected, underTest.methodToTest());

    }

}
