package com.tracholar.demo.engine.recall.merge;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.engine.recall.IMerger;
import com.tracholar.demo.engine.recall.IRecaller;
import org.springframework.stereotype.Component;

import java.util.*;

/**
 * @author zuoyuan
 * @date 2021/9/29 19:19
 */
@Component
public class SimpleMerger implements IMerger {
    @Override
    public List<IEngineItem> merge(Map<IRecaller, List<IEngineItem>> results, EngineRequest request) {
        Set<IEngineItem> r = new HashSet<>();
        results.values().forEach(e -> r.addAll(e));
        return new LinkedList<>(r);
    }
}
