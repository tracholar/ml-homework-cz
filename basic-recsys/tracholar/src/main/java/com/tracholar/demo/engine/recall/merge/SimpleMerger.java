package com.tracholar.demo.engine.recall.merge;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.IMerger;
import com.tracholar.demo.engine.recall.IRecaller;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:19
 */
public class SimpleMerger implements IMerger {
    @Override
    public List<IEngineItem> merge(Map<IRecaller, List<IEngineItem>> results, EngineRequest request) {
        List<IEngineItem> r = new LinkedList<>();
        results.values().forEach(e -> r.addAll(e));
        return r;
    }
}
