
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
        o.addRepresentation("ball+stick", {
          name: "ligand",
          visible: true,
          sele: "not ( polymer or water or ion )"
        })
        Labrador1 = o.addRepresentation("label", {
          labelType: "atomname",
          visible: false
        })
      })
    }
    
    // var loadStructureButton = createFileButton("load structure", {
    //   accept: ".pdb,.cif,.ent,.gz,.mol2",
    //   onchange: function (e) {
    //     if (e.target.files[ 0 ]) {
    //       loadStructure(e.target.files[ 0 ])
    //     }
    //   }
    // })
    // document.getElementById('buttons1').appendChild(loadStructureButton)
    
    var polymerSelect = createSelect([
      [ "black", "Black" ],
      [ "white", "White" ],
      [ "transparent", "Transparent" ]
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
  
    
  
    x = false
 
    var spinButton = createElement("input", {
      type: "button",
      id: "toggleSpin",
      value: "Spin Off",
      onclick: function () {
        if (x){
        stage.setSpin(false)
        x=false
        spinButton.value = "Spin Off"
        }
        else{
        stage.spinAnimation = stage.animationControls.spin([ 0, 1, 0 ], 0.05)
        stage.setSpin(true)
        x=true
        spinButton.value = "Dream On"
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
    
    labradrzwi1 = false
    var Labels = createElement("input", {
      type: "button",
      id: "label",
      value: "Label Off",
      onclick: function () {
        if (labradrzwi1){
          Labrador1.setVisibility(false)
          Labels.value = "Lable Off"
          labradrzwi1 = false
        }else {
          Labrador1.setVisibility(true)
          Labels.value = "Lable On"
          labradrzwi1 = true
        }
      },
    }, { top: "108px", left: "12px" })
    document.getElementById('buttons1').appendChild(Labels)
    
    postid = document.getElementById("postid").textContent
    loadStructure("/media/"+postid+"/start.mol2")
    
    });
    
    //////////////////////////////////////////////////////////////////////////
    //Viewer 2
    //////////////////////////////////////////////////////////////////////////
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
          o.addRepresentation("ball+stick", {
            name: "ligand",
            visible: true,
            sele: "not ( polymer or water or ion )"
          })
          Labrador = o.addRepresentation("label", {
            labelType: "atomname",
            visible: false
          })
        })
      }
      
      // var loadStructureButton = createFileButton("load structure", {
      //   accept: ".pdb,.cif,.ent,.gz,.mol2",
      //   onchange: function (e) {
      //     if (e.target.files[ 0 ]) {
      //       loadStructure(e.target.files[ 0 ])
      //     }
      //   }
      // })
      // document.getElementById('buttons1').appendChild(loadStructureButton)
      
      var polymerSelect = createSelect([
        [ "black", "Black" ],
        [ "white", "White" ],
        [ "transparent", "Transparent" ]
      ], {
        onchange: function (e) {
          stage.getRepresentationsByName("bg").dispose()
          stage.eachComponent(function (o) {
            if(e.target.value == "transparent"){
              document.getElementsByTagName("canvas")[1].style.backgroundColor = "transparent"
            }
            else{
            stage.setParameters({ backgroundColor: e.target.value })
            }
          })
        }
      })
      document.getElementById('buttons2').appendChild(polymerSelect)

      
      
      
      x = false
      
      var spinButton = createElement("input", {
        type: "button",
        id: "toggleSpin",
        value: "Spin Off",
        onclick: function () {
          if (x){
          stage.setSpin(false)
          x=false
          spinButton.value = "Spin Off"
          }
          else{
          stage.spinAnimation = stage.animationControls.spin([ 0, 1, 0 ], 0.05)
          stage.setSpin(true)
          x=true
          spinButton.value = "Dream On"
          }
        }
      }, { top: "108px", left: "12px" })
      document.getElementById('buttons2').appendChild(spinButton)
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/molecule.mol2")
      
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
      
      labradrzwi = false
      var Labels = createElement("input", {
        type: "button",
        id: "label",
        value: "Label Off",
        onclick: function () {
          if (labradrzwi){
            Labrador.setVisibility(false)
            Labels.value = "Lable Off"
            labradrzwi = false
          }else {
            Labrador.setVisibility(true)
            Labels.value = "Lable On"
            labradrzwi = true
          }
        },
      }, { top: "108px", left: "12px" })
      document.getElementById('buttons2').appendChild(Labels)
      
      postid = document.getElementById("postid").textContent
      loadStructure("/media/"+postid+"/molecule.mol2")
      
      });

try{
  loading_button = document.getElementById("loading-button");
  loading_button.onclick = function() {loadingScreen()};
}
finally{
  console.log("nothing to load")
};
function loadingScreen() {
  document.getElementById("loading").style.display = "block";
};