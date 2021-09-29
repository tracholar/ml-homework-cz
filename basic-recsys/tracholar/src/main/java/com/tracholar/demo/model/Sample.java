package com.tracholar.demo.model;

import com.tracholar.demo.feature.IFeature;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/29 20:31
 */
@Getter
@Setter
public class Sample {
    private long id;
    private List<IFeature> features;
}
