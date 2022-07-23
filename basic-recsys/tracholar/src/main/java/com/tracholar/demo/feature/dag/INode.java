package com.tracholar.demo.feature.dag;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:17
 *
 * 注意，节点Node实现不应该有内部可变的状态
 * 静态图
 */
public interface INode<T extends IEngineContext, R> {
    /**
     * 依赖的节点
     * @return
     */
    List<INode> getDependenceNode();

    /**
     * 执行节点内部的计算逻辑
     * @return
     */
    R run(T ctx);
}
