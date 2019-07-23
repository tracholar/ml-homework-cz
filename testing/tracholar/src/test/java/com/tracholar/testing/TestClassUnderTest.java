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
@RunWith(PowerMockRunner.class)
@PrepareForTest(IdGenerator.class)
public class TestClassUnderTest {
    @Test
    public void demoStaticMethodMocking() throws Exception {
        mockStatic(IdGenerator.class);
        when(IdGenerator.generateNewId()).thenReturn(2L);
        new ClassUnderTest().methodToTest();

        verifyStatic(IdGenerator.class);
        IdGenerator.generateNewId();
    }
}
