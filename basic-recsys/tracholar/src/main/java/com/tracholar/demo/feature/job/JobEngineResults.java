package com.tracholar.demo.feature.job;

import com.tracholar.demo.feature.job.global.GlobalJobResults;
import com.tracholar.demo.feature.job.item.ItemJobResults;
import lombok.Data;

/**
 * @author zuoyuan
 * @date 2021/10/1 22:18
 */
@Data
public class JobEngineResults {
    private GlobalJobResults globalJobResults;
    private ItemJobResults itemJobResults;
}
