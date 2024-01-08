function getNotificationCount() {
  lis = document.getElementById("nav-list")
    .getElementsByTagName("li")
  for(let li of lis) {
    let anchors = li.getElementsByTagName("a")
    if(anchors.length > 0 &&
       anchors[0].href.indexOf("notification") != -1) {
      return anchors[0]
    }
  }
}

function setNotification(val) {
  a = getNotificationCount()
  let text = a.innerHTML.trim().split(" | ")
  if(val == 0) {
    a.innerHTML = text[0]
  } else {
    a.innerHTML = text[0] + " | " + val
  }
}

function subtractNotification(val) {
  a = getNotificationCount()
  let text = a.innerHTML.trim().split(" | ")
  if(Number(text[1])-val == 0) {
    a.innerHTML = text[0]
  } else {
    a.innerHTML = text[0] + " | " + (Number(text[1])-val)
  }
}

function deleteReadE() {
  function display() {
    let read = document.getElementById("main")
      .getElementsByClassName("container-list")[0]
      .querySelectorAll("li:not(.highlight-container)")
    for(let notification of read) {
      notification.remove()
    }
  }
  ajax(display, "GET", "notifications/delete-read")
}

function readAllE() {
  function display() {
    let unread = document.getElementById("main")
      .getElementsByClassName("container-list")[0]
      .getElementsByClassName("highlight-container")
    while(unread.length) {
      unread[0].classList.remove("highlight-container")
    }
    setNotification(0)
  }
  ajax(display, "GET", "notifications/read-all")
}

function deleteNotificationE(id) {
  let t = event.target.parentNode.parentNode
  function display() {
    if(t.classList.contains("highlight-container"))
      subtractNotification(1)
    t.remove()
  }
  ajax(display, "GET", "notifications/" + id + "/delete")
}
