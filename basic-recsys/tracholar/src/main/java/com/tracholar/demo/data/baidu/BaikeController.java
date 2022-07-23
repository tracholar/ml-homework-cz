package com.tracholar.demo.data.baidu;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author zuoyuan
 * @date 2021/10/9 19:27
 */
@RestController
@RequestMapping("/baike")
public class BaikeController {
    @Autowired
    private BaikeRepository repository;

    @RequestMapping("/load")
    public int load() throws Exception {
        File file = new File("./data/baidu_baike.txt");
        BufferedReader r = new BufferedReader(new FileReader(file));
        List<Baike> dataset = r.lines().map(line -> line.split("\t", 4))
                .filter(e -> e.length == 4)
                .map(e -> {
                    Baike baike = new Baike();
                    baike.setTitle(e[0]);
                    baike.setUrl(e[1]);
                    baike.setDescription(e[2]);
                    baike.setContentBody(e[3]);

                    return baike;
                }).collect(Collectors.toList());
        repository.saveAll(dataset);
        return dataset.size();
    }

    @RequestMapping("/sample")
    public Iterable<Baike> sample(){
        return repository.sample();
    }
}
