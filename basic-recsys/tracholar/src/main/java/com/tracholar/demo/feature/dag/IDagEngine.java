package com.tracholar.demo.feature.dag;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/30 21:18
 *
 * DAG执行引擎
 */
public interface IDagEngine {
    /**
     * 执行节点计算逻辑
     * @param ctx
     */
    boolean run(IEngineContext ctx);
}
