package com.tracholar.demo.data.amazon;

import com.tracholar.demo.api.IDetail;
import lombok.Data;

import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 15:28
 */
@Data
public class ElectronicsDetail implements IDetail {
    private Electronics electronics;
    private List<Review> reviews;
}
