package com.tracholar.demo.feature.job.item;

import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.job.IJobResults;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/10/1 16:45
 */
public class ItemJobResults extends HashMap<IEngineItem, Map<String, Object>>
        implements IJobResults<ItemJobResults> {
    @Override
    public void merge(ItemJobResults r) {
        if(r == null){
            return;
        }
        for(IEngineItem e : r.keySet()){
            if(!this.containsKey(e)){
                this.put(e, new HashMap<>());
            }
            this.get(e).putAll(r.get(e));
        }
    }
}
