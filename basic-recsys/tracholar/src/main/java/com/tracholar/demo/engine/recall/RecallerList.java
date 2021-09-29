package com.tracholar.demo.engine.recall;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.merge.SimpleMerger;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:58
 *
 * 多路召回
 */
public class RecallerList implements IRecaller{
    private List<IRecaller> recallList = new LinkedList();
    private IMerger merger = new SimpleMerger();

    @Override
    public List<IEngineItem> recall(EngineRequest request) {
        Map<IRecaller, List<IEngineItem>> results = new HashMap();

        for(IRecaller r : recallList){
            results.put(r, r.recall(request));
        }

        return merger.merge(results, request);
    }
}
