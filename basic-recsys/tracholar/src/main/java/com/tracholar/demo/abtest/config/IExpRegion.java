package com.tracholar.demo.abtest.config;

import com.tracholar.demo.abtest.ABTestInfo;

/**
 * @author zuoyuan
 * @date 2021/10/3 11:34
 */
public interface IExpRegion {
    /**
     * 生产命中的实验key
     * @param flowId
     * @param bucketNum
     * @return
     */
    ABTestInfo genABTestInfo(String flowId, int bucketNum);
}
