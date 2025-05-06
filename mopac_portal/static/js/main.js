
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
        o.addRepresentation('surface', {
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
    document.getElementById('buttons1').appendChild(loadStructureButton)
    
    var polymerSelect = createSelect([
      [ "black", "black" ],
      [ "white", "white" ],
      [ "transparent", "transparent" ]
    ], {
      onchange: function (e) {
        stage.getRepresentationsByName("bg").dispose()
        stage.eachComponent(function (o) {
          if(e.target.value == "transparent"){
            document.getElementsByTagName("canvas")[0].style.backgroundColor = "transparent"
          }
          else{
          stage.setParameters({ backgroundColor: e.target.value })
          }
        })
      }
    })
    document.getElementById('buttons1').appendChild(polymerSelect)
    
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
        stage.spinAnimation = stage.animationControls.spin([ 0, 1, 0 ], 0.05)
        stage.setSpin(true)
        x=true
        }
      }
    }, { top: "108px", left: "12px" })
    document.getElementById('buttons1').appendChild(spinButton)
    postid = document.getElementById("postid").textContent
    loadStructure("/media/"+postid+"/start.mol2")
    
    var centerButton = createElement("input", {
      type: "button",
      id: "center",
      value: "Center",
      onclick: function () {
        stage.autoView(1000)
      }
    }, { top: "108px", left: "12px" })
    document.getElementById('buttons1').appendChild(centerButton)
    postid = document.getElementById("postid").textContent
    loadStructure("/media/"+postid+"/start.mol2")
    
    var Labels = createElement("input", {
      type: "button",
      id: "label",
      value: "Label",
      onclick: function () {
        stage.addRepresentation("angle")
      }
    }, { top: "108px", left: "12px" })
    document.getElementById('buttons1').appendChild(Labels)
    postid = document.getElementById("postid").textContent
    loadStructure("/media/"+postid+"/start.mol2")
    
    });
    
    
        
    
    
    document.addEventListener("DOMContentLoaded", function () {
      // Setup to load data from rawgit
      NGL.DatasourceRegistry.add(
          "data", new NGL.StaticDatasource( "//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/" )
      );
      
      // Create NGL Stage object
      var stage = new NGL.Stage( "viewport2" );
      
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
          o.addRepresentation('surface', {
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
      document.getElementById('buttons2').appendChild(loadStructureButton)
      
      var polymerSelect = createSelect([
        [ "white", "white" ],
        [ "black", "black" ],
        [ "transparent", "transparent" ],
        [ "surface", "surface" ]
      ], {
        onchange: function (e) {
          stage.getRepresentationsByName("bg").dispose()
          stage.eachComponent(function (o) {
            if(e.target.value == "transparent"){
              document.getElementsByTagName("canvas")[0].style.backgroundColor = "transparent"
            }
            else{
            stage.setParameters({ backgroundColor: e.target.value })
            }
          })
        }
      })
      document.getElementById('buttons2').appendChild(polymerSelect)
      
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
      }, { top: "84px", left: "12px" })``
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
          stage.spinAnimation = stage.animationControls.spin([ 0, 1, 0 ], 0.05)
          stage.setSpin(true)
          x=true
          }
        }
      }, { top: "108px", left: "12px" })
      document.getElementById('buttons2').appendChild(spinButton)
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/start.mol2")
      
      var centerButton = createElement("input", {
        type: "button",
        id: "center",
        value: "Center",
        onclick: function () {
          stage.autoView(1000)
        }
      }, { top: "108px", left: "12px" })
      document.getElementById('buttons2').appendChild(centerButton)
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/molecule.mol2")
      
      y = false
      var bgButton = createElement("input", {
        type: "button",
        id: "toggleBg",
        value: "Background",
        onclick: function () {
          if (y){
          stage.setParameters({ backgroundColor: "black" })
          y=false
          }
          else{
          stage.setParameters({ backgroundColor: "white" })
          y=true
          }
        }
      }, { top: "108px", left: "12px" })
      document.getElementById('buttons2').appendChild(bgButton)
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/start.mol2")
         
      
      });