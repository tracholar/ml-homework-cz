package com.tracholar.demo.abtest;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:41
 *
 * 获取AB测试信息
 */
public interface IABTestInfo {
    /**
     * 获取实验层的key
     * @param layer
     * @return
     */
    String getLayerKey(String layer);
}
