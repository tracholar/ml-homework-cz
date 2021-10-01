package com.tracholar.demo.feature.job.item;

import com.tracholar.demo.data.FeatureEntity;
import com.tracholar.demo.data.FeatureEntityRepository;
import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.IFeatureJob;
import com.tracholar.demo.feature.dag.INode;
import com.tracholar.demo.feature.job.FeatureJobContext;
import com.tracholar.demo.feature.job.IItemJob;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/10/1 16:33
 */
@Component
public class ItemBaseFeatureJob implements IItemJob {
    @Override
    public List<String> getDependence() {
        return null;
    }

    @Override
    public void addDependence(IFeatureJob job) {

    }

    @Override
    public List<INode> getDependenceNode() {
        return null;
    }

    @Getter
    private List<String> outputNames = Arrays.asList(
            "ITEM_INFO",
            "ITEM_STAT_FEAT"
    );

    @Autowired
    private FeatureEntityRepository rep;

    @Override
    public ItemJobResults run(FeatureJobContext ctx) {
        Map<EngineItemType, List<IEngineItem>> map = new HashMap<>();
        ctx.getItems().forEach(e -> {
            if(map.get(e.getType()) == null){
                map.put(e.getType(), new LinkedList<>());
            }
            map.get(e.getType()).add(e);
        });

        ItemJobResults results = new ItemJobResults();
        map.entrySet().stream()
                .forEach(e -> {
                    List<Long> ids = e.getValue().stream().map(x -> x.getId())
                            .collect(Collectors.toList());
                    List<FeatureEntity> r = rep.findFeature(e.getKey().getId(), ids, outputNames);
                    for(IEngineItem item : e.getValue()){
                        if(!results.containsKey(item)){
                            results.put(item, new HashMap<>());
                        }
                    }
                    for(FeatureEntity entity : r){
                        // TODO 待完成
                    }
                });
        return results;
    }
}
