package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.INode;
import lombok.Data;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:30
 *
 * 查
 */
@Data
public class IOJob implements IFeatureJob {
    private List<String> outputNames;
    private boolean executed = false;

    @Override
    public List<String> getDependence() {
        return null;
    }

    @Override
    public List<INode> getDependenceNode() {
        return null;
    }

    @Override
    public boolean run() {
        // TODO 查数据
        executed = true;
        return true;
    }
}
