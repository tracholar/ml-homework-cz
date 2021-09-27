package com.tracholar.demo.abtest;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:38
 */
public interface IABTest {
    /**
     * 获取流量的AB测试信息
     * @param flowId 流量信息，可以是uid，cooke-id等等
     * @return
     */
    IABTestInfo getABTestInfo(String flowId);
}
