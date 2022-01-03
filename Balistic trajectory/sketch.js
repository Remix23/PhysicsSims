let ball = {
  angle : 0, // in degrees
  r : 1, // in meters
  mass : 10, // in kg 
  dragCoefficient : 0.45,

  posX : 0,
  posY : 0,

  velX : 0,
  velY : 0,

  accX : 0,
  accY : 0,
}

const airDensity = 1.225;
const canvasHeight = 600;
const canvasWidth = 1000;
const frameRateCount = 60;


const velStart = 100;
const angleStart = 45;

function setup() {
  createCanvas(canvasWidth, canvasHeight);

  frameRate(frameRateCount);

  translate(0, canvasHeight);

  console.log(ball)

  ball.velX = Math.cos(Math.PI / 180 * angleStart) * velStart;
  ball.velY = Math.sin(Math.PI / 180 * angleStart) * velStart;
  
  for (let i = 0; i < 5; i++)
  {
    update();
    console.log(ball)
  }
}

function calculateDrag ()
{
  let ballCrossection = Math.PI * ball.r * ball.r
  let dragForceX = Math.pow(ball.velX, 2) * ball.dragCoefficient * ballCrossection * airDensity / 2;
  let dragForceY = Math.pow(ball.velY, 2) * ball.dragCoefficient * ballCrossection * airDensity / 2;
  console.log(dragForceX, dragForceY);
  return {x : dragForceX, y : dragForceY};
}

function update ()
{
  ball.accX = 0;
  ball.accY = -9.8;

  let dragForces = calculateDrag();

  ball.accX -= dragForces.x / ball.mass;
  ball.accY -= dragForces.y / ball.mass;

  ball.velX += ball.accX * deltaTime;
  ball.velY += ball.accY * deltaTime;

  ball.posX += ball.velX * deltaTime;
  ball.posY += ball.velY * deltaTime;
}

function draw() {
  clear();
  fill(255);
  ellipse(ball.posX - ball.r / 2, ball.posY - ball.r / 2, ball.r, ball.r )
  // update();
}
