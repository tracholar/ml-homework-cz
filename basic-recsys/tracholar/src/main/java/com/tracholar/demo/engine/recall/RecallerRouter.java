package com.tracholar.demo.engine.recall;

import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.IEngineItem;
import lombok.Setter;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 17:54
 *
 * 召回的路由
 */
@Setter
public class RecallerRouter implements IRecaller{
    private IRecaller defaultRecaller;
    private Map<String, IRecaller> routerTable = new HashMap();

    @Override
    public List<IEngineItem> recall(EngineRequest request) {
        IRecaller recaller = routerTable.get(request.getRecallerKey());
        recaller = recaller == null ? defaultRecaller : recaller;

        return recaller.recall(request);
    }
}
