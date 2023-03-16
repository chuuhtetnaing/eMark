const stage = new Konva.Stage({
    height: 750,
    width: 450,
    container:"konva-holder",
});

const layer = new Konva.Layer();
stage.add(layer);

const rect = new Konva.Rect({
    x: 50, //rectangle location
    y: 50, //rectangle location
    fill: "blue", //fill color
    height: 100,
    width: 200,
    stroke: "orange",
    strokeWidth: 8,
    cornerRadius: 8,
    draggable: true,
});

layer.add(rect)

function rectangle(){
    layer.add(rect)
}

function save (){
    var filename = document.getElementById("fname").ariaValueMax;
    var data = JSON.stringify(canvas_data);

    $.post("/", {save_fname: filename, save_cdata: data });
    alert(file + "saved");
    
}
