package com.tracholar.demo.model;

import com.tracholar.demo.engine.engine.EngineItemType;
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
    private EngineItemType type;
    private long id;
    private Map<String, Object> features;

    public String getUniqueId(){
        return String.format("%s-%s-%s-%s", reqId, uid, type.toString(), id);
    }
}
