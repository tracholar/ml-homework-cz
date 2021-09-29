package com.tracholar.demo.model;

import lombok.Builder;
import lombok.Getter;

import java.util.List;
import java.util.Map;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:36
 */
@Builder
@Getter
public class PredictResponse implements IPredictResponse{
    private Map<Integer, PredictResult> results;
}
