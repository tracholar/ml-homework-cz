package com.tracholar.demo.data;

import lombok.Data;

import javax.persistence.*;

@Table(name = "feature_entity")
@Entity
@Data
public class FeatureEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private String id;

    @Column(nullable = false)
    private short type;

    @Column(nullable = false)
    private long entityId;

    @Column(nullable = false)
    private String name;

    @Column(name = "value", columnDefinition = "TEXT", nullable = false)
    private String value;
}