
document.addEventListener("DOMContentLoaded", function () {
// Setup to load data from rawgit
NGL.DatasourceRegistry.add(
    "data", new NGL.StaticDatasource( "//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/" )
);

// Create NGL Stage object
var stage = new NGL.Stage( "viewport1" );

// Handle window resizing
window.addEventListener( "resize", function( event ){
    stage.handleResize();
}, false );


// Code for example: interactive/simple-viewer

function addElement (el) {
  Object.assign(el.style, {
    position: "absolute",
    zIndex: 10
  })
  stage.viewer.container.appendChild(el)
}

function createElement (name, properties, style) {
  var el = document.createElement(name)
  Object.assign(el, properties)
  Object.assign(el.style, style)
  return el
}

function createSelect (options, properties, style) {
  var select = createElement("select", properties, style)
  options.forEach(function (d) {
    select.add(createElement("option", {
      value: d[ 0 ], text: d[ 1 ]
    }))
  })
  return select
}

function createFileButton (label, properties, style) {
  var input = createElement("input", Object.assign({
    type: "file"
  }, properties), { display: "none" })
  addElement(input)
  var button = createElement("input", {
    value: label,
    type: "button",
    onclick: function () { input.click() }
  }, style)
  return button
}

function loadStructure (input) {
  stage.removeAllComponents()
  return stage.loadFile(input).then(function (o) {
    o.autoView()
    o.addRepresentation(polymerSelect.value, {
      sele: "polymer",
      name: "polymer"
    })
    o.addRepresentation("ball+stick", {
      name: "ligand",
      visible: ligandCheckbox.checked,
      sele: "not ( polymer or water or ion )"
    })
    o.addRepresentation("spacefill", {
      name: "waterIon",
      visible: waterIonCheckbox.checked,
      sele: "water or ion",
      scale: 0.25
    })
  })
}

var loadStructureButton = createFileButton("load structure", {
  accept: ".pdb,.cif,.ent,.gz,.mol2",
  onchange: function (e) {
    if (e.target.files[ 0 ]) {
      loadStructure(e.target.files[ 0 ])
    }
  }
})
document.getElementById('buttons').appendChild(loadStructureButton)

var polymerSelect = createSelect([
  [ "cartoon", "cartoon" ],
  [ "spacefill", "spacefill" ],
  [ "licorice", "licorice" ],
  [ "surface", "surface" ]
], {
  onchange: function (e) {
    stage.getRepresentationsByName("polymer").dispose()
    stage.eachComponent(function (o) {
      o.addRepresentation(e.target.value, {
        sele: "polymer",
        name: "polymer"
      })
    })
  }
})
document.getElementById('buttons').appendChild(polymerSelect)

var ligandCheckbox = createElement("input", {
  type: "checkbox",
  checked: true,
  onchange: function (e) {
    stage.getRepresentationsByName("ligand")
      .setVisibility(e.target.checked)
  }
})
addElement(ligandCheckbox)
addElement(createElement("span", {
  innerText: "ligand"
}))

var waterIonCheckbox = createElement("input", {
  type: "checkbox",
  checked: false,
  onchange: function (e) {
    stage.getRepresentationsByName("waterIon")
      .setVisibility(e.target.checked)
  }
}, { top: "84px", left: "12px" })
addElement(waterIonCheckbox)
addElement(createElement("span", {
  innerText: "water+ion"
}, { top: "84px", left: "32px" }))

x = false

var spinButton = createElement("input", {
  type: "button",
  id: "toggleSpin",
  value: "Spin",
  onclick: function () {
    if (x){
    stage.setSpin(false)
    x=false
    }
    else{
    stage.setSpin(true)
    x=true
    }
  }
}, { top: "108px", left: "12px" })
document.getElementById('buttons').appendChild(spinButton)
postid = document.getElementById("postid").textContent
loadStructure("/media/"+postid+"/start.mol2")

    });
