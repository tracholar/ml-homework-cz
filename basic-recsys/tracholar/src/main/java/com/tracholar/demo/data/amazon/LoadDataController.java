package com.tracholar.demo.data.amazon;

import com.google.gson.Gson;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/9/30 15:02
 */
@RestController
@RequestMapping("/dataset/amazon")
public class LoadDataController {
    private Gson gson = new Gson();
    private <T> T safeToJson(String line, Class<T> cls){
        try{
            return gson.fromJson(line, cls);
        }catch(Exception ex){
            return null;
        }
    }
    private <T> List<T> load(String path, Class<T> cls) throws IOException {
        File file = new File(path);
        BufferedReader r = new BufferedReader(new FileReader(file));
        List<T> dataset = r.lines()
                .map(line -> safeToJson(line, cls))
                .filter(e -> e != null)
                .collect(Collectors.toList());

        return dataset;
    }

    @Autowired
    private ElectronicsRepository elecRep;
    @Autowired
    private ReviewRepository reviewRep;

    @RequestMapping("/load")
    public int load() throws IOException{
        List<Electronics> electronics = load("./data/meta_Electronics.json", Electronics.class);
        elecRep.saveAll(electronics);

        List<Review> reviews = load("./data/reviews_Electronics_5.json", Review.class);
        reviewRep.saveAll(reviews);

        return 0;
    }

    @RequestMapping("/list/electronics")
    public List<Electronics> listElec(){
        List<Electronics> dataset = new LinkedList<>();
        for(Electronics e : elecRep.sampleList()){
            dataset.add(e);
            if(dataset.size() >= 100){
                break;
            }
        }

        return dataset;
    }

    @RequestMapping("/list/review")
    public List<Review> listReview(){
        List<Review> dataset = new LinkedList<>();
        for(Review e : reviewRep.sampleList()){
            dataset.add(e);
            if(dataset.size() >= 100){
                break;
            }
        }

        return dataset;
    }
}
