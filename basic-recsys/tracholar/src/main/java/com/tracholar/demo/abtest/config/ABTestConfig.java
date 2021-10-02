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
    private int seed;
    private String desc;
    /**
     * 多个实验区，一般配置为 跨层实验区，正交试验区
     */
    private List<ExpRegion> regions;
}
