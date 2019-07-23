package com.tracholar.testing;

import sun.security.provider.MD5;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class IdGenerator {
    public static long generateNewId(){
        return System.currentTimeMillis();
    }
}
