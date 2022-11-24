$(".owl-carousel").owlCarousel({
  loop: true,
  margin: 24,

  autoplay: true,
  autoplayTimeout: 3000,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 2,
    },
    1000: {
      items: 3,
    },
  },
});

AOS.init({
  duration: 700,
});

// Number rush configurations
new numberRush("jobs", {
  speed: 4,
  maxNumber: 120,
});
new numberRush("employers", {
  speed: 3,
  maxNumber: 1000,
});
new numberRush("people", {
  speed: 3,
  steps: 5,
  maxNumber: 2200,
});
new numberRush("companies", {
  speed: 3,
  maxNumber: 40,
});









//initialize all tooltips on a page would be to select them by their data-bs-toggle attribute
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))