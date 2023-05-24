let canvas = document.getElementById("paint")
let ctx = canvas.getContext("2d")
let width = canvas.width, height = canvas.height
let curX, curY, prevX, prevY
let hold = false
let fill_value = true, stroke_value = false
let canvas_data = {
    "pencil": [], 
    "line": [], 
    "rectangle": [], 
    "circle": [], 
    "eraser": []
}

ctx.lineWidth = 2

function color(color_value){
    ctx.strokeStyle = color_value
    ctx.fillStyle = color_value
}

function add_pixel(){
    ctx.lineWidth += 1
}

function reduce_pixel(){
    if (ctx.lineWidth ==2)
        return
    else
        ctx.lineWidth -= 1
}

function fill(){
    fill_value = false
    stroke_value = true
}

function outline(){
    fill_value = true
    stroke_value = false
}

function reset(){
    ctx.clearRect(0, 0, width, height)
    canvas_data = {
        "pencil": [], 
        "line": [], 
        "rectangle": [], 
        "circle": [], 
        "eraser": []
    }
}

function pencil (){
    canvas.onmousedown = function(e){
        curX = e.clientX - canvas.offsetLeft
        curY = e.clientY - canvas.offsetTop
        hold = true

        prevX = curX
        prevY = curY
        ctx.beginPath()
        ctx.moveTo(prevX, prevY)
    }

    canvas.onmousemove = function(e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft
            curY = e. clientY - canvas.offsetTop
            draw()
        }
    }
}