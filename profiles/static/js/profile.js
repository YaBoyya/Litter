function getUser() {
  return document.getElementById("profile-name")
    .getElementsByClassName("icon-text")[0]
    .textContent.trim()
}

function changeFollowE() {
  t = event.target
  function display() {
    if(t.textContent == "Follow") {
      t.textContent = "Unfollow"
    } else {
      t.textContent = "Follow"
    }
  }
  ajax(display, "GET", getUser() + "/follow")
}
