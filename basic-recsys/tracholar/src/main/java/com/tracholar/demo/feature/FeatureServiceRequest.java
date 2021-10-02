package com.tracholar.demo.feature;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.feature.dag.IEngineContext;
import com.tracholar.demo.feature.job.FeatureJobContext;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:24
 */
@Builder
@Getter
public class FeatureServiceRequest {
    private List<IEngineItem> items;
    private EngineRequest req;

    public FeatureJobContext buildFeatureJobContext(){
        FeatureJobContext ctx = new FeatureJobContext();
        ctx.setUid(req.getUid());
        ctx.setItems(items);

        return ctx;
    }
}
