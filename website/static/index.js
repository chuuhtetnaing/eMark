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

// main API:
var imageObj = new Image();
imageObj.src = '/website/static/watermarked.jpg';

imageObj.onload = function () {
  var yoda = new Konva.Image({
    x: 50,
    y: 50,
    image: imageObj,
    width: 106,
    height: 118,
  });

  // add the shape to the layer
  layer.add(yoda);
};


var addButton = document.getElementById('rectangletool');
addButton.addEventListener('click', function(){
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
