package com.tracholar.demo.engine.engine;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/27 13:49
 */
@Builder
public class EngineResponse {
    /**
     * 引擎返回的结果
     * @return
     */
    @Getter
    private List<IEngineItem> items;
}
