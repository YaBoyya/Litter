function getRandomColor() {
  var letters = '0123456789ABCDEF'
  var color = '#'
  for(var i = 0; i<6; i++) {
    color += letters[Math.floor(Math.random() * 16)]
  }
  return color
}

let langs = {
  New:       "#a0a000",
  Hot:       "#ff0000",
  Easy:      "#00ff00",
  Medium:    "#ffff00",
  Hard:      "#ff0000",
  C:         "#0000ff",
  Javascript:"#5E1DB8",
  Java:      "#C5D5E9",
  Python:    "#19125D",
  Cpp:       "#07CE0B",
  Scheme:    "#EAB738",
  Scala:     "#2AE44A",
  Ruby:      "#6305FD",
  Lua:       "#684D53",
  Fortran:   "#3F37C3",
  Matlab:    "#7148F2",
  R:         "#D994E9"}

function check(e) {
  let t = e.target
  let status = t.getElementsByTagName("input")[0].checked
  if(status) {
    t.style.backgroundColor = ""
  } else {
    t.style.backgroundColor = langs[t.textContent]
  }
  t.getElementsByTagName("input")[0].checked = !status
}

function randomPalette() {
  let compStyle=getComputedStyle(document.documentElement,null)
  var diff = Array(3).fill(0).map(x=>Math.floor(Math.random()*25+25))
  var colors = (new Array(5)).fill(0).map(x=>(new Array(3)))
  colors[0] = diff;
  for(var i=1;i<5;i++) {
    colors[i][0]=colors[i-1][0]+diff[0]
    colors[i][1]=colors[i-1][1]+diff[1]
    colors[i][2]=colors[i-1][2]+diff[2]
  }
  for(var i=1;i<6;i++) {
    document.documentElement.style.setProperty("--color"+i.toString(),
      "#"+
      colors[i-1][0].toString(16)+
      colors[i-1][1].toString(16)+
      colors[i-1][2].toString(16))
  }
}


let input
function script() {
  //Add listener for tag checkboxes
  for(let ul of document.getElementsByClassName("tag-list")) {
    for(let li of ul.getElementsByTagName("li"))
      li.style.borderColor = langs[li.textContent]
    if(ul.classList.contains("tag-list")) {
      for(let li of ul.getElementsByTagName("li")) {
        if(li.firstChild instanceof HTMLInputElement) {
          li.addEventListener("click", check)
        }
      }
    }
  }
  //Add listener to posts
  for(let ul of document.getElementsByClassName("post-list")) {
    for(let li of ul.getElementsByTagName("li")) {
      li.addEventListener("click", () => window.location.href="/post/2");
    }
  }
  randomPalette()
}
