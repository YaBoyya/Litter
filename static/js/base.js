let langs = new Map([ 
  ["New", "#a0a000"],
  ["Hot", "#ff0000"],
  ["Easy", "#00ff00"],
  ["Medium", "#ffff00"],
  ["Hard", "#ff0000"],
  ["E", "#00ff00"],
  ["M", "#ffff00"],
  ["H", "#ff0000"],
  ["C", "#0000ff"],
  ["JavaScript", "#5E1DB8"],
  ["Java", "#C5D5E9"],
  ["Python", "#19125D"],
  ["Cpp", "#07CE0B"],
  ["Scheme", "#EAB738"],
  ["Scala", "#2AE44A"],
  ["Ruby", "#6305FD"],
  ["Lua", "#684D53"],
  ["Fortran", "#3F37C3"],
  ["Matlab", "#7148F2"],
  ["R", "#D994E9"]])

class Post {
  constructor(id, upvoted) {
    this.id = id
    this.upvoted = upvoted
  }
}

function delay(fn, ms) {
  let timer = 0
  return function(...args) {
    clearTimeout(timer)
    timer = setTimeout(fn.bind(this, ...args), ms || 0)
  }
}

class Comments {
  constructor(id, upvoted) {
    this.id = id
    this.upvoted = upvoted
  }
}

posts = []
comments = []

function getRandomColor() {
  var letters = '0123456789ABCDEF'
  var color = '#'
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)]
  }
  return color
}

function rgb2hsl(rgb) {
  rgb = rgb.map(x=>x/255)
  var hsl = Array(3)
  let max = rgb.reduce((acc,x)=>(acc>x)?acc:x)
  let min = rgb.reduce((acc,x)=>(acc<x)?acc:x)
  let c = max-min
  if(c==0) {
    hsl[0]=0
  } else if(max==rgb[0]) {
    hsl[0]=((rgb[1]-rgb[2])/c)%6
  } else if(max==rgb[1]) {
    hsl[0]=(rgb[2]-rgb[0])/c+2
  } else if(max==rgb[2]) {
    hsl[0]=(rgb[0]-rgb[1])/c+4
  }
  hsl[0]*=60
  hsl[2] = (max+min)/2
  if(hsl[2]==0 || hsl[2]==1) {
    hsl[1] = 0
  } else {
    hsl[1] = c/(1-Math.abs(2*hsl[2]-1))
  }
  return hsl
}

function hsl2rgb(hsl) {
  let c = (1-Math.abs(2*hsl[2]-1))*hsl[1]
  let hprim = hsl[0]/60
  let x = c*(1-Math.abs(hprim%2-1))
  let m = hsl[2]-c/2
  if(hprim<=1) {
    rgb = [c, x, 0]
  } else if(hprim<=2) {
    rgb = [x, c, 0]
  } else if(hprim<=3) {
    rgb = [0, c, x]
  } else if(hprim<=4) {
    rgb = [0, x, c]
  } else if(hprim<=5) {
    rgb = [x, 0, c]
  } else if(hprim<=6) {
    rgb = [c, 0, x]
  }
  rgb = rgb.map(x=>Math.round((x+m)*255))
  return rgb
}

function rgb2string(rgb) {
  return rgb.map(x=> {
    let str = x.toString(16)
    if(str.length==1)
      return "0"+str
    else
      return str
  }).reduce((acc,x) => (acc+x))
}

function randomPalette() {
  var colors = (new Array(5)).fill(0).map(x => (new Array(3)))
  colors[0] = [Math.random()*360, (Math.random()+0.3)%1-0.3, 0.1]
  for (var i = 1; i < 5; i++) {
    colors[i] = colors[i - 1].slice(0) //clones array
    colors[i][2]+=0.15 //lightness
  }
  for (var i = 1; i < 6; i++) {
    document.documentElement.style.setProperty("--color" + i.toString(),
      "#" +
      rgb2string(hsl2rgb(colors[i-1])))
    colors[i-1][0] = (colors[i-1][0]+45)%360
    document.documentElement.style.setProperty("--highlight" + i.toString(),
      "#" +
      rgb2string(hsl2rgb(colors[i-1])))
  }
}

function popupSetState(state) {
  if(state) {
    document.getElementById("popup-background").style.visibility = "unset"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "blur(5px)";
    }
    document.getElementById("popup").style.visibility = "unset"
  } else {
    document.getElementById("popup-background").style.visibility = "collapse"
    for(div of document.getElementsByClassName("blur-on-popup")) {
      div.style.filter = "none";
    }
    document.getElementById("popup").style.visibility = "collapse"
    for(child of document.getElementById("popup").children) {
      child.style.visibility = "collapse"
      child.style.display = "none"
    }
  }
}

function setTagState(tag, state) {
  if (state) {
    tag.style.backgroundColor = getComputedStyle(tag).borderColor;
  } else {
    tag.style.backgroundColor = ""
  }
}

function selectTagE() {
  event.preventDefault()
  let tag = event.currentTarget
  let input = tag.getElementsByTagName("input")[0];
  let status = input.checked;
  if(input.getAttribute("type")==="radio") {
    radios = tag.parentNode.children
    for(li of radios) { setTagState(li, false) }
  }
  setTagState(tag, !status);
  input.checked = !status
}

function ajax(f, type, url) {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if(xhttp.readyState == 4) {
      if(xhttp.status == 200) {
        f();
      } else {
        console.log("Error in", xhttp)
      }
    }
  };
  xhttp.open(type, url, true);
  xhttp.send();
}

function removeElement() {
  let id = event.target.id;
  event.target.remove();
  input = document.getElementById(id)
  document.getElementById(id).checked = false;
}

function initTag(tag) {
  tag.style.borderColor = langs.get(tag.textContent.trim())
}

function initTags() {
  for(let ul of document.getElementsByClassName("tag-list")) {
    for (let li of ul.children) {
      initTag(li)
    }
  }
}

function refreshPopupMenu(menu) {
  let liList = Array.from(menu.getElementsByTagName("li"))
  let visible = liList.filter((x)=>getComputedStyle(x).visibility=="visible")
  for(let i=0;i<visible.length-1;i++) {
    visible[i].style.borderBottomColor = "var(--border-color)";
    visible[i].style.borderRadius = "0"
  }
  if(visible.length>1)
    visible[visible.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
}

function initPopupMenus() {
  for(let m of document.getElementsByClassName("popup-menu")) {
    let liList = Array.from(m.getElementsByTagName("li"))
    for(let i=0;i<liList.length-1;i++) {
      liList[i].style.borderBottomColor = "var(--border-color)";
      liList[i].style.borderRadius = "0"
    }
    liList[liList.length-1].style.borderRadius = "0 0 var(--radius) var(--radius)"
  }
}

function onLoad() {
  randomPalette()
  initTags()
  initPopupMenus()
  if(initFeed) initFeed()
  for (let ul of document.getElementsByClassName("tag-list")) {
    if (ul.classList.contains("button-list")) {
      for (let li of ul.children) {
        if (li.firstElementChild instanceof HTMLInputElement) {
          li.addEventListener("click", selectTagE)
          if(li.firstElementChild.checked) {
            setTagState(li, true)
          }
        }
      }
    }
  }
}
