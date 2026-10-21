
/// --- Spawn a cube ---

const cube = new Entity()

// add a transform to the entity
cube.addComponent(new Transform({ position: new Vector3(8, 1, 8) }))

// add a shape to the entity
cube.addComponent(new BoxShape())

// add the entity to the engine
engine.addEntity(cube)

// Create AudioClip object, holding audio file
const clip = new AudioClip('sounds/puzzlepiece.mp3')

// Create AudioSource component, referencing `clip`
const source = new AudioSource(clip)

// Add AudioSource component to entity
cube.addComponent(source)

// Play sound

cube.addComponent(
  new OnClick(() => {
    source.playOnce()
  })
)

/// --- Spawn a remaining cubes ---

const cube2 = new Entity()
const cube3 = new Entity()
const cube4 = new Entity()
const cube5 = new Entity()
const cube6 = new Entity()
const cube7 = new Entity()
const cube8 = new Entity()
const cube9 = new Entity()

// add a transform to the entities
cube2.addComponent(new Transform({ position: new Vector3(8, 7, 9) }))
cube3.addComponent(new Transform({ position: new Vector3(8, 7.5, 8) }))
cube4.addComponent(new Transform({ position: new Vector3(8, 7, 7) }))
cube5.addComponent(new Transform({ position: new Vector3(8, 6, 9.5) }))
cube6.addComponent(new Transform({ position: new Vector3(8, 6, 6.75) }))
cube7.addComponent(new Transform({ position: new Vector3(8, 5, 9) }))
cube8.addComponent(new Transform({ position: new Vector3(8, 4, 8) }))
cube9.addComponent(new Transform({ position: new Vector3(8, 3, 8) }))

// add a shape to the entity
cube2.addComponent(new BoxShape())
cube3.addComponent(new BoxShape())
cube4.addComponent(new BoxShape())
cube5.addComponent(new BoxShape())
cube6.addComponent(new BoxShape())
cube7.addComponent(new BoxShape())
cube8.addComponent(new BoxShape())
cube9.addComponent(new BoxShape())

// add the entity to the engine
engine.addEntity(cube2)
engine.addEntity(cube3)
engine.addEntity(cube4)
engine.addEntity(cube5)
engine.addEntity(cube6)
engine.addEntity(cube7)
engine.addEntity(cube8)
engine.addEntity(cube9)


///TEXT

const MytextEntity = new Entity()
MytextEntity.addComponent(new Transform({ position: new Vector3(5,5,10) }))
const myText = new TextShape("GSMG.IO \n5 BTC PUZZLE CHALLENGE")
MytextEntity.addComponent(myText)
myText.fontSize = 5
myText.color = Color3.Blue()
myText.fontFamily = "Arial, Helvetica, sans-serif"
// add the entity to the engine
engine.addEntity(MytextEntity)
