package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.INode;
import lombok.Data;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:35
 *
 * 中间节点
 */
@Data
public abstract class TransformerJob implements IFeatureJob {
    private List<String> dependence;
    private List<String> outputNames;
    private List<INode> dependenceNode;

}
