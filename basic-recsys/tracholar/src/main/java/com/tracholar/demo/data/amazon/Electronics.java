package com.tracholar.demo.data.amazon;

import com.tracholar.demo.api.IDetail;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/9/30 14:31
 */
@Data
@Entity
@AllArgsConstructor
@NoArgsConstructor
public class Electronics implements IDetail{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "asin", nullable = false)
    private String asin;
    private String imUrl;
    private String description;
    private String[][] categories;
    private String title;
}
