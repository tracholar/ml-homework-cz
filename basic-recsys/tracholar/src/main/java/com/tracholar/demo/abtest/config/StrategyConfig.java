package com.tracholar.demo.abtest.config;

import lombok.Data;

import java.util.Set;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:55
 */
@Data
public class StrategyConfig {
    private String strategyName;
    private Set<Integer> flows;
    private String desc;
}
