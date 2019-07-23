package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.core.PowerMockUtils;
import org.powermock.modules.junit4.PowerMockRunner;
import org.powermock.reflect.Whitebox;

import static org.powermock.configuration.ConfigurationType.PowerMock;


/**
 * Created by zuoyuan on 2019/7/19.
 */
@RunWith(PowerMockRunner.class)
public class TestServiceA {
    @Test
    public void test1(){
        ServiceA a = new ServiceA();
    }
}
