package com.tracholar.demo.model;

import lombok.Builder;
import lombok.Getter;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:35
 */
@Builder
@Getter
public class PredictResult {
    private long id;
    private float score;
}
