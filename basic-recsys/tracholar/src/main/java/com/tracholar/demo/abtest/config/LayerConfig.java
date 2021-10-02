package com.tracholar.demo.abtest.config;

import lombok.Data;

import java.util.List;
import java.util.Set;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:47
 */
@Data
public class LayerConfig {
    // 层的hash因子
    private int seed;

    // 实验层名
    private String layerName;

    // 多个策略的配置
    private List<StrategyConfig> configs;

    // 默认策略名
    private String defaultStrategy;

    public StrategyConfig findDefaultStrategy(){
        for(StrategyConfig s : configs){
            if(s.getStrategyName().equals(defaultStrategy)){
                return s;
            }
        }
        return null;
    }

    private String desc;
}
