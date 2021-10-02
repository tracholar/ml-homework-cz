package com.tracholar.demo.abtest.config;

import lombok.Data;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:46
 */
@Data
public class ABTestConfig {
    private String appName;
    /**
     * 分桶数目，所有层都用这个配置
     */
    private int bucketNum;
    /**
     * 流量区分流随机种子
     */
    private int seed;
    private String desc;
    /**
     * 多个实验区，一般配置为 跨层实验区，正交试验区
     */
    private List<ExpRegion> regions;
    // 默认区域
    private String defaultRegion;

    public ExpRegion findDefaultRegion(){
        for(ExpRegion region : regions){
            if(region.getName().equals(defaultRegion)){
                return region;
            }
        }
        return null;
    }
}
