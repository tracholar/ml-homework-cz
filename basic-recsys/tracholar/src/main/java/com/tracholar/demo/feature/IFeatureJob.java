package com.tracholar.demo.feature;

import com.tracholar.demo.feature.dag.IEngineContext;
import com.tracholar.demo.feature.dag.INode;
import com.tracholar.demo.feature.job.IJobResults;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:54
 *
 * 生产特征的Job，也是DAG图的节点
 */
public interface IFeatureJob<T extends IEngineContext, R extends IJobResults>
        extends INode<T, R> {
    /**
     * 依赖的其他特征
     * @return
     */
    List<String> getDependence();

    /**
     * 用于engine添加依赖
     * @param job
     */
    void addDependence(IFeatureJob job);

    /**
     * 输出特征名
     * @return
     */
    List<String> getOutputNames();

    /**
     * 执行特征抽取逻辑
     * @param ctx
     * @return
     */
    @Override
    R run(T ctx);
}
