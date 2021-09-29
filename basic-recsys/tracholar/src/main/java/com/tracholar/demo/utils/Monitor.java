package com.tracholar.demo.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:50
 */
public class Monitor {
    private static final Logger logger = LoggerFactory.getLogger(Monitor.class);

    public static void log(String type, String name){
        logger.info("{}\t{}", type, name);
    }
}
