package com.tracholar.demo.abtest.config;

import lombok.Data;

import java.util.List;
import java.util.Set;

/**
 * @author zuoyuan
 * @date 2021/10/2 16:07
 */
@Data
public class ExpRegion {
    private String name;
    private Set<Integer> flows;
    private List<LayerConfig> configs;
}
