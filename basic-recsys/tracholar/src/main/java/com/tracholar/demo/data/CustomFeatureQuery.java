package com.tracholar.demo.data;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/1 23:05
 */
public interface CustomFeatureQuery {
    /**
     * 查询特征
     * @param type
     * @param items
     * @param names
     * @return
     */
    List<FeatureEntity> findFeature(int type, List<Long> items, List<String> names);
}
