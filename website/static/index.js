function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).catch(console.error).then((_res) => {
    window.location.href = "/";
  });
}
function deleteChore(taskId) {
  fetch("/delete-chore", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).catch(console.error).then((_res) => {
    window.location.href = "/chore";
  });
}
function deleteSupply(supplyId) {
  fetch("/delete-supply", {
    method: "POST",
    body: JSON.stringify({ supplyId: supplyId }),
  }).catch(console.error).then((_res) => {
    window.location.href = "/supplies";
  });
}
