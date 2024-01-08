function deleteReadE() {
  function display() {
    read = document.getElementById("main")
      .getElementsByClassName("container-list")[0]
      .querySelectorAll("li:not(highlight-container)")
    for(let notification of read) {
      notification.remove()
    }
  }
  ajax(display, "GET", "notifications/delete-read")
}

function readAllE() {
  function display() {
    unread = document.getElementById("main")
      .getElementsByClassName("container-list")[0]
      .getElementsByClassName("highlight-container")
    for(let notification of unread) {
      notification.classList.remove("highlight-container")
    }
  }
  ajax(display, "GET", "notifications/read-all")
}

function deleteNotificationE(id) {
  t = event.target.parentNode.parentNode
  function display() {
    t.remove()
  }
  ajax(display, "GET", "notifications/" + id + "/delete")
}
