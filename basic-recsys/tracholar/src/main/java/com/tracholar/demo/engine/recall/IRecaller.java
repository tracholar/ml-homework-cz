package com.tracholar.demo.engine.recall;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:25
 */
public interface IRecaller {
    /**
     * 执行召回
     * @param request
     * @return
     */
    List<IEngineItem> recall(EngineRequest request);
}
