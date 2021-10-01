package com.tracholar.demo.feature;

import com.tracholar.demo.feature.dag.INode;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:54
 *
 * 生产特征的Job，也是DAG图的节点
 */
public interface IFeatureJob extends INode {
    /**
     * 依赖的其他特征
     * @return
     */
    List<String> getDependence();

    /**
     * 输出特征名
     * @return
     */
    List<String> getOutputNames();
}
