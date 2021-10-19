package com.tracholar.demo.engine.api.render;

import com.tracholar.demo.api.Item;
import com.tracholar.demo.engine.api.IRender;
import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.IEngineItem;
import com.tracholar.demo.utils.Monitor;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/30 16:26
 */
@Component
public class RenderRouter implements IRender, InitializingBean {
    private Map<EngineItemType, IRender> router = new HashMap<>();

    @Override
    public List<Item> render(List<IEngineItem> items) {
        Map<IRender, List<IEngineItem>> toRender = new HashMap<>();

        for(IEngineItem item : items) {
            EngineItemType type = item.getType();
            IRender r = router.get(type);
            if (r != null) {
                if (!toRender.containsKey(r)) {
                    toRender.put(r, new LinkedList<>());
                }
                toRender.get(r).add(item);
            }else{
                Monitor.log("RenderRouter.NotFoundRender", type.getName());
            }
        }

        // 并行渲染
        List<Item> results = new LinkedList<>();
        toRender.entrySet().parallelStream().map(e ->
                e.getKey().render(e.getValue())
            ).filter(e -> e != null)
            .collect(Collectors.toList())
            .forEach(e -> results.addAll(e));

        results.sort((a, b) -> -a.compareTo(b));
        return results;
    }

    @Autowired
    private ApplicationContext context;
    @Override
    public void afterPropertiesSet() throws Exception {
        router.put(EngineItemType.ARTICLE, context.getBean(ArticleRender.class));
        router.put(EngineItemType.ELECTRONICS, context.getBean(ElectronicsRender.class));
        router.put(EngineItemType.BAIKE, context.getBean(BaikeRender.class));
    }
}
