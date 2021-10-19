package com.tracholar.demo.data.baidu;

import com.tracholar.demo.api.IDetail;
import lombok.Data;

import javax.persistence.*;

/**
 * @author zuoyuan
 * @date 2021/10/9 19:24
 *
 * 百度百科词条
 */
@Data
@Entity
public class Baike implements IDetail {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;
    private String title;
    @Column(length = 1024)
    private String url;
    @Column(columnDefinition = "text")
    private String description;
    @Column(columnDefinition = "longtext")
    private String contentBody;
}
