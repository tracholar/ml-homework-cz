package com.tracholar.demo.abtest.config;

import com.tracholar.demo.abtest.ABTestInfo;
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
     * 多个实验区，跨层实验区，正交试验区
     */
    private MultiLayerExpRegion multiLayerExpRegion;
    private ExpRegion region;

    public IExpRegion findMatchRegion(String flowId){
        int flow = Hash.hash(flowId, seed) % bucketNum;
        if(multiLayerExpRegion.getFlows().contains(flow)){
            return multiLayerExpRegion;
        }
        return region;
    }

    public ABTestInfo generateExpInfo(String flowId){
        IExpRegion reg = findMatchRegion(flowId);
        return reg.genABTestInfo(flowId, bucketNum);
    }
}
