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
        String sql = "select * from feature_entity where type = :type and id in :ids and name in :names";
        Query query = entityManager.createNativeQuery(sql);
        query.setParameter("type", (short)type);
        query.setParameter("ids", items);
        query.setParameter("names", names);
        List<FeatureEntity> data = query.getResultList();

        return data;
    }
}
