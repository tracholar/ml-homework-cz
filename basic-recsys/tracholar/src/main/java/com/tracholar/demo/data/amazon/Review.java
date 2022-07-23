package com.tracholar.demo.data.amazon;

import com.tracholar.demo.api.IDetail;
import lombok.Data;

import javax.persistence.*;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 14:31
 */
@Data
@Entity
public class Review {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "reviewer_id", nullable = false)
    private String reviewerID;
    private String asin;
    private String reviewerName;
    private int[] helpful;
    private String reviewText;
    private float overall;
    private String summary;
    private long unixReviewTime;
    private String reviewTime;
}
