package com.tracholar.demo.model;

import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.IFeature;
import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:31
 */
@Getter
@Setter
public class Sample {
    private String reqId;
    private long uid;
    public EngineItemType getType(){
        if(item == null){
            return null;
        }
        return item.getType();
    }
    public long getId(){
        if(item == null){
            return 0;
        }
        return item.getId();
    }
    private Map<String, Object> features;

    public String getUniqueId(){
        return String.format("%s-%s-%s-%s", reqId, uid, getType().toString(), getId());
    }

    private IEngineItem item;
}
