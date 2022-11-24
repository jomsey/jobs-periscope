const toTopBtn = document.getElementById("back-to-top");

this.addEventListener("scroll", function () {
  toTopBtn.style.visibility = this.scrollY > 200 ? "visible" : "hidden";
});
