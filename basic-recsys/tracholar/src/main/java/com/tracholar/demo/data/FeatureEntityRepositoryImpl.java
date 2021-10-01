package com.tracholar.demo.data;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.List;

/**
 * @author zuoyuan
 * @date 2021/10/1 23:04
 */
public class FeatureEntityRepositoryImpl implements CustomFeatureQuery{
    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public List<FeatureEntity> findFeature(int type, List<Long> items, List<String> names) {
        String sql = "select * from feature_entity where type = ? and id in (?) and name in (?)";
        Query query = entityManager.createNativeQuery(sql);
        query.setParameter(1, (short)type);
        query.setParameter(2, items);
        query.setParameter(3, names);
        List<FeatureEntity> data = query.getResultList();

        return data;
    }
}
