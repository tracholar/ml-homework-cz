package com.tracholar.testing;

import java.util.logging.Logger;

/**
 * Created by zuoyuan on 2019/7/23.
 */
public class StaticFieldTest {
    private static Logger logger = Logger.getLogger(StaticFieldTest.class.getName());

    public void doSomething(){
        logger.info("Hello");
    }
}
