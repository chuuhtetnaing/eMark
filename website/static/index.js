var height = 450;
var width = 800;

const stage = new Konva.Stage({
    height: height,
    width: width,
    container:"konva-holder",
});

const layer = new Konva.Layer();
stage.add(layer);

const stageBorder = new Konva.Rect({
    x: 0,
    y: 0,
    stroke: "black",
    strokeWidth: 1,
    height: stage.height(),
    width: stage.width(),
});
layer.add(stageBorder)

var imageObj = new Image();
imageObj.src = "website/static/watermarked.jpg";

// var imageButton = document.getElementById('insert_image');
imageObj.onload = function () {
    var imageKon = new Konva.Image({
        x: 50,
        y: 50,
        image: imageObj,
        width: imageObj.width,
        height: imageObj.height,
    });
// add the shape to the layer
layer.add(imageKon);
};


var rectButton = document.getElementById('rectangletool');
rectButton.addEventListener('click', function(){
    //create new shape
    var rect = new Konva.Rect({
        x: 50,
        y: 50,
        height: 100,
        width: 200,
        fill: "white",
        stroke: "orange",
        strokeWidth: 2,
        cornerRadius: 8,
        draggable: true,
    })

    layer.add(rect);
})

// $("#file").change(function(e){


//     var URL = window.webkitURL || window.URL;
//     var url = URL.createObjectURL(e.target.files[0]);
//     var img = new Image();
//     img.src = url;


//     img.onload = function() {

//         var img_width = img.width;
//         var img_height = img.height;
  
//         // calculate dimensions to get max 300px
//         var max = 300;
//         var ratio = (img_width > img_height ? (img_width / max) : (img_height / max))
  
//         // now load the Konva image
//         var theImg = new Konva.Image({
//           image: img,
//           x: 50,
//           y: 30,
//           width: img_width/ratio,
//           height: img_height/ratio,
//           draggable: true,
//           rotation: 0
//         });
  
//         layer.add(theImg);
//         layer.draw();
//       }
//     });

function save (){
    var filename = document.getElementById("fname").ariaValueMax;
    var data = JSON.stringify(canvas_data);

    $.post("/", {save_fname: filename, save_cdata: data });
    alert(file + "saved");
    
}

function convertToDataURLviaCanvas(url, callback, outputFormat){
    var img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = function(){
        var canvas = document.createElement('CANVAS');
        var ctx = canvas.getContext('2d');
        var dataURL;
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this, 0, 0);
        dataURL = canvas.toDataURL(outputFormat);
        callback(dataURL);
        canvas = null;
    };
    img.src = url;
}
