package com.tracholar.testing;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.powermock.reflect.Whitebox;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class TestLocalServiceImplMock {
    private LocalServiceImpl localService;

    private ServiceA remoteService;

    @Before
    public void setUp(){
        localService = new LocalServiceImpl();

    }

    @Test
    public void testMock(){
        //TODO 测试下面的方法调用
        Node target = new Node(1, "target");
        Node result = localService.getRemoteNode(1);

        assertEquals(target, result);
        assertEquals(1, result.getNum());
        assertEquals("target", result.getName());

        Node result2 = localService.getRemoteNode(2);
        assertNull(result2);
    }
}
