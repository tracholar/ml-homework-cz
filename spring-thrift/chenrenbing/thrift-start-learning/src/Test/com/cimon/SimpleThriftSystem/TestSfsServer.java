package Test.com.cimon.SimpleThriftSystem;
import com.cimon.SimpleFileSystem.*;
import org.apache.thrift.TException;
import java.util.List;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class TestSfsServer {
    @Before
    public void StartTest(){
        System.out.println("Start to test ....");
    }

    @Test
    public void TestLs() throws TException {
       FileSystemHandler fsl= new FileSystemHandler();
       List<ThriftFile> tfl=fsl.ls("./");
       for(ThriftFile tf : tfl){
           //System.out.println(" in  ");
           if(tf==null)
               break;
           else
               tools.printThriftFile(tf);
       }

   }
    @Test
    public void TestCat(){

   }
    @After
    public void AfterTest(){
        System.out.println("test end ....");
    }
}
