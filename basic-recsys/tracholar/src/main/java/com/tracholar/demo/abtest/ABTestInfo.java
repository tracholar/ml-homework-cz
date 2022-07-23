package com.tracholar.demo.abtest;

import lombok.Data;
import org.springframework.util.StringUtils;

import java.util.HashMap;

/**
 * @author zuoyuan
 * @date 2021/10/2 15:37
 */
public class ABTestInfo extends HashMap<String, String> implements IABTestInfo{
    @Override
    public String getLayerKey(String layer) {
        return getOrDefault(layer, "default");
    }
}
