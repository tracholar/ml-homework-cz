package com.tracholar.demo.data;

import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.GeneralEngineItem;
import com.tracholar.demo.engine.engine.IEngineItem;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.HashMap;
import java.util.Map;

@Table(name = "feature_entity")
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FeatureEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private long id;

    @Column(nullable = false)
    private short type;

    @Column(nullable = false)
    private long entityId;

    @Column(nullable = false)
    private String name;

    @Column(name = "value", columnDefinition = "TEXT", nullable = false)
    private String value;

    public IEngineItem getEngineItem(){
        GeneralEngineItem item = new GeneralEngineItem();
        item.setType(EngineItemType.fromId(type));
        item.setId(entityId);

        return item;
    }

    public Map<String, Object> getFeature(){
        Map<String, Object> feat = new HashMap<>();
        feat.put(name, value);

        return feat;
    }
}