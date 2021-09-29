package com.tracholar.demo.data;

import com.tracholar.demo.engine.engine.EngineItemType;
import com.tracholar.demo.engine.engine.GeneralEngineItem;
import com.tracholar.demo.engine.engine.IEngineItem;
import lombok.Getter;

import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:30
 *
 * 倒排索引
 */
public class InvertIndex extends LinkedList<InvertIndex.Data> {
    public static class Data {
        @Getter
        private int type;
        @Getter
        private long id;
        @Getter
        private float score;

        public Data(int type, long id, float score) {
            this.type = type;
            this.id = id;
            this.score = score;
        }

        @Override
        public String toString() {
            return String.format("(%d,%d,%.2g)", type, id, score);
        }

        public GeneralEngineItem toItem(){
            GeneralEngineItem item = new GeneralEngineItem();
            item.setType(EngineItemType.fromId(type));
            item.setId(id);
            item.setScore(score);

            return item;
        }
    }

    public List<IEngineItem> toItems(){
        return this.stream().map(e -> e.toItem())
                .collect(Collectors.toList());
    }
}
