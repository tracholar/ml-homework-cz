package com.tracholar.demo.feature.dag;

/**
 * @author zuoyuan
 * @date 2021/10/1 12:15
 *
 * 引擎执行上下文
 */
public interface IEngineContext<T extends INode, S> {
    /**
     * 是否已经执行过了
     * @param node
     * @return
     */
    boolean isExecuted(T node);

    /**
     *
     * @param node
     */
    void addFinishedNode(T node, S results);
}
