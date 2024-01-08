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
  }
  ajax(display, "GET", "notifications/read-all")
}

function deleteNotificationE(id) {
  let t = event.target.parentNode.parentNode
  function display() {
    t.remove()
  }
  ajax(display, "GET", "notifications/" + id + "/delete")
}
