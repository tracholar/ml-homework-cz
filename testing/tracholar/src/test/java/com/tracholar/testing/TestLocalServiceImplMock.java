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
@RunWith(MockitoJUnitRunner.class)
public class TestLocalServiceImplMock {
    private LocalServiceImpl localService;

    private ServiceA remoteService;

    @Before
    public void setUp(){
        localService = new LocalServiceImpl();
        remoteService = Mockito.mock(ServiceA.class);
        Whitebox.setInternalState(localService, "remoteService", remoteService);

    }

    @Test
    public void testMock(){
        Node target = new Node(1, "target");
        Mockito.when(remoteService.getRemoteNode(1)).thenReturn(target);
        Node result = localService.getRemoteNode(1);

        assertEquals(target, result);
        assertEquals(1, result.getNum());
        assertEquals("target", result.getName());

        Node result2 = localService.getRemoteNode(2);
        assertNull(result2);
    }
}
