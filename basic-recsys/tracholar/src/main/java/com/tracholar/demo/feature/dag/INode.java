package com.tracholar.demo.feature.dag;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:17
 */
public interface INode {
    /**
     * 依赖的节点
     * @return
     */
    List<INode> getDependenceNode();

    /**
     * 执行节点内部的计算逻辑
     * @return
     */
    boolean run();

    /**
     * 是否已经计算过滤
     * @return
     */
    boolean isExecuted();
}
