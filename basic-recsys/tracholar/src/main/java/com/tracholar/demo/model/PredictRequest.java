package com.tracholar.demo.model;

import com.tracholar.demo.engine.engine.IEngineItem;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:23
 */
@Getter
@Builder
public class PredictRequest implements IPredictRequest{
    private List<Sample> items;
}
