
image = document.getElementById('image');
result = document.getElementById('results');
prob = document.getElementById('prob');

ml5.imageClassifier('MobileNet')
    .then(cls => cls.classify(image))
    .then(function (res){
        console.log(res);
        result.innerText = res[0].label;
        prob.innerText = res[0].confidence.toFixed(4);
    })

