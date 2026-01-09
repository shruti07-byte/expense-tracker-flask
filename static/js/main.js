// Confirm before logout
document.addEventListener("DOMContentLoaded", function () {
  const logoutBtn = document.querySelector('a[href="/logout"]');

  if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
      if (!confirm("Are you sure you want to logout?")) {
        e.preventDefault();
      }
    });
  }
});
