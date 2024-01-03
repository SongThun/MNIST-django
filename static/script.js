// document.addEventListener('DOMContentLoaded', function () {
const canvas = document.getElementById('drawCanvas');
const context = canvas.getContext('2d');
// const clearButton = document.getElementById('clearButton');

let isDrawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

context.fillStyle='black';
context.fillRect(0,0,canvas.width,canvas.height);


function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function draw(e) {
    if (!isDrawing) return;

    context.lineWidth = 10;
    context.lineCap = 'round';
    context.strokeStyle = 'White';

    context.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    context.stroke();
    context.beginPath();
    context.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function stopDrawing() {
    isDrawing = false;
    context.beginPath();
}

function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle='black';
    context.fillRect(0,0,canvas.width,canvas.height);
}


