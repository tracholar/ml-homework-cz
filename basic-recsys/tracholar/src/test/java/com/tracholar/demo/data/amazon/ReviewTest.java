package com.tracholar.demo.data.amazon;

import com.google.gson.Gson;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/30 14:38
 */
public class ReviewTest {
    private Gson gson = new Gson();
    private <T> T safeToJson(String line, Class<T> cls){
        try{
            return gson.fromJson(line, cls);
        }catch(Exception ex){
            return null;
        }
    }
    @Test
    public void test() throws IOException {
        File file = new File("./data/meta_Electronics.json");
        BufferedReader r = new BufferedReader(new FileReader(file));
        List<Electronics> dataset = r.lines()
                .map(line -> safeToJson(line, Electronics.class))
                .collect(Collectors.toList());

        System.out.println(dataset.size());
        System.out.println(dataset.get(1));
    }

    @Test
    public void testReview() throws IOException {
        File file = new File("./data/reviews_Electronics_5.json");
        BufferedReader r = new BufferedReader(new FileReader(file));
        List<Review> dataset = r.lines()
                .map(line -> safeToJson(line, Review.class))
                .collect(Collectors.toList());

        System.out.println(dataset.size());
        System.out.println(dataset.get(1));
    }
}
