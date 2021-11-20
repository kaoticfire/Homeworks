function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function deleteChore(taskId) {
  fetch("/delete-chore", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/chore";
  });
}
function approveChore(choreId) {
  fetch("/approve-chore", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/chore";
  });
}
function rejectChore(choreId) {
  fetch("/reject-chore", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/chore";
  });
}
window.setTimeout(function() {
    $(".alert").fadeTo(500, 0)
}, 4000);
function deleteSupply(supplyId) {
  fetch("/delete-supply", {
    method: "POST",
    body: JSON.stringify({ supplyId: supplyId }),
  }).then((_res) => {
    window.location.href = "/supplies";
  });
}
