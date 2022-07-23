package com.tracholar.demo.data;


import com.tracholar.demo.engine.engine.EngineItemType;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

/**
 * @author zuoyuan
 * @date 2021/9/29 15:38
 */
@RunWith(SpringJUnit4ClassRunner.class)
@DataJpaTest
public class InvertIndexTest {
    @Autowired
    private InvertIndexEntityRepository repository;

    @Test
    public void test(){
        InvertIndex index = new InvertIndex();
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 1, 0.21f));
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 2, 0.1f));
        index.add(new InvertIndex.Data(EngineItemType.ARTICLE.getId(), 3, 0.1f));

        System.out.println(index);

        InvertIndexEntity entity = new InvertIndexEntity();
        entity.setData(index);
        entity.setKey("toplist");

        System.out.println(entity);
        repository.save(entity);
    }
}
