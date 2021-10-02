package com.tracholar.demo.engine.api;

import com.tracholar.demo.abtest.IABTest;
import com.tracholar.demo.api.Item;
import com.tracholar.demo.api.RecsysApi;
import com.tracholar.demo.api.Request;
import com.tracholar.demo.api.Response;
import com.tracholar.demo.engine.api.render.ArticleRender;
import com.tracholar.demo.engine.engine.EngineRequest;
import com.tracholar.demo.engine.engine.EngineResponse;
import com.tracholar.demo.engine.engine.IEngine;
import com.tracholar.demo.engine.engine.SimpleRecEngine;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:35
 */
@RestController
@RequestMapping("/api")
public class RecsysApiImpl implements RecsysApi {
    @Resource(name = "simpleRecEngine")
    private IEngine engine;
    @Resource(name = "renderRouter")
    private IRender render;
    @Autowired
    private IABTest abTest;

    public Response recommend(Request req) {
        EngineRequest engineReq = EngineRequest.builder()
                .uid(req.getUid())
                .abTestInfo(abTest.getABTestInfo(String.valueOf(req.getUid())))
                .build();

        EngineResponse response = engine.recommend(engineReq);
        List<Item> items = render.render(response.getItems());

        return ApiResponse.builder()
                .results(items)
                .build();
    }

    @RequestMapping("/recommend")
    public Response index(ApiRequest req){
        return recommend(req);
    }
}
