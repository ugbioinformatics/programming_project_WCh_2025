
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
    
    function loadStructure (input) {
      stage.removeAllComponents()
      return stage.loadFile(input).then(function (o) {
        o.autoView()
        o.addRepresentation("ball+stick", {
          name: "ligand",
          visible: true,
          sele: "not ( polymer or water or ion )"
        })
      })
    }
    
    var backgroundSelect = createSelect([
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
    document.getElementById('buttons1').appendChild(backgroundSelect)
    
    x = false
    var spinButton = createElement("input", {
      type: "button",
      id: "toggleSpin",
      value: "Spin On",
      onclick: function () {
        if (x){
        stage.setSpin(false)
        x=false
        spinButton.value = "Spin On"
        }
        else{
        stage.spinAnimation = stage.animationControls.spin([ 0, 1, 0 ], 0.05)
        stage.setSpin(true)
        x=true
        spinButton.value = "Spin Off"
        }
      }
    }, { top: "108px", left: "12px" })
    document.getElementById('buttons1').appendChild(spinButton)

    
    var centerButton = createElement("input", {
      type: "button",
      id: "center",
      value: "Center",
      onclick: function () {
        stage.autoView(1000)
      }
    })
    document.getElementById('buttons1').appendChild(centerButton)
    
    var Labels = createElement("input", {
      type: "button",
      id: "label",
      value: "Label",
      onclick: function () {
        stage.La
      }
    })
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
    
      
      function loadStructure (input) {
        stage.removeAllComponents()
        return stage.loadFile(input).then(function (o) {
          o.autoView()
          o.addRepresentation("ball+stick", {
            name: "ligand",
            visible: true,
            sele: "not ( polymer or water or ion )"
          })
        })
      }
      
      var backgroundSelect = createSelect([
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
      document.getElementById('buttons2').appendChild(backgroundSelect)
  
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
      })
      document.getElementById('buttons2').appendChild(spinButton)
      
      var centerButton = createElement("input", {
        type: "button",
        id: "center",
        value: "Center",
        onclick: function () {
          stage.autoView(1000)
        }
      })
      document.getElementById('buttons2').appendChild(centerButton)
      
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/start.mol2")
      });