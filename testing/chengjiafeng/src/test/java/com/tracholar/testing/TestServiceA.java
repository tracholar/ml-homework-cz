package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.core.PowerMockUtils;
import org.powermock.modules.junit4.PowerMockRunner;
import org.powermock.reflect.Whitebox;

import static org.powermock.configuration.ConfigurationType.PowerMock;


@RunWith(PowerMockRunner.class)
public class TestServiceA {
    @Test
    public void test1(){
        ServiceA a;
        a = new ServiceA();
    }
}
