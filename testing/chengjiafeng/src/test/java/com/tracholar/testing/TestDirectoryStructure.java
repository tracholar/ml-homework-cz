package com.tracholar.testing;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

import java.io.File;

import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.powermock.api.mockito.PowerMockito.verifyNew;
import static org.powermock.api.mockito.PowerMockito.when;
import static org.powermock.api.mockito.PowerMockito.whenNew;

/**
 * Created by zuoyuan on 2019/7/19.
 */
@RunWith(PowerMockRunner.class)
@PrepareForTest(DirectoryStructure.class)
public class TestDirectoryStructure {
    @Test
    public void createDirectoryWhenNotExists() throws Exception {
        final String directoryPath = "mocked path";
        //TODO 测试下面的方法调用
        File directoryMock = mock(File.class);

        whenNew(File.class).withArguments(directoryPath).thenReturn(directoryMock);
        when(directoryMock.exists()).thenReturn(false);
        when(directoryMock.mkdirs()).thenReturn(true);

        assertTrue(new DirectoryStructure().create(directoryPath));
        verifyNew(File.class).withArguments(directoryPath);
    }
}
